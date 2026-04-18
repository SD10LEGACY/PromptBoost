/**
 * PROMPTBOOST — CONTENT ENGINE v3.2
 * Shreyojit Das
 *
 * Intentionally thin. All AI calls and remote fetches are delegated to background.js
 * which is CSP-exempt. This file owns: DOM detection, text injection, UI lifecycle.
 */
(function () {
    "use strict";

    const PLATFORM_SELECTORS = {
        'chatgpt.com':       ['#prompt-textarea', 'textarea[data-id="root"]'],
        'claude.ai':         ['.ProseMirror[contenteditable="true"]', 'div[contenteditable="true"]'],
        'gemini.google.com': ['div.ql-editor[contenteditable="true"]', 'rich-textarea div[contenteditable="true"]', 'div[contenteditable="true"]'],
        'perplexity.ai':     ['textarea[placeholder*="Ask"]', 'textarea', 'div[contenteditable="true"]'],
        'grok.com':          ['textarea[placeholder*="Ask"]', 'textarea', 'div[contenteditable="true"]'],
        'x.com':             ['div[contenteditable="true"]', 'textarea'],
    };

    const host = window.location.hostname;
    let platformKey = null;
    for (const domain of Object.keys(PLATFORM_SELECTORS)) {
        if (host.includes(domain)) { platformKey = domain; break; }
    }
    const platformName = platformKey?.split('.')[0] ?? 'unknown';
    if (platformKey) document.body.classList.add('pb-platform-' + platformName);

    // ─────────────────────────────────────────────────────────────────────────

    function findInput() {
        const selectors = platformKey
            ? PLATFORM_SELECTORS[platformKey]
            : ['div[contenteditable="true"]', 'textarea', '.ProseMirror'];

        for (const sel of selectors) {
            const el = document.querySelector(sel);
            if (el) return el;
        }

        // Some platforms (ChatGPT in particular) nest the textarea inside a shadow root
        for (const el of document.querySelectorAll('*')) {
            if (!el.shadowRoot) continue;
            for (const sel of selectors) {
                const found = el.shadowRoot.querySelector(sel);
                if (found) return found;
            }
        }

        const active = document.activeElement;
        if (active && (active.tagName === 'TEXTAREA' || active.getAttribute('contenteditable') === 'true')) {
            return active;
        }
        return null;
    }

    function injectText(text) {
        const input = findInput();
        if (!input) { showToast("❌ Input box not found"); return; }

        input.focus();
        try {
            if (input.tagName === 'TEXTAREA') {
                // React and other frameworks intercept the value setter to track state.
                // Assigning input.value directly bypasses their onChange — we need the
                // native setter so React's synthetic event system picks up the change.
                const nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
                nativeSetter.call(input, text);
                input.dispatchEvent(new Event('input', { bubbles: true }));
            } else {
                // ProseMirror/contenteditable: execCommand is deprecated but remains the
                // only cross-browser way to trigger the editor's internal history stack.
                // Modern alternatives (InputEvent with insertText) don't work consistently.
                document.execCommand('selectAll', false, null);
                document.execCommand('insertText', false, text);
            }
            input.style.height = 'auto';
            input.style.height = input.scrollHeight + 'px';
        } catch (e) {
            console.error('[PB] Text injection failed:', e);
            showToast("❌ Inject failed: " + e.message);
        }
    }

    function runAIEngineer(btn) {
        const input = findInput();
        if (!input) { showToast("❌ No input box found"); return; }

        const draft = (input.value || input.innerText || '').trim();
        if (draft.length < 3) { showToast("⚠️ Type a prompt first!"); return; }

        btn.classList.add('pb-loading');
        btn.textContent = '🌀';

        chrome.runtime.sendMessage({ action: 'engineerPrompt', text: draft }, (response) => {
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

    function loadTrendingLibrary() {
        const container = document.getElementById('pb-cards-container');
        if (!container) return;

        container.textContent = '';
        const loader = document.createElement('div');
        loader.className = 'pb-loader-text';
        loader.textContent = 'SYNCING_REALTIME_DATA...';
        container.appendChild(loader);

        // Fetch is delegated to background.js — direct fetches from content scripts get
        // blocked by ChatGPT's and Gemini's CSP, even for GitHub raw URLs.
        chrome.runtime.sendMessage({ action: 'fetchPrompts' }, (response) => {
            container.textContent = '';

            if (!response?.ok) {
                const errEl = document.createElement('div');
                errEl.className = 'pb-loader-text';
                errEl.textContent = 'NETWORK_ERROR: ' + (response?.error || 'Unknown');
                container.appendChild(errEl);
                return;
            }

            const prompts = response.data || [];
            if (!prompts.length) {
                const emptyEl = document.createElement('div');
                emptyEl.className = 'pb-loader-text';
                emptyEl.textContent = 'DATABASE_EMPTY — trigger GitHub Action';
                container.appendChild(emptyEl);
                return;
            }

            const accentColors = ['var(--pb-red)', 'var(--pb-blue)', 'var(--pb-yellow)'];
            prompts.forEach((prompt, i) => {
                const card    = document.createElement('div');
                card.className = 'pb-card';

                const deco    = document.createElement('div');
                deco.className = 'pb-card-deco';
                deco.style.background = accentColors[i % 3];

                const tag     = document.createElement('div');
                tag.className = 'pb-tag';
                tag.textContent = prompt.tag || 'General';

                const title   = document.createElement('h3');
                title.className = 'pb-card-title';
                title.textContent = prompt.title || 'Untitled';

                const preview = document.createElement('p');
                preview.className = 'pb-card-preview';
                preview.textContent = (prompt.text || '').substring(0, 120) + '...';

                const injectBtn = document.createElement('button');
                injectBtn.className = 'pb-use-btn';
                injectBtn.textContent = 'INJECT_PROMPT';
                injectBtn.onclick = () => {
                    injectText(prompt.text);
                    document.getElementById('pb-sidebar')?.classList.remove('pb-open');
                };

                card.append(deco, tag, title, preview, injectBtn);
                container.appendChild(card);
            });
        });
    }

    function buildSidebar() {
        if (document.getElementById('pb-sidebar')) return;

        const sidebar  = document.createElement('div');
        sidebar.id = 'pb-sidebar';

        const header   = document.createElement('div');
        header.className = 'pb-sidebar-header';

        const heading  = document.createElement('h2');
        heading.className = 'pb-sidebar-title';
        heading.textContent = 'PROMPT_BOOST_LIB';

        const closeBtn = document.createElement('button');
        closeBtn.className = 'pb-close-btn';
        closeBtn.textContent = '×';
        closeBtn.onclick = () => sidebar.classList.remove('pb-open');

        header.append(heading, closeBtn);

        const body = document.createElement('div');
        body.className = 'pb-sidebar-content';
        body.id = 'pb-cards-container';

        sidebar.append(header, body);
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
        if (!parent) return;
        parent.style.position = 'relative';
        parent.appendChild(group);

        buildSidebar();
    }

    function showToast(msg) {
        const toast = document.createElement('div');
        toast.className = 'pb-status-msg';
        toast.textContent = msg;
        document.body.appendChild(toast);
        setTimeout(() => toast.remove(), 3000);
    }

    // ─────────────────────────────────────────────────────────────────────────

    const domObserver = new MutationObserver(() => injectButtons());
    domObserver.observe(document.body, { childList: true, subtree: true });

    // Initial injection attempt after a brief delay — many SPAs don't have the
    // input rendered synchronously on DOMContentLoaded.
    setTimeout(injectButtons, 1500);
})();
