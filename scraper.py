"""
PromptBoost Auto-Scraper
Shreyojit Das

Sources:
  - YouTube (via YouTube Data API v3 + Transcript API)
  - Hacker News (Algolia API — free, no key)
  - Dev.to (public API — free, no key)
  - Reddit r/PromptEngineering, r/ChatGPT (JSON API — free, no key)
  - GitHub: awesome-chatgpt-prompts CSV (free, no key)
  -more would be added soon. *wink*

AI Engine Rotation (in order of preference per item):
  Gemini 2.0 Flash → Groq Llama3 → Mistral Small → OpenRouter Llama3 → skip
  Borlox hole BYOK 
"""

import csv
import json
import logging
import os
import random
import sys
import time

import requests
from dotenv import load_dotenv
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi

load_dotenv()

# csv's default is absurdly small for long-form prompt content
csv.field_size_limit(2147483647)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-7s %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("promptboost")

# ─── CONSTANTS ────────────────────────────────────────────────────────────────

GEMINI_KEY     = os.getenv("GEMINI_API_KEY")
GROQ_KEY       = os.getenv("GROQ_API_KEY")
MISTRAL_KEY    = os.getenv("MISTRAL_API_KEY")
OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")
YOUTUBE_KEY    = os.getenv("YOUTUBE_API_KEY")
DB_PATH        = "database/prompts.json"

ALL_PLATFORMS = ["chatgpt", "claude", "gemini", "perplexity", "grok"]
MAX_PER_TAG   = 5
HEADERS       = {"User-Agent": "PromptBoost/2.0 (github.com/SD10LEGACY/PromptBoost)"}

SYSTEM_PROMPT = """You are a Staff Prompt Engineer. 
Extract the single most actionable, reusable AI prompt from the text.
If no clear prompt can be extracted, reply ONLY with the word: SKIP
Otherwise, output ONLY a raw JSON object (no markdown, no preamble):
{
    "title": "Concise 3-6 word title",
    "tag": "Coding | Writing | Marketing | Research | Creative | Lifestyle | General",
    "platforms": ["chatgpt", "claude", "gemini", "perplexity", "grok"],
    "text": "The full, ready-to-use engineered prompt with no placeholders"
}"""

if not all([GEMINI_KEY, YOUTUBE_KEY]):
    log.critical("GEMINI_API_KEY or YOUTUBE_API_KEY missing — check GitHub Secrets.")
    raise SystemExit(1)

youtube_client = build("youtube", "v3", developerKey=YOUTUBE_KEY)
raw_firehose: list[dict] = []


# ─── HELPERS ──────────────────────────────────────────────────────────────────

