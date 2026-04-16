```markdown
<div align="center">
<!-- ══════════════════════════════════════════════════════ -->
<!-- ANIMATED HEADER -->
<!-- ══════════════════════════════════════════════════════ -->
<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0d1117,35:063b35,70:10a37f,100:0d1117&height=300&section=header&text=PromptBoost&fontSize=82&fontAlignY=42&fontColor=ffffff&desc=The%20On-Device%20Prompt%20Engineering%20Engine&descAlignY=62&descSize=24&animation=fadeIn&v=2" width="100%" alt="PromptBoost Header"/>
<!-- ══════════════════════════════════════════════════════ -->
<!-- TYPING ANIMATION -->
<!-- ══════════════════════════════════════════════════════ -->

```
![alt text](https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=18&duration=2800&pause=900&color=10A37F&center=true&vCenter=true&width=750&height=48&lines=Bring+Your+Own+Key+BYOK;Multi-Engine+Rotation+via+Gemini+2.0+Flash+%2C+Groq+%2C+Mistral+%2C+OpenRouter;Zero+Latency.+Zero+Extension+Servers.;CO-STAR+and+ReAct+Frameworks+On+the+Fly.;Bauhaus+Constructivist+UI+-+Pure+Vanilla+CSS.)
```

 
<br><br>
<!-- ══════════════════════════════════════════════════════ -->
<!-- BADGES -->
<!-- ══════════════════════════════════════════════════════ -->
<p>
<img src="https://img.shields.io/badge/Microsoft_Edge-IN_REVIEW-0078d4?style=for-the-badge&logo=microsoftedge&logoColor=white" alt="Microsoft Edge (IN REVIEW)"/>
<img src="https://img.shields.io/badge/Chrome_Extension-COMING_SOON-10a37f?style=for-the-badge&logo=googlechrome&logoColor=white" alt="Chrome Extension (COMING SOON)"/>
</p>
<p>
<img src="https://img.shields.io/badge/Chrome_Extension-In_Development-10a37f?style=for-the-badge&logo=googlechrome&logoColor=white" alt="Chrome Extension"/>
<img src="https://img.shields.io/badge/Manifest-V3_Compliant-4ade80?style=for-the-badge&logo=googlechrome&logoColor=black" alt="Manifest V3"/>
</p>
<p>
<img src="https://img.shields.io/badge/Privacy-100%25_BYOK-ef4444?style=for-the-badge&logo=shield&logoColor=white" alt="Privacy"/>
<img src="https://img.shields.io/badge/API_Keys-BYOK_Local-f59e0b?style=for-the-badge&logo=keycdn&logoColor=white" alt="BYOK API Keys"/>
<img src="https://img.shields.io/badge/License-MIT-3b82f6?style=for-the-badge&logo=opensourceinitiative&logoColor=white" alt="MIT License"/>
</p>
<br>
A privacy-first, zero-latency browser extension that seamlessly intercepts and perfectly engineers your LLM prompts using Bring Your Own Key (BYOK) with Intelligent Multi-Engine Rotation — before they ever reach a server.
<br>
</div>
<div align="center">
🚨 The Problem. The Solution.
</div>
🔴 The Problem: Cloud-based prompt engineers introduce network latency, require expensive API keys managed by third parties, and force you to send private chat context to external servers you don't control.
🟢 The Solution: PromptBoost leverages Bring Your Own Key (BYOK) architecture with Intelligent Multi-Engine Rotation — intelligently falling back between Gemini 2.0 Flash, Groq Llama-3.3, Mistral, and OpenRouter. Your API keys are stored securely in chrome.storage.local. Nothing is sent to the developer's servers. No cloud. No cost. No compromise.
✨ Core Architecture & Features
<table>
<tr>
<td width="50%" valign="top">
<h3>🧠 BYOK Multi-Engine Inference</h3>
<p>Powered exclusively by your own API keys with intelligent rotation across Gemini 2.0 Flash, Groq Llama-3.3, Mistral, and OpenRouter. API keys are stored locally in chrome.storage.local — 100% privacy as nothing is sent to any servers controlled by PromptBoost. Your keystrokes and context stay under your control.</p>
</td>
<td width="50%" valign="top">
<h3>⚡ DOM-Level Interception</h3>
<p>Bypasses standard <code>value</code> assignments by dispatching React Synthetic Events and formatting <code>contenteditable</code> nodes. Natively controls complex Single-Page Applications without breaking their internal state.</p>
</td>
</tr>
<tr>
<td width="50%" valign="top">
<h3>📚 Dynamic Cloud Library</h3>
<p>A slide-out, glassmorphism UI panel that fetches a live database of trending, community-sourced prompts. Updates propagate instantly via a cloud JSON feed powered by GitHub Actions Python Scraper (auto-scraper.yml) — <b>no Chrome Web Store re-submission required.</b></p>
</td>
<td width="50%" valign="top">
<h3>🎯 Context-Aware Platform Detection</h3>
<p>Automatically detects the host environment (<code>chatgpt.com</code>, <code>claude.ai</code>, <code>gemini.google.com</code>) and serves <b>platform-specific prompt frameworks</b>, filtering out irrelevant structural metadata.</p>
</td>
</tr>
<tr>
<td width="50%" valign="top">
<h3>📐 Scientific Prompt Frameworks</h3>
<p>Transforms rough, unstructured input into structured frameworks. <b>CO-STAR</b> (Context, Objective, Style, Tone, Audience, Response) for deep reasoning. <b>ReAct</b> (Reason + Act) for agentic, multi-step tasks.</p>
</td>
<td width="50%" valign="top">
<h3>🔐 Privacy by Architecture</h3>
<p>There is no telemetry, no analytics, no logging. API keys are stored only in chrome.storage.local. The extension's architecture is <b>fundamentally incapable</b> of exfiltrating data to the developer's servers because all inference happens via your chosen LLM providers using your keys. Privacy isn't a policy — it's the code itself.</p>
</td>
</tr>
</table>
🌐 Cloud Library Update Pipeline
The dynamic cloud library is now powered by a GitHub Actions Python Scraper (auto-scraper.yml) that automatically updates the cloud JSON feed with trending, community-sourced prompts.

<div align="center">
```
┌───────────────────────────────┐
│     PromptBoost Pipeline      │
├───────────────────────────────┤
│ Trending / Community Prompts  │
│          (Web Sources)        │
└──────────────┬────────────────┘
               │
       ┌───────▼───────┐
       │ Python Scraper│
       │ auto-scraper.yml │
       │ GitHub Actions│
       └───────┬───────┘
               │
       ┌───────▼───────┐
       │ prompts.json  │
       │ Cloud JSON    │
       │   Feed        │
       └───────────────┘
               │
       Slide-out UI in Extension
