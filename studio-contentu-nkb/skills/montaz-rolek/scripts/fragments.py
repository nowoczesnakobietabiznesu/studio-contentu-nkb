#!/usr/bin/env python3
"""The fragment picker: the buyer sees every line of every clip with its time, listens to it, and ticks what goes
into the reel BEFORE anything is cut. Runs after ingest.py, before edl.json is written. It is a gate: assemble.py
refuses to cut without a fragments.json that is newer than transcript.txt.

Usage:  PY fragments.py <project_dir> [--until-saved] [--no-open] [--port N]
        PY fragments.py <project_dir> --auto buyer|no-browser

  --until-saved    stop by itself a few seconds after the buyer presses Save (run it in the background and wait)
  --no-open        do not open the browser (the READY line has the address)
  --auto WHY       no page: write the pre-ticked lines as fragments.json and let Claude pick the takes. Only two
                   reasons count: "buyer" (she said "wybierz sam" / "nie chcę wybierać" in THIS edit) or
                   "no-browser" (the page cannot open on this computer). Never on Claude's own judgement.

Reads <project>/transcript.txt, words_cN.json and work/cN.wav (all from ingest.py). Writes <project>/fragments.json:
  {"saved": "...", "by": "buyer"|"claude", "reason": "", "note": "<her note to the edit>",
   "picked": [{"clip": "c1", "in": 12.60, "out": 15.74, "text": "...", "take": 2, "takes": 3}, ...]}   in reel order
"in"/"out" are the first word's start and the last word's end of that line (word timings, not the looser segment
edges): edl.json still trims them to the speech as references/cutting.md says.

Pre-ticked: of every line she said more than once, the LAST complete take (people repeat a line until it lands);
lines of one or two words (fillers, "jeszcze raz") are never pre-ticked. She changes any tick and the order.

Lines to watch for:
    STATUS fragments READY http://127.0.0.1:4760/
    STATUS fragments SAVED <path> picked=<n> of <total>
    STATUS fragments CLOSED
Standard library only. Localhost only; nothing leaves the computer.
"""
import datetime
import difflib
import json
import os
import re
import socket
import sys
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import skillenv  # noqa: E402

SEG = re.compile(r'^\[\s*([\d.]+)-\s*([\d.]+)\]\s*(.*)$')
AUTO_REASONS = ('buyer', 'no-browser')


def say(line):
    print(line, flush=True)


def norm(t):
    return ' '.join(re.findall(r"[\w']+", t.lower()))


def read_lines(proj):
    """-> list of {id, clip, file, in, out, text} in clip order, from transcript.txt + word timings"""
    rows, clip, fname = [], None, ''
    with open(os.path.join(proj, 'transcript.txt'), encoding='utf-8') as fh:
        for raw in fh:
            line = raw.rstrip('\n')
            if line.startswith('===== '):
                parts = line[6:].split(None, 1)
                clip, fname = parts[0], (parts[1] if len(parts) > 1 else '')
                continue
            m = SEG.match(line)
            if clip and m and m.group(3).strip():
                rows.append({'clip': clip, 'file': fname, 'in': float(m.group(1)), 'out': float(m.group(2)),
                             'text': m.group(3).strip()})
    words = {}
    for r in rows:
        if r['clip'] not in words:
            try:
                with open(os.path.join(proj, f"words_{r['clip']}.json"), encoding='utf-8') as fh:
                    words[r['clip']] = json.load(fh)
            except (OSError, ValueError):
                words[r['clip']] = []
        inside = [w for w in words[r['clip']] if w['start'] >= r['in'] - .05 and w['end'] <= r['out'] + .05]
        if inside:                       # word edges are tighter than the segment's
            r['in'], r['out'] = round(inside[0]['start'], 2), round(inside[-1]['end'], 2)
    for k, r in enumerate(rows):
        r['id'] = k
    return rows


