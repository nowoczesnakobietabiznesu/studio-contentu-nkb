# Ekran za Tobą: the demo clip

The demo of this effect is the clip the buyer sees on the catalog page (`picker/previews/effects/ui-world.mp4`): a
Polish talking-head reel recorded for Studio Contentu NKB and edited in the Studio's style "Wyrazisty" (Inter Tight
800 white captions, key word in DM Serif Display yellow #FFF04A). Use it as a worked example of the settings, never
as the buyer's own result.

Footage: medium shot, camera still, 1080x1920, 30 fps. Slot: 5.0 s (150 frames).
Spoken line in the slot: "Teraz wrzucam surowe nagranie do Claude Code, zatwierdzam koncepcję i na tym"

The CLIP block it was built with:
```
# What is on the screen. 'chat' = the packaged chat-style screen filled with YOUR text (fields below). Or the path of
# a picture / screen recording of your own app or page, e.g. 'assets/screen.png' or 'assets/screen.mp4' (portrait,
# at least 1080 wide; a recording must be at least as long as the slot). Only show screens you have the right to show.
SCREEN = 'chat'
APP_NAME = 'Claude'      # chat: the name in the header (your app, your tool, your page)
APP_MARK = None          # chat: small logo next to the name, an svg / png you supply in assets_fx/. None = no logo
GREETING =  'Co dziś montujemy?'   # chat: line in the empty screen before anything happens. None = none
PLACEHOLDER =  'W czym mogę pomóc?'  # chat: grey text in the empty message box
# Chat story. Every frame number is the frame of the spoken word the thing lands on (from `python onsets.py`).
# Any part can be None and is then left out. REPLY and STEPS need SEND.
ATTACH =   (40, ['nagranie'])   # (frame, 1 to 5 things that fly into the box).
#                          Each thing is a short label, or the path of a picture ('assets/screen/a.jpg') for a thumbnail
TYPE =  (62, '/montaz-rolek')   # (frame, text typed into the box, max ~30 characters). A leading "/" gets a tinted pill
SEND =  79                # frame the message is sent (button click, the box drops away, the message moves up)
REPLY =  (84, 'Działam. Montuję Twoją rolkę.')   # (frame, the answer that streams in word by word, max ~34 characters)
STEPS = ('Montaż rolki', [(95, 'Wybrałam najlepsze ujęcia'), (105, 'Wycięłam pauzy'), (118, 'Koncepcja zatwierdzona'), (128, 'Napisy i dźwięk')])
#                          (card title, [(frame, row text), ...]) 1 to 4 rows: each row appears on its frame and
#                          ticks 5 frames later. Rows max ~30 characters
RESULT =   (140, 'rolka.mp4', None, 'Gotowe')   # (frame, title, picture path or None, badge text): the card that
#                          pops in beside the speaker's head on the payoff word. A 9:16 picture works best
LABELS =  [(45, 'SUROWE NAGRANIE', 'attach')]   # highlighter tags: (frame, TEXT, where).
#                          where = 'attach' (beside the attachments), 'text' (after the typed text) or (x, y) frame px
#                          read off a SAFE=1 snapshot. [] = none. Tags placed before SEND leave when it sends

F_IN = 0                 # frame the screen drops in (the frames before it are untouched a-roll)
F_OUT = None             # frame the screen lifts away again. None = it stays to the last frame
EDGE = None              # y (frame px) of the bottom edge of the screen = the speaker's chest line. None = measured from the speaker's
#                          cutout (neck + 0.45 head). Set it by eye if work/measure.jpg shows the pink line off
HEAD_Y = 860             # y the top of the speaker's head is moved down to, so the screen has room above it (the speaker is never
#                          moved up; if the speaker already sits lower the speaker stays where the speaker is). 760 to 900 works
ZOOM = None              # punch-in on the speaker. None = measured (up to 1.25 when the speaker's head is under 190px tall). 1 = none
RESULT_SIDE = None       # 'L' or 'R': side of the speaker's head the result card lands on. None = the side with more room
ACCENT = '#1F1E1D'       # button / progress colour: your app's brand colour
HILITE =  '#FFF04A'       # highlighter tag colour (butter yellow)
CAPTION_FIX = {}         # captions come from words.json: fix what Whisper misheard, {'claw': 'Claude'}; '' drops a word
CAP_Y = None             # y of the caption line in the room band. None = 114px under the chest line
SCREEN_ZOOM = 1.0        # media: 1 = the picture fills the frame width; more = closer
SCREEN_X = 0             # media: px to slide the picture sideways (negative = left)
SCREEN_Y = 0             # media: px to slide the picture down (negative = up). The top 220px sits under app chrome
SCREEN_SCROLL = 0        # media: px the picture scrolls up over the slot (a long page). 0 = still
SHADOW = .26             # how dark the speaker's shadow on the screen is (0 = none)
FIX_EDGE = True          # use the cleaned cutout from prep.py (assets/fg.webm). False = assets/subject.webm as is
VOICE = True             # False = silent slot (no a-roll audio in the render)
SOUNDS = None            # None = whoosh on F_IN and ATTACH, pop on the first tag and on RESULT, click on SEND.
#                          Or your own list [(sound, frame, base volume)], played at 0.75x. [] = none
```
Everything not in the block was left at the effect's default unless the block says otherwise.
