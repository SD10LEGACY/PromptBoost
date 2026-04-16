"""
PromptBoost Auto-Scraper v2.0
Shreyojit Das (Class of 2026, IEM)

Sources:
  - YouTube (via YouTube Data API v3 + Transcript API)
  - Hacker News (Algolia API — free, no key)
  - Dev.to (public API — free, no key)
  - Reddit r/PromptEngineering, r/ChatGPT (JSON API — free, no key)
  - GitHub: awesome-chatgpt-prompts CSV (free, no key)

AI Engine Rotation (in order of preference per item):
  Gemini 2.0 Flash → Groq Llama3 → Mistral Small → OpenRouter Llama3 → skip

Fixes over v1.0:
  - [FIX] unique_db dedup: safe .get('text') guards crash on malformed entries
  - [FIX] dict_values sliced via explicit list() before [-1000:]
  - [FIX] Dev.to: single bulk fetch instead of one request per article
  - [FIX] Added Reddit + GitHub harvesters for category diversity
  - [FIX] Category diversity enforcer: max 5 prompts per tag per run
  - [FIX] All output prompts include perplexity + grok in platforms[]
  - [FIX] Exponential backoff on rate-limit (429) responses
"""

import os
import csv
import json
import time
import random
import requests
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi

# Increase CSV field size limit to handle massive prompts
csv.field_size_limit(2147483647)

# ─── 1. SECRETS ───────────────────────────────────────────────────────────────
GEMINI_KEY      = os.getenv("GEMINI_API_KEY")
GROQ_KEY        = os.getenv("GROQ_API_KEY")
MISTRAL_KEY     = os.getenv("MISTRAL_API_KEY")
OPENROUTER_KEY  = os.getenv("OPENROUTER_API_KEY")
YOUTUBE_KEY     = os.getenv("YOUTUBE_API_KEY")
DB_PATH         = "database/prompts.json"

if not all([GEMINI_KEY, YOUTUBE_KEY]):
    print("❌ GEMINI_API_KEY or YOUTUBE_API_KEY missing — check GitHub Secrets.")
    raise SystemExit(1)

youtube_client  = build("youtube", "v3", developerKey=YOUTUBE_KEY)
raw_firehose    = []   # list of {"source": str, "text": str}

ALL_PLATFORMS   = ["chatgpt", "claude", "gemini", "perplexity", "grok"]
MAX_PER_TAG     = 5    # diversity cap per run
HEADERS         = {"User-Agent": "PromptBoost/2.0 (github.com/SD10LEGACY/PromptBoost)"}

