# Okładka magazynu: the demo clip

The demo of this effect is the clip the buyer sees on the catalog page (`picker/previews/effects/cover-story.mp4`): a
Polish talking-head reel recorded for Studio Contentu NKB and edited in the Studio's style "Wyrazisty" (Inter Tight
800 white captions, key word in DM Serif Display yellow #FFF04A). Use it as a worked example of the settings, never
as the buyer's own result.

Footage: wide shot, camera still, 1080x1920, 30 fps. Slot: 6.3 s (189 frames).
Spoken line in the slot: "Daję Claude'owi surowy materiał i odchodzę od komputera. On montuje, a ja tylko sprawdzam."

The CLIP block it was built with:
```
T_IN = 'Daję'        # the cover arrives on this word: a word from words.json ('video', or 'video#2' for its 2nd time),
                     # seconds, or 'auto' (first word that starts after 0.4 s). The onset is re-measured on the audio.
T_LAND = 'montuje,'      # the cover line lands on this word (same forms). 'auto' = longest word that leaves 1.5 s to read.
OUT = 'auto'         # when the cover leaves: 'auto' (gone 3 frames before the slot ends), seconds, or 'cut' (holds
                     # to the last frame; only when the reel cuts away right after the slot)
MASTHEAD = 'ROLKI'    # an invented title, never a real magazine's logotype. 3 to 6 letters. Letters that end in a stem
                     # or bowl sit best over the head (build.py prints which letters are over it)
LINES = [
    ('NUMER\nO ROLKACH', 'label-left', None),
    ('MONTAŻ\nZ CLAUDE', 'label-right', None),
    ('TEMAT NUMERU', 'kicker', None),
    ('On montuje,\na ja tylko *sprawdzam*', 'main', None),
]
FONT = 'DM Serif Display'      # cover line family: any family in assets/fonts/fonts.css (the buyer's caption font)
ITALIC = False                  # cover line in the italic of FONT when the slot has one
WEIGHT = 400                   # cover line weight (variable fonts follow it; a static file stays what it is)
CASE = 'as typed'              # cover line + kicker: 'as typed', 'upper', 'lower', 'title'
MAST_FONT = 'DM Serif Display'  # masthead family (a high-contrast serif reads as a magazine)
LABEL_FONT = 'DM Serif Display'         # tracked caps of the labels and kicker
INK = 'auto'                   # type colour: 'auto' (cream, near-black over a bright wall) or (r, g, b)
ACCENT = (255, 240, 74)       # the *word* colour (butter yellow); used once
FRAMING = 'auto'               # 'auto', or force 'behind' / 'above' / 'clear' (see effect.md "Adapting")
HEAD_TOP = 'auto'              # highest row the head reaches (1080x1920 px) if the measured one is off, else 'auto'
ZOOM_CENTRE = 'auto'           # (x, y) the push-in grows from; 'auto' = the measured face
PUSH = 0.03                    # push-in on T_IN (0.03 = 3 percent), then a slow drift
```
Everything not in the block was left at the effect's default unless the block says otherwise.
