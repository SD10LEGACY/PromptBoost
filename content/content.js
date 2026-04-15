/**
 * PROMPTBOOST - ADVANCED CONTENT ENGINE v3.0
 * Developed by: Shreyojit Das (Class of 2026, IEM)
 * * Features:
 * - Shadow DOM Traversal (ChatGPT Fix)
 * - Cross-Platform SPA Injection (Claude/Gemini)
 * - On-Device Inference (Gemini Nano)
 * - Constructivist Bauhaus UI Integration
 */

(function () {
    "use strict";

    // --- 1. GLOBAL CONFIGURATION & CONSTANTS ---
    const GITHUB_RAW_DB = 'https://raw.githubusercontent.com/SD10LEGACY/PromptBoost/refs/heads/main/database/prompts.json';

    const PLATFORMS = {
        CHATGPT: { domain: 'chatgpt.com', key: 'chatgpt' },
        CLAUDE: { domain: 'claude.ai', key: 'claude' },
        GEMINI: { domain: 'gemini.google.com', key: 'gemini' }
    };

    // --- 2. THE "FUZZY" DEEP INPUT FINDER ---
    // This looks through standard DOM and Shadow Roots to find the active text area.
    function findActiveAIInput() {
        // High-priority known selectors
        const primarySelectors = [
            '#prompt-textarea',
            'div[contenteditable="true"]',
            '.ProseMirror',
            'textarea[placeholder*="message"]'
        ];

        for (let selector of primarySelectors) {
            const el = document.querySelector(selector);
            if (el) return el;
        }

        // Deep Search through Shadow Roots (The ChatGPT/Claude secret)
        let foundInput = null;
        const allElements = document.querySelectorAll('*');

        for (let el of allElements) {
            if (el.shadowRoot) {
                for (let selector of primarySelectors) {
                    const shadowEl = el.shadowRoot.querySelector(selector);
                    if (shadowEl) return shadowEl;
                }
            }
        }

        // Fallback to active element if it's an input
        const active = document.activeElement;
        if (active && (active.tagName === 'TEXTAREA' || active.getAttribute('contenteditable') === 'true')) {
            return active;
        }

        return null;
    }

    // --- 3. THE REACT / PROSEMIRROR INJECTION HACK ---
    // Forces modern SPAs to recognize the change in their internal State Managers
    function injectTextToAI(text) {
        const input = findActiveAIInput();
        if (!input) {
            console.error("PB: Target input not found for injection.");
            return;
        }

        input.focus();

        try {
            if (input.tagName === 'TEXTAREA') {
                // Target the value setter on the prototype to bypass React's tracking
                const setter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, "value").set;
                setter.call(input, text);

                // Dispatch input event so the 'Send' button enables
                input.dispatchEvent(new Event('input', { bubbles: true }));
            } else {
                // For ContentEditable (Claude/Gemini)
                // We use the Selection API to insert text where the cursor is
                const selection = window.getSelection();
                if (selection.rangeCount > 0) {
                    document.execCommand('selectAll', false, null);
                    document.execCommand('insertText', false, text);
                } else {
                    input.innerText = text;
                    input.dispatchEvent(new Event('input', { bubbles: true }));
                }
            }

            // Adjust height for auto-expanding textareas
            input.style.height = 'auto';
            input.style.height = (input.scrollHeight) + 'px';

            if (DEBUG_MODE) console.log("PB: Successfully injected prompt.");
        } catch (error) {
            console.error("PB: Injection Failed", error);
        }
    }

    // --- 4. ON-DEVICE AI CORE (Gemini Nano) ---
    async function runGeminiEngineering(btn) {
        const input = findActiveAIInput();
        if (!input) return;

        const rawContent = (input.value || input.innerText || "").trim();
        if (rawContent.length < 3) return;

        btn.classList.add('pb-loading');
        btn.innerHTML = '🌀';

        try {
            // More robust check
            if (!window.ai || !window.ai.createTextSession) {
                throw new Error("Gemini Nano is not exposed to this window. Check Manifest 'world: MAIN' or Chrome Flags.");
            }

            const capabilities = await window.ai.canCreateTextSession();
            if (capabilities === "no") {
                throw new Error("Model not ready. Visit chrome://components and update 'Optimization Guide'.");
            }

            const session = await window.ai.createTextSession();
            // ... rest of your logic ...

            const systemPrompt = `
                Context: You are a Staff Prompt Engineer.
                Task: Rewrite the user's rough prompt into a high-performance CO-STAR prompt.
                Constraint: Return ONLY the rewritten prompt. No conversational filler.
                User Draft: "${rawContent}"
            `;

            const refinedPrompt = await session.prompt(systemPrompt);
            injectTextToAI(refinedPrompt.trim());

            session.destroy();
        } catch (err) {
            console.error("PB: AI Engine Error:", err);
            showToast("❌ AI Error: " + err.message);
        } finally {
            btn.classList.remove('pb-loading');
            btn.innerHTML = '✨';
        }
    }

    // --- 5. THE TRENDING LIBRARY (Omin-Channel Fetch) ---
    async function loadTrendingLibrary() {
        const sidebarContent = document.getElementById('pb-cards-container');
        if (!sidebarContent) return;

        sidebarContent.innerHTML = '<div class="pb-loader-text">SYNCING_REALTIME_DATA...</div>';

        try {
            // Cache-busting URL to ensure we get the 10,000+ growing list, not a cached local copy
            // Force a fresh fetch by adding a unique timestamp
            const response = await fetch(`${GITHUB_RAW_DB}?t=${new Date().getTime()}`);
            const prompts = await response.json();

            if (!prompts || prompts.length === 0) {
                sidebarContent.innerHTML = '<div class="pb-loader-text">DATABASE_EMPTY_TRY_LATER</div>';
                return;
            }

            // Render logic with Bauhaus color cycling
            const colors = ['var(--pb-red)', 'var(--pb-blue)', 'var(--pb-yellow)'];

            sidebarContent.innerHTML = prompts.map((p, i) => `
                <div class="pb-card" data-fulltext="${encodeURIComponent(p.text)}">
                    <div class="pb-card-deco" style="background: ${colors[i % 3]};"></div>
                    <div class="pb-tag">${p.tag}</div>
                    <h3 class="pb-card-title">${p.title}</h3>
                    <p class="pb-card-preview">${p.text.substring(0, 120)}...</p>
                    <button class="pb-use-btn">INJECT_PROMPT</button>
                </div>
            `).join('');

            // Card Click Actions
            sidebarContent.querySelectorAll('.pb-card').forEach(card => {
                card.querySelector('.pb-use-btn').onclick = (e) => {
                    const text = decodeURIComponent(card.dataset.fulltext);
                    injectTextToAI(text);
                    document.getElementById('pb-sidebar').classList.remove('pb-open');
                };
            });

        } catch (err) {
            console.error("PB: Fetch Error", err);
            sidebarContent.innerHTML = '<div class="pb-loader-text">NETWORK_ERROR: CHECK_GITHUB_SYNC</div>';
        }
    }

    // --- 6. UI CONSTRUCTION ---
    function buildSidebar() {
        if (document.getElementById('pb-sidebar')) return;

        const sidebar = document.createElement('div');
        sidebar.id = 'pb-sidebar';
        sidebar.innerHTML = `
            <div class="pb-sidebar-header">
                <h2 class="pb-sidebar-title">PROMPT_BOOST_LIB</h2>
                <button class="pb-close-btn" id="pb-close-sidebar">×</button>
            </div>
            <div class="pb-sidebar-content" id="pb-cards-container"></div>
        `;
        document.body.appendChild(sidebar);

        document.getElementById('pb-close-sidebar').onclick = () => {
            sidebar.classList.remove('pb-open');
        };
    }

    function injectNativeControls() {
        const input = findActiveAIInput();
        if (!input || document.querySelector('.pb-btn-group')) return;

        // Create the container
        const btnGroup = document.createElement('div');
        btnGroup.className = 'pb-btn-group';
        btnGroup.innerHTML = `
            <button class="pb-native-btn pb-wand-btn" title="AI Engineer">✨</button>
            <button class="pb-native-btn pb-lib-btn" title="Trending Library">📚</button>
        `;

        // Position it based on the parent of the input
        const parent = input.parentElement;
        parent.style.position = 'relative';
        parent.appendChild(btnGroup);

        // Events
        btnGroup.querySelector('.pb-wand-btn').onclick = (e) => {
            e.preventDefault();
            runGeminiEngineering(e.currentTarget);
        };

        btnGroup.querySelector('.pb-lib-btn').onclick = (e) => {
            e.preventDefault();
            document.getElementById('pb-sidebar').classList.add('pb-open');
            loadTrendingLibrary();
        };

        buildSidebar();
    }

    // --- 7. UTILS & OBSERVER ---
    function showToast(msg) {
        const toast = document.createElement('div');
        toast.className = 'pb-status-msg';
        toast.innerText = msg;
        document.body.appendChild(toast);
        setTimeout(() => toast.remove(), 3000);
    }

    // Detection Loop: Modern AI sites are single-page apps (SPAs)
    // We use a MutationObserver to re-inject buttons if they are removed by React
    const observer = new MutationObserver((mutations) => {
        for (let mutation of mutations) {
            if (mutation.addedNodes.length) {
                injectNativeControls();
            }
        }
    });

    observer.observe(document.body, { childList: true, subtree: true });

    // Initial load
    setTimeout(injectNativeControls, 1000);

    if (DEBUG_MODE) console.log("PB: Content Engine Initialized.");

})();
