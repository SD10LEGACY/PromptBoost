/**
 * PromptBoost Background Service Worker v3.2
 *
 * All API calls happen here — background workers are exempt from page CSP.
 * Keys are read from chrome.storage.local (set by popup.js).
 *
 * AI ROTATION ORDER:
 *   1. BYOK (user's premium key — OpenRouter with any model)
 *   2. Gemini 2.0 Flash  (AI Studio free tier: 15 RPM / 1M TPD)
 *   3. Groq Llama-3.3-70b (fastest inference, generous free tier)
 *   4. Mistral Small      (solid quality, free tier)
 *   5. OpenRouter free    (llama-3.1-8b, last resort)
 */

const GITHUB_RAW_DB = 'https://raw.githubusercontent.com/SD10LEGACY/PromptBoost/refs/heads/main/database/prompts.json';

// ── PROMPT ENGINEERING SYSTEM PROMPT ─────────────────────────────────────
const ENGINEER_SYSTEM = `You are a Staff Prompt Engineer.
Your task: rewrite the user's rough draft into a high-performance CO-STAR prompt.
CO-STAR format: Context, Objective, Style, Tone, Audience, Response.
Rules:
- Return ONLY the rewritten prompt. No preamble, no explanation, no markdown fences.
- Preserve the user's original intent exactly.
- Make it specific, actionable, and structured.`;

// ── API CALLERS ───────────────────────────────────────────────────────────

async function callGemini(key, userText) {
    const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${key}`;
    const body = {
        contents: [{ parts: [{ text: `${ENGINEER_SYSTEM}\n\nUser draft: ${userText}` }] }],
        generationConfig: { maxOutputTokens: 1024, temperature: 0.7 }
    };
    const r = await fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
    if (!r.ok) throw new Error(`Gemini HTTP ${r.status}`);
    const j = await r.json();
    const text = j.candidates?.[0]?.content?.parts?.[0]?.text?.trim();
    if (!text) throw new Error('Gemini: empty response');
    return { text, engine: 'GEMINI_2.0_FLASH' };
}

async function callGroq(key, userText) {
    const r = await fetch('https://api.groq.com/openai/v1/chat/completions', {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${key}`, 'Content-Type': 'application/json' },
        body: JSON.stringify({
            model: 'llama-3.3-70b-versatile',
            messages: [
                { role: 'system', content: ENGINEER_SYSTEM },
                { role: 'user',   content: userText }
            ],
            max_tokens: 1024, temperature: 0.7
        })
    });
    if (!r.ok) throw new Error(`Groq HTTP ${r.status}`);
    const j = await r.json();
    const text = j.choices?.[0]?.message?.content?.trim();
    if (!text) throw new Error('Groq: empty response');
    return { text, engine: 'GROQ_LLAMA3.3_70B' };
}

async function callMistral(key, userText) {
    const r = await fetch('https://api.mistral.ai/v1/chat/completions', {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${key}`, 'Content-Type': 'application/json' },
        body: JSON.stringify({
            model: 'mistral-small-latest',
            messages: [
                { role: 'system', content: ENGINEER_SYSTEM },
                { role: 'user',   content: userText }
            ],
            max_tokens: 1024, temperature: 0.7
        })
    });
    if (!r.ok) throw new Error(`Mistral HTTP ${r.status}`);
    const j = await r.json();
    const text = j.choices?.[0]?.message?.content?.trim();
    if (!text) throw new Error('Mistral: empty response');
    return { text, engine: 'MISTRAL_SMALL' };
}

async function callOpenRouter(key, userText, model = 'meta-llama/llama-3.1-8b-instruct:free') {
    const r = await fetch('https://openrouter.ai/api/v1/chat/completions', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${key}`,
            'Content-Type': 'application/json',
            'HTTP-Referer': 'https://github.com/SD10LEGACY/PromptBoost',
            'X-Title': 'PromptBoost'
        },
        body: JSON.stringify({
            model,
            messages: [
                { role: 'system', content: ENGINEER_SYSTEM },
                { role: 'user',   content: userText }
            ],
            max_tokens: 1024
        })
    });
    if (!r.ok) throw new Error(`OpenRouter HTTP ${r.status}`);
    const j = await r.json();
    const text = j.choices?.[0]?.message?.content?.trim();
    if (!text) throw new Error('OpenRouter: empty response');
    const label = model.includes('free') ? 'OPENROUTER_FREE' : 'OPENROUTER_BYOK';
    return { text, engine: label };
}

