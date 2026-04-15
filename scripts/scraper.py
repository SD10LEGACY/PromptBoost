import os
import json
import time
import requests
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

youtube_client = build("youtube", "v3", developerKey=YOUTUBE_KEY)
raw_data_firehose = []

def load_existing_db():
    if os.path.exists(DB_PATH):
        try:
            with open(DB_PATH, "r", encoding="utf-8") as f: return json.load(f)
        except: return []
    return []

# --- 2. THE HARVESTERS ---

def harvest_youtube():
    print("📺 Sweeping YouTube Transcripts...")
    queries = ["best chatgpt prompts 2026", "advanced claude prompts"]
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
                    print(f"✅ YouTube Extracted: {item['snippet']['title']}")
                except: pass
        except Exception as e: print(f"⚠️ YouTube API Error: {e}")

def harvest_hackernews():
    print("🟧 Sweeping Hacker News...")
    url = "https://hn.algolia.com/api/v1/search?query=AI+prompt+engineering&tags=story&hitsPerPage=5"
    try:
        res = requests.get(url).json()
        for hit in res.get('hits', []):
            content = f"Title: {hit.get('title')} Text: {hit.get('story_text', '')}"
            raw_data_firehose.append({"source": "hacker_news", "text": content})
    except: pass

def harvest_devto():
    print("👩‍💻 Sweeping Dev.to...")
    url = "https://dev.to/api/articles?tag=promptengineering&top=5"
    try:
        res = requests.get(url).json()
        for article in res:
            full = requests.get(f"https://dev.to/api/articles/{article['id']}").json()
            raw_data_firehose.append({"source": "dev_to", "text": full.get('body_markdown')})
    except: pass

# --- 3. THE AI ENGINE ROTATION (THE BRAIN) ---

def ask_gemini(prompt, text):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_KEY}"
    payload = {"contents": [{"parts": [{"text": f"{prompt}\n\n<text>\n{text[:6000]}\n</text>"}]}]}
    res = requests.post(url, json=payload, timeout=10)
    if res.status_code == 200:
        return res.json()['candidates'][0]['content']['parts'][0]['text']
    raise Exception(f"Gemini Error {res.status_code}")

def ask_groq(prompt, text):
    if not GROQ_KEY: raise Exception("No Key")
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": f"{prompt}\n\n<text>\n{text[:6000]}\n</text>"}]
    }
    res = requests.post(url, headers=headers, json=payload, timeout=10)
    return res.json()['choices'][0]['message']['content']

def ask_mistral(prompt, text):
    if not MISTRAL_KEY: raise Exception("No Key")
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {MISTRAL_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "mistral-small-latest",
        "messages": [{"role": "user", "content": f"{prompt}\n\n<text>\n{text[:6000]}\n</text>"}]
    }
    res = requests.post(url, headers=headers, json=payload, timeout=10)
    return res.json()['choices'][0]['message']['content']

def ask_openrouter(prompt, text):
    if not OPENROUTER_KEY: raise Exception("No Key")
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {"Authorization": f"Bearer {OPENROUTER_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "meta-llama/llama-3.1-8b-instruct:free",
        "messages": [{"role": "user", "content": f"{prompt}\n\n<text>\n{text[:6000]}\n</text>"}]
    }
    res = requests.post(url, headers=headers, json=payload, timeout=10)
    return res.json()['choices'][0]['message']['content']

def process_with_ai():
    print(f"\n🧠 Processing {len(raw_data_firehose)} items with AI Rotation...")
    
    SYSTEM_PROMPT = """You are a Staff Prompt Engineer. Extract the single most actionable AI prompt. 
If no prompt exists, reply ONLY: SKIP. 
Otherwise, output ONLY raw valid JSON:
{
    "title": "Short Name",
    "tag": "Coding | Writing | Creative",
    "platforms": ["chatgpt", "claude", "gemini"],
    "text": "The full engineered prompt"
}"""

    engines = [
        {"name": "Gemini", "func": ask_gemini},
        {"name": "Groq", "func": ask_groq},
        {"name": "Mistral", "func": ask_mistral},
        {"name": "OpenRouter", "func": ask_openrouter}
    ]

    refined_list = []
    for i, item in enumerate(raw_data_firehose[:20]):
        print(f"  🤖 Item {i+1}: ", end="")
        success = False
        
        for engine in engines:
            try:
                raw_text = engine['func'](SYSTEM_PROMPT, item['text'])
                
                if "SKIP" in raw_text.upper():
                    print(f"⏭️ Skipped via {engine['name']}")
                    success = True
                    break

                clean_text = raw_text.replace("```json", "").replace("```", "").strip()
                p_data = json.loads(clean_text)
                p_data["id"] = int(time.time()) + i
                p_data["source"] = item["source"]
                
                refined_list.append(p_data)
                print(f"✨ Saved via {engine['name']} ({p_data['title']})")
                success = True
                break # Move to next item in firehose
            except Exception as e:
                continue # Try next engine
        
        if not success:
            print("❌ All engines failed or out of quota.")
        time.sleep(2) # Global throttle
        
    return refined_list

# --- 4. EXECUTION ---
if __name__ == "__main__":
    harvest_youtube()
    harvest_hackernews()
    harvest_devto()
    
    new_prompts = process_with_ai()
    existing = load_existing_db()
    
    unique_db = {p['text'].lower().strip(): p for p in existing + new_prompts}.values()
    
    os.makedirs("database", exist_ok=True)
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(list(unique_db)[-1000:], f, indent=4)
    
    print(f"\n✅ Pipeline Complete! Library size: {len(unique_db)}")