```
</div>

🛠️ Tech Stack
<div align="center">
<img src="https://skillicons.dev/icons?i=js,html,css,chrome,git,github,vscode&perline=7&theme=dark" alt="Tech Stack Icons"/>
<br>
LayerTechnologyPurpose🧠 AI EngineGemini 2.0 Flash, Groq Llama-3.3, Mistral, OpenRouterBYOK Intelligent Multi-Engine Rotation🔌 ExtensionChrome MV3 — Service WorkersBackground orchestration💉 InjectionContent Scripts — DOM APIsReact/ProseMirror overrides🎨 UIVanilla CSS — GlassmorphismZero-dependency sidebar☁️ Library FeedCloud JSONLive prompt database🛠️ PipelineGitHub Actions (auto-scraper.yml)Python Scraper for automatic updates
</div>
🎨 UI / UX Design System
The extension's interface avoids the standard "SaaS Bootstrap" aesthetic by implementing a Constructivist Bauhaus design language using pure Vanilla CSS — no frameworks, no dependencies.
 code Code
downloadcontent_copy
expand_less

```
┌─────────────────────────────────────────────────────────┐
│  DESIGN PILLARS                                         │
│                                                         │
│  📐 GEOMETRY    →  Strict programmatic color-blocking   │
│  🌑 DEPTH       →  Hard offset shadows, not soft blurs  │
│  🌊 MOTION      →  CSS translation matrices for reveals │
│  🎭 SIDEBAR     →  Slide-out glassmorphism panel        │
│  🖤 PALETTE     →  #0d1117 base · #10a37f accent        │
└─────────────────────────────────────────────────────────┘
```

Philosophy: Every pixel is intentional. The UI should feel like a precision instrument — not a landing page.
🔬 The React / ProseMirror Injection Hack
Injecting text into modern AI web apps is notoriously difficult. React and ProseMirror maintain their own virtual state trees and silently reject external DOM mutations. PromptBoost targets the HTMLTextAreaElement prototype directly to force the React reconciler to acknowledge the injection as a genuine user event.
 code JavaScript
downloadcontent_copy
expand_less

```
/**
 * PROMPTBOOST — Native React State Override
 * 
 * Intercepts the HTMLTextAreaElement's native setter via Object.getOwnPropertyDescriptor,
 * then fires a bubbling 'input' event to trick React's SyntheticEvent system
 * into treating the programmatic write as organic user input.
 */
