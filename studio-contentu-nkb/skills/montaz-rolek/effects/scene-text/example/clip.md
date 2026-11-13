# Tapeta ze słowa: the demo clip

The demo of this effect is the clip the buyer sees on the catalog page (`picker/previews/effects/scene-text.mp4`): a
Polish talking-head reel recorded for Studio Contentu NKB and edited in the Studio's style "Wyrazisty" (Inter Tight
800 white captions, key word in DM Serif Display yellow #FFF04A). Use it as a worked example of the settings, never
as the buyer's own result.

Footage: medium shot, camera still, 1080x1920, 30 fps. Slot: 5.5 s (165 frames).
Spoken line in the slot: "A wszystko to w ramach subskrypcji za 18 euro miesięcznie."

The CLIP block it was built with:
```
PRINT_TEXT = 'SUBSKRYPCJA'        # the small word printed across her wall, over and over: the line's loudest idea, 1 or 2 short words
PRINT_FRAME = 64              # frame the print starts spreading out from behind her head: the frame she says that word (onsets.py, column "swap")
HERO = [(86, '18'), (100, 'EURO')]   # the 1 to 3 big painted words, each (frame it lands, 'WORD'). Frames from onsets.py; a frame late beats a frame early. [] = print only
CLEAR_FRAME = None            # frame the print lifts off again. None = 32 frames after the last big word
OUT_FRAME = None              # frame the big words are gone and the plain picture is back. None = CLEAR_FRAME + 14 (always 12 frames before the slot ends)
HOLD_TO_END = False           # True only when this slot ends the reel or ends on a cut: the big words then stay to the last frame
# ---- the look (defaults = a calm house look; take the buyer's caption style when the reel has one)
FONT, WEIGHT = 'Bebas Neue', 400      # big words: a family from assets/fonts/fonts.css and its weight (stand-in for Futura Condensed ExtraBold)
BOLDEN = 0.035                # extra stroke on the big words, as a share of the letter size (Bebas is thinner than the demo's poster face). 0 for an already heavy font
CASE = 'upper'                # 'upper', 'lower' or 'as is' (the print and the big words)
ACCENT = '#FFF04A'            # big-word paint colour (6-digit hex)
INK = '#14161C'               # colour of the block shade under the big words
PRINT_FONT, PRINT_WEIGHT = 'Inter Tight', 900   # the small print's font and weight
PRINT_INK = '#6F8263'         # print colour, sage (the default). On a light wall it is multiplied in, so it can only darken the plaster
PRINT_SIZE = None             # print letter size in px. None = from her head size (about 40 on a wide shot, up to 64 on a selfie)
# ---- placement (None / 'auto' = measured by `scene.py measure`; read its printout and work/measure.jpg)
HERO_BOX = None               # (x, y, w): left, top and width in px of the big-word block. None = the biggest open wall near her head
HERO_LAYOUT = 'auto'          # 'stack' (one word per line, all the same width), 'line' (side by side), 'auto' = whichever reads bigger
KEYSTONE = 'auto'             # wall perspective: 'auto' = from the room's vertical lines, None = flat on, (x, y) = point where the wall's verticals meet (px, may be far off frame)
PRINT_MODE = 'auto'           # 'multiply' (light wall), 'lift' (dark wall), 'auto' = by the wall's brightness
BUMP = 0.012                  # tiny camera punch as each big word lands (0 = off)
VOL_PRINT, VOL_HIT = 0.20, 0.05       # whoosh as the print spreads, low hit on each big word (template volumes, x0.75 applied). 0 = off
```
Everything not in the block was left at the effect's default unless the block says otherwise.
