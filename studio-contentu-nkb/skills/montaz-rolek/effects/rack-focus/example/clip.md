# Ostrość na tytuł: the demo clip

The demo of this effect is the clip the buyer sees on the catalog page (`picker/previews/effects/rack-focus.mp4`): a
Polish talking-head reel recorded for Studio Contentu NKB and edited in the Studio's style "Wyrazisty" (Inter Tight
800 white captions, key word in DM Serif Display yellow #FFF04A). Use it as a worked example of the settings, never
as the buyer's own result.

Footage: close-up shot, camera still, 1080x1920, 30 fps. Slot: 5.6 s (168 frames).
Spoken line in the slot: "Czyli spokojnie dwie godziny roboty, której szczerze nie miałam ochoty robić."

The CLIP block it was built with:
```
T_LAND =  'godziny'      # the word the focus lands on (title sharp): a word from words.json ('skill', or 'skill#2' for its
                     # 2nd time), seconds, or 'auto' (the longest word that leaves 1.6 s after it). Audio onset re-measured.
T_BACK = 'auto'      # when focus starts back to the speaker: 'auto' (HOLD seconds after the title is sharp), a word, or s
HOLD =  1.3           # seconds the title stays sharp when T_BACK is 'auto' (shortened if the slot ends too soon)
SMALL =  'SPOKOJNIE'    # the tracked caps line above the word: a few of the speaker's own words, '' for none
BIG =  '2 godziny'         # the one word in the big serif: the key word of the sentence (the speaker's own word)
FONT =  'DM Serif Display'   # big word family: any family in assets/fonts/fonts.css (the buyer's caption font works)
ITALIC =  False        # big word in the italic of FONT when the slot has one
WEIGHT = 400         # big word weight (variable fonts follow it; a static file stays what it is)
CASE = 'as typed'    # big word: 'as typed', 'upper', 'lower', 'title'
SMALL_FONT = 'Inter Tight'  # tracked caps family (keep it bold: thin caps vanish over the blurred picture)
SMALL_WEIGHT = 700   # tracked caps weight
SMALL_CASE = 'upper'  # tracked caps case
INK =  (255, 255, 255)  # colour of the caps line (cream); (r, g, b)
ACCENT =  (255, 240, 74)       # colour of the big word: 'ink' (same as INK) or (r, g, b), e.g. the buyer's highlight colour
ALIGN = 'left'       # 'left' (caps start over the word, the demo look) or 'centre'
BOKEH = 'auto'       # disc colour: 'auto' (from the lights in the room, kept off orange) or (r, g, b)
TITLE_CENTRE = 'auto'  # (x, y) of the sharp title block in 1080x1920 px; 'auto' = best spot off the face (printed)
SHOT = 'auto'        # 'auto' (from the head width), or force 'close' / 'medium' / 'wide' / 'none' (no person)
MAX_RADIUS = 'auto'  # room blur in px at full focus on the title; auto: close 30, medium 26, wide 22
SUBJECT_RATIO = 'auto'  # speaker's blur as a share of the room's; auto: close 0.62, medium 0.78, wide 0.88
REST_RADIUS = 'auto'  # disc size while the title is out of focus; auto: 0.31 (close) or 0.26 x the big word's size
BREATHING = 0.026    # the picture grows this much as the focus comes forward (a real lens breathes)
```
Everything not in the block was left at the effect's default unless the block says otherwise.
