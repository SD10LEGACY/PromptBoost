<div align="center">

<!-- ══════════════════════════════════════════════════════ -->
<!--                   ANIMATED HEADER                      -->
<!-- ══════════════════════════════════════════════════════ -->

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0d1117,35:063b35,70:10a37f,100:0d1117&height=300&section=header&text=⚡%20PromptBoost&fontSize=82&fontAlignY=42&fontColor=ffffff&desc=The%20On-Device%20Prompt%20Engineering%20Engine&descAlignY=62&descSize=24&animation=fadeIn&stroke=10a37f&strokeWidth=2" width="100%" alt="PromptBoost Header"/>

<!-- ══════════════════════════════════════════════════════ -->
<!--                  TYPING ANIMATION (FIXED)              -->
<!-- ══════════════════════════════════════════════════════ -->

[](https://github.com/SD10LEGACY/PromptBoost)

<br><br>

<!-- ══════════════════════════════════════════════════════ -->
<!--                      BADGES                            -->
<!-- ══════════════════════════════════════════════════════ -->

<p>
  <img src="https://img.shields.io/badge/Chrome_Extension-In_Development-10a37f?style=for-the-badge&logo=googlechrome&logoColor=white" alt="Chrome Extension"/>
  <img src="https://img.shields.io/badge/Manifest-V3_Compliant-4ade80?style=for-the-badge&logo=googlechrome&logoColor=black" alt="Manifest V3"/>
  <img src="https://img.shields.io/badge/Gemini_Nano-Built--In_AI-8A2BE2?style=for-the-badge&logo=google&logoColor=white" alt="Gemini Nano"/>
</p>
<p>
  <img src="https://img.shields.io/badge/Privacy-100%25_On--Device-ef4444?style=for-the-badge&logo=shield&logoColor=white" alt="Privacy"/>
  <img src="https://img.shields.io/badge/API_Keys-Zero_Required-f59e0b?style=for-the-badge&logo=keycdn&logoColor=white" alt="No API Keys"/>
  <img src="https://img.shields.io/badge/License-MIT-3b82f6?style=for-the-badge&logo=opensourceinitiative&logoColor=white" alt="MIT License"/>
</p>

<br>

> *A privacy-first, zero-latency browser extension that seamlessly intercepts and perfectly engineers your LLM prompts using Chrome's Built-In AI — before they ever reach a server.*

<br>

</div>

***

<div align="center">

## 🚨 The Problem. The Solution.

</div>

> **🔴 The Problem:** Cloud-based prompt engineers introduce network latency, require expensive API keys, and force you to send **private chat context** to third-party servers you don't control.
>
> **🟢 The Solution:** PromptBoost leverages **on-device inference** to silently rewrite rough, unstructured text into scientifically-backed prompt frameworks (`CO-STAR`, `ReAct`) — *before* injecting them directly into the DOM of major AI platforms. **No cloud. No cost. No compromise.**

***

## ✨ Core Architecture & Features

<table>
  <tr>
    <td width="50%" valign="top">
      <h3>🧠 Local-First Inference</h3>
      <p>Powered exclusively by Chrome's experimental <code>window.ai</code> (Gemini Nano) API. <b>Zero API keys, zero network latency, and 100% privacy</b> — your keystrokes never leave your local machine or touch a third-party server.</p>
    </td>
    <td width="50%" valign="top">
      <h3>⚡ DOM-Level Interception</h3>
      <p>Bypasses standard <code>value</code> assignments by dispatching React Synthetic Events and formatting <code>contenteditable</code> nodes. Natively controls complex Single-Page Applications without breaking their internal state.</p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>📚 Dynamic Cloud Library</h3>
      <p>A slide-out, glassmorphism UI panel that fetches a live database of trending, community-sourced prompts. Updates propagate instantly via a cloud JSON feed — <b>no Chrome Web Store re-submission required.</b></p>
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
      <p>There is no telemetry, no analytics, no logging. The extension's architecture is <b>fundamentally incapable</b> of exfiltrating data because inference runs inside Chrome's sandboxed on-device model. Privacy isn't a policy — it's the code itself.</p>
    </td>
  </tr>
</table>

***

## 🛠️ Tech Stack

<div align="center">

<img src="https://skillicons.dev/icons?i=js,html,css,chrome,git,github,vscode&perline=7&theme=dark" alt="Tech Stack Icons"/>

<br>

| Layer | Technology | Purpose |
|---|---|---|
| 🧠 **AI Engine** | `window.ai` — Gemini Nano | On-device prompt rewriting |
| 🔌 **Extension** | Chrome MV3 — Service Workers | Background orchestration |
| 💉 **Injection** | Content Scripts — DOM APIs | React/ProseMirror overrides |
| 🎨 **UI** | Vanilla CSS — Glassmorphism | Zero-dependency sidebar |
| ☁️ **Library Feed** | Cloud JSON | Live prompt database |

</div>

***

## 🎨 UI / UX Design System

The extension's interface avoids the standard "SaaS Bootstrap" aesthetic by implementing a **Constructivist Bauhaus** design language using pure Vanilla CSS — no frameworks, no dependencies.

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

> **Philosophy:** Every pixel is intentional. The UI should feel like a precision instrument — not a landing page.

***

## 🔬 The React / ProseMirror Injection Hack

Injecting text into modern AI web apps is notoriously difficult. React and ProseMirror maintain their own virtual state trees and **silently reject** external DOM mutations. PromptBoost targets the `HTMLTextAreaElement` prototype directly to force the React reconciler to acknowledge the injection as a genuine user event.

```javascript
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

> **For `contenteditable` nodes** (Claude, Gemini): PromptBoost uses `execCommand('insertText', false, text)` with a `MutationObserver` fallback to handle ProseMirror's immutable document model.

***

## 🗺️ Roadmap

<div align="center">

| Status | Feature |
|:---:|---|
| ✅ | Core DOM injection engine for `chatgpt.com` |
| ✅ | CO-STAR framework transformer |
| ✅ | Cloud JSON prompt library with slide-out sidebar |
| ✅ | Bauhaus Constructivist UI system |
| 🔄 | ReAct framework for agentic task prompts |
| 🔄 | `claude.ai` & `gemini.google.com` support |
| ⏳ | Custom prompt framework builder (user-defined templates) |
| ⏳ | Chrome Web Store submission |
| ⏳ | Firefox MV3 port |
| 💡 | Prompt history & versioning |

</div>

`✅ Done` &nbsp; `🔄 In Progress` &nbsp; `⏳ Planned` &nbsp; `💡 Idea`

***

<details>
<summary><h2>🚀 Quick Start (Development Setup)</h2></summary>

<br>

**Prerequisites:** Chrome Canary or Chrome Dev Channel with Built-In AI flags enabled.

**1. Clone the repository**
```bash
git clone https://github.com/SD10LEGACY/PromptBoost.git
cd PromptBoost
```

**2. Enable Chrome's Built-In AI APIs**

Open Chrome and navigate to the following flags:
```
chrome://flags/#prompt-api-for-gemini-nano
chrome://flags/#optimization-guide-on-device-model
```
Set both to **`Enabled`**, then relaunch Chrome.

**3. Load as an Unpacked Extension**

1. Navigate to `chrome://extensions/`
2. Toggle **Developer Mode** ON (top-right corner)
3. Click **"Load unpacked"**
4. Select the cloned `PromptBoost/` directory

**4. Verify On-Device Model**

Open the browser console on any page and run:
```javascript
// Should return a session object, not an error
const session = await window.ai.languageModel.create();
console.log(await session.prompt("Hello, are you on-device?"));
```

✅ If you get a response, PromptBoost is ready to run.

</details>

***

<details>
<summary><h2>🤝 Contributing</h2></summary>

<br>

Contributions, issues and feature requests are welcome!

1. **Fork** the repository
2. Create a feature branch: `git checkout -b feat/your-feature-name`
3. Commit your changes: `git commit -m 'feat: add some feature'`
4. Push to your branch: `git push origin feat/your-feature-name`
5. Open a **Pull Request**

Please follow [Conventional Commits](https://www.conventionalcommits.org/) for commit messages.

</details>

***

<div align="center">

<!-- ══════════════════════════════════════════════════════ -->
<!--                    FOOTER ANIMATION (FIXED)            -->
<!-- ══════════════════════════════════════════════════════ -->

[

<br>

<img src="https://komarev.com/ghpvc/?username=SD10LEGACY&label=Profile+Views&color=10a37f&style=for-the-badge" alt="Profile Views"/>

<br><br>

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0d1117,35:063b35,70:10a37f,100:0d1117&height=140&section=footer&animation=fadeIn" width="100%" alt="PromptBoost Footer"/>

</div>