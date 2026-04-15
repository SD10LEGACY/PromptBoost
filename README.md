The reason the image wasn't loading is likely because GitHub blocked the placeholder URL, or the raw Markdown syntax (`![]()`) got stripped when copying and pasting.

To make this README truly immersive and recruiter-ready, we are going to use **Capsule Render** (which generates a beautiful, animated SVG wave banner natively in GitHub) and clean up the HTML grid.

Here is the upgraded, ultra-premium Markdown.

### What to do:

1.  Open your `README.md` file in VS Code.
2.  Delete **everything** currently in it.
3.  Copy the code block below and paste it in.

-----

````markdown
<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=10a37f&height=250&section=header&text=⚡%20PromptBoost&fontSize=70&fontAlignY=38&fontColor=ffffff&desc=The%20On-Device%20Prompt%20Engineering%20Engine&descAlignY=58&descSize=20" width="100%">

<p align="center">
  <img src="https://img.shields.io/badge/Chrome_Web_Store-Pending-10a37f?style=for-the-badge&logo=googlechrome&logoColor=white" alt="Chrome">
  <img src="https://img.shields.io/badge/Manifest_V3-Compliant-success?style=for-the-badge" alt="Manifest V3">
  <img src="https://img.shields.io/badge/AI-Gemini_Nano-8A2BE2?style=for-the-badge&logo=googlebard&logoColor=white" alt="Gemini Nano">
</p>

*A privacy-first, zero-latency browser extension that seamlessly intercepts and perfectly engineers your LLM prompts using Chrome's Built-In AI.*

</div>

<br>

> **The Problem:** Cloud-based prompt engineers introduce network latency, require expensive API keys, and force you to send private chat context to third-party servers.
>
> **The Solution:** PromptBoost utilizes on-device inference to rewrite rough text into scientifically backed prompt frameworks (CO-STAR, ReAct) *before* injecting them directly into the DOM of major AI platforms.

---

## ✨ Core Architecture & Features

<table style="width:100%">
  <tr>
    <td width="50%" valign="top">
      <h3>🧠 Local-First Inference</h3>
      <p>Powered exclusively by Chrome's experimental <code>window.ai</code> (Gemini Nano) API. <b>Zero API keys, zero latency, and 100% privacy</b>—your keystrokes never leave your local machine.</p>
    </td>
    <td width="50%" valign="top">
      <h3>⚡ DOM-Level Interception</h3>
      <p>Bypasses standard <code>value</code> assignments by dispatching React Synthetic Events and formatting <code>contenteditable</code> nodes to natively control complex SPAs.</p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>📚 Dynamic Cloud Library</h3>
      <p>A slide-out, glassmorphism UI that fetches a live database of trending prompts. Updates happen instantly via a cloud JSON, requiring no Chrome Web Store version bumps.</p>
    </td>
    <td width="50%" valign="top">
      <h3>🎯 Context-Aware SPAs</h3>
      <p>Automatically detects the host environment (<code>chatgpt.com</code>, <code>claude.ai</code>) and serves platform-specific prompt frameworks, filtering out irrelevant structural data.</p>
    </td>
  </tr>
</table>

---

## 🎨 UI / UX Design System

The extension's interface avoids the standard "bootstrap" look by implementing a **Constructivist Bauhaus** aesthetic using pure Vanilla CSS. 

* 📐 **Geometry:** Strict, programmatic color-blocking.
* 🌑 **Depth:** Hard offset shadows rather than soft blurs.
* 🌊 **Motion:** Smooth CSS translation matrices for the slide-out sidebar.

---

## 🛠️ The React / ProseMirror Injection Hack

Injecting text into modern AI web apps is notoriously difficult because they do not use standard `<textarea>` elements. ChatGPT uses tightly controlled React inputs, while Claude relies on ProseMirror `contenteditable` wrappers. 

PromptBoost solves this by targeting the `HTMLTextAreaElement` prototype directly, forcing the React state manager to acknowledge the external injection without breaking the internal state of the application.

```javascript
// Native React State Override Logic
const setter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, "value").set;

// Bypass the DOM and set value at the prototype level
setter.call(inputElement, engineeredPromptText);

// Force the SPA to register the change
inputElement.dispatchEvent(new Event('input', { bubbles: true }));
````

-----

\<details\>
\<summary\>\<h2\>🚀 Quick Start (Development)\</h2\>\</summary\>

Want to run PromptBoost locally in VS Code?

1.  Clone the repository:
    ```bash
    git clone [https://github.com/SD10LEGACY/PromptBoost.git](https://github.com/SD10LEGACY/PromptBoost.git)
    ```
2.  Open the project in **VS Code**.
3.  Ensure Chrome's Built-In AI is active:
      * Navigate to `chrome://flags/#prompt-api-for-gemini-nano` and set to **Enabled**.
      * Navigate to `chrome://components` and update the **Optimization Guide On Device Model**.
4.  Go to `chrome://extensions/`, enable **Developer Mode**, and click **Load unpacked**.
5.  Select the `PromptBoost` directory.

\</details\>

<br>

\<div align="center"\>
\<p\>Built with ☕ and on-device AI by Shreyojit.\</p\>
\</div\>

```
```