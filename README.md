code
Markdown
download
content_copy
expand_less
<div align="center">

<!-- ══════════════════════════════════════════════════════ -->
<!--                   ANIMATED HEADER                      -->
<!-- ══════════════════════════════════════════════════════ -->

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0d1117,35:063b35,70:10a37f,100:0d1117&height=300&section=header&text=PromptBoost&fontSize=82&fontAlignY=42&fontColor=ffffff&desc=The%20Intelligent%20Prompt%20Engineering%20Engine&descAlignY=62&descSize=24&animation=fadeIn&v=2" width="100%" alt="PromptBoost Header"/>

<!-- ══════════════════════════════════════════════════════ -->
<!--                  TYPING ANIMATION                      -->
<!-- ══════════════════════════════════════════════════════ -->

[![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=18&duration=2800&pause=900&color=10A37F&center=true&vCenter=true&width=750&height=48&lines=Bring+Your+Own+Key+(BYOK)+Architecture;Intelligent+Multi-Engine+Rotation;Gemini+2.0+Flash,+Groq,+Mistral,+OpenRouter;Keys+Safely+Stored+in+chrome.storage.local;CO-STAR+and+ReAct+Frameworks+On+the+Fly.;Bauhaus+Constructivist+UI+-+Pure+Vanilla+CSS.)](https://git.io/typing-svg)

<br><br>

<!-- ══════════════════════════════════════════════════════ -->
<!--                      BADGES                            -->
<!-- ══════════════════════════════════════════════════════ -->

<p>
  <img src="https://img.shields.io/badge/Microsoft_Edge-IN_REVIEW-0078D7?style=for-the-badge&logo=microsoftedge&logoColor=white" alt="Microsoft Edge"/>
  <img src="https://img.shields.io/badge/Chrome_Extension-COMING_SOON-10a37f?style=for-the-badge&logo=googlechrome&logoColor=white" alt="Chrome Extension"/>
</p>
<p>
  <img src="https://img.shields.io/badge/Manifest-V3_Compliant-4ade80?style=for-the-badge&logo=googlechrome&logoColor=black" alt="Manifest V3"/>
  <img src="https://img.shields.io/badge/Multi--Engine-BYOK_Supported-8A2BE2?style=for-the-badge&logo=smartthings&logoColor=white" alt="Multi-Engine"/>
</p>
<p>
  <img src="https://img.shields.io/badge/Privacy-100%25_Local_Storage-ef4444?style=for-the-badge&logo=shield&logoColor=white" alt="Privacy"/>
  <img src="https://img.shields.io/badge/License-MIT-3b82f6?style=for-the-badge&logo=opensourceinitiative&logoColor=white" alt="MIT License"/>
</p>

<br>

> *A privacy-first browser extension that seamlessly intercepts and perfectly engineers your LLM prompts using your own API keys via Intelligent Multi-Engine Rotation — securely stored on your device.*

<br>

</div>

***

<div align="center">

## 🚨 The Problem. The Solution.

</div>

> **🔴 The Problem:** Cloud-based prompt engineers introduce platform lock-in, require you to use their specific models, and force you to send **private chat context** to third-party servers you don't control.
>
> **🟢 The Solution:** PromptBoost leverages **Bring Your Own Key (BYOK)** architecture coupled with **Intelligent Multi-Engine Rotation** (Gemini 2.0 Flash, Groq Llama-3.3, Mistral, and OpenRouter) to silently rewrite rough, unstructured text into scientifically-backed prompt frameworks (`CO-STAR`, `ReAct`). All keys remain completely localized via `chrome.storage.local`. **No middleman servers. No tracking. No compromise.**

***

## ✨ Core Architecture & Features

<table>
  <tr>
    <td width="50%" valign="top">
      <h3>🧠 Intelligent Multi-Engine Rotation</h3>
      <p>Powered by a flexible Bring Your Own Key (BYOK) system. PromptBoost dynamically falls back and rotates between <b>Gemini 2.0 Flash, Groq Llama-3.3, Mistral, and OpenRouter</b> to ensure guaranteed uptime and blazing-fast prompt rewriting.</p>
    </td>
    <td width="50%" valign="top">
      <h3>⚡ DOM-Level Interception</h3>
      <p>Bypasses standard <code>value</code> assignments by dispatching React Synthetic Events and formatting <code>contenteditable</code> nodes. Natively controls complex Single-Page Applications without breaking their internal state.</p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>📚 Dynamic Cloud Library</h3>
      <p>A slide-out, glassmorphism UI panel that fetches a live database of trending, community-sourced prompts. Updates propagate instantly via a cloud JSON feed powered by a <b>GitHub Actions Python Scraper</b> — no store re-submission required.</p>
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
      <p>There is no telemetry, no analytics, no logging. Your API keys are strictly kept in <b><code>chrome.storage.local</code></b>. Nothing is sent to our servers. You communicate directly with the LLM providers, ensuring your data remains entirely under your control.</p>
    </td>
  </tr>
</table>

***

## 🤖 Automated Scraper Pipeline

The dynamic cloud library isn't manually updated. Instead, PromptBoost utilizes an automated pipeline built on GitHub Actions. A Python scraping script (`auto-scraper.yml`) runs on a schedule to discover trending prompts, validate them, and compile them into a centralized JSON feed.

```text
┌──────────────────┐      ┌────────────────────────┐      ┌─────────────────┐
│  Trending Web    │ ───▶ │ GitHub Actions Scraper │ ───▶ │  Cloud JSON     │
│  Prompt Sources  │      │  (auto-scraper.yml)    │      │  Database Feed  │
└──────────────────┘      └────────────────────────┘      └─────────────────┘
                                                                   │
                                                                   ▼
                                                          ┌─────────────────┐
                                                          │ PromptBoost Ext │
                                                          │  (Sidebar UI)   │
                                                          └─────────────────┘
🛠️ Tech Stack
<div align="center">

<img src="https://skillicons.dev/icons?i=js,html,css,githubactions,python,chrome,git,github,vscode&perline=9&theme=dark" alt="Tech Stack Icons"/>

<br>

Layer	Technology	Purpose
🧠 Primary AI	Gemini 2.0 Flash	Blazing fast primary prompt engineering
⚡ Speed AI	Groq (Llama-3.3)	High-speed fallback inference engine
🌬️ Alt AI	Mistral	Alternative routing model
🌐 Hub AI	OpenRouter	Universal fallback and flexible access
🔌 Extension	MV3 — Service Workers	Background orchestration
🤖 Automation	GitHub Actions	Python scraper for live prompt library (auto-scraper.yml)
💉 Injection	Content Scripts — DOM APIs	React/ProseMirror overrides
🎨 UI	Vanilla CSS — Glassmorphism	Zero-dependency sidebar
☁️ Library Feed	Cloud JSON	Live prompt database
</div>

🎨 UI / UX Design System

The extension's interface avoids the standard "SaaS Bootstrap" aesthetic by implementing a Constructivist Bauhaus design language using pure Vanilla CSS — no frameworks, no dependencies.

code
Code
download
content_copy
expand_less
┌─────────────────────────────────────────────────────────┐
│  DESIGN PILLARS                                         │
│                                                         │
│  📐 GEOMETRY    →  Strict programmatic color-blocking   │
│  🌑 DEPTH       →  Hard offset shadows, not soft blurs  │
│  🌊 MOTION      →  CSS translation matrices for reveals │
│  🎭 SIDEBAR     →  Slide-out glassmorphism panel        │
│  🖤 PALETTE     →  #0d1117 base · #10a37f accent        │
└─────────────────────────────────────────────────────────┘

Philosophy: Every pixel is intentional. The UI should feel like a precision instrument — not a landing page.

🔬 The React / ProseMirror Injection Hack

Injecting text into modern AI web apps is notoriously difficult. React and ProseMirror maintain their own virtual state trees and silently reject external DOM mutations. PromptBoost targets the HTMLTextAreaElement prototype directly to force the React reconciler to acknowledge the injection as a genuine user event.

code
JavaScript
download
content_copy
expand_less
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

For contenteditable nodes (Claude, Gemini): PromptBoost uses execCommand('insertText', false, text) with a MutationObserver fallback to handle ProseMirror's immutable document model.

🗺️ Roadmap
<div align="center">

Status	Feature
✅	Microsoft Edge Add-ons Store submission
✅	Intelligent Multi-Engine Rotation (Gemini, Groq, Mistral, OpenRouter)
✅	GitHub Actions Python Scraper integration
✅	Core DOM injection engine for chatgpt.com
✅	CO-STAR framework transformer
✅	Cloud JSON prompt library with slide-out sidebar
✅	Bauhaus Constructivist UI system
🔄	ReAct framework for agentic task prompts
🔄	claude.ai & gemini.google.com support
⏳	Custom prompt framework builder (user-defined templates)
⏳	Chrome Web Store submission
💡	Prompt history & versioning
</div>


✅ Done   🔄 In Progress   ⏳ Planned   💡 Idea

<details>
<summary><h2>🚀 Quick Start (Development Setup)</h2></summary>

<br>


1. Clone the repository

code
Bash
download
content_copy
expand_less
git clone https://github.com/SD10LEGACY/PromptBoost.git
cd PromptBoost

2. Load as an Unpacked Extension

Navigate to chrome://extensions/ or edge://extensions/ in your browser.

Toggle Developer Mode ON (usually top-right corner).

Click "Load unpacked".

Select the cloned PromptBoost/ directory.

3. Configure Your API Keys (BYOK)

Click on the PromptBoost icon in your browser toolbar to open the popup.

Enter your preferred API keys (Gemini, Groq, Mistral, or OpenRouter).

Click Save. Note: Your keys are instantly stored in your browser's local sandbox via chrome.storage.local and will never be transmitted to our servers.

4. Start Prompt Engineering

Navigate to chatgpt.com, type your rough prompt, and watch PromptBoost silently intercept and supercharge your input using your designated LLM engine!

</details>

<details>
<summary><h2>🤝 Contributing</h2></summary>

<br>


Contributions, issues and feature requests are welcome!

Fork the repository

Create a feature branch: git checkout -b feat/your-feature-name

Commit your changes: git commit -m 'feat: add some feature'

Push to your branch: git push origin feat/your-feature-name

Open a Pull Request

Please follow Conventional Commits for commit messages.

</details>

<div align="center">

<!-- ══════════════════════════════════════════════════════ -->

<!-- FOOTER ANIMATION -->

<!-- ══════════════════════════════════════════════════════ -->


![alt text](https://readme-typing-svg.demolab.com?font=Fira+Code&weight=500&size=15&duration=4000&pause=1500&color=10A37F&center=true&vCenter=true&width=600&height=40&lines=Built+with+BYOK+Architecture+by+Shreyojit.;Your+Keys+Never+Leave+Your+Local+Storage.)

<br>

<img src="https://komarev.com/ghpvc/?username=SD10LEGACY&label=Profile+Views&color=10a37f&style=for-the-badge" alt="Profile Views"/>


<br><br>

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0d1117,35:063b35,70:10a37f,100:0d1117&height=140&section=footer&animation=fadeIn" width="100%" alt="PromptBoost Footer"/>

</div>
```
