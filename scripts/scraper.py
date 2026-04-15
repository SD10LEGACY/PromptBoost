import os
import json
import time
import requests
from google import genai # Modern 2026 SDK
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi

# --- 1. INITIALIZATION ---
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
YOUTUBE_KEY = os.getenv("YOUTUBE_API_KEY")
DB_PATH = "database/prompts.json"

if not all([GEMINI_KEY, YOUTUBE_KEY]):
    print("❌ API keys missing. Check GitHub Secrets.")
    exit(1)

# New 2026 Client Syntax
client = genai.Client(api_key=GEMINI_KEY)
youtube = build('youtube', 'v3', developerKey=YOUTUBE_KEY)

raw_data_firehose = []

# --- 2. DATA PERSISTENCE ---
def load_existing_db():
    if os.path.exists(DB_PATH):
        try:
            with open(DB_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except: return []
    return []

# --- 3. AGGRESSIVE REDDIT HARVESTING ---
print("🕵️ Harvesting Reddit (Top 50 per sub)...")
subreddits = ["PromptEngineering", "ChatGPTPro", "ClaudeAI", "OpenAI", "Midjourney", "StableDiffusion"]
headers = {'User-Agent': 'PromptBoost/3.0 (BCA Project Class of 2026)'}

for sub in subreddits:
    try:
        # Increased limit to 50 for higher volume
        url = f"https://www.reddit.com/r/{sub}/top.json?t=week&limit=50"
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            posts = res.json()['data']['children']
            for post in posts:
                p = post['data']
                content = f"{p.get('title', '')} {p.get('selftext', '')}"
                if len(content) > 200: 
                    raw_data_firehose.append({"source": "reddit", "text": content})
    except Exception as e:
        print(f"⚠️ Reddit Error (r/{sub}): {e}")

# --- 4. YOUTUBE TRANSCRIPT DEEP-DIVE ---
print("📺 Listening to YouTube Transcripts...")
queries = ["best AI prompts 2026", "secret claude prompts", "advanced prompt engineering"]

for query in queries:
    try:
        yt_res = youtube.search().list(q=query, part="snippet", type="video", maxResults=10).execute()
        for item in yt_res['items']:
            v_id = item['id'].get('videoId')
            if not v_id: continue
            
            try:
                # Actual spoken text from the video
                transcript = YouTubeTranscriptApi.get_transcript(v_id)
                text = " ".join([t['text'] for t in transcript])
                raw_data_firehose.append({"source": "youtube", "text": text})
            except:
                # Fallback to description
                raw_data_firehose.append({"source": "youtube", "text": item['snippet']['description']})
    except Exception as e:
        print(f"⚠️ YouTube Error: {e}")

# --- 5. GEMINI 2.0 CLEANING ENGINE ---
print(f"🧠 Gemini 2.0 is processing {len(raw_data_firehose)} raw sources...")

SYSTEM_PROMPT = """
You are a Staff Prompt Engineer. Extract the absolute best, most useful AI prompt from the text.
Strip all filler, 'subscribe' calls, and conversational fluff.
Return ONLY valid JSON:
{
    "title": "Catchy Name",
    "tag": "Coding/Writing/Creative/Career",
    "platforms": ["chatgpt", "claude", "gemini"], 
    "text": "The full cleaned prompt"
}
"""

final_prompts = []
# Process a larger batch to grow the library faster
for i, item in enumerate(raw_data_firehose[:50]): 
    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash', # Updated for 2026 performance
            contents=f"{SYSTEM_PROMPT}\n\nRAW TEXT: {item['text'][:6000]}"
        )
        # Handle new SDK response structure
        cleaned = response.text.replace('```json', '').replace('```', '').strip()
        data = json.loads(cleaned)
        data["id"] = int(time.time()) + i
        data["source"] = item["source"]
        final_prompts.append(data)
        time.sleep(1) # Safety delay
    except: continue

# --- 6. MERGE & DEDUPLICATE ---
existing = load_existing_db()
full_list = existing + final_prompts

# Remove duplicates based on text content
unique_db = {p['text'].lower().strip(): p for p in full_list}.values()

# Keep the library growing (Setting limit to 5000 for now)
final_list = list(unique_db)[-5000:] 

os.makedirs("database", exist_ok=True)
with open(DB_PATH, "w", encoding="utf-8") as f:
    json.dump(final_list, f, indent=4)

print(f"✅ Library synced. Current size: {len(final_list)} prompts.")