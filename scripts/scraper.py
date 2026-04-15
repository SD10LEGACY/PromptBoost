import requests
import google.generativeai as genai
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
import json
import os
import time

# --- 1. SECURE API KEYS ---
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
YOUTUBE_KEY = os.getenv("YOUTUBE_API_KEY")

if not all([GEMINI_KEY, YOUTUBE_KEY]):
    print("❌ API keys missing. Check GitHub Secrets.")
    exit(1)

# --- 2. CONFIGURATION ---
print("🔌 Initializing the Prompt-Firehose Engine...")
youtube = build('youtube', 'v3', developerKey=YOUTUBE_KEY)
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

DB_PATH = "database/prompts.json"
raw_data_firehose = []

# --- 3. DATA PERSISTENCE (Load Existing) ---
def load_existing_db():
    if os.path.exists(DB_PATH):
        try:
            with open(DB_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except: return []
    return []

# --- 4. REDDIT AGGRESSIVE SCRAPE ---
print("🕵️ Scraping Reddit Firehose...")
subreddits = ["PromptEngineering", "ChatGPTPro", "ClaudeAI", "OpenAI", "Midjourney", "StableDiffusion"]
headers = {'User-Agent': 'PromptBoost/2.0 (BCA Project Class of 2026)'}

for sub in subreddits:
    try:
        # Pulling 25 top posts from the last week for each sub
        url = f"https://www.reddit.com/r/{sub}/top.json?t=week&limit=25"
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            posts = res.json()['data']['children']
            for post in posts:
                p = post['data']
                content = f"{p.get('title', '')} {p.get('selftext', '')}"
                if len(content) > 150: # Only quality length
                    raw_data_firehose.append({"source": "reddit", "text": content})
    except Exception as e:
        print(f"⚠️ Reddit Error (r/{sub}): {e}")

# --- 5. YOUTUBE DEEP-DIVE (Transcripts) ---
print("📺 Extracting Prompts from YouTube Transcripts...")
search_queries = ["best chatgpt prompts 2026", "secret claude prompts", "advanced prompt engineering"]

for query in search_queries:
    try:
        yt_res = youtube.search().list(q=query, part="snippet", type="video", maxResults=5).execute()
        for item in yt_res['items']:
            v_id = item['id']['videoId']
            title = item['snippet']['title']
            
            # Try to get Transcript
            try:
                transcript_list = YouTubeTranscriptApi.get_transcript(v_id)
                transcript_text = " ".join([t['text'] for t in transcript_list])
                raw_data_firehose.append({"source": "youtube", "text": f"{title} {transcript_text}"})
            except:
                # Fallback to description if transcript is disabled
                raw_data_firehose.append({"source": "youtube", "text": f"{title} {item['snippet']['description']}"})
    except Exception as e:
        print(f"⚠️ YouTube Error: {e}")

# --- 6. GEMINI INTELLIGENT CLEANER ---
print(f"🧠 Gemini is processing {len(raw_data_firehose)} raw candidates...")

SYSTEM_PROMPT = """
Extract the absolute BEST prompt from this text. 
Remove all conversational filler, "Like and Subscribe" requests, or Reddit intros.
Format as JSON: 
{
    "title": "Short catchy name",
    "tag": "Coding/Writing/Creative/Career",
    "platforms": ["chatgpt", "claude", "gemini"], 
    "text": "The full engineered prompt text"
}
Output ONLY valid JSON. If no clear prompt exists, return null.
"""

new_prompts = []
for i, item in enumerate(raw_data_firehose[:40]): # Processing top 40 to avoid API rate limits
    try:
        response = model.generate_content(f"{SYSTEM_PROMPT}\n\nRAW TEXT: {item['text'][:5000]}")
        cleaned = response.text.replace('```json', '').replace('```', '').strip()
        
        if "null" in cleaned.lower() and len(cleaned) < 10: continue
        
        p_data = json.loads(cleaned)
        p_data["id"] = int(time.time()) + i
        p_data["source"] = item["source"]
        new_prompts.append(p_data)
        time.sleep(1) # Safety delay
    except: continue

# --- 7. MERGE, DEDUPLICATE & SAVE ---
existing_db = load_existing_db()
full_db = existing_db + new_prompts

# Deduplicate based on text content (keep unique prompts only)
unique_db = {p['text'].lower().strip(): p for p in full_db}.values()

# Sort by newest first and keep the library manageable
final_list = list(unique_db)[-1000:] # Keep latest 1000 high-quality prompts

os.makedirs("database", exist_ok=True)
with open(DB_PATH, "w", encoding="utf-8") as f:
    json.dump(final_list, f, indent=4)

print(f"✅ Mission Accomplished! Library now has {len(final_list)} Real-Time prompts.")