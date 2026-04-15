import os
import json
import time
import praw
import google.generativeai as genai
from googleapiclient.discovery import build
import youtube_transcript_api

# --- 1. CONFIGURATION & SECRETS ---
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
YOUTUBE_KEY = os.getenv("YOUTUBE_API_KEY")
REDDIT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")

DB_PATH = "database/prompts.json"

if not all([GEMINI_KEY, YOUTUBE_KEY, REDDIT_ID, REDDIT_SECRET]):
    print("❌ API Keys missing. Check GitHub Secrets.")
    exit(1)

# Initialize APIs
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")
youtube_client = build("youtube", "v3", developerKey=YOUTUBE_KEY)

# Initialize Official Reddit API Wrapper
reddit = praw.Reddit(
    client_id=REDDIT_ID,
    client_secret=REDDIT_SECRET,
    user_agent="script:PromptBoost:v3.0 (by /u/your_reddit_username)" # IMPORTANT: It requires any username here
)

raw_data_firehose = []

def load_existing_db():
    if os.path.exists(DB_PATH):
        try:
            with open(DB_PATH, "r", encoding="utf-8") as f: return json.load(f)
        except: return []
    return []

# --- 2. AUTHENTICATED REDDIT HARVESTER ---
def harvest_reddit():
    print("🕵️ Harvesting Reddit Trends (Authenticated)...")
    subs = ["PromptEngineering", "ChatGPTPro", "ClaudeAI"]
    
    for sub in subs:
        try:
            subreddit = reddit.subreddit(sub)
            # Fetch top 15 posts from the past week
            for post in subreddit.top(time_filter="week", limit=15):
                content = f"TITLE: {post.title} \nTEXT: {post.selftext}"
                if len(content) > 150:
                    raw_data_firehose.append({"source": "reddit", "text": content})
            print(f"✅ Reddit r/{sub}: Successfully extracted via API!")
        except Exception as e:
            print(f"⚠️ Reddit Auth Error (r/{sub}): {e}")

# --- 3. BULLETPROOF YOUTUBE HARVESTER ---
def harvest_youtube():
    print("📺 Listening to YouTube Transcripts...")
    queries = ["chatgpt prompts", "claude 3 prompts", "prompt engineering guide"]
    
    for q in queries:
        try:
            search = youtube_client.search().list(q=q, part="snippet", type="video", maxResults=3).execute()
            for item in search.get('items', []):
                v_id = item['id'].get('videoId')
                if not v_id: continue
                try:
                    # Explicit module calling to avoid namespace crashes
                    transcript = youtube_transcript_api.YouTubeTranscriptApi.get_transcript(v_id)
                    text = " ".join([t['text'] for t in transcript])
                    raw_data_firehose.append({"source": "youtube", "text": text})
                    print(f"✅ YouTube Video Extracted: {v_id}")
                except Exception as e:
                    print(f"⚠️ YouTube Transcript Failed ({v_id}): {e}")
        except Exception as e:
            print(f"⚠️ YouTube Search Failed: {e}")

# --- 4. GEMINI CLEANING ENGINE ---
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
