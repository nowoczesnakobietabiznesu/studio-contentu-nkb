# Kolaż z papieru: the demo clip

The demo of this effect is the clip the buyer sees on the catalog page (`picker/previews/effects/paper-cut.mp4`): a
Polish talking-head reel recorded for Studio Contentu NKB and edited in the Studio's style "Wyrazisty" (Inter Tight
800 white captions, key word in DM Serif Display yellow #FFF04A). Use it as a worked example of the settings, never
as the buyer's own result.

Footage: close-up shot, camera still, 1080x1920, 30 fps. Slot: 2.7 s (81 frames).
Spoken line in the slot: "zwracasz uwagę. Przecież on tego nie wie."

The CLIP block it was built with:
```
T_IN =   0.6         # the paper rips in on this word: a word from words.json ('look', or 'look#2' for its 2nd time),
                      # seconds, or 'auto' (the first word that starts after 0.4 s). Re-measured on the audio.
T_OUT =  'cut'        # the collage tears away: 'auto' (room back 4 frames before the slot ends), seconds, or 'cut'
                      # (holds to the last frame; only when the reel cuts away right after the slot)
ROWS = [
    'PRZECIEŻ ON',
    'TEGO NIE WIE',
]                     # or seconds. Use the speaker's own words; no names, numbers or outlets they did not say.
LAYOUT = 'auto'       # 'auto', 'above' (letters above the head, cutout shrinks toward its corner) or 'below' (letters
                      # across the chest, under the chin). Leave 'auto' unless the printout's choice looks wrong.
FONT =   'mix'          # 'mix' = the ransom mix of the shipped faces, or ONE family from assets/fonts/fonts.css (the
                      # buyer's caption font: every letter in it, still on mixed papers), or a list of families
WEIGHT = 800          # weight for a named FONT (variable faces follow it; static faces stay what they are)
CASE = 'upper'        # 'upper', 'as typed', 'lower', 'title'
INK = (20, 22, 28)            # the dark ink and dark scraps (r, g, b): the buyer's text colour if it is dark
ACCENT = (200, 34, 47)        # the red scraps, the pen ellipse and underline: the buyer's highlight colour
ACCENT2 = (43, 73, 194)       # the blue scraps and the crayon: a second brand colour
HIGHLIGHT =  (255, 240, 74)   # the yellow paper and yellow scraps
ELLIPSE = 'auto'      # which row gets the pen ellipse: a row number (0 = top), 'auto' (the shortest row that is not
                      # the last), or None
TAPE = True           # a strip of tape slaps on the first letter of the last row
MATTE_KILL_POLYS = []  # matte repairs, off by default: polygons [(x, y), ...] in 1080x1920 px where the cutout grabbed
                       # room (a picture frame, a cabinet edge). Look at a preview first; add only what you see.
MATTE_PLATE = None     # still camera only: dict(roi=(x0, y0, x1, y1), frames=[...], thr=20, min_area=2200): a clean
                       # plate of a region, from frames where the speaker is out of it, drops pixels that match the room
SEED = 7               # change for a different scatter of papers, fonts and tilts
```
Everything not in the block was left at the effect's default unless the block says otherwise.
