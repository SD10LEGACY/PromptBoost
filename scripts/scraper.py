import requests
import google.generativeai as genai
from googleapiclient.discovery import build
import json
import os
import time

# --- 1. SECURE API KEYS (Only Gemini & YouTube Needed Now!) ---
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
YOUTUBE_KEY = os.getenv("YOUTUBE_API_KEY")

if not all([GEMINI_KEY, YOUTUBE_KEY]):
    print("❌ Missing Gemini or YouTube API keys. Exiting.")
    exit(1)

# --- 2. CONFIGURE APIS ---
print("🔌 Initializing Omnichannel Connections...")
youtube = build('youtube', 'v3', developerKey=YOUTUBE_KEY)
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

raw_data_firehose = []

# --- 3. FETCH REDDIT DATA (The CryptoPanic Method - NO KEYS!) ---
print("🕵️ Scraping Reddit via Public JSON endpoints...")
subreddits = ["PromptEngineering", "ChatGPTPro", "ClaudeAI"]

# Reddit requires a custom User-Agent or it blocks the request
headers = {'User-Agent': 'PromptBoost Data Aggregator/1.0 (Contact: local-dev)'}

for sub in subreddits:
    try:
        url = f"https://www.reddit.com/r/{sub}/top.json?t=week&limit=3"
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            for post in data['data']['children']:
                title = post['data'].get('title', '')
                text = post['data'].get('selftext', '')
                if text and len(text) > 100:
                    raw_data_firehose.append(f"[REDDIT] {title}\n{text}")
        else:
            print(f"⚠️ Reddit returned status {response.status_code} for r/{sub}")
    except Exception as e:
        print(f"⚠️ Reddit Fetch Error: {e}")

# --- 4. FETCH YOUTUBE DATA ---
print("📺 Scraping YouTube...")
try:
    yt_request = youtube.search().list(
        q="best ChatGPT Claude prompts", part="snippet", type="video", maxResults=3, order="viewCount"
    )
    yt_response = yt_request.execute()
    for item in yt_response['items']:
        video_id = item['id']['videoId']
        vid_request = youtube.videos().list(part="snippet", id=video_id)
        vid_response = vid_request.execute()
        desc = vid_response['items'][0]['snippet']['description']
        if len(desc) > 100:
            raw_data_firehose.append(f"[YOUTUBE] {item['snippet']['title']}\n{desc}")
except Exception as e:
    print(f"⚠️ YouTube Error: {e}")

# --- 5. THE GEMINI CLEANER (AI Formatting) ---
print(f"🧠 Processing {len(raw_data_firehose)} raw sources with Gemini...")
final_database = []

SYSTEM_PROMPT = """
You are an expert data extractor. Extract the core AI prompt from the following raw internet text.
Format your response EXACTLY as a JSON object with these keys:
{
    "title": "A catchy title (e.g., 'Viral YouTube Coding Assistant')",
    "tag": "Career, Coding, Writing, Analysis, or Image Gen",
    "platforms": ["chatgpt", "claude", "gemini"], 
    "text": "The actual prompt text, cleaned of all conversational filler."
}
Output ONLY valid JSON. No markdown formatting, no backticks.
"""

for i, raw_text in enumerate(raw_data_firehose):
    try:
        res = model.generate_content(SYSTEM_PROMPT + "\n\nRAW TEXT:\n" + raw_text)
        cleaned_json = res.text.replace('```json', '').replace('```', '').strip()
        prompt_data = json.loads(cleaned_json)
        prompt_data["id"] = i + 1
        final_database.append(prompt_data)
        time.sleep(2) # Respect rate limits
    except Exception as e:
        print(f"⚠️ Failed to parse item {i}: {e}")

# --- 6. OVERWRITE CLOUD DATABASE ---
if final_database:
    os.makedirs("database", exist_ok=True)
    with open("database/prompts.json", "w", encoding="utf-8") as f:
        json.dump(final_database, f, indent=4)
    print(f"✅ Successfully updated database with {len(final_database)} Omni-Channel prompts!")
else:
    print("❌ No prompts were extracted today.")