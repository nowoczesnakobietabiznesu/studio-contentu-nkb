#!/usr/bin/env python3
"""Open the Studio Picker on the buyer's own picks file.

Usage:  PY picker.py [--tab styles|captions|effects] [--until-saved] [--no-open] [--port N]

  --tab            open straight on one section ("zmień napisy" -> captions: "Stwórz swój styl";
                   "zmień efekty" -> effects: the effects under the caption styles, demo clips she can tick)
  --until-saved    stop by itself a few seconds after the buyer presses Save (handy when you wait on this command).
                   Without it the picker stops about 25 seconds after its browser tab is closed.

The picks are saved to studio-picks.json in the state folder (the "picks" path in .platform.json), never inside the
skill folder. Lines to watch for:
    STATUS picker READY http://127.0.0.1:4747/
    STATUS picks SAVED <path> mode=... style=... captions=... effects=... parts=...
    STATUS nkb SAVED <state>/nkb-pick.json kind=overall|captions key=<nkb style> accent=#RRGGBB effects=auto|<keys>|unchanged
    STATUS effects SAVED <path> effects=auto|<keys>        (she changed only the effects)
    STATUS picker CLOSED
effects=auto: she ticked no effect, so you pick the ones that fit each reel (SKILL.md, "Effects").
Standard library only, so it also runs before setup has finished.
"""
import os
import subprocess
import sys
import threading

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import skillenv  # noqa: E402


def main():
    skillenv.utf8_stdio()
    args = [a for a in sys.argv[1:] if a != '--until-saved']
    until_saved = '--until-saved' in sys.argv
    serve = os.path.join(skillenv.SKILL_DIR, 'picker', 'serve.py')
    picks = skillenv.picks_file()
    os.makedirs(os.path.dirname(picks), exist_ok=True)
    cmd = [sys.executable, '-u', serve, '--config', picks] + args
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='replace')
    for line in proc.stdout:
        print(line.rstrip(), flush=True)
        # the NKB catalog saves "STATUS nkb SAVED" (a style + brand colour + effects) or "STATUS effects SAVED"
        if until_saved and line.startswith(('STATUS picks SAVED', 'STATUS nkb SAVED', 'STATUS effects SAVED')):
            threading.Timer(3.0, proc.terminate).start()      # leave the page a moment to show its "saved" message
    code = proc.wait()
    nkb = os.path.join(os.path.dirname(picks), 'nkb-pick.json')
    if until_saved and (os.path.isfile(picks) or os.path.isfile(nkb)):
        print('STATUS picker CLOSED after save', flush=True)
        return 0
    return code


if __name__ == '__main__':
    sys.exit(main())