def group_takes(rows):
    """same line said again -> one group; tick the last take of every group of 3+ words"""
    groups = []
    for r in rows:
        n = norm(r['text'])
        best = None
        for g in groups:
            ratio = difflib.SequenceMatcher(None, n, g['key']).ratio()
            if ratio >= .62 and (best is None or ratio > best[0]):
                best = (ratio, g)
        if best:
            best[1]['ids'].append(r['id'])
            best[1]['key'] = n               # compare with the newest take: a line drifts as it is re-said
        else:
            groups.append({'key': n, 'ids': [r['id']]})
    for gi, g in enumerate(groups):
        for k, i in enumerate(g['ids']):
            rows[i].update(group=gi, take=k + 1, takes=len(g['ids']))
        last = rows[g['ids'][-1]]
        last['tick'] = len(norm(last['text']).split()) >= 3
    for r in rows:
        r.setdefault('tick', False)
    return rows


PAGE = r'''<!doctype html>
<html lang="pl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Wybór fragmentów</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,500;1,500&family=Poppins:wght@300;400;500;600&display=swap">
<style>
:root{--bg:#f7f3ec;--card:#fff;--ink:#141414;--muted:#5c5c5c;--line:#e6ddcc;--gold:#cd9f38;--gold-ink:#94701f;--green:#1e3e3a}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:300 15px/1.6 Poppins,Arial,sans-serif}
header{background:linear-gradient(150deg,#1e3e3a,#000);color:#fff;padding:28px max(16px,4vw) 22px}
header .e{font:500 11px/1 Poppins,Arial,sans-serif;letter-spacing:.22em;text-transform:uppercase;color:var(--gold)}
header h1{font:500 clamp(28px,4vw,40px)/1.1 "Playfair Display",Georgia,serif;margin:8px 0 6px}
header h1 em{color:var(--gold)}header p{margin:0;max-width:62ch;color:rgba(255,255,255,.78)}
main{display:grid;grid-template-columns:minmax(0,1fr) 340px;gap:24px;padding:24px max(16px,4vw) 120px;max-width:1300px;margin:0 auto}
@media(max-width:900px){main{grid-template-columns:1fr}}
.clip{margin-bottom:26px}.clip h2{font:500 20px/1.2 "Playfair Display",Georgia,serif;margin:0 0 10px}
.clip h2 span{font:400 13px Poppins,Arial,sans-serif;color:var(--muted);margin-left:8px}
.row{display:grid;grid-template-columns:28px 34px 92px minmax(0,1fr);gap:10px;align-items:start;background:var(--card);border:1px solid var(--line);border-radius:8px;padding:10px 12px;margin-bottom:6px}
.row.on{border-color:var(--gold);box-shadow:inset 3px 0 0 var(--gold);border-radius:0 8px 8px 0}
.row input{width:18px;height:18px;margin-top:3px;accent-color:var(--green);cursor:pointer}
.play{width:30px;height:30px;border-radius:50%;border:1px solid var(--line);background:var(--bg);cursor:pointer;font-size:12px;line-height:1}
.play.now{background:var(--gold);border-color:var(--gold)}
.t{font:500 12.5px/1.9 ui-monospace,Consolas,monospace;color:var(--muted);font-variant-numeric:tabular-nums}
.txt{min-width:0}.badge{display:inline-block;font:500 11px/1 Poppins,Arial,sans-serif;background:#efe8da;color:var(--gold-ink);border-radius:999px;padding:4px 8px;margin-left:6px;vertical-align:1px}
aside{position:sticky;top:16px;align-self:start;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px}
aside h3{font:500 18px/1.2 "Playfair Display",Georgia,serif;margin:0 0 4px}aside .sum{color:var(--muted);font-size:13px;margin-bottom:10px}
ol{margin:0 0 12px;padding-left:22px;max-height:45vh;overflow:auto;font-size:13px}ol li{margin-bottom:6px}
ol button{border:1px solid var(--line);background:var(--bg);border-radius:4px;cursor:pointer;font-size:11px;padding:1px 6px;margin-left:4px}
textarea{width:100%;min-height:70px;border:1px solid var(--line);border-radius:8px;padding:8px;font:inherit;font-size:13px}
.save{width:100%;margin-top:10px;background:var(--gold);color:#141414;border:0;border-radius:999px;padding:12px;font:600 14px Poppins,Arial,sans-serif;cursor:pointer}
.msg{margin-top:8px;font-size:13px;min-height:1.2em}.msg.err{color:#a3261d}.msg.ok{color:var(--green)}
button:focus-visible,input:focus-visible,textarea:focus-visible{outline:2px solid var(--gold);outline-offset:2px}
</style></head><body>
<header><div class="e">Studio Contentu NKB</div><h1>Wybierz <em>fragmenty</em></h1>
<p>To wszystko, co powiedziałaś w nagraniach, z czasem każdej kwestii. Zaznaczone są ostatnie pełne ujęcia powtarzanych zdań. Odsłuchaj, popraw zaznaczenia i kliknij Zapisz.</p></header>
<main><section id="list"></section>
<aside><h3>Twoja rolka</h3><div class="sum" id="sum"></div><ol id="order"></ol>
<label for="note" style="font-size:13px;font-weight:500">Uwagi do montażu (opcjonalnie)</label>
<textarea id="note" placeholder="np. zacznij od zdania o wieczorach, końcówkę skróć"></textarea>
<button class="save" id="save" type="button">Zapisz wybór</button><div class="msg" id="msg" role="status"></div></aside></main>
<audio id="au" preload="none"></audio>
<script>
const ROWS = __ROWS__;
let order = ROWS.filter(r=>r.tick).map(r=>r.id);
const fmt=s=>{const m=Math.floor(s/60), x=(s-m*60).toFixed(1).padStart(4,'0'); return m+':'+x};
const list=document.getElementById('list'), au=document.getElementById('au');
let clip=null, box=null, stopAt=0, playing=null;
ROWS.forEach(r=>{
  if(r.clip!==clip){clip=r.clip; const d=document.createElement('div'); d.className='clip';
    d.innerHTML=`<h2>Nagranie ${clip.replace('c','')}<span>${r.file}</span></h2>`; list.appendChild(d); box=d;}
  const el=document.createElement('label'); el.className='row'+(r.tick?' on':''); el.htmlFor='r'+r.id;
  el.innerHTML=`<input type="checkbox" id="r${r.id}" ${r.tick?'checked':''}><button type="button" class="play" aria-label="Odsłuchaj">&#9654;</button>
    <span class="t">${fmt(r.in)}–${fmt(r.out)}</span><span class="txt"></span>`;
  el.querySelector('.txt').textContent=r.text;
  if(r.takes>1){const b=document.createElement('span');b.className='badge';b.textContent=`ujęcie ${r.take} z ${r.takes}`;el.querySelector('.txt').appendChild(b);}
  el.querySelector('input').addEventListener('change',e=>{el.classList.toggle('on',e.target.checked);
    if(e.target.checked){order.push(r.id);order.sort((a,b)=>a-b)} else order=order.filter(i=>i!==r.id); draw();});
  const pb=el.querySelector('.play');
  pb.addEventListener('click',e=>{e.preventDefault(); if(playing===pb){au.pause();return;}
    document.querySelectorAll('.play.now').forEach(x=>x.classList.remove('now'));
    const src='/audio/'+r.clip; if(!au.src.endsWith(src)) au.src=src;
    const go=()=>{au.currentTime=Math.max(0,r.in-0.15); stopAt=r.out+0.2; au.play(); playing=pb; pb.classList.add('now');};
    if(au.readyState>=1) go(); else {au.addEventListener('loadedmetadata',go,{once:true}); au.load();}});
  box.appendChild(el);
});
au.addEventListener('timeupdate',()=>{if(au.currentTime>=stopAt) au.pause();});
au.addEventListener('pause',()=>{if(playing){playing.classList.remove('now');playing=null;}});
function draw(){
  const ol=document.getElementById('order'); ol.innerHTML='';
  let total=0;
  order.forEach((id,k)=>{const r=ROWS[id]; total+=r.out-r.in; const li=document.createElement('li');
    li.textContent=r.text.length>70?r.text.slice(0,70)+'…':r.text;
    const up=document.createElement('button');up.type='button';up.textContent='↑';up.setAttribute('aria-label','Wyżej');
    const dn=document.createElement('button');dn.type='button';dn.textContent='↓';dn.setAttribute('aria-label','Niżej');
    up.onclick=()=>{if(k>0){[order[k-1],order[k]]=[order[k],order[k-1]];draw();}};
    dn.onclick=()=>{if(k<order.length-1){[order[k+1],order[k]]=[order[k],order[k+1]];draw();}};
    li.append(up,dn); ol.appendChild(li);});
  const n=order.length, d=n%10, h=n%100;
  const word=n===1?'fragment':(d>=2&&d<=4&&!(h>=12&&h<=14))?'fragmenty':'fragmentów';
  document.getElementById('sum').textContent=`${n} ${word}, około ${Math.round(total)} s mowy`;
}
draw();
document.getElementById('save').addEventListener('click',async()=>{
  const msg=document.getElementById('msg');
  if(!order.length){msg.className='msg err';msg.textContent='Zaznacz co najmniej jeden fragment.';return;}
  try{const res=await fetch('/save',{method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({order,note:document.getElementById('note').value})});
    if(!res.ok) throw new Error(await res.text());
    msg.className='msg ok';msg.textContent='Zapisane. Wróć do Claude, montaż rusza.';
  }catch(e){msg.className='msg err';msg.textContent='Nie udało się zapisać. Spróbuj jeszcze raz.';}
});
</script></body></html>'''


