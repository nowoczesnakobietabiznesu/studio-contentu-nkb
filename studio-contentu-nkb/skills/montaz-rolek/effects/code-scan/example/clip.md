# Kod: the demo clip

The demo of this effect is the clip the buyer sees on the catalog page (`picker/previews/effects/code-scan.mp4`): a
Polish talking-head reel recorded for Studio Contentu NKB and edited in the Studio's style "Wyrazisty" (Inter Tight
800 white captions, key word in DM Serif Display yellow #FFF04A). Use it as a worked example of the settings, never
as the buyer's own result.

Footage: close-up shot, camera still, 1080x1920, 30 fps. Slot: 5.3 s (159 frames).
Spoken line in the slot: "Serio, jestem w szoku, co to narzędzie robi teraz dla biznesu"

The CLIP block it was built with:
```
T_IN =  'szoku,'        # the print front starts on this word ('drop', or 'drop#2' for its 2nd time), seconds, or 'auto'
                     # (the first word after 0.5 s). Re-measured on the audio; the code has landed IN_DUR later.
T_OUT = 'auto'       # the picture is fully back by this word's onset (a word or seconds), or 'auto' (HOLD after landing)
HOLD = 1.7           # seconds the full code look holds when T_OUT is 'auto' (1.4 to 2.0 lets the card type and read)
IN_DUR = 0.55        # seconds the print front takes to cover the frame (0.45 to 0.6 reads deliberate, not jumpy)
OUT_DUR = 0.50       # seconds back to the plain picture
PROMPT = '> '        # what the card's first line starts with
LINE1 =  'co to narzędzie robi'    # the card's typed line: a few of the speaker's own words, lower case reads as a command. Never a
                     # product, app or person's name unless the buyer asks for it.
LINE2 =  ''       # the line that pops in with a check mark when the typing ends ('' for none)
FONT = 'JetBrains Mono'   # card font: any family in assets/fonts/fonts.css (the buyer's caption font works)
WEIGHT = 500         # card font weight (variable fonts follow it; a static file stays what it is)
CASE = 'as typed'    # card lines: 'as typed', 'upper', 'lower', 'title'
CODE_FONT = 'JetBrains Mono'  # the glyphs the picture is drawn in (a monospace face keeps the code readable)
CODE_WEIGHT = 500
INK = (255, 248, 239)         # the speaker's tokens and the card text (cream); the buyer's text colour works
ACCENT =  (255, 240, 74)      # accent tokens, her outline, the prompt and check mark (butter); the buyer's highlight
ROOM_INK = (124, 135, 158)    # the room's glyphs (slate)
BACKDROP = (20, 22, 28)       # the code world's background (near black slate)
TOKENS =  ['cięcie', 'napisy', 'montaż', 'render', 'rolka', 'hook', 'klatka', 'dźwięk', 'eksport', 'tempo', 'ujęcie', 'zoom']
                     # the words the code is written in: the topic of the line works best (lower case, 3 to 8 letters)
ACCENT_WORDS =  ['montaż', 'render']   # tokens always drawn in ACCENT inside the speaker
TERM_CENTRE = 'auto' # (x, y) of the card in 1080x1920 px; 'auto' = below the chin, else beside or above the head
TERM_SCALE = 'auto'  # card size factor; 'auto' = 1.0, smaller only when the lines are long
SHOT = 'auto'        # 'auto' (from the head width), or force 'close' / 'medium' / 'wide' / 'none' (no person)
FACE_BLEND = 0.26    # how much of the real face shows through the head glyphs (0.15 to 0.35)
GLINT = 1.0          # light on the print front and the one breath as the code lands (0 = off)
FRONT = 0.35         # softness of the print front (0.25 crisper, 0.5 more of a dissolve)
```
Everything not in the block was left at the effect's default unless the block says otherwise.