# ─── 2. HELPERS ───────────────────────────────────────────────────────────────
def load_existing_db():
    if os.path.exists(DB_PATH):
        try:
            with open(DB_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []


def safe_get(url, **kwargs):
    """GET with retry on 429 (rate-limit) using exponential backoff."""
    for attempt in range(4):
        try:
            r = requests.get(url, headers=HEADERS, timeout=12, **kwargs)
            if r.status_code == 429:
                wait = (2 ** attempt) + random.uniform(0, 1)
                print(f"   ⏳ Rate limited — waiting {wait:.1f}s")
                time.sleep(wait)
                continue
            return r
        except requests.RequestException as e:
            print(f"   ⚠️  Network error: {e}")
            time.sleep(2)
    return None


def safe_post(url, **kwargs):
    for attempt in range(3):
        try:
            r = requests.post(url, headers=HEADERS, timeout=15, **kwargs)
            if r.status_code == 429:
                time.sleep((2 ** attempt) + 1)
                continue
            return r
        except requests.RequestException as e:
            print(f"   ⚠️  Post error: {e}")
    return None

# ─── 3. HARVESTERS ────────────────────────────────────────────────────────────

def harvest_youtube():
    print("\n📺 YouTube Transcripts...")
    queries = [
        "best chatgpt prompts 2025 tutorial",
        "advanced claude prompts guide",
        "gemini AI prompts tips",
        "prompt engineering techniques 2025",
        "perplexity AI prompts",
    ]
    for q in queries[:4]:
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
                    text = " ".join(t["text"] for t in transcript)
                    title = item["snippet"]["title"]
                    raw_firehose.append({
                        "source": "youtube",
                        "text": f"Video Title: {title}\nTranscript:\n{text[:4000]}"
                    })
                    print(f"   ✅ {title[:60]}")
                except Exception:
                    pass
        except Exception as e:
            print(f"   ⚠️  YouTube query '{q}': {e}")


def harvest_hackernews():
    print("\n🟧 Hacker News...")
    url = "https://hn.algolia.com/api/v1/search?query=AI+prompt+engineering&tags=story&hitsPerPage=8"
    r = safe_get(url)
    if not r:
        return
    for hit in r.json().get("hits", []):
        content = f"Title: {hit.get('title', '')}\n{hit.get('story_text', '') or ''}"
        if len(content.strip()) > 40:
            raw_firehose.append({"source": "hacker_news", "text": content})
    print(f"   ✅ {len(r.json().get('hits', []))} items")


def harvest_devto():
    """Single request for article list; use body_html stripped of tags as content."""
    print("\n👩‍💻 Dev.to...")
    url = "https://dev.to/api/articles?tag=promptengineering&top=5&per_page=8"
    r = safe_get(url)
    if not r:
        return
    articles = r.json()
    count = 0
    for article in articles[:6]:
        # Use description + title — avoids per-article requests that were hitting rate limits
        content = f"Title: {article.get('title', '')}\n{article.get('description', '')}"
        if len(content.strip()) > 40:
            raw_firehose.append({"source": "dev_to", "text": content})
            count += 1
    print(f"   ✅ {count} items")


def harvest_reddit():
    """
    Scrapes r/PromptEngineering and r/ChatGPT top posts of the week.
    Uses Reddit's public .json endpoint — no OAuth key required.
    """
    print("\n🔴 Reddit...")
    subreddits = [
        "PromptEngineering",
        "ChatGPT",
        "ClaudeAI",
    ]
    count = 0
    for sub in subreddits:
        url = f"https://www.reddit.com/r/{sub}/top.json?limit=10&t=week"
        r = safe_get(url)
        if not r:
            continue
        try:
            posts = r.json()["data"]["children"]
            for post in posts:
                d = post["data"]
                title   = d.get("title", "")
                selftext = d.get("selftext", "")
                if len(selftext.strip()) < 20:
                    continue
                raw_firehose.append({
                    "source": f"reddit_{sub.lower()}",
                    "text": f"Post Title: {title}\nContent:\n{selftext[:3000]}"
                })
                count += 1
        except Exception as e:
            print(f"   ⚠️  r/{sub}: {e}")
        time.sleep(1.2)  # Reddit rate-limit: ~1 req/sec
    print(f"   ✅ {count} Reddit posts")


def harvest_github_awesome_prompts():
    """
    Pulls the entire 'awesome-chatgpt-prompts' CSV (~160 high-quality prompts).
    Direct load — no AI processing needed, these are already clean prompts.
    """
    print("\n⭐ GitHub Awesome Prompts CSV...")
    url = "https://raw.githubusercontent.com/f/awesome-chatgpt-prompts/main/prompts.csv"
    r = safe_get(url)
    if not r:
        return []

    existing_db   = load_existing_db()
    existing_texts = {p.get("text", "").lower().strip()[:100] for p in existing_db}

    direct_prompts = []
    reader = csv.DictReader(r.text.splitlines())
    for i, row in enumerate(reader):
        act  = row.get("act", "").strip()
        text = row.get("prompt", "").strip()
        if not text or text.lower()[:100] in existing_texts:
            continue
        # Classify tag by keywords in the act label
        tag = "General"
        lower_act = act.lower()
        if any(k in lower_act for k in ["code", "python", "javascript", "linux", "terminal", "sql", "developer"]):
            tag = "Coding"
        elif any(k in lower_act for k in ["write", "essay", "novel", "story", "poet", "journal"]):
            tag = "Writing"
        elif any(k in lower_act for k in ["market", "advertis", "sales", "seo", "social"]):
            tag = "Marketing"
        elif any(k in lower_act for k in ["teach", "tutor", "explain", "math", "science", "research"]):
            tag = "Research"
        elif any(k in lower_act for k in ["chef", "food", "recipe", "travel", "fitness", "health"]):
            tag = "Lifestyle"
        elif any(k in lower_act for k in ["dream", "story", "game", "role", "fiction", "creative"]):
            tag = "Creative"

        direct_prompts.append({
            "id":        1700000 + i,
            "title":     act,
            "tag":       tag,
            "platforms": ALL_PLATFORMS,
            "text":      text,
            "source":    "github_awesome",
        })

    print(f"   ✅ {len(direct_prompts)} new prompts from awesome-chatgpt-prompts")
    return direct_prompts

# ─── 4. AI ENGINE ROTATION ────────────────────────────────────────────────────

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


def ask_gemini(text):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_KEY}"
    payload = {"contents": [{"parts": [{"text": f"{SYSTEM_PROMPT}\n\n<source>\n{text[:5000]}\n</source>"}]}]}
    r = safe_post(url, json=payload)
    if r and r.status_code == 200:
        return r.json()["candidates"][0]["content"]["parts"][0]["text"]
    raise Exception(f"Gemini HTTP {r.status_code if r else 'no response'}")


