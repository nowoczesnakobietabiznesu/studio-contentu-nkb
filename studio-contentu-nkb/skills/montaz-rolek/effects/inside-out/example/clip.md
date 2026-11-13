# Okno w sylwetce: the demo clip

The demo of this effect is the clip the buyer sees on the catalog page (`picker/previews/effects/inside-out.mp4`): a
Polish talking-head reel recorded for Studio Contentu NKB and edited in the Studio's style "Wyrazisty" (Inter Tight
800 white captions, key word in DM Serif Display yellow #FFF04A). Use it as a worked example of the settings, never
as the buyer's own result.

Footage: close-up shot, camera still, 1080x1920, 30 fps. Slot: 6.5 s (195 frames).
Spoken line in the slot: "możemy rozmawiać o tym, że AI napisze nam posta szybciej, tylko tutaj mówimy o czymś zupełnie innym"

The CLIP block it was built with:
```
FILL =  'fill/ekran-1-pion.mp4'           # the buyer's fill: a file in fill/ ('fill/shop.mp4') or 'auto' (the first video in fill/, else
                        # the first image). B-roll of a place, a product or a screen. NEVER a person, no big text.
FILL_START = 0.0        # seconds into the fill clip to start from (skip a shaky start, a title or a person walking in)
FILL_FOCUS = (0.5, 0.5)  # which part of a landscape fill stays in the 9:16 crop: (x, y) from 0 to 1, 0.5 = centre.
                        # Look at work/qa/fill.jpg and move it toward the interesting part.
FILL_PUSH = (1.03, 1.10)  # slow push on the fill: zoom on its first and last frame (1.0 = no push)
FIT = 'auto'            # 'auto' (wide shots only: the whole picture is framed inside the small body, then grows into
                        # the room with the flip), True (always), False (never: the picture is room-sized throughout)
T_IN =  'AI'           # the window opens on this word: a word from words.json ('edit', 'edit#2' for its 2nd time),
                        # seconds, or 'auto' (the first word that starts after 0.4 s). Re-measured on the audio.
T_FLIP =  'tylko'         # the flip (the clip becomes the room): a word, seconds, or 'auto' (the word that starts
                        # nearest 1 s after T_IN and still leaves a 1 s hold). Best on the payoff word of the line.
T_OUT = 'auto'          # the real room eases back: 'auto' (over 10 frames, plain for the last 4), seconds, or 'cut'
                        # (holds to the last frame; only when the reel cuts away right after the slot)
ACCENT = (255, 248, 239)  # the thin cut line (r, g, b): cream. The buyer's accent works if it reads on their shirt
LINE_PX = (2.0, 3.0)    # line thickness: px inside / outside the matte edge (thicker reads bolder, calmer is thinner)
KEEP = 'auto'           # the live head-and-neck zone: 'auto' (from the measured head) or dict(cy=, rx=, ry=) in px:
                        # ellipse centre below the head top, half width, half height. Only if the window eats the chin.
MATTE_KILL_POLYS = []   # matte repairs, off: polygons [(x, y), ...] in 1080x1920 px where the cutout grabbed room
                        # (a chair arm, a frame). Look at a preview first; add only what you see.
SEED = 7                # the sounds are synthesised from this seed
```
Everything not in the block was left at the effect's default unless the block says otherwise.
