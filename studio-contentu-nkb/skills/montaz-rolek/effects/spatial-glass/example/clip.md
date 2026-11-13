# Szklane panele: the demo clip

The demo of this effect is the clip the buyer sees on the catalog page (`picker/previews/effects/spatial-glass.mp4`): a
Polish talking-head reel recorded for Studio Contentu NKB and edited in the Studio's style "Wyrazisty" (Inter Tight
800 white captions, key word in DM Serif Display yellow #FFF04A). Use it as a worked example of the settings, never
as the buyer's own result.

Footage: wide shot, camera still, 1080x1920, 30 fps. Slot: 5.3 s (160 frames).
Spoken line in the slot: "a on dobiera napisy, grafiki i animacje pasujące do danej sceny."

The CLIP block it was built with:
```
STEPS = [('napisy,', 'napisy'), ('grafiki', 'grafiki'), ('animacje', 'animacje')]       # the speaker's own short words (1 to 3 words). Pane 1 grid header, pane 2 typed, pane 3 ring
DONE = 'auto'          # when the ring resolves to a check: a word, seconds, or 'auto' (about 1 s after step 3)
DONE_LABEL =  ''    # the ring's label after the check ('' keeps the step-3 text)
OUT = 'auto'           # when the panes leave: 'auto' (plain footage 3 frames before the end), seconds, or 'cut'
PANES = 'auto'         # 'auto' (3, or 2 when the shot has no room), or force 3 / 2 (2 = the bar types steps 1 and 2)
LAYOUT = 'auto'        # 'auto', or {'grid': (cx, cy, k), 'ring': (cx, cy, k), 'bar': (cx, cy, k, width)} in frame REF px
REF = 'auto'           # the frame every position is measured in ('auto' = middle of the effect)
GLASS = 'auto'         # 'light' (frosted, dark type) or 'smoke' (darker glass, cream type); auto = smoke in a dark room
FONT =  'Inter Tight'                 # the sans on the panes (bar text, grid header): a family in assets/fonts/fonts.css
WEIGHT =  800                   # its weight (nearest face)
FONT2 = 'Instrument Serif'     # the ring label
ITALIC2 = True                 # ring label in italic when the family has one
CASE = 'as typed'              # bar text + ring label: 'as typed', 'upper', 'lower', 'title' (grid header is always caps)
INK = 'auto'                   # type colour: 'auto' (near-black on light glass, cream on smoke) or (r, g, b)
ACCENT =  (255, 240, 74)       # send button + check fill (butter yellow); the buyer's highlight colour
PUSH = 0.03                    # camera push-in while the panes are up (0.03 = 3 percent), 0 = none
TRUCK = 'auto'                 # sideways camera slide (parallax), 'auto' = 0.12 towards the grid side, 0 = none
LAMP = 'auto'                  # a practical light in shot (x, y) in frame REF, None, or 'auto' (brightest small blob)
```
Everything not in the block was left at the effect's default unless the block says otherwise.
