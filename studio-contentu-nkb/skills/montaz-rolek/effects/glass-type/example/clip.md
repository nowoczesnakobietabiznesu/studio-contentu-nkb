# Szklane słowo: the demo clip

The demo of this effect is the clip the buyer sees on the catalog page (`picker/previews/effects/glass-type.mp4`): a
Polish talking-head reel recorded for Studio Contentu NKB and edited in the Studio's style "Wyrazisty" (Inter Tight
800 white captions, key word in DM Serif Display yellow #FFF04A). Use it as a worked example of the settings, never
as the buyer's own result.

Footage: close-up shot, camera still, 1080x1920, 30 fps. Slot: 3.6 s (108 frames).
Spoken line in the slot: "pracy, zrób z niej skilla, czyli instrukcję, jak jej"

The CLIP block it was built with:
```
TEXT =  'SKILL'               # the ONE word in glass: the word the line turns on, as she says it (8 letters or fewer read biggest)
T_IN =  'skilla,'                 # when it arrives: 'auto' = the spoken word matching TEXT in words.json, or a word ('design#2' = its 2nd time), or seconds. Re-measured on the audio
T_OUT = 'auto'                # when it leaves: 'auto' = HOLD seconds after it lands (always gone 6 frames before the slot ends), a word, seconds, or 'cut' (stays to the last frame: only when the reel cuts right after)
HOLD = 1.3                    # seconds it stands after landing (with T_OUT 'auto')
PLACE = 'auto'                # 'auto' = the biggest open wall near her head (printed by measure), 'above', 'left', 'right', or (x, y, width) in px for the word's top-left and width
MAX_HIDDEN = 0.10             # share of the letters she may stand in front of (she occludes the glass; no single letter more than 30%)
LEVEL = 'auto'                # 'auto' = level unless the wall's lines really slope at that height (then follows at most 4 deg), True = always level, or degrees
# ---- the look (defaults = the approved demo; take the buyer's caption font and colours when the reel has a style)
FONT, WEIGHT = 'Inter Tight', 900     # a family from assets/fonts/fonts.css and its weight. Heavy faces only: thin strokes leave no glass to bend the room through
CASE = 'upper'                # 'upper', 'lower', 'title' or 'as is'
STRETCH, TRACKING = 1.10, 0.035       # vertical stretch of the letters and letter spacing (em): the demo's tall condensed look
INK = '#0B1016'               # the dark glass rim, the hairline round each letter and the soft backing shade (a deep near-black; the buyer's darkest colour works)
ACCENT = '#FFF6EA'            # the light on the glass: the travelling highlight and the rim light (warm white; a pale tint of the buyer's accent works)
TINT = '#F2F8F4'              # the glass body colour, very pale (white = perfectly clear, a pale green = real window glass)
BACKING = 'auto'              # soft dark shade behind the letters, 0..1: 'auto' = strong over a window or a lamp, light on a wall
RIM_DARK = 'auto'             # dark glass edge, 0..1: 'auto' = by the light behind (stronger over bright)
RIM_LIGHT = 'auto'            # thin bright rim on the bevels that face the light, 0..2: 'auto' = stronger on a plain or dark wall
SHADOW = 'auto'               # the glass's shadow + caustic on the wall, 0..0.4: 'auto' = off on a dark wall, stronger on a plain one
LIGHT_FROM = (-0.7, -0.7)     # where the room's key light comes from in the picture (x, y; -1 = left / top): sets the shadow side and the rim light
IOR, BEVEL, DEPTH = 1.52, 15.0, 62.0  # glass: refractive index, bevel radius and thickness (canvas px of a 400 px tall word)
DISPERSION = 0.035            # rainbow split at the rims
KEY_GAIN = 0.50               # brightness of the travelling highlight on the flat faces
DRIFT = 1.0                   # the slow slide and turn while it stands (0 = dead still)
VOL_AIR, VOL_LAND, VOL_RING = 0.16, 0.10, 0.05   # sounds: air swell into the landing, soft low thump, faint glass ring (x0.75 applied). 0 = off
SEED = 3                      # the sounds' noise (same seed, same sound)
```
Everything not in the block was left at the effect's default unless the block says otherwise.
