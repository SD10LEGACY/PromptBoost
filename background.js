/**
 * PromptBoost Background Service Worker
 *
 * All AI calls live here — service workers are exempt from the host page's CSP,
 * which means we can hit external APIs that content scripts can't touch directly.
 * Keys are read from chrome.storage.local (written by popup.js on save).
 *Nano gemini not working on my PC ffs
 * Engine rotation order:
 *   BYOK (OpenRouter, premium model) → Gemini 2.0 Flash → Groq Llama-3.3-70b
 *   → Mistral Small → OpenRouter free tier
 */

const GITHUB_RAW_DB = 'https://raw.githubusercontent.com/SD10LEGACY/PromptBoost/refs/heads/main/database/prompts.json';

const ENGINEER_SYSTEM = `You are a Staff Prompt Engineer.
Your task: rewrite the user's rough draft into a high-performance CO-STAR prompt.
CO-STAR format: Context, Objective, Style, Tone, Audience, Response.
Rules:
- Return ONLY the rewritten prompt. No preamble, no explanation, no markdown fences.
- Preserve the user's original intent exactly.
- Make it specific, actionable, and structured.`;

// ─────────────────────────────────────────────────────────────────────────────

async function callGemini(key, userText) {
    const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${key}`;
    const r = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            contents: [{ parts: [{ text: `${ENGINEER_SYSTEM}\n\nUser draft: ${userText}` }] }],
            generationConfig: { maxOutputTokens: 1024, temperature: 0.7 }
        })
    });
    if (!r.ok) throw new Error(`Gemini HTTP ${r.status}`);
    const j = await r.json();
    const text = j.candidates?.[0]?.content?.parts?.[0]?.text?.trim();
    if (!text) throw new Error('Gemini returned an empty candidate');
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
            max_tokens: 1024,
            temperature: 0.7
        })
    });
    if (!r.ok) throw new Error(`Groq HTTP ${r.status}`);
    const j = await r.json();
    const text = j.choices?.[0]?.message?.content?.trim();
    if (!text) throw new Error('Groq returned an empty choice');
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
            max_tokens: 1024,
            temperature: 0.7
        })
    });
    if (!r.ok) throw new Error(`Mistral HTTP ${r.status}`);
    const j = await r.json();
    const text = j.choices?.[0]?.message?.content?.trim();
    if (!text) throw new Error('Mistral returned an empty choice');
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
    if (!text) throw new Error('OpenRouter returned an empty choice');
    return { text, engine: model.includes('free') ? 'OPENROUTER_FREE' : 'OPENROUTER_BYOK' };
}

// ─────────────────────────────────────────────────────────────────────────────

async function engineerWithRotation(userText, keys) {
    const failures = [];

    if (keys.byok) {
        try {
            // BYOK routes through OpenRouter so users can swap any model they want
            return await callOpenRouter(keys.byok, userText, 'google/gemini-2.0-flash-001');
        } catch (e) {
            console.warn('[PB] BYOK failed, falling through rotation:', e.message);
            failures.push(`BYOK: ${e.message}`);
        }
    }

    if (keys.gemini) {
        try { return await callGemini(keys.gemini, userText); }
        catch (e) {
            console.warn('[PB] Gemini failed:', e.message);
            failures.push(`Gemini: ${e.message}`);
        }
    }

    if (keys.groq) {
        try { return await callGroq(keys.groq, userText); }
        catch (e) {
            console.warn('[PB] Groq failed:', e.message);
            failures.push(`Groq: ${e.message}`);
        }
    }

    if (keys.mistral) {
        try { return await callMistral(keys.mistral, userText); }
        catch (e) {
            console.warn('[PB] Mistral failed:', e.message);
            failures.push(`Mistral: ${e.message}`);
        }
    }

    if (keys.openrouter) {
        try { return await callOpenRouter(keys.openrouter, userText); }
        catch (e) {
            console.warn('[PB] OpenRouter free tier failed:', e.message);
            failures.push(`OpenRouter: ${e.message}`);
        }
    }

    throw new Error('All engines exhausted:\n' + failures.join('\n'));
}

function loadKeys() {
    return new Promise(resolve => {
        chrome.storage.local.get(
            ['pb_key_gemini', 'pb_key_groq', 'pb_key_mistral', 'pb_key_openrouter', 'pb_key_byok'],
            (r) => resolve({
                gemini:     r.pb_key_gemini     || '',
                groq:       r.pb_key_groq        || '',
                mistral:    r.pb_key_mistral     || '',
                openrouter: r.pb_key_openrouter  || '',
                byok:       r.pb_key_byok        || '',
            })
        );
    });
}

// ─────────────────────────────────────────────────────────────────────────────

chrome.runtime.onMessage.addListener((request, _sender, sendResponse) => {
    const { action } = request;

    if (action === 'fetchPrompts') {
        fetch(`${GITHUB_RAW_DB}?t=${Date.now()}`)
            .then(r => {
                if (!r.ok) throw new Error(`HTTP ${r.status}`);
                return r.json();
            })
            .then(data => sendResponse({ ok: true, data }))
            .catch(err => sendResponse({ ok: false, error: err.message }));
        return true;
    }

    if (action === 'engineerPrompt') {
        loadKeys().then(async keys => {
            if (!Object.values(keys).some(v => v.length > 0)) {
                sendResponse({ ok: false, error: 'No API keys set. Click the PromptBoost icon (🅿) to add your keys.' });
                return;
            }
            try {
                const { text, engine } = await engineerWithRotation(request.text, keys);
                sendResponse({ ok: true, data: text, engine });
            } catch (err) {
                sendResponse({ ok: false, error: err.message });
            }
        });
        return true;
    }

    if (action === 'testKeys') {
        loadKeys().then(async keys => {
            if (!Object.values(keys).some(v => v.length > 0)) {
                sendResponse({ ok: false, error: 'No keys configured.' });
                return;
            }
            try {
                const { text, engine } = await engineerWithRotation('Write a blog post about AI.', keys);
                sendResponse({ ok: true, engine, preview: text.substring(0, 60) + '...' });
            } catch (err) {
                sendResponse({ ok: false, error: err.message });
            }
        });
        return true;
    }
});
