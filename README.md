<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0d1117,35:063b35,70:10a37f,100:0d1117&height=300&section=header&text=PromptBoost&fontSize=82&fontAlignY=42&fontColor=ffffff&desc=The%20Ultimate%20Prompt%20Engineering%20Engine&descAlignY=62&descSize=24&animation=fadeIn&v=2" width="100%" alt="PromptBoost Header"/>

[![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=18&duration=2800&pause=900&color=10A37F&center=true&vCenter=true&width=750&height=48&lines=Bring+Your+Own+Key+(BYOK)+Architecture.;Instant+Rotation:+Gemini+%E2%86%92+Groq+%E2%86%92+Mistral;Zero+Data+Leakage.+100%25+Local+Key+Storage.;CO-STAR+and+ReAct+Frameworks+On+the+Fly.;Bauhaus+Constructivist+UI+-+Pure+Vanilla+CSS.)](https://git.io/typing-svg)

<br><br>

<a href="#"><img src="https://img.shields.io/badge/Microsoft_Edge-IN_REVIEW-0078D7?style=for-the-badge&logo=microsoftedge&logoColor=white" alt="Edge Extension"/></a>
<a href="#"><img src="https://img.shields.io/badge/Chrome_Web_Store-COMING_SOON-4285F4?style=for-the-badge&logo=googlechrome&logoColor=white" alt="Chrome Extension"/></a>

<br><br>

<p>
  <img src="https://img.shields.io/badge/Chrome_Extension-v1.2-10a37f?style=for-the-badge&logo=googlechrome&logoColor=white" alt="Chrome Extension"/>
  <img src="https://img.shields.io/badge/Manifest-V3_Compliant-4ade80?style=for-the-badge&logo=googlechrome&logoColor=black" alt="Manifest V3"/>
  <img src="https://img.shields.io/badge/AI_Engine-Multi--Model_Rotation-8A2BE2?style=for-the-badge&logo=openai&logoColor=white" alt="Multi Model AI"/>
</p>
<p>
  <img src="https://img.shields.io/badge/Privacy-100%25_On--Device_Storage-ef4444?style=for-the-badge&logo=shield&logoColor=white" alt="Privacy"/>
  <img src="https://img.shields.io/badge/Auth-BYOK_Enabled-f59e0b?style=for-the-badge&logo=keycdn&logoColor=white" alt="BYOK"/>
  <img src="https://img.shields.io/badge/License-MIT-3b82f6?style=for-the-badge&logo=opensourceinitiative&logoColor=white" alt="MIT License"/>
</p>

<br>

> *A privacy-first browser extension that seamlessly intercepts and perfectly engineers your LLM prompts using a Bring-Your-Own-Key multi-engine architecture.*

<br>

</div>

***

<div align="center">

## 🚨 The Problem. The Solution.

</div>

> **🔴 The Problem:** Standard prompt engineering requires you to manually type tedious frameworks, while automated cloud services force you to send **private chat context** to third-party servers you don't control, often charging monthly subscription fees.
>
> **🟢 The Solution:** PromptBoost leverages a **Bring Your Own Key (BYOK)** architecture to securely communicate directly from your browser to top-tier AI providers. It rewrites rough text into scientifically-backed prompt frameworks (`CO-STAR`) and injects them directly into the DOM of major AI platforms. **Complete privacy. Ultimate control. Zero latency.**

***

## ✨ Core Architecture & Features

<table>
  <tr>
    <td width="50%" valign="top">
      <h3>🧠 Intelligent Engine Rotation</h3>
      <p>Configure multiple API keys directly in the extension. PromptBoost automatically rotates between <b>Gemini 2.0 Flash, Groq Llama-3.3, Mistral, and OpenRouter</b>. If one API fails, it instantly falls back to the next to ensure zero downtime.</p>
    </td>
    <td width="50%" valign="top">
      <h3>⚡ DOM-Level Interception</h3>
      <p>Bypasses standard <code>value</code> assignments by dispatching React Synthetic Events and formatting <code>contenteditable</code> nodes. Natively controls complex SPAs like ChatGPT and Claude without breaking internal state.</p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>📚 Dynamic Cloud Library</h3>
      <p>A slide-out Bauhaus-style panel that fetches a live database of trending, community-sourced prompts. Powered by a GitHub Actions Python scraper (<code>auto-scraper.yml</code>), updates propagate instantly via a cloud JSON feed without requiring store updates.</p>
    </td>
    <td width="50%" valign="top">
      <h3>🎯 Context-Aware Platform Filtering</h3>
      <p>Automatically detects your host environment (<code>chatgpt.com</code>, <code>claude.ai</code>, <code>gemini.google.com</code>) and serves <b>platform-specific prompt frameworks</b> directly in the UI, ensuring syntax compatibility.</p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>📐 Scientific Prompt Frameworks</h3>
      <p>Transforms rough, unstructured input into structured frameworks like <b>CO-STAR</b> (Context, Objective, Style, Tone, Audience, Response) for maximum AI comprehension and reasoning.</p>
    </td>
    <td width="50%" valign="top">
      <h3>🔐 Privacy by Architecture</h3>
      <p>There is no telemetry, no analytics, no logging. Your API keys are stored securely in <code>chrome.storage.local</code>. Prompts are processed strictly between your local machine and your chosen provider.</p>
    </td>
  </tr>
</table>

***

## ⚙️ Advanced System Architecture

### 1. Multi-Engine API Rotation Logic
PromptBoost does not rely on a single point of failure. The `background.js` service worker implements an asynchronous fallback rotation. If the primary engine (e.g., Gemini 2.0 Flash) hits a rate limit or a Content Security Policy (CSP) block, the system automatically routes the request to the next available provider — Groq Llama-3.3, then Mistral, then OpenRouter — until a successful response is received.

```javascript
// Simplified Representation of the Rotation Engine
async function routePrompt(text, keys) {
    const sequence = [
        { name: 'Gemini',      call: () => fetchGemini(text, keys.gemini) },
        { name: 'Groq',        call: () => fetchGroq(text, keys.groq) },
        { name: 'Mistral',     call: () => fetchMistral(text, keys.mistral) },
        { name: 'OpenRouter',  call: () => fetchOpenRouter(text, keys.openrouter) }
    ];

    for (const engine of sequence) {
        try {
            const result = await engine.call();
            if (result.ok) return { engine: engine.name, data: result.data };
        } catch (e) {
            console.warn(`[PromptBoost] ${engine.name} failed, falling back...`);
            continue; // Proceed to next engine in rotation
        }
    }
    return { error: "All configured engines failed." };
}
```

### 2. The React / ProseMirror Injection Hack

Injecting text into modern AI web apps is notoriously difficult. React and ProseMirror maintain their own virtual state trees and **silently reject** external DOM mutations. PromptBoost targets the `HTMLTextAreaElement` prototype directly to force the React reconciler to acknowledge the injection as a genuine user event.

```javascript
/**
 * PROMPTBOOST — Native React State Override
 * Intercepts the HTMLTextAreaElement's native setter via Object.getOwnPropertyDescriptor,
 * then fires a bubbling 'input' event to trick React's SyntheticEvent system.
 */
function injectIntoReactControlledInput(element, engineeredText) {
  // Step 1: Grab the native setter React has overridden
  const nativeSetter = Object.getOwnPropertyDescriptor(
    window.HTMLTextAreaElement.prototype,
    "value"
  ).set;

  // Step 2: Bypass React's proxy and write directly to the DOM node
  nativeSetter.call(element, engineeredText);

  // Step 3: Dispatch a bubbling synthetic input event
  element.dispatchEvent(new Event("input", { bubbles: true }));
}
```

***

## ☁️ GitHub Actions Automation — Trending Library Pipeline

The **Trending Prompt Library** is not static. It is powered by a fully automated Python scraper defined in `.github/workflows/auto-scraper.yml` that runs on a scheduled cron job. The pipeline fetches, deduplicates, and ranks community-sourced prompts, then commits an updated `prompts.json` feed to the repository. The extension's `background.js` fetches this JSON at runtime, meaning the library content is always fresh without ever requiring a new store submission.
┌──────────────────────────────────────────────────────────────┐
│ AUTOMATED PIPELINE: auto-scraper.yml │
│ │
│ [Cron Schedule] │
│ │ │
│ ▼ │
│ [Python Scraper] → Fetches & ranks trending prompts │
│ │ │
│ ▼ │
│ [Deduplication] → Filters noise, normalises schema │
│ │ │
│ ▼ │
│ [Git Commit] → Pushes updated prompts.json to repo │
│ │ │
│ ▼ │
│ [background.js] → Extension fetches live JSON at runtime │
└──────────────────────────────────────────────────────────────┘

text

> **Zero store submissions required.** The library updates propagate to all users instantly through the cloud JSON feed.

***

## 🔐 Security & Data Privacy

Privacy is not a feature of PromptBoost; it is the fundamental architectural constraint.

1. **Zero Data Harvesting:** The extension contains zero tracking pixels, analytics suites, or telemetry modules. Your data is your data.
2. **Local Credential Storage:** API keys entered into the extension are stored strictly using the `chrome.storage.local` API. They are **never** synced across devices via cloud accounts, and they are **never** transmitted to our servers.
3. **Direct-to-Provider Routing:** When you click the engineer button, your prompt is sent directly from your browser to the official API endpoints of Google (Gemini 2.0 Flash), Groq, Mistral, or OpenRouter. There is no middleman server.
4. **Isolated Worlds:** The extension operates within Chrome's Isolated World paradigm, ensuring that malicious scripts on websites cannot access the extension's memory space or your stored API keys.

***

## 🎨 UI / UX Design System

The extension's interface avoids the standard "SaaS Bootstrap" aesthetic by implementing a **Constructivist Bauhaus** design language using pure Vanilla CSS — no frameworks, no dependencies.
┌─────────────────────────────────────────────────────────┐
│ DESIGN PILLARS │
│ │
│ 📐 GEOMETRY → Strict programmatic color-blocking │
│ 🌑 DEPTH → Hard offset shadows (4px/8px black) │
│ 🌊 MOTION → CSS translation matrices for reveals │
│ 🎭 SIDEBAR → Slide-out prompt library panel │
│ 🖤 PALETTE → #D02020 · #1040C0 · #F0C020 │
└─────────────────────────────────────────────────────────┘

text

> **Philosophy:** Every pixel is intentional. The UI should feel like a precision, mechanical instrument — grounded in pure primary colors, hard borders, and bold typography.

***

## 🛠️ Tech Stack

<div align="center">

| Layer | Technology | Purpose |
|---|---|---|
| 🧠 **AI — Primary** | Gemini 2.0 Flash API | High-speed prompt engineering, rotation slot 1 |
| ⚡ **AI — Fallback 1** | Groq Llama-3.3 API | Ultra-low latency fallback, rotation slot 2 |
| 🔁 **AI — Fallback 2** | Mistral API | European-hosted fallback, rotation slot 3 |
| 🌐 **AI — Fallback 3** | OpenRouter API | Universal model gateway, rotation slot 4 |
| 🔌 **Extension Runtime** | Chrome MV3 — Service Workers | CSP-exempt background orchestration |
| 💉 **DOM Injection** | Content Scripts — DOM APIs | React/ProseMirror prototype overrides |
| 🎨 **UI** | Vanilla CSS — Bauhaus System | Constructivist design, zero dependencies |
| ☁️ **Automation** | GitHub Actions + Python | `auto-scraper.yml` — Trending Library Pipeline |
| 🔐 **Key Storage** | `chrome.storage.local` | BYOK — On-device only, never synced |

</div>

***

## 🗺️ Roadmap

<div align="center">

| Status | Feature |
|:---:|---|
| ✅ | Core DOM injection engine for modern AI platforms |
| ✅ | BYOK Multi-Engine Rotation (Gemini 2.0 Flash → Groq → Mistral → OpenRouter) |
| ✅ | Cloud JSON prompt library with GitHub Actions auto-scraper |
| ✅ | Bauhaus Constructivist UI design system |
| ✅ | Microsoft Edge Add-ons Submission |
| 🔄 | Chrome Web Store submission |
| ⏳ | Custom prompt framework builder (user-defined templates) |
| ⏳ | Firefox MV3 port |
| 💡 | Prompt history & local version control |

</div>

`✅ Done`   `🔄 In Progress`   `⏳ Planned`   `💡 Idea`

***

<details>
<summary><h2>🤝 Contributing & Developer Setup</h2></summary>

<br>

Contributions, issues, and feature requests are welcome!

**1. Clone the repository**

```bash
git clone https://github.com/SD10LEGACY/PromptBoost.git
cd PromptBoost
```

**2. Load as an Unpacked Extension**

1. Navigate to `chrome://extensions/` or `edge://extensions/`
2. Toggle **Developer Mode** ON (top-right corner)
3. Click **"Load unpacked"**
4. Select the cloned `PromptBoost/` directory

**3. Enter Your API Keys**

PromptBoost uses a **Bring Your Own Key (BYOK)** model. No keys are bundled with the extension.

1. Click the **PromptBoost icon** in your browser toolbar to open the popup
2. Enter at least one valid API key in the corresponding field:
   - **Gemini 2.0 Flash** — get your key at [aistudio.google.com](https://aistudio.google.com/)
   - **Groq** (recommended for fastest cold starts) — get your key at [console.groq.com](https://console.groq.com/)
   - **Mistral** — get your key at [console.mistral.ai](https://console.mistral.ai/)
   - **OpenRouter** — get your key at [openrouter.ai](https://openrouter.ai/)
3. Keys are saved to `chrome.storage.local` — they never leave your device
4. The engine rotation will automatically skip any slots with no key configured

> **Tip:** You only need one key to get started. Groq's free tier is the fastest option for development.

**4. Submitting Changes**

1. **Fork** the repository
2. Create a feature branch: `git checkout -b feat/your-feature-name`
3. Commit your changes: `git commit -m 'feat: add some feature'`
4. Push to your branch: `git push origin feat/your-feature-name`
5. Open a **Pull Request**

Please follow [Conventional Commits](https://www.conventionalcommits.org/) for commit messages.

</details>

***

<div align="center">

[![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&weight=500&size=14&duration=3000&pause=1000&color=10A37F&center=true&vCenter=true&width=600&lines=Built+with+%E2%9D%A4%EF%B8%8F+by+Shreyojit+Das+%E2%80%94+IEM+Class+of+2026;BYOK.+No+Servers.+No+Tracking.+Pure+Engineering.)](https://git.io/typing-svg)

<br>

<img src="https://komarev.com/ghpvc/?username=SD10LEGACY&label=Profile+Views&color=10a37f&style=for-the-badge" alt="Profile Views"/>

<br><br>

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0d1117,35:063b35,70:10a37f,100:0d1117&height=140&section=footer&animation=fadeIn" width="100%" alt="PromptBoost Footer"/>

</div>
