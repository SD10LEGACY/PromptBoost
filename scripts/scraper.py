import os
import json
import time
import requests
import google.generativeai as genai
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi

# --- 1. CONFIGURATION & SECRETS ---
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
GROQ_KEY = os.getenv("GROQ_API_KEY")
MISTRAL_KEY = os.getenv("MISTRAL_API_KEY")
OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")
YOUTUBE_KEY = os.getenv("YOUTUBE_API_KEY")
DB_PATH = "database/prompts.json"

# Check for mandatory keys (Gemini is primary, others are fallbacks)
if not all([GEMINI_KEY, YOUTUBE_KEY]):
    print("❌ Critical API Keys missing. Check GitHub Secrets.")
    exit(1)

# STABLE CONFIGURATION
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

youtube_client = build("youtube", "v3", developerKey=YOUTUBE_KEY)
raw_data_firehose = []

def load_existing_db():
    if os.path.exists(DB_PATH):
        try:
            with open(DB_PATH, "r", encoding="utf-8") as f: return json.load(f)
        except: return []
    return []

def harvest_reddit():
    print("🕵️ Harvesting Reddit Trends...")
    subs = ["PromptEngineering", "ChatGPTPro", "ClaudeAI"]
    headers = {'User-Agent': 'PromptBoost/3.0'}
    
    for sub in subs:
        try:
            url = f"https://www.reddit.com/r/{sub}/top.json?t=week&limit=25"
            res = requests.get(url, headers=headers)
            if res.status_code == 200:
                posts = res.json()['data']['children']
                for post in posts:
                    p = post['data']
                    content = f"TITLE: {p.get('title')} \nTEXT: {p.get('selftext')}"
                    if len(content) > 200:
                        raw_data_firehose.append({"source": "reddit", "text": content})
        except Exception as e:
            print(f"⚠️ Reddit Error: {e}")

def harvest_youtube():
    print("📺 Listening to YouTube Transcripts...")
    queries = ["best ai prompts 2026", "advanced prompt engineering"]
    
    for q in queries:
        try:
            search = youtube_client.search().list(q=q, part="snippet", type="video", maxResults=3).execute()
            for item in search.get('items', []):
                v_id = item['id'].get('videoId')
                if not v_id: continue
                try:
                    transcript = YouTubeTranscriptApi.get_transcript(v_id)
                    text = " ".join([t['text'] for t in transcript])
                    raw_data_firehose.append({"source": "youtube", "text": text})
                except: continue
        except: continue

def process_with_ai():
    print(f"🧠 Gemini processing {len(raw_data_firehose)} raw candidates...")
    SYSTEM_PROMPT = """Extract the single best AI prompt from the text.
Output ONLY raw valid JSON:
{
    "title": "Short Name",
    "tag": "Coding",
    "platforms": ["chatgpt", "claude", "gemini"],
    "text": "The prompt"
}"""

    engines = [
        {"name": "Gemini", "func": ask_gemini},
        {"name": "Groq", "func": ask_groq},
        {"name": "Mistral", "func": ask_mistral},
        {"name": "OpenRouter", "func": ask_openrouter}
    ]

    refined_list = []
    for i, item in enumerate(raw_data_firehose[:25]):
        try:
            response = model.generate_content(f"{SYSTEM_PROMPT}\n\n<text>\n{item['text'][:4000]}\n</text>")
            raw_text = response.text.strip().replace("```json", "").replace("```", "").strip()
            
            p_data = json.loads(raw_text)
            p_data["id"] = int(time.time()) + i
            p_data["source"] = item["source"]
            
            if "title" in p_data and "text" in p_data:
                refined_list.append(p_data)
                print(f"  Saved: {p_data['title']}")
        except: continue
        time.sleep(1.5)
    return refined_list

if __name__ == "__main__":
    harvest_youtube()
    harvest_hackernews()
    harvest_devto()
    
    new_prompts = process_with_ai()
    existing = load_existing_db()
    
    full_library = existing_prompts + new_prompts
    unique_db = {p['text'].lower().strip(): p for p in full_library}.values()
    
    os.makedirs("database", exist_ok=True)
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(list(unique_db)[-1000:], f, indent=4)
    
    print(f"✅ Mission Accomplished! Library size: {len(unique_db)}")