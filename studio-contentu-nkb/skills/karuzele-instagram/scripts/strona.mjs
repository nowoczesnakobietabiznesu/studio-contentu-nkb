// Studio Contentu NKB: zrzut całej strony www przez Chrome DevTools, bez banerów cookies,
// z wybranymi zdaniami w złotym markerze. Wywołuje go wideo.py strona (nie uruchamiaj ręcznie).
// Użycie: node strona.mjs <przeglądarka> <url> <plik.png> [szerokość=460] ["zdanie 1" "zdanie 2" ...]
import { spawn } from 'node:child_process';
import { writeFileSync, mkdtempSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

const [browser, url, out, width = '460', ...phrases] = process.argv.slice(2);
const PORT = 9300 + Math.floor(Math.random() * 600);
const prof = mkdtempSync(join(tmpdir(), 'nkb-strona-'));
const chrome = spawn(browser, ['--headless=new', `--remote-debugging-port=${PORT}`, `--user-data-dir=${prof}`,
  '--hide-scrollbars', '--no-first-run', '--no-default-browser-check', 'about:blank'], { stdio: 'ignore' });
const sleep = ms => new Promise(r => setTimeout(r, ms));
const done = code => { try { chrome.kill(); } catch {} process.exit(code); };

let targets = [];
for (let i = 0; i < 75 && !targets.length; i++) {
  try { targets = (await (await fetch(`http://127.0.0.1:${PORT}/json/list`)).json()).filter(t => t.type === 'page'); } catch {}
  if (!targets.length) await sleep(200);
}
if (!targets.length) { console.error('przeglądarka nie odpowiedziała'); done(1); }
const ws = new WebSocket(targets[0].webSocketDebuggerUrl);
await new Promise(r => ws.addEventListener('open', r));
let id = 0; const wait = new Map();
ws.addEventListener('message', e => { const m = JSON.parse(e.data); if (m.id && wait.has(m.id)) { wait.get(m.id)(m); wait.delete(m.id); } });
const send = (method, params = {}) => new Promise(r => { const i = ++id; wait.set(i, r); ws.send(JSON.stringify({ id: i, method, params })); });

await send('Page.enable');
await send('Emulation.setDeviceMetricsOverride', { width: +width, height: 1200, deviceScaleFactor: 2, mobile: false });
await send('Page.navigate', { url });
await sleep(7000);
const js = `(() => {
  document.querySelectorAll('[id*="cookie" i],[class*="cookie" i],[class*="consent" i],[id*="consent" i],iframe').forEach(e => e.remove());
  document.querySelectorAll('*').forEach(e => { const s = getComputedStyle(e); if ((s.position === 'fixed' || s.position === 'sticky') && e.tagName !== 'HTML' && e.tagName !== 'BODY') e.style.position = 'static'; });
  const art = document.querySelector('article') || document.querySelector('main') || document.body;
  const mark = (needle) => {
    const w = document.createTreeWalker(art, NodeFilter.SHOW_TEXT);
    let n; while ((n = w.nextNode())) { const i = n.data.indexOf(needle); if (i < 0) continue;
      const r = document.createRange(); r.setStart(n, i); r.setEnd(n, i + needle.length);
      const s = document.createElement('span'); s.style.cssText = 'background:linear-gradient(transparent 10%, rgba(214,170,82,.55) 10%, rgba(214,170,82,.55) 92%, transparent 92%);';
      r.surroundContents(s); return true; }
    return false; };
  const found = ${JSON.stringify(phrases)}.map(p => mark(p) || mark(p.replace(/'/g, '’')));
  const h = document.querySelector('h1');
  const top = (h ? h.getBoundingClientRect().top : art.getBoundingClientRect().top) + scrollY - 40;
  const ar = art.getBoundingClientRect();
  return JSON.stringify({ found, top, bottom: ar.bottom + scrollY + 20, height: document.documentElement.scrollHeight });
})()`;
const r = await send('Runtime.evaluate', { expression: js, returnByValue: true });
const info = JSON.parse(r.result.result.value);
info.found.forEach((f, i) => { if (!f) console.log('NIE ZNALEZIONO zdania: ' + phrases[i]); });
const y = Math.max(0, info.top);
const clip = { x: 0, y, width: +width, height: Math.max(400, Math.min(info.bottom, info.height) - y), scale: 1 };
const shot = await send('Page.captureScreenshot', { format: 'png', captureBeyondViewport: true, clip });
writeFileSync(out, Buffer.from(shot.result.data, 'base64'));
ws.close();
done(0);
