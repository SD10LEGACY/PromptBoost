import os
import json
import time
import requests
import google.generativeai as genai # FIXED IMPORT
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi

GEMINI_KEY = os.getenv("GEMINI_API_KEY")
YOUTUBE_KEY = os.getenv("YOUTUBE_API_KEY")
DB_PATH = "database/prompts.json"

if not all([GEMINI_KEY, YOUTUBE_KEY]):
    print("API Keys missing. Check GitHub Secrets.")
    exit(1)

# FIXED CONFIGURATION
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel("gemini-1.5-flash") # Highly stable for extraction tasks

youtube_client = build("youtube", "v3", developerKey=YOUTUBE_KEY)
raw_data_firehose = []

# --- 2. PERSISTENCE ENGINE ---
def load_existing_db():
    """Loads existing prompts to ensure we accumulate data, not overwrite it."""
    if os.path.exists(DB_PATH):
        try:
            with open(DB_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except: return []
    return []

# --- 3. REDDIT HARVESTER ---
def harvest_reddit():
    print("🕵️ Harvesting Reddit Trends...")
    subs = ["PromptEngineering", "ChatGPTPro", "ClaudeAI", "OpenAI", "Midjourney"]
    headers = {'User-Agent': 'PromptBoost/3.0 (BCA Project Class of 2026)'}
    
    for sub in subs:
        try:
            url = f"https://www.reddit.com/r/{sub}/top.json?t=week&limit=30"
            res = requests.get(url, headers=headers)
            if res.status_code == 200:
                posts = res.json()['data']['children']
                for post in posts:
                    p = post['data']
                    content = f"TITLE: {p.get('title')} \nTEXT: {p.get('selftext')}"
                    if len(content) > 200:
                        raw_data_firehose.append({"source": "reddit", "text": content})
        except Exception as e:
            print(f"⚠️ Reddit Error (r/{sub}): {e}")

# --- 4. YOUTUBE TRANSCRIPT LISTENER ---
def harvest_youtube():
    print("📺 Listening to YouTube Transcripts...")
    queries = ["best ai prompts 2026", "advanced prompt engineering", "secret claude prompts"]
    
    for q in queries:
        try:
            search = youtube_client.search().list(q=q, part="snippet", type="video", maxResults=5).execute()
            for item in search['items']:
                v_id = item['id'].get('videoId')
                title = item['snippet']['title']
                if not v_id: continue
                
                try:
                    # Attempt to pull spoken words
                    transcript = YouTubeTranscriptApi.get_transcript(v_id)
                    text = " ".join([t['text'] for t in transcript])
                    raw_data_firehose.append({"source": "youtube", "text": f"{title} {text}"})
                except:
                    # Fallback to description
                    raw_data_firehose.append({"source": "youtube", "text": f"{title} {item['snippet']['description']}"})
        except Exception as e:
            print(f"⚠️ YouTube Search Error: {e}")

# --- 5. GEMINI CLEANING ENGINE ---
def process_with_ai():
    print(f"🧠 Gemini processing {len(raw_data_firehose)} raw candidates...")

    SYSTEM_PROMPT = """You are a Staff Prompt Engineer. Your job is to extract the single best, 
high-performance AI prompt from the raw text provided.

Rules:
- IGNORE: Subscribe calls, Reddit/YouTube intros, conversational filler, self-promotion
- EXTRACT: The most actionable, reusable prompt a user could paste into ChatGPT, Claude, or Gemini
- If no usable prompt exists in the text, respond with exactly: SKIP

Output ONLY raw valid JSON — no markdown, no code fences, no explanation:
{
    "title": "Short Catchy Name (max 6 words)",
    "tag": "Coding | Writing | Creative | Career | Research | Productivity",
    "platforms": ["chatgpt", "claude", "gemini"],
    "text": "The complete, copy-paste ready engineered prompt"
}"""

    refined_list = []
    total        = min(len(raw_data_firehose), 30)

    for i, item in enumerate(raw_data_firehose[:30]):
        try:
            # FIXED GENERATION CALL
            response = model.generate_content(
                f"{SYSTEM_PROMPT}\n\n<raw_text>\n{item['text'][:5000]}\n</raw_text>"
            )

            raw_text = response.text.strip()

            # Skip if Gemini signals no usable prompt
            if raw_text.upper().startswith("SKIP"):
                print(f"  [{i+1}/{total}] Skipped — no usable prompt found")
                time.sleep(1)
                continue

            # Strip any markdown fences Gemini may still include
            clean_json = (
                raw_text
                .replace("```json", "")
                .replace("```", "")
                .strip()
            )

            p_data            = json.loads(clean_json)
            p_data["id"]      = int(time.time()) + i
            p_data["source"]  = item["source"]

            # Validate required fields before saving
            if all(k in p_data for k in ("title", "tag", "text", "platforms")):
                refined_list.append(p_data)
                print(f"  [{i+1}/{total}] Saved: {p_data['title']}")
            else:
                print(f"  [{i+1}/{total}] Dropped — missing required fields")

        except json.JSONDecodeError:
            print(f"  [{i+1}/{total}] Dropped — invalid JSON from Gemini")
        except Exception as e:
            print(f"  [{i+1}/{total}] Error: {e}")

        time.sleep(1)  # Stay within free-tier rate limits (15 RPM)

    print(f"Extracted {len(refined_list)} valid prompts from {total} candidates")
    return refined_list

# --- 6. EXECUTION & SYNC ---
if __name__ == "__main__":
    harvest_reddit()
    harvest_youtube()
    
    new_prompts = process_with_ai()
    existing_prompts = load_existing_db()
    
    # Merge and Deduplicate based on the 'text' content
    full_library = existing_prompts + new_prompts
    unique_db = {p['text'].lower().strip(): p for p in full_library}.values()
    
    # Save the latest 1000 prompts to the database
    os.makedirs("database", exist_ok=True)
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(list(unique_db)[-1000:], f, indent=4)
    
    print(f"✅ Mission Accomplished! Library size: {len(unique_db)} prompts.")