def load_existing_db() -> list:
    if not os.path.exists(DB_PATH):
        return []
    try:
        with open(DB_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        log.warning("DB at %s is corrupt or unreadable (%s) — starting fresh.", DB_PATH, e)
        return []


def safe_get(url: str, **kwargs) -> requests.Response | None:
    """GET with exponential backoff on 429. Returns None after 4 failed attempts."""
    for attempt in range(4):
        try:
            r = requests.get(url, headers=HEADERS, timeout=12, **kwargs)
            if r.status_code == 429:
                wait = (2 ** attempt) + random.uniform(0, 1)
                log.warning("Rate-limited on GET — backing off %.1fs (attempt %d/4)", wait, attempt + 1)
                time.sleep(wait)
                continue
            return r
        except requests.RequestException as e:
            log.warning("Network error on GET attempt %d: %s", attempt + 1, e)
            time.sleep(2)
    return None


def safe_post(url: str, **kwargs) -> requests.Response | None:
    for attempt in range(3):
        try:
            r = requests.post(url, headers=HEADERS, timeout=15, **kwargs)
            if r.status_code == 429:
                wait = (2 ** attempt) + 1
                log.warning("Rate-limited on POST — backing off %.1fs", wait)
                time.sleep(wait)
                continue
            return r
        except requests.RequestException as e:
            log.warning("Network error on POST attempt %d: %s", attempt + 1, e)
    return None


# ─── HARVESTERS ───────────────────────────────────────────────────────────────

def harvest_youtube():
    log.info("▶  Harvesting YouTube transcripts...")
    queries = [
        "best chatgpt prompts 2025 tutorial",
        "advanced claude prompts guide",
        "gemini AI prompts tips",
        "prompt engineering techniques 2025",
    ]
    for q in queries:
        try:
            search = youtube_client.search().list(
                q=q, part="snippet", type="video", maxResults=3
            ).execute()
            for item in search.get("items", []):
                v_id = item["id"].get("videoId")
                if not v_id:
                    continue
                try:
                    transcript = YouTubeTranscriptApi.get_transcript(v_id, languages=["en"])
                    body = " ".join(t["text"] for t in transcript)
                    title = item["snippet"]["title"]
                    raw_firehose.append({
                        "source": "youtube",
                        "text": f"Video Title: {title}\nTranscript:\n{body[:4000]}"
                    })
                    log.info("   ✓ %s", title[:70])
                except Exception:
                    pass
        except Exception as e:
            log.warning("YouTube query '%s' failed: %s", q, e)


def harvest_hackernews():
    log.info("▶  Harvesting Hacker News...")
    url = "https://hn.algolia.com/api/v1/search?query=AI+prompt+engineering&tags=story&hitsPerPage=8"
    r = safe_get(url)
    if not r:
        log.warning("HN harvest skipped — no response.")
        return
    try:
        hits = r.json().get("hits", [])
    except ValueError:
        log.warning("HN harvest skipped — response was not valid JSON.")
        return
    for hit in hits:
        content = f"Title: {hit.get('title', '')}\n{hit.get('story_text', '') or ''}"
        if len(content.strip()) > 40:
            raw_firehose.append({"source": "hacker_news", "text": content})
    log.info("   ✓ %d items", len(hits))


def harvest_devto():
    # Using description+title only — full article body requires one req/article and
    # we kept hitting dev.to's undocumented burst limit last time around.
    log.info("▶  Harvesting Dev.to...")
    url = "https://dev.to/api/articles?tag=promptengineering&top=5&per_page=8"
    r = safe_get(url)
    if not r:
        log.warning("Dev.to harvest skipped — no response.")
        return
    articles = r.json()
    ingested = 0
    for article in articles[:6]:
        content = f"Title: {article.get('title', '')}\n{article.get('description', '')}"
        if len(content.strip()) > 40:
            raw_firehose.append({"source": "dev_to", "text": content})
            ingested += 1
    log.info("   ✓ %d items", ingested)


def harvest_reddit():
    """
    Scrapes r/PromptEngineering, r/ChatGPT, and r/ClaudeAI top posts of the week.
    Reddit's public .json endpoint requires no OAuth — but enforces ~1 req/sec.
    """
    log.info("▶  Harvesting Reddit...")
    subreddits = ["PromptEngineering", "ChatGPT", "ClaudeAI"]
    ingested = 0
    for sub in subreddits:
        url = f"https://www.reddit.com/r/{sub}/top.json?limit=10&t=week"
        r = safe_get(url)
        if not r:
            log.warning("   r/%s skipped — no response.", sub)
            continue
        try:
            posts = r.json()["data"]["children"]
            for post in posts:
                d = post["data"]
                selftext = d.get("selftext", "")
                if len(selftext.strip()) < 20:
                    continue
                raw_firehose.append({
                    "source": f"reddit_{sub.lower()}",
                    "text": f"Post Title: {d.get('title', '')}\nContent:\n{selftext[:3000]}"
                })
                ingested += 1
        except (KeyError, ValueError) as e:
            log.warning("   r/%s parse error: %s", sub, e)
        time.sleep(1.2)  # Reddit will 429 you instantly if you skip this
    log.info("   ✓ %d Reddit posts", ingested)


def harvest_github_awesome_prompts() -> list:
    """
    Pulls the entire awesome-chatgpt-prompts CSV (~160 curated prompts).
    These land directly in the DB — no AI extraction pass needed.
    """
    log.info("▶  Harvesting awesome-chatgpt-prompts CSV...")
    url = "https://raw.githubusercontent.com/f/awesome-chatgpt-prompts/main/prompts.csv"
    r = safe_get(url)
    if not r:
        log.warning("GitHub harvest skipped — no response.")
        return []

    existing_db = load_existing_db()
    existing_fingerprints = {p.get("text", "").lower().strip()[:100] for p in existing_db}

    tag_keywords = {
        "Coding":    ["code", "python", "javascript", "linux", "terminal", "sql", "developer"],
        "Writing":   ["write", "essay", "novel", "story", "poet", "journal"],
        "Marketing": ["market", "advertis", "sales", "seo", "social"],
        "Research":  ["teach", "tutor", "explain", "math", "science", "research"],
        "Lifestyle": ["chef", "food", "recipe", "travel", "fitness", "health"],
        "Creative":  ["dream", "story", "game", "role", "fiction", "creative"],
    }

    harvested = []
    reader = csv.DictReader(r.text.splitlines())
    for i, row in enumerate(reader):
        act  = row.get("act", "").strip()
        text = row.get("prompt", "").strip()
        if not text or text.lower()[:100] in existing_fingerprints:
            continue

        lower_act = act.lower()
        tag = next(
            (t for t, keywords in tag_keywords.items() if any(k in lower_act for k in keywords)),
            "General"
        )

        harvested.append({
            "id":        1700000 + i,
            "title":     act,
            "tag":       tag,
            "platforms": ALL_PLATFORMS,
            "text":      text,
            "source":    "github_awesome",
        })

    log.info("   ✓ %d new prompts from awesome-chatgpt-prompts", len(harvested))
    return harvested


# ─── AI ENGINE ROTATION ───────────────────────────────────────────────────────

def ask_gemini(text: str) -> str:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_KEY}"
    payload = {"contents": [{"parts": [{"text": f"{SYSTEM_PROMPT}\n\n<source>\n{text[:5000]}\n</source>"}]}]}
    r = safe_post(url, json=payload)
    if r and r.status_code == 200:
        return r.json()["candidates"][0]["content"]["parts"][0]["text"]
    raise Exception(f"Gemini HTTP {r.status_code if r else 'no response'}")