function injectIntoReactControlledInput(element, engineeredText) {
  // Step 1: Grab the native setter React has overridden
  const nativeSetter = Object.getOwnPropertyDescriptor(
    window.HTMLTextAreaElement.prototype,
    "value"
  ).set;

  // Step 2: Bypass React's proxy and write directly to the DOM node
  nativeSetter.call(element, engineeredText);

  // Step 3: Dispatch a bubbling synthetic input event — React picks this up
  element.dispatchEvent(new Event("input", { bubbles: true }));
}
```

For contenteditable nodes (Claude, Gemini): PromptBoost uses execCommand('insertText', false, text) with a MutationObserver fallback to handle ProseMirror's immutable document model.
🗺️ Roadmap
<div align="center">
StatusFeature✅Core DOM injection engine for chatgpt.com✅CO-STAR framework transformer✅Cloud JSON prompt library with slide-out sidebar✅Bauhaus Constructivist UI system✅Intelligent Multi-Engine BYOK Rotation (Gemini 2.0 Flash, Groq Llama-3.3, Mistral, OpenRouter)🔄ReAct framework for agentic task prompts✅claude.ai & gemini.google.com support✅Microsoft Edge Store submission⏳Custom prompt framework builder (user-defined templates)⏳Chrome Web Store submission⏳Firefox MV3 port💡Prompt history & versioning
</div>
✅ Done   🔄 In Progress   ⏳ Planned   💡 Idea
<details>
<summary><h2>🚀 Quick Start (Development Setup)</h2></summary>
<br>
Prerequisites: Google Chrome or Microsoft Edge (Manifest V3 supported).
1. Clone the repository
 code Bash
downloadcontent_copy
expand_less

```
git clone https://github.com/SD10LEGACY/PromptBoost.git
cd PromptBoost
```

2. Load as an Unpacked Extension

1. Navigate to chrome://extensions/ (or edge://extensions/ for Edge)

2. Toggle Developer Mode ON (top-right corner)

3. Click "Load unpacked"

4. Select the cloned PromptBoost/ directory

3. Configure API Keys

Open the PromptBoost popup by clicking the extension icon in the toolbar.

Enter your personal API keys for Gemini 2.0 Flash, Groq, Mistral, or OpenRouter.

All keys are securely stored in chrome.storage.local and never sent to any external servers.

4. Start Using PromptBoost

Navigate to any supported AI platform and begin typing — the extension will automatically detect, rewrite using your chosen engine, and inject the engineered prompt.

No special flags or model downloads required.
</details>
<details>
<summary><h2>🤝 Contributing</h2></summary>
<br>
Contributions, issues and feature requests are welcome!

1. Fork the repository

2. Create a feature branch: git checkout -b feat/your-feature-name

3. Commit your changes: git commit -m 'feat: add some feature'

4. Push to your branch: git push origin feat/your-feature-name

5. Open a Pull Request

Please follow Conventional Commits for commit messages.
</details>
<div align="center">
<!-- ══════════════════════════════════════════════════════ -->
<!-- FOOTER ANIMATION -->
<!-- ══════════════════════════════════════════════════════ -->

```
![alt text](https://readme-typing-svg.demolab.com?font=Fira+Code&weight=500&size=15&duration=4000&pause=1500&color=10A37F&center=true&vCenter=true&width=600&height=40&lines=Built+with+BYOK+Multi-Engine+AI+by+Shreyojit.;Privacy+is+not+a+feature.+Its+the+foundation.)
```

 
<br>
<img src="https://komarev.com/ghpvc/?username=SD10LEGACY&label=Profile+Views&color=10a37f&style=for-the-badge" alt="Profile Views"/>
<br><br>
<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0d1117,35:063b35,70:10a37f,100:0d1117&height=140&section=footer&animation=fadeIn" width="100%" alt="PromptBoost Footer"/>
</div>
```
