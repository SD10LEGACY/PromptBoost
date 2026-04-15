import os
import json
import time
import requests
import google.generativeai as genai
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi

GEMINI_KEY = os.getenv("GEMINI_API_KEY")
YOUTUBE_KEY = os.getenv("YOUTUBE_API_KEY")
DB_PATH = "database/prompts.json"

if not all([GEMINI_KEY, YOUTUBE_KEY]):
    print("❌ API Keys missing. Check GitHub Secrets.")
    exit(1)

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
    # HEAVY DUTY BROWSER DISGUISE
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept': 'application/json'
    }
    
    for sub in subs:
        try:
            url = f"https://www.reddit.com/r/{sub}/top.json?t=week&limit=15"
            res = requests.get(url, headers=headers)
            
            if res.status_code == 200:
                posts = res.json()['data']['children']
                for post in posts:
                    p = post['data']
                    content = f"TITLE: {p.get('title')} \nTEXT: {p.get('selftext')}"
                    if len(content) > 150:
                        raw_data_firehose.append({"source": "reddit", "text": content})
                print(f"✅ Reddit r/{sub}: Success!")
            else:
                print(f"⚠️ Reddit r/{sub} Blocked Us! Status Code: {res.status_code}")
        except Exception as e:
            print(f"⚠️ Reddit Crash: {e}")

def harvest_youtube():
    print("📺 Listening to YouTube Transcripts...")
    # BROADENED SEARCH QUERIES
    queries = ["chatgpt prompts", "claude 3 prompts", "prompt engineering guide"]
    
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
                    print(f"✅ YouTube Video Extracted: {v_id}")
                except Exception as e:
                    print(f"⚠️ YouTube Transcript Failed ({v_id}): {e}")
        except Exception as e:
            print(f"⚠️ YouTube Search Failed: {e}")

def process_with_ai():
    print(f"🧠 Gemini processing {len(raw_data_firehose)} raw candidates...")
    if len(raw_data_firehose) == 0:
        print("❌ CRITICAL: No data found to process. Scrapers failed.")
        return []

    SYSTEM_PROMPT = """Extract the single best AI prompt from the text.
Output ONLY raw valid JSON:
{
    "title": "Short Name",
    "tag": "Coding",
    "platforms": ["chatgpt", "claude", "gemini"],
    "text": "The prompt"
}"""

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
        except: continue
        time.sleep(1.5)
    return refined_list

if __name__ == "__main__":
    harvest_reddit()
    harvest_youtube()
    
    new_prompts = process_with_ai()
    existing_prompts = load_existing_db()
    
    full_library = existing_prompts + new_prompts
    unique_db = {p['text'].lower().strip(): p for p in full_library}.values()
    
    os.makedirs("database", exist_ok=True)
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(list(unique_db)[-1000:], f, indent=4)
    
    print(f"✅ Mission Accomplished! Library size: {len(unique_db)}")