def ask_groq(text: str) -> str:
    if not GROQ_KEY:
        raise Exception("GROQ_KEY not configured")
    r = safe_post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"},
        json={
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "user", "content": f"{SYSTEM_PROMPT}\n\n<source>\n{text[:5000]}\n</source>"}],
        },
    )
    if r and r.status_code == 200:
        return r.json()["choices"][0]["message"]["content"]
    raise Exception(f"Groq HTTP {r.status_code if r else 'no response'}")


def ask_mistral(text: str) -> str:
    if not MISTRAL_KEY:
        raise Exception("MISTRAL_KEY not configured")
    r = safe_post(
        "https://api.mistral.ai/v1/chat/completions",
        headers={"Authorization": f"Bearer {MISTRAL_KEY}", "Content-Type": "application/json"},
        json={
            "model": "mistral-small-latest",
            "messages": [{"role": "user", "content": f"{SYSTEM_PROMPT}\n\n<source>\n{text[:5000]}\n</source>"}],
        },
    )
    if r and r.status_code == 200:
        return r.json()["choices"][0]["message"]["content"]
    raise Exception(f"Mistral HTTP {r.status_code if r else 'no response'}")


def ask_openrouter(text: str) -> str:
    if not OPENROUTER_KEY:
        raise Exception("OPENROUTER_KEY not configured")
    r = safe_post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={"Authorization": f"Bearer {OPENROUTER_KEY}", "Content-Type": "application/json"},
        json={
            "model": "meta-llama/llama-3.1-8b-instruct:free",
            "messages": [{"role": "user", "content": f"{SYSTEM_PROMPT}\n\n<source>\n{text[:5000]}\n</source>"}],
        },
    )
    if r and r.status_code == 200:
        return r.json()["choices"][0]["message"]["content"]
    raise Exception(f"OpenRouter HTTP {r.status_code if r else 'no response'}")


