/**
 * PromptBoost Popup — Key Management
 * Reads/writes to chrome.storage.local (sandboxed per-extension, encrypted at rest by the OS).
 */

const ENGINE_IDS = ['gemini', 'groq', 'mistral', 'openrouter', 'byok'];

const ENGINE_LABELS = {
    gemini:     'GEMINI',
    groq:       'GROQ',
    mistral:    'MISTRAL',
    openrouter: 'OPENROUTER',
};

function setStatus(msg, type = 'info') {
    const bar = document.getElementById('status-bar');
    bar.textContent = msg;
    bar.className = 'status-bar ' + type;
}

function updateDot(id, isActive) {
    const dot   = document.getElementById('dot-' + id);
    const block = document.getElementById('block-' + id);
    const input = document.getElementById('key-' + id);
    if (!dot) return;
    dot.className   = 'provider-dot' + (isActive ? ' set' : '');
    block.className = 'provider-block' + (isActive ? ' active-key' : '');
    input?.classList.toggle('has-value', isActive);
}

function showActiveEngineBar(text) {
    const bar = document.getElementById('active-engine-bar');
    const txt = document.getElementById('active-engine-text');
    bar.classList.add('visible');
    txt.textContent = text;
}

chrome.storage.local.get(ENGINE_IDS.map(k => 'pb_key_' + k), (stored) => {
    const activeEngineLabels = [];

    ENGINE_IDS.forEach(id => {
        const value = stored['pb_key_' + id] || '';
        const input = document.getElementById('key-' + id);
        if (value && input) {
            input.value = value;
            input.classList.add('has-value');
        }
        updateDot(id, !!value);
        if (value && id !== 'byok') {
            activeEngineLabels.push(ENGINE_LABELS[id] ?? id.toUpperCase());
        }
    });

    const byokValue = stored['pb_key_byok'] || '';
    if (byokValue) {
        showActiveEngineBar('BYOK_ACTIVE — custom key takes priority');
    } else if (activeEngineLabels.length) {
        showActiveEngineBar('ACTIVE_ENGINES: ' + activeEngineLabels.join(' → '));
    }
});

document.querySelectorAll('.toggle-vis').forEach(btn => {
    btn.addEventListener('click', () => {
        const input = document.getElementById(btn.dataset.target);
        if (!input) return;
        input.type = input.type === 'password' ? 'text' : 'password';
    });
});

document.getElementById('save-btn').addEventListener('click', async () => {
    const saveBtn = document.getElementById('save-btn');
    saveBtn.textContent = 'SAVING...';
    saveBtn.classList.add('saving');

    const payload = Object.fromEntries(
        ENGINE_IDS.map(id => {
            const val = (document.getElementById('key-' + id)?.value || '').trim();
            updateDot(id, !!val);
            return ['pb_key_' + id, val];
        })
    );

    chrome.storage.local.set(payload, () => {
        setStatus('✅ Keys saved. Testing connection...', 'ok');

        chrome.runtime.sendMessage({ action: 'testKeys' }, (response) => {
            saveBtn.textContent = 'SAVE_AND_TEST_KEYS';
            saveBtn.classList.remove('saving');

            if (response?.ok) {
                setStatus(`✅ ${response.engine} is LIVE — "${response.preview}"`, 'ok');
                showActiveEngineBar('ACTIVE_ENGINE: ' + response.engine);
            } else {
                setStatus('❌ ' + (response?.error || 'All keys failed. Check your keys.'), 'err');
            }
        });
    });
});
