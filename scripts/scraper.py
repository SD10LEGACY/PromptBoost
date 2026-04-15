import os
import json
import time
import requests
import google.generativeai as genai
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi

# --- 1. CONFIGURATION ---
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

# --- 2. THE HARVESTERS (No Authentication Required!) ---

def harvest_youtube():
    print("📺 Sweeping YouTube Transcripts...")
    queries = ["best chatgpt prompts 2026", "advanced claude prompts", "prompt engineering tutorial"]
    for q in queries:
        try:
            search = youtube_client.search().list(q=q, part="snippet", type="video", maxResults=3).execute()
            for item in search.get('items', []):
                v_id = item['id'].get('videoId')
                if not v_id: continue
                try:
                    transcript = YouTubeTranscriptApi.get_transcript(v_id)
                    text = " ".join([t['text'] for t in transcript])
                    raw_data_firehose.append({"source": "youtube", "text": f"Title: {item['snippet']['title']} Text: {text}"})
                except: continue
        except Exception as e: print(f"⚠️ YouTube Search Failed: {e}")

def harvest_hackernews():
    print("🟧 Sweeping Hacker News (Algolia API)...")
    # HN has a free, unblockable search API
    url = "https://hn.algolia.com/api/v1/search?query=AI+prompt+engineering&tags=story&hitsPerPage=5"
    try:
        res = requests.get(url).json()
        for hit in res.get('hits', []):
            content = f"Title: {hit.get('title')} Text: {hit.get('story_text', '')}"
            if len(content) > 50:
                raw_data_firehose.append({"source": "hacker_news", "text": content})
                print(f"✅ HN Thread Extracted: {hit.get('title')}")
    except Exception as e: print(f"⚠️ Hacker News Failed: {e}")

def harvest_devto():
    print("👩‍💻 Sweeping Dev.to Articles...")
    # Dev.to has a free, open API for developers
    url = "https://dev.to/api/articles?tag=promptengineering&top=7"
    try:
        res = requests.get(url).json()
        for article in res[:5]:
            # We fetch the full article body using its ID
            article_url = f"https://dev.to/api/articles/{article['id']}"
            full_article = requests.get(article_url).json()
            content = f"Title: {full_article.get('title')} Text: {full_article.get('body_markdown')}"
            raw_data_firehose.append({"source": "dev_to", "text": content})
            print(f"✅ Dev.to Article Extracted: {full_article.get('title')}")
    except Exception as e: print(f"⚠️ Dev.to Failed: {e}")

# --- 3. GEMINI CLEANING ENGINE ---
def process_with_ai():
    print(f"🧠 Gemini processing {len(raw_data_firehose)} raw data streams...")
    if len(raw_data_firehose) == 0: return []

    SYSTEM_PROMPT = """You are a Staff Prompt Engineer. Read this text from a blog, video, or forum. Extract the single most actionable, complete AI prompt mentioned. 
Output ONLY raw valid JSON:
{
    "title": "Short Catchy Name",
    "tag": "Coding | Writing | Creative | Productivity",
    "platforms": ["chatgpt", "claude", "gemini"],
    "text": "The full engineered prompt ready to copy-paste"
}"""

    refined_list = []
    for i, item in enumerate(raw_data_firehose[:25]): 
        try:
            response = model.generate_content(f"{SYSTEM_PROMPT}\n\n<text>\n{item['text'][:6000]}\n</text>")
            raw_text = response.text.strip().replace("```json", "").replace("```", "").strip()
            
            p_data = json.loads(raw_text)
            p_data["id"] = int(time.time()) + i
            p_data["source"] = item["source"]
            
            if "title" in p_data and "text" in p_data:
                refined_list.append(p_data)
                print(f"  ✨ Saved Prompt from {item['source'].upper()}: {p_data['title']}")
        except: continue
        time.sleep(2) 
    return refined_list

# --- 4. EXECUTION & SYNC ---
if __name__ == "__main__":
    harvest_youtube()
    harvest_hackernews()
    harvest_devto()
    
    new_prompts = process_with_ai()
    existing_prompts = load_existing_db()
    
    # Merge and Deduplicate
    full_library = existing_prompts + new_prompts
    unique_db = {p['text'].lower().strip(): p for p in full_library}.values()
    
    os.makedirs("database", exist_ok=True)
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(list(unique_db)[-1000:], f, indent=4)
    
    print(f"✅ Pipeline Complete! Total unique prompts: {len(unique_db)}")
