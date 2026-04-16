/**
 * PROMPTBOOST - CONTENT ENGINE v3.2
 * Developed by: Shreyojit Das (Class of 2026, IEM)
 *
 * This file is intentionally thin.
 * All AI calls and fetches live in background.js (CSP-exempt).
 * This file only handles: DOM detection, text injection, UI.
 */
(function () {
    "use strict";

    const PLATFORM_SELECTORS = {
        'chatgpt.com':         ['#prompt-textarea', 'textarea[data-id="root"]'],
        'claude.ai':           ['.ProseMirror[contenteditable="true"]', 'div[contenteditable="true"]'],
        'gemini.google.com':   ['div.ql-editor[contenteditable="true"]', 'rich-textarea div[contenteditable="true"]', 'div[contenteditable="true"]'],
        'perplexity.ai':       ['textarea[placeholder*="Ask"]', 'textarea', 'div[contenteditable="true"]'],
        'grok.com':            ['textarea[placeholder*="Ask"]', 'textarea', 'div[contenteditable="true"]'],
        'x.com':               ['div[contenteditable="true"]', 'textarea'],
    };

    // ── PLATFORM ──────────────────────────────────────────────────────────
    const host = window.location.hostname;
    let PLATFORM_KEY = null;
    for (const domain of Object.keys(PLATFORM_SELECTORS)) {
        if (host.includes(domain)) { PLATFORM_KEY = domain; break; }
    }
    const PLATFORM_NAME = PLATFORM_KEY?.split('.')[0] || 'unknown';
    if (PLATFORM_KEY) document.body.classList.add('pb-platform-' + PLATFORM_NAME);

    // ── INPUT FINDER ──────────────────────────────────────────────────────
    function findInput() {
        const selectors = PLATFORM_KEY
            ? PLATFORM_SELECTORS[PLATFORM_KEY]
            : ['div[contenteditable="true"]', 'textarea', '.ProseMirror'];

        for (const sel of selectors) {
            const el = document.querySelector(sel);
            if (el) return el;
        }
        for (const el of document.querySelectorAll('*')) {
            if (el.shadowRoot) {
                for (const sel of selectors) {
                    const found = el.shadowRoot.querySelector(sel);
                    if (found) return found;
                }
            }
        }
        const active = document.activeElement;
        if (active && (active.tagName === 'TEXTAREA' || active.getAttribute('contenteditable') === 'true')) return active;
        return null;
    }

    // ── INJECT TEXT ───────────────────────────────────────────────────────
    function injectText(text) {
        const input = findInput();
        if (!input) { showToast("❌ Input box not found"); return; }
        input.focus();
        try {
            if (input.tagName === 'TEXTAREA') {
                const setter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
                setter.call(input, text);
                input.dispatchEvent(new Event('input', { bubbles: true }));
            } else {
                document.execCommand('selectAll', false, null);
                document.execCommand('insertText', false, text);
            }
            input.style.height = 'auto';
            input.style.height = input.scrollHeight + 'px';
        } catch (e) {
            console.error('PB inject error:', e);
            showToast("❌ Inject failed: " + e.message);
        }
    }

    // ── AI ENGINEER ───────────────────────────────────────────────────────
    // Sends to background.js → rotates through Gemini → Groq → Mistral → OpenRouter
    function runAIEngineer(btn) {
        const input = findInput();
        if (!input) { showToast("❌ No input box found"); return; }
        const rawText = (input.value || input.innerText || '').trim();
        if (rawText.length < 3) { showToast("⚠️ Type a prompt first!"); return; }

        btn.classList.add('pb-loading');
        btn.textContent = '🌀';

        chrome.runtime.sendMessage({ action: 'engineerPrompt', text: rawText }, (response) => {
            btn.classList.remove('pb-loading');
            btn.textContent = '✨';
            if (response?.ok) {
                injectText(response.data);
                showToast("✅ Engineered via " + (response.engine || 'AI'));
            } else {
                showToast("❌ " + (response?.error || 'AI failed'));
            }
        });
    }

    // ── TRENDING LIBRARY ──────────────────────────────────────────────────
    // background.js does the fetch — bypasses ChatGPT/Gemini/Grok CSP
    function loadTrendingLibrary() {
        const container = document.getElementById('pb-cards-container');
        if (!container) return;

        container.textContent = '';
        const loader = document.createElement('div');
        loader.className = 'pb-loader-text';
        loader.textContent = 'SYNCING_REALTIME_DATA...';
        container.appendChild(loader);

        chrome.runtime.sendMessage({ action: 'fetchPrompts' }, (response) => {
            container.textContent = '';
            if (!response?.ok) {
                const err = document.createElement('div');
                err.className = 'pb-loader-text';
                err.textContent = 'NETWORK_ERROR: ' + (response?.error || 'Unknown');
                container.appendChild(err);
                return;
            }
            const prompts = response.data || [];
            if (!prompts.length) {
                const empty = document.createElement('div');
                empty.className = 'pb-loader-text';
                empty.textContent = 'DATABASE_EMPTY — trigger GitHub Action';
                container.appendChild(empty);
                return;
            }
            const colors = ['var(--pb-red)', 'var(--pb-blue)', 'var(--pb-yellow)'];
            prompts.forEach((p, i) => {
                const card = document.createElement('div');
                card.className = 'pb-card';
                const deco = document.createElement('div');
                deco.className = 'pb-card-deco';
                deco.style.background = colors[i % 3];
                const tag = document.createElement('div');
                tag.className = 'pb-tag';
                tag.textContent = p.tag || 'General';
                const title = document.createElement('h3');
                title.className = 'pb-card-title';
                title.textContent = p.title || 'Untitled';
                const preview = document.createElement('p');
                preview.className = 'pb-card-preview';
                preview.textContent = (p.text || '').substring(0, 120) + '...';
                const btn = document.createElement('button');
                btn.className = 'pb-use-btn';
                btn.textContent = 'INJECT_PROMPT';
                btn.onclick = () => {
                    injectText(p.text);
                    document.getElementById('pb-sidebar')?.classList.remove('pb-open');
                };
                card.append(deco, tag, title, preview, btn);
                container.appendChild(card);
            });
        });
    }

    // ── UI BUILDERS ───────────────────────────────────────────────────────
    function buildSidebar() {
        if (document.getElementById('pb-sidebar')) return;
        const sidebar = document.createElement('div');
        sidebar.id = 'pb-sidebar';
        const header = document.createElement('div');
        header.className = 'pb-sidebar-header';
        const h2 = document.createElement('h2');
        h2.className = 'pb-sidebar-title';
        h2.textContent = 'PROMPT_BOOST_LIB';
        const closeBtn = document.createElement('button');
        closeBtn.className = 'pb-close-btn';
        closeBtn.textContent = '×';
        closeBtn.onclick = () => sidebar.classList.remove('pb-open');
        header.append(h2, closeBtn);
        const content = document.createElement('div');
        content.className = 'pb-sidebar-content';
        content.id = 'pb-cards-container';
        sidebar.append(header, content);
        document.body.appendChild(sidebar);
    }

    function injectButtons() {
        const input = findInput();
        if (!input || document.querySelector('.pb-btn-group')) return;
        const group = document.createElement('div');
        group.className = 'pb-btn-group';
        const wandBtn = document.createElement('button');
        wandBtn.className = 'pb-native-btn pb-wand-btn';
        wandBtn.title = 'AI Engineer (Gemini → Groq → Mistral fallback)';
        wandBtn.textContent = '✨';
        wandBtn.onclick = (e) => { e.preventDefault(); runAIEngineer(e.currentTarget); };
        const libBtn = document.createElement('button');
        libBtn.className = 'pb-native-btn pb-lib-btn';
        libBtn.title = 'Trending Prompt Library';
        libBtn.textContent = '📚';
        libBtn.onclick = (e) => {
            e.preventDefault();
            document.getElementById('pb-sidebar')?.classList.add('pb-open');
            loadTrendingLibrary();
        };
        group.append(wandBtn, libBtn);
        const parent = input.parentElement;
        if (parent) {
            parent.style.position = 'relative';
            parent.appendChild(group);
        }
        buildSidebar();
    }

    // ── TOAST ─────────────────────────────────────────────────────────────
    function showToast(msg) {
        const toast = document.createElement('div');
        toast.className = 'pb-status-msg';
        toast.textContent = msg;
        document.body.appendChild(toast);
        setTimeout(() => toast.remove(), 3000);
    }

    // ── OBSERVER ──────────────────────────────────────────────────────────
    const observer = new MutationObserver(() => injectButtons());
    observer.observe(document.body, { childList: true, subtree: true });
    setTimeout(injectButtons, 1500);
})();
