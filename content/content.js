// --- 1. CLOUD FETCH (Your Trending Database) ---
async function fetchTrendingPrompts() {
    try {
        const response = await fetch('https://raw.githubusercontent.com/SD10LEGACY/PromptBoost/refs/heads/main/database/prompts.json');
        return await response.json();
    } catch (e) {
        console.error("Failed to fetch cloud database", e);
        return [];
    }
}

// --- 2. PLATFORM DETECTOR ---
function getCurrentPlatform() {
    const host = window.location.hostname;
    if (host.includes("claude.ai")) return "claude";
    if (host.includes("gemini.google.com")) return "gemini";
    return "chatgpt";
}

// --- 3. UI INJECTION ---
function injectUI() {
    // Currently targets ChatGPT's specific input box format.
    // (You will add CSS selectors for Claude/Gemini later)
    const textarea = document.querySelector('#prompt-textarea');
    if (!textarea || document.querySelector('.pb-wand-btn')) return;

    const parent = textarea.parentElement;

    // ✨ Magic Wand Button
    const wandBtn = document.createElement('button');
    wandBtn.className = 'pb-action-btn pb-wand-btn';
    wandBtn.innerHTML = '✨';
    wandBtn.title = "Engineer this prompt";
    wandBtn.onclick = (e) => {
        e.preventDefault();
        const text = textarea.value;
        if (!text.trim()) return;

        wandBtn.classList.add('pb-loading');
        chrome.runtime.sendMessage({ action: "improve", text: text }, (res) => {
            wandBtn.classList.remove('pb-loading');
            if (res.success) fillChatBox(res.text, textarea);
            else alert("Error: " + res.error);
        });
    };
    parent.appendChild(wandBtn);

    // 📚 Library Button
    const libBtn = document.createElement('button');
    libBtn.className = 'pb-action-btn pb-lib-btn';
    libBtn.innerHTML = '📚';
    libBtn.title = "Trending Library";
    libBtn.onclick = (e) => {
        e.preventDefault();
        openSidebar();
    };
    parent.appendChild(libBtn);

    buildSidebar();
}

// --- 4. SIDEBAR LOGIC ---
// ... (keep fetchTrendingPrompts, getCurrentPlatform, and fillChatBox exactly the same) ...

// --- 4. SIDEBAR LOGIC (BAUHAUS UPDATE) ---
function buildSidebar() {
    if (document.getElementById('pb-sidebar')) return;
    const sidebar = document.createElement('div');
    sidebar.id = 'pb-sidebar';
    sidebar.innerHTML = `
        <div class="pb-sidebar-header">
            <h2 class="pb-sidebar-title">🔥 <span id="pb-platform-title"></span></h2>
            <button class="pb-close-btn" id="pb-close-sidebar">&times;</button>
        </div>
        <div class="pb-sidebar-content" id="pb-cards-container">
            <div style="text-align:center; font-weight:700; text-transform:uppercase;">Loading Data...</div>
        </div>
    `;
    document.body.appendChild(sidebar);
    document.getElementById('pb-close-sidebar').onclick = () => sidebar.classList.remove('pb-open');
}

async function openSidebar() {
    const sidebar = document.getElementById('pb-sidebar');
    const container = document.getElementById('pb-cards-container');
    const platform = getCurrentPlatform();

    document.getElementById('pb-platform-title').innerText = platform;
    sidebar.classList.add('pb-open');

    const allPrompts = await fetchTrendingPrompts();
    const platformPrompts = allPrompts.filter(p => p.platforms.includes(platform));

    // Bauhaus Array to cycle through geometric corner decorations
    const bauhausColors = ['var(--pb-red)', 'var(--pb-blue)', 'var(--pb-yellow)'];
    const bauhausShapes = ['50%', '0px']; // Circle (50%), Square (0px)

    container.innerHTML = platformPrompts.map((p, index) => {
        // Assign a rotating geometric style to each card
        const color = bauhausColors[index % bauhausColors.length];
        const shape = bauhausShapes[index % bauhausShapes.length];

        return `
        <div class="pb-card" data-prompt="${escape(p.text)}">
            <div class="pb-card-deco" style="background: ${color}; border-radius: ${shape};"></div>
            <div class="pb-card-header">
                <h3 class="pb-card-title">${p.title}</h3>
                <span class="pb-tag">${p.tag}</span>
            </div>
            <p class="pb-card-preview">${p.text}</p>
        </div>
    `}).join('');

    document.querySelectorAll('.pb-card').forEach(card => {
        card.onclick = function () {
            fillChatBox(unescape(this.getAttribute('data-prompt')), document.querySelector('#prompt-textarea'));
            sidebar.classList.remove('pb-open');
        };
    });
}

// ... (keep the rest of your observer and injectUI logic exactly the same) ...

// --- 5. CLICK TO FILL (REACT HACK) ---
function fillChatBox(text, textarea) {
    if (!textarea) return;
    const setter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, "value").set;
    setter.call(textarea, text);
    textarea.dispatchEvent(new Event('input', { bubbles: true }));
    textarea.style.height = 'auto';
    textarea.style.height = textarea.scrollHeight + 'px';
}

const observer = new MutationObserver(() => injectUI());
observer.observe(document.body, { childList: true, subtree: true });