class Server(ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = os.name != 'nt'


def handler(proj, rows, until_saved, server_box):
    out_path = os.path.join(proj, 'fragments.json')
    page = PAGE.replace('__ROWS__', json.dumps(rows, ensure_ascii=False)).encode('utf-8')

    class H(BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def local(self):
            host = (self.headers.get('Host') or '').split(':')[0]
            return host in ('127.0.0.1', 'localhost')

        def reply(self, code, body=b'', ctype='text/plain; charset=utf-8', extra=None):
            self.send_response(code)
            self.send_header('Content-Type', ctype)
            self.send_header('Content-Length', str(len(body)))
            self.send_header('Cache-Control', 'no-store')
            for k, v in (extra or {}).items():
                self.send_header(k, v)
            self.end_headers()
            if self.command != 'HEAD':
                self.wfile.write(body)

        def do_GET(self):
            if not self.local():
                return self.reply(403, b'local only')
            if self.path in ('/', '/index.html'):
                return self.reply(200, page, 'text/html; charset=utf-8')
            m = re.match(r'^/audio/(c\d+)$', self.path)
            if m:
                return self.audio(os.path.join(proj, 'work', m.group(1) + '.wav'))
            self.reply(404, b'not found')

        do_HEAD = do_GET

        def audio(self, path):
            """the clip's wav, with Range support so the page can jump to any line"""
            if not os.path.isfile(path):
                return self.reply(404, b'no audio')
            size = os.path.getsize(path)
            rng = re.match(r'bytes=(\d*)-(\d*)', self.headers.get('Range') or '')
            a, b = 0, size - 1
            if rng and (rng.group(1) or rng.group(2)):
                if rng.group(1):
                    a = int(rng.group(1))
                    b = int(rng.group(2)) if rng.group(2) else size - 1
                else:
                    a = max(0, size - int(rng.group(2)))
                b = min(b, size - 1)
            with open(path, 'rb') as fh:
                fh.seek(a)
                body = fh.read(b - a + 1)
            extra = {'Accept-Ranges': 'bytes'}
            if rng and (rng.group(1) or rng.group(2)):
                extra['Content-Range'] = f'bytes {a}-{b}/{size}'
                return self.reply(206, body, 'audio/wav', extra)
            self.reply(200, body, 'audio/wav', extra)

        def do_POST(self):
            if not self.local() or self.path != '/save':
                return self.reply(403, b'no')
            try:
                data = json.loads(self.rfile.read(int(self.headers.get('Content-Length') or 0)) or b'{}')
                ids = [int(i) for i in data.get('order') or []]
                picked = [{k: rows[i][k] for k in ('clip', 'in', 'out', 'text', 'take', 'takes')} for i in ids]
                if not picked:
                    raise ValueError('nothing picked')
            except (ValueError, IndexError, TypeError, KeyError) as e:
                return self.reply(400, str(e).encode())
            result = {'saved': datetime.datetime.now().isoformat(timespec='seconds'), 'by': 'buyer', 'reason': '',
                      'note': str(data.get('note') or '').strip()[:2000], 'picked': picked}
            with open(out_path, 'w', encoding='utf-8') as fh:
                json.dump(result, fh, indent=1, ensure_ascii=False)
            self.reply(200, b'ok')
            say(f'STATUS fragments SAVED {out_path} picked={len(picked)} of {len(rows)}')
            if result['note']:
                say(f'NOTE her note to the edit: {result["note"]}')
            if until_saved:
                threading.Timer(2.0, server_box[0].shutdown).start()

    return H


def free_port(want):
    for p in [want] + list(range(want + 1, want + 40)):
        with socket.socket() as s:
            try:
                s.bind(('127.0.0.1', p))
                return p
            except OSError:
                continue
    return 0


def main():
    skillenv.utf8_stdio()
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    proj = skillenv.path_arg(args[0])
    if not os.path.isfile(os.path.join(proj, 'transcript.txt')):
        sys.exit('transcript.txt is missing: run ingest.py first.')
    rows = group_takes(read_lines(proj))
    if not rows:
        sys.exit('transcript.txt has no lines: nothing to pick (was anything said in the clips?)')
    if '--auto' in args:
        i = args.index('--auto')
        why = args[i + 1] if i + 1 < len(args) else ''
        if why not in AUTO_REASONS:
            sys.exit('--auto needs a reason: "buyer" (she said "wybierz sam" in this edit) or "no-browser" (the page '
                     'cannot open here). Anything else: open the page, she picks.')
        picked = [{k: r[k] for k in ('clip', 'in', 'out', 'text', 'take', 'takes')} for r in rows if r['tick']]
        result = {'saved': datetime.datetime.now().isoformat(timespec='seconds'), 'by': 'claude', 'reason': why,
                  'note': '', 'picked': picked}
        out_path = os.path.join(proj, 'fragments.json')
        with open(out_path, 'w', encoding='utf-8') as fh:
            json.dump(result, fh, indent=1, ensure_ascii=False)
        say(f'STATUS fragments AUTO {out_path} reason={why} pre-ticked={len(picked)} of {len(rows)}: '
            f'you pick the takes (references/cutting.md)')
        return
    port =free_port(int(args[args.index('--port') + 1]) if '--port' in args else 4760)
    box = [None]
    srv = Server(('127.0.0.1', port), handler(proj, rows, '--until-saved' in args, box))
    box[0] = srv
    url = f'http://127.0.0.1:{srv.server_address[1]}/'
    say(f'STATUS fragments READY {url}  lines={len(rows)} pre-ticked={sum(r["tick"] for r in rows)}')
    if '--no-open' not in args:
        threading.Timer(.4, lambda: webbrowser.open(url)).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
    say('STATUS fragments CLOSED')


if __name__ == '__main__':
    main()
