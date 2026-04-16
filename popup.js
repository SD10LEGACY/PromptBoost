/**
 * PromptBoost Popup — Key Management
 * Reads/writes to chrome.storage.local (encrypted by Chrome OS, extension-only)
 */

const KEYS = ['gemini', 'groq', 'mistral', 'openrouter', 'byok'];

function setStatus(msg, type = 'info') {
    const bar = document.getElementById('status-bar');
    bar.textContent = msg;
    bar.className = 'status-bar ' + type;
}

function updateDot(id, hasValue) {
    const dot   = document.getElementById('dot-' + id);
    const block = document.getElementById('block-' + id);
    const input = document.getElementById('key-' + id);
    if (!dot) return;
    dot.className   = 'provider-dot' + (hasValue ? ' set' : '');
    block.className = 'provider-block' + (hasValue ? ' active-key' : '');
    if (input && hasValue) input.classList.add('has-value');
    else if (input) input.classList.remove('has-value');
}

// ── LOAD saved keys on open ───────────────────────────────────────────────
chrome.storage.local.get(KEYS.map(k => 'pb_key_' + k), (result) => {
    let activeEngines = [];
    KEYS.forEach(id => {
        const stored = result['pb_key_' + id] || '';
        const input  = document.getElementById('key-' + id);
        if (stored && input) {
            input.value = stored;
            input.classList.add('has-value');
        }
        updateDot(id, !!stored);
        if (stored && id !== 'byok') {
            const labels = { gemini: 'GEMINI', groq: 'GROQ', mistral: 'MISTRAL', openrouter: 'OPENROUTER' };
            activeEngines.push(labels[id] || id.toUpperCase());
        }
    });

    const byok = result['pb_key_byok'] || '';
    const bar  = document.getElementById('active-engine-bar');
    const txt  = document.getElementById('active-engine-text');
    if (byok) {
        bar.classList.add('visible');
        txt.textContent = 'BYOK_ACTIVE — custom key takes priority';
    } else if (activeEngines.length) {
        bar.classList.add('visible');
        txt.textContent = 'ACTIVE_ENGINES: ' + activeEngines.join(' → ');
    }
});

// ── TOGGLE VISIBILITY ─────────────────────────────────────────────────────
document.querySelectorAll('.toggle-vis').forEach(btn => {
    btn.addEventListener('click', () => {
        const input = document.getElementById(btn.dataset.target);
        if (!input) return;
        input.type = input.type === 'password' ? 'text' : 'password';
    });
});

// ── SAVE & TEST ───────────────────────────────────────────────────────────
document.getElementById('save-btn').addEventListener('click', async () => {
    const btn = document.getElementById('save-btn');
    btn.textContent = 'SAVING...';
    btn.classList.add('saving');

    const toSave = {};
    KEYS.forEach(id => {
        const val = (document.getElementById('key-' + id)?.value || '').trim();
        toSave['pb_key_' + id] = val;
        updateDot(id, !!val);
    });

    chrome.storage.local.set(toSave, async () => {
        setStatus('✅ Keys saved. Testing connection...', 'ok');

        // Send test message to background to verify at least one key works
        chrome.runtime.sendMessage({ action: 'testKeys' }, (response) => {
            btn.textContent = 'SAVE_AND_TEST_KEYS';
            btn.classList.remove('saving');
            if (response?.ok) {
                setStatus(`✅ ${response.engine} is LIVE — "${response.preview}"`, 'ok');
                const bar = document.getElementById('active-engine-bar');
                const txt = document.getElementById('active-engine-text');
                bar.classList.add('visible');
                txt.textContent = 'ACTIVE_ENGINE: ' + response.engine;
            } else {
                setStatus('❌ ' + (response?.error || 'All keys failed. Check your keys.'), 'err');
            }
        });
    });
});
