import os
import json
import time
import requests
import google.generativeai as genai
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi

# --- 1. INITIALIZATION & SECURE KEYS ---
# These are pulled from your GitHub Secrets
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
YOUTUBE_KEY = os.getenv("YOUTUBE_API_KEY")
DB_PATH = "database/prompts.json"

if not all([GEMINI_KEY, YOUTUBE_KEY]):
    print("❌ API Keys missing in environment. Check GitHub Secrets.")
    exit(1)

# Configure Gemini (Big Brain Cloud Version)
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Configure YouTube
youtube_client = build('youtube', 'v3', developerKey=YOUTUBE_KEY)

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

# --- 5. THE GEMINI CLEANING ENGINE ---
def process_with_ai():
    print(f"🧠 Gemini is cleaning {len(raw_data_firehose)} raw candidates...")
    
    SYSTEM_PROMPT = """
    You are a Staff Prompt Engineer. Extract the BEST high-performance AI prompt from this text.
    Ignore 'Subscribe' calls, Reddit intros, or conversational fluff.
    Format your response ONLY as valid JSON:
    {
        "title": "Short Catchy Name",
        "tag": "Coding/Writing/Creative/Career",
        "platforms": ["chatgpt", "claude", "gemini"], 
        "text": "The full engineered prompt text"
    }
    """
    
    refined_list = []
    # Process top 30 to stay within free-tier rate limits
    for i, item in enumerate(raw_data_firehose[:30]):
        try:
            response = model.generate_content(f"{SYSTEM_PROMPT}\n\nRAW TEXT:\n{item['text'][:5000]}")
            # Remove markdown code blocks if Gemini includes them
            clean_json = response.text.replace('```json', '').replace('```', '').strip()
            
            p_data = json.loads(clean_json)
            p_data["id"] = int(time.time()) + i
            p_data["source"] = item["source"]
            refined_list.append(p_data)
            time.sleep(1) # Safety delay
        except: continue
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