def ask_groq(text):
    if not GROQ_KEY:
        raise Exception("No GROQ_KEY")
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


def ask_mistral(text):
    if not MISTRAL_KEY:
        raise Exception("No MISTRAL_KEY")
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


def ask_openrouter(text):
    if not OPENROUTER_KEY:
        raise Exception("No OPENROUTER_KEY")
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
    ("Gemini",      ask_gemini),
    ("Groq",        ask_groq),
    ("Mistral",     ask_mistral),
    ("OpenRouter",  ask_openrouter),
]


def process_with_ai(tag_counts):
    print(f"\n🧠 AI Processing {len(raw_firehose)} raw items...")
    refined = []
    for i, item in enumerate(raw_firehose[:25]):
        print(f"  [{i+1}/{min(25, len(raw_firehose))}] ", end="", flush=True)
        for engine_name, engine_fn in ENGINES:
            try:
                raw_output = engine_fn(item["text"])
                if "SKIP" in raw_output.upper()[:20]:
                    print(f"⏭️  SKIP ({engine_name})")
                    break

                clean = raw_output.replace("```json", "").replace("```", "").strip()
                p = json.loads(clean)

                # Enforce diversity cap
                tag = p.get("tag", "General")
                if tag_counts.get(tag, 0) >= MAX_PER_TAG:
                    print(f"⏭️  Capped tag '{tag}' ({engine_name})")
                    break

                p["id"]        = int(time.time()) + i + random.randint(0, 999)
                p["source"]    = item["source"]
                p["platforms"] = ALL_PLATFORMS  # always include all 5

                refined.append(p)
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
                print(f"✨ '{p['title']}' [{tag}] via {engine_name}")
                break
            except json.JSONDecodeError:
                continue   # try next engine
            except Exception as e:
                print(f" ({engine_name} err: {e.__class__.__name__})", end="")
                continue
        else:
            print("❌ All engines failed")
        time.sleep(2)
    return refined


# ─── 5. EXECUTION ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    existing_db = load_existing_db()
    print(f"📦 Existing DB: {len(existing_db)} prompts")

    # Count existing tags for diversity enforcement
    tag_counts = {}
    for p in existing_db:
        t = p.get("tag", "General")
        tag_counts[t] = tag_counts.get(t, 0) + 1

    # Run all harvesters
    harvest_youtube()
    harvest_hackernews()
    harvest_devto()
    harvest_reddit()

    # Direct-inject GitHub awesome prompts (no AI processing needed — already clean)
    direct_prompts = harvest_github_awesome_prompts()

    # AI processing of scraped raw text
    ai_prompts = process_with_ai(tag_counts)

    # Merge: existing + direct + AI-generated
    all_prompts = existing_db + direct_prompts + ai_prompts

    # Deduplicate by first 120 chars of text (safe .get() guards malformed entries)
    seen  = set()
    dedup = []
    for p in all_prompts:
        key = p.get("text", "").lower().strip()[:120]
        if key and key not in seen:
            seen.add(key)
            # Ensure all prompts have all platforms
            p["platforms"] = ALL_PLATFORMS
            dedup.append(p)

    # Keep newest 1000
    final_db = list(dedup)[-1000:]

    os.makedirs("database", exist_ok=True)
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(final_db, f, indent=4, ensure_ascii=False)

    # Summary
    final_tags = {}
    for p in final_db:
        t = p.get("tag", "?")
        final_tags[t] = final_tags.get(t, 0) + 1

    print(f"\n✅ Pipeline Complete!")
    print(f"   Total prompts: {len(final_db)}")
    print(f"   Tag breakdown: {json.dumps(final_tags, indent=4)}")