// ── ROTATION ENGINE ───────────────────────────────────────────────────────
async function engineerWithRotation(userText, keys) {
    const errors = [];

    // 1. BYOK (premium — highest priority)
    if (keys.byok) {
        try {
            // Use a smart model if BYOK is set
            return await callOpenRouter(keys.byok, userText, 'google/gemini-2.0-flash-001');
        } catch (e) {
            errors.push('BYOK: ' + e.message);
            // Fall through to standard rotation
        }
    }

    // 2. Gemini AI Studio
    if (keys.gemini) {
        try { return await callGemini(keys.gemini, userText); }
        catch (e) { errors.push('Gemini: ' + e.message); }
    }

    // 3. Groq
    if (keys.groq) {
        try { return await callGroq(keys.groq, userText); }
        catch (e) { errors.push('Groq: ' + e.message); }
    }

    // 4. Mistral
    if (keys.mistral) {
        try { return await callMistral(keys.mistral, userText); }
        catch (e) { errors.push('Mistral: ' + e.message); }
    }

    // 5. OpenRouter free tier
    if (keys.openrouter) {
        try { return await callOpenRouter(keys.openrouter, userText); }
        catch (e) { errors.push('OpenRouter: ' + e.message); }
    }

    throw new Error('All engines failed:\n' + errors.join('\n'));
}

// ── LOAD KEYS FROM STORAGE ────────────────────────────────────────────────
function loadKeys() {
    return new Promise(resolve => {
        chrome.storage.local.get(
            ['pb_key_gemini', 'pb_key_groq', 'pb_key_mistral', 'pb_key_openrouter', 'pb_key_byok'],
            (r) => resolve({
                gemini:      r.pb_key_gemini      || '',
                groq:        r.pb_key_groq         || '',
                mistral:     r.pb_key_mistral      || '',
                openrouter:  r.pb_key_openrouter   || '',
                byok:        r.pb_key_byok         || '',
            })
        );
    });
}

// ── MESSAGE HANDLER ───────────────────────────────────────────────────────
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {

    // ── FETCH PROMPTS (CSP-safe proxy) ─────────────────────────────────
    if (request.action === 'fetchPrompts') {
        fetch(`${GITHUB_RAW_DB}?t=${Date.now()}`)
            .then(r => { if (!r.ok) throw new Error(`HTTP ${r.status}`); return r.json(); })
            .then(data => sendResponse({ ok: true, data }))
            .catch(err => sendResponse({ ok: false, error: err.message }));
        return true;
    }

    // ── AI ENGINEER ────────────────────────────────────────────────────
    if (request.action === 'engineerPrompt') {
        loadKeys().then(async keys => {
            const hasAnyKey = Object.values(keys).some(v => v.length > 0);
            if (!hasAnyKey) {
                sendResponse({
                    ok: false,
                    error: 'No API keys set. Click the PromptBoost icon (🅿) to add your keys.'
                });
                return;
            }
            try {
                const result = await engineerWithRotation(request.text, keys);
                sendResponse({ ok: true, data: result.text, engine: result.engine });
            } catch (err) {
                sendResponse({ ok: false, error: err.message });
            }
        });
        return true;
    }

    // ── TEST KEYS (called by popup on save) ────────────────────────────
    if (request.action === 'testKeys') {
        loadKeys().then(async keys => {
            const hasAnyKey = Object.values(keys).some(v => v.length > 0);
            if (!hasAnyKey) {
                sendResponse({ ok: false, error: 'No keys configured.' });
                return;
            }
            try {
                const result = await engineerWithRotation('Write a blog post about AI.', keys);
                const preview = result.text.substring(0, 60) + '...';
                sendResponse({ ok: true, engine: result.engine, preview });
            } catch (err) {
                sendResponse({ ok: false, error: err.message });
            }
        });
        return true;
    }
});
