import os
import json
import time
import requests
import google.generativeai as genai
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi

# --- 1. SETUP & AUTH ---
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
YOUTUBE_KEY = os.getenv("YOUTUBE_API_KEY")
DB_PATH = "database/prompts.json"

if not all([GEMINI_KEY, YOUTUBE_KEY]):
    print("❌ API Keys missing. Check GitHub Secrets.")
    exit(1)

# Configure Gemini API (Cloud)
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Configure YouTube
yt_service = build('youtube', 'v3', developerKey=YOUTUBE_KEY)
raw_data_firehose = []

def load_db():
    if os.path.exists(DB_PATH):
        try:
            with open(DB_PATH, "r", encoding="utf-8") as f: return json.load(f)
        except: return []
    return []

# --- 2. THE HARVESTERS ---
print("🕵️ Harvesting Reddit...")
subs = ["PromptEngineering", "ChatGPTPro", "ClaudeAI", "OpenAI", "Midjourney"]
for sub in subs:
    try:
        url = f"https://www.reddit.com/r/{sub}/top.json?t=week&limit=40"
        res = requests.get(url, headers={'User-Agent': 'PromptBoost/3.0'})
        if res.status_code == 200:
            for post in res.json()['data']['children']:
                p = post['data']
                content = f"{p.get('title')} {p.get('selftext')}"
                if len(content) > 200: raw_data_firehose.append({"source": "reddit", "text": content})
    except: continue

print("📺 Extracting YouTube Transcripts...")
queries = ["best chatgpt prompts 2026", "advanced prompt engineering", "ai prompt hacks"]
for q in queries:
    try:
        search = yt_service.search().list(q=q, part="snippet", type="video", maxResults=5).execute()
        for item in search['items']:
            v_id = item['id'].get('videoId')
            if not v_id: continue
            try:
                transcript = YouTubeTranscriptApi.get_transcript(v_id)
                text = " ".join([t['text'] for t in transcript])
                raw_data_firehose.append({"source": "youtube", "text": f"{item['snippet']['title']} {text}"})
            except:
                raw_data_firehose.append({"source": "youtube", "text": item['snippet']['description']})
    except: continue

# --- 3. THE CLEANING ENGINE ---
print(f"🧠 Gemini is processing {len(raw_data_firehose)} candidates...")
final_list = []
SYSTEM_PROMPT = "Extract the best AI prompt. Return ONLY valid JSON: {'title', 'tag', 'platforms', 'text'}. No filler."

for i, item in enumerate(raw_data_firehose[:35]):
    try:
        response = model.generate_content(f"{SYSTEM_PROMPT}\n\nRAW TEXT: {item['text'][:5000]}")
        clean_json = response.text.replace('```json', '').replace('```', '').strip()
        data = json.loads(clean_json)
        data.update({"id": int(time.time()) + i, "source": item["source"]})
        final_list.append(data)
        time.sleep(1) # Respect Rate Limits
    except: continue

# --- 4. SYNC ---
existing = load_db()
all_prompts = existing + final_list
unique = {p['text'].lower().strip(): p for p in all_prompts}.values()

os.makedirs("database", exist_ok=True)
with open(DB_PATH, "w", encoding="utf-8") as f:
    json.dump(list(unique)[-1000:], f, indent=4)
print(f"✅ Library synced. Size: {len(unique)}")