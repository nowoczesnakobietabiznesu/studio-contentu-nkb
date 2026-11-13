# Ściana nagłówków: the demo clip

The demo of this effect is the clip the buyer sees on the catalog page (`picker/previews/effects/headline-wall.mp4`): a
Polish talking-head reel recorded for Studio Contentu NKB and edited in the Studio's style "Wyrazisty" (Inter Tight
800 white captions, key word in DM Serif Display yellow #FFF04A). Use it as a worked example of the settings, never
as the buyer's own result.

Footage: wide shot, camera still, 1080x1920, 30 fps. Slot: 6.2 s (186 frames).
Spoken line in the slot: "Daję Claude rolkę referencyjną, a on robi mi podobne wideo z moim brandingiem."

The CLIP block it was built with:
```
# The headlines: a plain list, one string per card, every one a version of the SAME message in different words.
# Put the phrase to highlight in [brackets] (one per headline). Keep them under ~40 characters; the list is cycled
# if the wall needs more cards than you wrote. No real outlets, people, numbers or results the speaker did not say.
HEADLINES = [
    '[Claude] montuje rolki',
    'Wrzucam przykład, [Claude] montuje',
    'Montaż rolek z [Claude]',
    'POV: [Claude] montuje Twoją rolkę',
    '[Claude] skopiował styl mojej rolki',
    'Twój nowy montażysta: [Claude]',
    'Rolka w moim brandingu od [Claude]',
    'Czy [Claude] umie montować?',
    '[Claude] i rolka referencyjna',
    'Mój branding, montaż [Claude]',
    '[Claude] robi wideo w moim stylu',
    'Montaż bez montażysty? [Claude]',
    'Rolka referencyjna dla [Claude]',
    '[Claude] dobiera napisy i grafiki',
]
# Hero cards: (headline, frame of the spoken word it lands on). 2 to 4 of them, in spoken order. They alternate
# sides of the speaker's head, so each needs clear wall beside the speaker. Frames come from `python onsets.py`.
HEROES = [
    ('[Claude] montuje rolki', 28),
    ('Rolka referencyjna? [Claude] zrobi resztę', 49),
    ('[Claude] robi wideo w moim stylu', 110),
    ('Twój branding, montaż [Claude]', 164),
]
SEARCH = 'czy [claude] montuje rolki'   # a search-bar pill opposite the first hero, lowercase like a real query. None = no pill
F_START = 2          # frame of the speaker's first syllable: the first card starts here
F_PEAK = 26          # frame where the opening phrase ends ("wszyscy o tym mówią"): the last pile card starts here
F_ACCENT = 28        # frame of the key word (the [bracketed] one): highlighter + bump + hit. Usually = HEROES[0] frame
DENSITY = 1.8        # 1 = cards arrive evenly, higher = slow start and a faster and faster pile-up
LEAD = 4             # frames a hero starts before its word so it is ~90% landed ON the word (do not go under 3)
F_OUT = None         # frame the cards whip off the wall again (a slot inside one continuous take, e.g. b-roll).
                     # None = the wall stays to the last frame. With F_OUT set PUSH and BUMP must be 1 and the first
                     # frames before F_START and the last 2 frames come out as untouched a-roll. Needs F_OUT <= frames - 12
KEEP_OUT = []        # screen rectangles (x0, y0, x1, y1) no card may enter on any frame, e.g. the main reel's label
                     # pill [(140, 222, 940, 322)]
VOICE = True         # False = silent slot (no a-roll audio in the render; also run with SFX=0)

WALL = None          # (x0, y0, x1, y1) px: the bare wall the cards may cover. None = full width, down to the speaker's elbows.
                     # SET IT when furniture, a window or a door sits beside the speaker: look at work/layout.jpg (cyan box)
FACE = None          # (x, y) px the push-in aims at. None = measured from the speaker's cutout
HERO_FIRST_SIDE = 'L'  # side of the speaker's head the first hero lands on ('L' or 'R'): pick the side with more clear wall
N_MID = None         # mid-depth cards (readable, inside the safe zone, heroes land on top). None = by wall area (5 to 10)
N_FAR = None         # far cards (small, soft, dim). None = as many as the wall area holds (6 to 15)
FAR_BLEED_SIDES = True  # far cards may run off the left / right frame edge as texture (never into the top 220px)
PUSH = 1.06          # slow push-in over the whole slot (1 = none; keep under 1.08 on 1080p footage)
BUMP = 1.032         # camera bump on the accent word (1 = none)
DIM = 1.0            # how much the room dims as the wall fills (0 = not at all; raise to 1.3 on a white wall)
ACCENT = '#FAE67A'   # highlighter colour (butter yellow; never orange)
OUTLETS = ['Newsletter tech', 'Biuletyn twórców', 'Magazyn branżowy', 'Przegląd tygodnia', 'Gazeta lokalna', 'Blog marketingowy',
           'Dział biznesu', 'Notatka branżowa']                     # placeholder source labels, must stay generic
PEOPLE = ['Założycielka', 'Właścicielka agencji', 'Twórczyni', 'Montażystka', 'Przedsiębiorczyni']   # placeholder "who posted it" labels
CHAT_REPLIES = ['od kiedy?', 'serio?', 'jak to?']             # second bubble on chat cards
DARK_LABEL = 'Czat grupowy'                                        # small label on the dark cards
FOREGROUND = []      # polygons [(x, y), ...] in reference-frame px of furniture that stands IN FRONT of the wall (a
                     # pillow, a sofa back): cards then pass behind it. Only needed when a card has to cross it;
                     # after editing run `prep.py matte`
FIX_MATTE = True     # bake assets/fg.webm with motion-blurred sleeves / hands made solid. False = use subject.webm as is
TRACK_YMAX = None    # px: only wall above this line is used for the camera track. None = 1100. Lower it to the top
                     # of a sofa / desk if the track wobbles (layout.jpg cards slide off the wall on early frames)
REF = None           # reference frame the layout is drawn in. None = 4 frames before the end (a settled frame)
SEED = 7             # change it to reshuffle tilts and far-card positions
# (sound, frame, base volume). Base volumes are the template's; everything is played at 0.75x. click-soft is a very
# quiet file, hence .36. Files: assets/sfx/<name>.mp3 or assets_fx/<name>.mp3
SOUNDS = [('whoosh-short', F_START - 1, .22), ('impact-bass-short', F_ACCENT, .10)] + \
         [('click-soft', f - 1, .34) for _, f in HEROES[1:]]
```
Everything not in the block was left at the effect's default unless the block says otherwise.