ENGINES = [
    ("Gemini",     ask_gemini),
    ("Groq",       ask_groq),
    ("Mistral",    ask_mistral),
    ("OpenRouter", ask_openrouter),
]


def process_with_ai(tag_counts: dict) -> list:
    batch = raw_firehose[:25]
    log.info("▶  AI processing %d raw items (capped at 25)...", len(batch))
    extracted_prompts = []

    for i, item in enumerate(batch):
        log.info("  [%d/%d] source=%s", i + 1, len(batch), item["source"])
        for engine_name, engine_fn in ENGINES:
            try:
                raw_output = engine_fn(item["text"])

                if "SKIP" in raw_output.upper()[:20]:
                    log.info("   ↷  SKIP signal from %s", engine_name)
                    break

                clean = raw_output.replace("```json", "").replace("```", "").strip()
                p = json.loads(clean)

                # Guard against engines that hallucinate partial JSON
                if not all(k in p for k in ("title", "tag", "text")):
                    log.warning("   %s returned incomplete JSON — trying next engine.", engine_name)
                    continue

                tag = p.get("tag", "General")
                if tag_counts.get(tag, 0) >= MAX_PER_TAG:
                    log.info("   ↷  Tag '%s' at cap — skipping (%s)", tag, engine_name)
                    break

                p["id"]        = int(time.time()) + i + random.randint(0, 999)
                p["source"]    = item["source"]
                p["platforms"] = ALL_PLATFORMS

                extracted_prompts.append(p)
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
                log.info("   ✨ '%s' [%s] via %s", p["title"], tag, engine_name)
                break

            except json.JSONDecodeError:
                log.warning("   %s returned non-JSON — trying next engine.", engine_name)
                continue
            except Exception as e:
                log.warning("   %s failed (%s: %s) — trying next engine.", engine_name, type(e).__name__, e)
                continue
        else:
            log.error("   ✗  All engines exhausted for item %d.", i + 1)
        time.sleep(2)

    return extracted_prompts


# ─── MAIN ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    existing_db = load_existing_db()
    log.info("DB loaded: %d existing prompts.", len(existing_db))

    tag_counts = {}
    for p in existing_db:
        t = p.get("tag", "General")
        tag_counts[t] = tag_counts.get(t, 0) + 1

    harvest_youtube()
    harvest_hackernews()
    harvest_devto()
    harvest_reddit()

    direct_prompts   = harvest_github_awesome_prompts()
    ai_prompts       = process_with_ai(tag_counts)

    combined = existing_db + direct_prompts + ai_prompts

    seen: set[str] = set()
    deduped: list[dict] = []
    for p in combined:
        fingerprint = p.get("text", "").lower().strip()[:120]
        if not fingerprint or fingerprint in seen:
            continue
        seen.add(fingerprint)
        p["platforms"] = ALL_PLATFORMS
        deduped.append(p)

    final_db = deduped[-1000:]

    os.makedirs("database", exist_ok=True)
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(final_db, f, indent=4, ensure_ascii=False)

    tag_tally = {}
    for p in final_db:
        t = p.get("tag", "?")
        tag_tally[t] = tag_tally.get(t, 0) + 1

    log.info("Pipeline complete. %d prompts written.", len(final_db))
    log.info("Tag breakdown: %s", json.dumps(tag_tally))
