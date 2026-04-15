<div align="center">

# ⚡ PromptBoost
### *The On-Device Prompt Engineering Engine*

[![Chrome Web Store](https://img.shields.io/badge/Chrome_Web_Store-Pending-blue?style=for-the-badge&logo=googlechrome)](#)
[![Manifest V3](https://img.shields.io/badge/Manifest_V3-Compliant-success?style=for-the-badge&logo=googlechrome)](#)
[![Gemini Nano](https://img.shields.io/badge/AI-Gemini_Nano-8A2BE2?style=for-the-badge&logo=googlebard)](#)
[![License](https://img.shields.io/badge/License-MIT-gray?style=for-the-badge)](#)

*A privacy-first, zero-latency browser extension that seamlessly intercepts and perfectly engineers your LLM prompts using Chrome's Built-In AI.*

<br>

<img src="https://via.placeholder.com/800x400/10a37f/ffffff?text=[Drop+Your+Animated+Demo+GIF+Here]" width="100%" alt="PromptBoost Demo" style="border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.2);">

</div>

<br>

> **The Problem:** Cloud-based prompt engineers introduce network latency, require expensive API keys, and force you to send private chat context to third-party servers.
>
> **The Solution:** PromptBoost utilizes on-device inference to rewrite rough text into scientifically backed prompt frameworks (CO-STAR, ReAct) *before* injecting them directly into the DOM of major AI platforms.

---

## ✨ Core Architecture & Features

<table>
  <tr>
    <td width="50%">
      <h3>🧠 Local-First Inference</h3>
      <p>Powered exclusively by Chrome's experimental <code>window.ai</code> (Gemini Nano) API. <b>Zero API keys, zero latency, and 100% privacy</b>—your keystrokes never leave your local machine.</p>
    </td>
    <td width="50%">
      <h3>⚡ DOM-Level Interception</h3>
      <p>Bypasses standard <code>value</code> assignments by dispatching React Synthetic Events and formatting <code>contenteditable</code> nodes to natively control complex SPAs.</p>
    </td>
  </tr>
  <tr>
    <td width="50%">
      <h3>📚 Dynamic Cloud Library</h3>
      <p>A slide-out, glassmorphism UI that fetches a live database of trending prompts. Updates happen instantly via a cloud JSON, requiring no Chrome Web Store version bumps.</p>
    </td>
    <td width="50%">
      <h3>🎯 Context-Aware SPAs</h3>
      <p>Automatically detects the host environment (<code>chatgpt.com</code>, <code>claude.ai</code>) and serves platform-specific prompt frameworks, filtering out irrelevant structural data.</p>
    </td>
  </tr>
</table>

---

## 🎨 UI / UX Design System

The extension's interface avoids the standard "bootstrap" look by implementing a **Constructivist Bauhaus** aesthetic using pure Vanilla CSS. 
* **Geometry:** Strict, programmatic color-blocking.
* **Depth:** Hard offset shadows rather than soft blurs.
* **Motion:** Smooth CSS translation matrices for the slide-out sidebar.

---

## 🛠️ The React / ProseMirror Injection Hack

Injecting text into modern AI web apps is notoriously difficult because they do not use standard textareas. ChatGPT uses tightly controlled React inputs, while Claude relies on ProseMirror `contenteditable` wrappers. 

PromptBoost solves this by targeting the `HTMLTextAreaElement` prototype directly, forcing the React state manager to acknowledge the external injection without breaking the internal state of the application.

```javascript
// Native React State Override Logic
const setter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, "value").set;

// Bypass the DOM and set value at the prototype level
setter.call(inputElement, engineeredPromptText);

// Force the SPA to register the change
inputElement.dispatchEvent(new Event('input', { bubbles: true }));