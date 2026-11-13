# The effects

One flat list for you. An effect can go anywhere in a reel. What the buyer sees is `references/efekty.md`: the
same effects in Polish, in a few groups, one line each. On the catalog page (picker.py --tab effects) she sees
every effect as a finished demo reel recorded in the Studio and ticks as many as she likes. These 42 are all the
effects there are.

Every effect is one of two kinds (the "Kind" column below, `status` in `index.json`):

- **ready**: packaged. `effects/<key>/` holds finished machinery that measures the clip itself, one block of
  settings to fill in (the CLIP block at the top of `build.py`), an `effect.md` with the exact run order, and
  `slot.json` (what it needs and how it behaves inside a reel). You make a slot, fill the CLIP block, run the listed
  commands, check, add it to the reel. You do not rewrite code.
- **recipe**: the finished build of one real reel. Its machinery is reusable, but the block marked CLIP-SPECIFIC at
  the top (frames, words, positions, paths) belongs to that demo and has to be rewritten for the buyer's clip.

The effect folders hold no demo footage, cutouts or sounds: an effect only ever runs on the buyer's own clip. The
only demo footage in the skill is the NKB catalog's sample (`picker/nkb/`), used for the style previews and never in
a reel. An `example/clip.md` in an effect folder is a worked example in words: the settings one demo clip used,
with no footage.

Almost every effect needs the clean cutout (`setup.py --matting`, one time, about 105 MB). Pull-Back Reveal needs
none, and Comment Bubble can run without it (`fx_new.py --no-cutout` and `CHIN_Y` typed in). The Cutout column
below says what each one needs.

## Before you use one (every time)

1. **Footage check.** `PY "SK/scripts/footage_check.py" "<project>"` checks the picked effects against what was
   measured on this clip. `SKIP` means leave it out and tell the buyer the one line it prints. `CHECK` means look at
   the frames yourself. Never force an effect onto footage that fails. The lines under an `OK` say what has to be in
   place first: `setup.py --matting` (the clean cutout, one time, about 105 MB), `setup.py --fx <key>` (extra
   Python packages for that effect, one time), or something from the buyer.
2. **Parts.** When the picks carry `effectSections`, an effect may only go in the parts the buyer allowed
   (hook = the opening line, end = the call to action, middle = the rest). The footage check prints the time window
   of each part. `fx_new.py`, `fx_add.py` and `build_reel.py` all enforce it: a slot outside its parts is refused
   or left out, with the reason.
3. **Only where it fits the words.** An effect lands on a line that calls for it (a number for Odometer, a list for
   Checklist, the comment keyword for Comment Bubble). No line that fits means no effect, even if it was picked.
   One or two effects in a short reel is plenty.

## A ready effect

An effect slot is a small project of its own: it takes N frames of the reel and hands back the same N frames with
the effect applied (1080x1920, 30fps). The reel build lays that render over the reel for exactly those frames.

```
1. PY "SK/scripts/fx_new.py" <key> --project "<project>" --from <sec> --to <sec> [--hi]
       Reel seconds. Start about 0.1s before the first word the effect reacts to, end about 1.5s after it lands
       (or on a cut). It makes <project>/fx/<key>/ with the effect's scripts, the slot's frames, the reel's own
       words cut to the slot, fonts, sounds, and the speaker cutout (cut from the reel's cutout when there is one,
       else it mattes only the slot's frames: about 1.2s per frame, tell the buyer first).
       It prints the commands for this effect with the real paths filled in, and saves them as RUN.txt in the slot.
       Example snapshot times that would run past the end of this slot are spread over the slot for you.
       A line starting with CHECK layout.json means the slot's clean cutout and layout.json disagree about where
       the head is by more than 60 px: look at work/layout/check.jpg and run layout.py again before going on.
2. Read <slot>/effect.md. Fill the CLIP block at the top of <slot>/build.py with the Edit tool. Follow the
   "in a reel" lines fx_new.py printed (no grade of its own, leave before the slot ends, and so on).
3. Run the printed commands in order. They all look like this:
       PY "SK/scripts/fx_run.py" "<slot>" measure.py              one of the effect's own scripts
       PY "SK/scripts/fx_run.py" "<slot>" build.py SAFE=1         switches are plain NAME=value words
       PY "SK/scripts/fx_run.py" "<slot>" hf lint
       PY "SK/scripts/fx_run.py" "<slot>" hf snapshot --at 0.4,1.2,2.0     LOOK at <slot>/work/snap/contact-sheet.jpg
       PY "SK/scripts/fx_run.py" "<slot>" build.py                guide off: always the last build before a render
       PY "SK/scripts/fx_run.py" "<slot>" hf render               -> <slot>/renders/<slot folder>.mp4
   The render refuses to start while the red guide is on, and checks the frame count afterwards.
4. PY "SK/scripts/fx_add.py" "<project>" "<slot>"
       Checks the render, copies it to <project>/assets/fx/, and writes the slot into plan.json: its frames, what
       happens to the reel's captions, a small brightness lift so the slot matches its neighbours, and the
       effect's own sounds.
5. PY "SK/scripts/build_reel.py" "<project>", lint, render, then the self-check on the slot's moments and both of
   its edges: PY "SK/scripts/frames_check.py" "<project>" "renders/<file>.mp4" --at <the times fx_add.py printed>.
   Nothing on the face, nothing in the red area, clean cutout edge, readable text, no jump in or out of the slot.
   Fix it (one pass) or take it out: fx_add.py "<project>" "<slot>" --remove, and tell the buyer why.
```

A second slot of the same effect: add `--name <folder>` to `fx_new.py`. `--hi` also cuts the slot from the original
clip at its own size (Digital Zoom stays sharp that way). Two slots can never share frames.

An effect that lives ON a cut (Zoom-Through Cut): give `fx_new.py` a span ACROSS one cut of the reel, about 0.5s on
each side (the footage check prints where the cuts are). The slot then holds both shots and knows the cut frame.
Every other effect needs one continuous shot: `fx_new.py` refuses a span that crosses a cut, except an overlay effect.

**Overlay effects** (Depth Scatter, Stat Stack, Dot Counter, Chip Row, Prompt Box, Serif Flow; `"layer": "overlay"` in
their `slot.json`) are graphics only. Their final build is transparent and `hf render` makes `renders/<slot>.webm`; the
reel lays it over its OWN footage, so the reel's grade, cuts and punch-ins (the style's too) stay under it, and
the span may cross cuts. `build.py SAFE=1` (or `PREVIEW=1`) puts the slot's footage under the graphics for the
snapshots only; the build after it, without SAFE, is the transparent one. Their `build.py` writes
`work/reel_captions.json`, so `fx_add.py` hides the reel's captions just while the effect's own words are up (Chip
Row keeps them on). They need no cutout and read where the face is from the reel's `layout.json`: on a close-up with
no room under the chin they move above the head, and with no room either side they stop with a one-line reason.

## A recipe

1. Copy `SK/effects/<key>/` (and `SK/engine/fonts` as `assets/fonts`, plus the two files in `SK/engine/template/`)
   to `<project>/fx/<key>/`. Cut the frames the effect covers into `fx/<key>/assets/aroll.mp4` with ffmpeg
   (exactly N frames, 1080x1920, 30fps, from `<project>/assets/aroll.mp4`), and its words into `words.json`
   (times counted from the start of the slot).
2. Rewrite the CLIP-SPECIFIC block from the buyer's footage. Where a build reads a tool by a fixed path, use `ffmpeg`
   / `ffprobe` from PATH and `PY` for Python. Paths that start with `FXLAB/`, `WORKSPACE/` or `HOME/` are the demo's
   own files: replace every one. Helper scripts ending in `.sh` are the demo's shell notes: run the same ffmpeg /
   HyperFrames commands directly (they work the same on Windows), do not run the `.sh` file.
3. Build, lint, snapshot, render the slot with `PY "SK/scripts/hf.py" "<project>/fx/<key>" <command>` (the folder
   comes first, it runs inside it): the slot is a full-frame 1080x1920
   render with exactly the same number of frames it was given.
4. Add it to `<project>/plan.json` by hand and run `build_reel.py` again:
   `"slots": [{"key": "<key>", "src": "fx/<key>/renders/slot.mp4", "from": 3.2, "to": 6.4, "captions": "hide"}]`
5. Self-check the slot from the final render, as for a ready effect.

## Captions, sound and parts around a slot

- **Captions.** Each ready effect says what the reel's own captions do while it plays (`reel_captions` in its
  `slot.json`): `hide` when the effect carries the words itself or sits where the captions go, `keep` when it stays
  out of their way. `fx_add.py --captions keep|hide` overrides it for one slot. When an effect's own words cover
  only part of the slot, hide the captions for just that window: `fx_add.py ... --hide-captions 3.9-4.9`.
  Before and After, when it is built with its own words on (a reel with no captions), works its own window out
  and `fx_add.py` applies it without a flag. `fx_add.py --caption-y N` keeps the reel's captions on but moves
  the top of their line to screen y N while the slot plays. An effect that needs the chest for itself prints the
  value in its build. The same value is right for every caption style, and the move happens on a caption change,
  never in the middle of a caption.
  Check in the slot snapshots that no spoken word is left without a caption.
- **The buyer's caption style wins.** See "Restyling an effect's own words" below. No effect brings its own
  caption look into a reel that has a style.
- **Sound.** The voice always comes from the reel's own cut, so there is no audio seam. The effect's own sounds are
  read from the slot and replayed in the reel. `--no-sfx` leaves them out.
- **A style with its own grade or motion.** A slot gets the reel's colour grade but not the style's push-ins or
  reframing. Look at both edges of the slot. If it jumps, drop the effect for that reel.
- **Cutouts.** "clean" means `rvm_cut.py` (about 1.2 seconds per frame; `fx_new.py` mattes only the slot's frames).
  "quick" means `cutout.py` is enough. The clean one needs `setup.py --matting` once.
- Everything shown on screen is real (the buyer's own numbers and reels) or a generic placeholder. Never a real
  person, never made-up proof, no like or view counts that were not given.

## Restyling an effect's own words (the buyer's style wins)

The rule is at the top of SKILL.md. The effects in the table below can put words on screen. In a reel that has a
caption style (or a style the buyer showed or described) they never keep their own caption look. An effect that
draws words and has no row here yet follows the same rule: read its `effect.md`, decide which of the two kinds
its words are, and add what you find to the slot.

- **Words that only repeat what is said: turn them off.** The reel's captions carry the words in the buyer's
  style. `fx_new.py` already prints the build commands with `CAPTIONS=0` for those effects.
- **Words that are the effect: restyle them** to the buyer's style before the first build. Typeface, case, weight,
  colours, plate or no plate. The slot is the buyer's own copy of the effect, so edit its `build.py` freely.
- Everything else in an effect is open too: sound level (`SFX_GAIN`, `SOUNDS`, `SFX=0`), motion strength (`PUSH`,
  the scales in `ZOOMS`), timing (the frame and second values in the CLIP block), colours (`ACCENT`, `GRADE`).

| Effect | Its words | Switch that turns them off | Where the look is set in the slot's `build.py` |
|---|---|---|---|
| Before and After | repeat speech (the after-side captions). The two tags are the effect | `CAPTIONS=0` (the default in a reel; the tags stay) | Tags: `LABELS`, `LABEL_Y`. Own captions, only for a reel with no captions: `CAPS`, `CAP_Y`, `CAP_FS`, `ACCENT`, `PUNCH`; typeface in the `font-family:'Inter Tight'` rules at the end of the page template |
| Orbit | repeat speech | `CAPTIONS=0` (the default in a reel), then `fx_add.py --caption-y <printed value>` | Own captions, only for a reel with no captions: `CAPS`, `CAP_Y`, `CAP_LINE` (sizes); typeface in the `.cap` css rules |
| The Stack | caption words repeat speech. The title and the cards are the effect | `CAPTIONS=0` for the caption words (the default in a reel), then `fx_add.py --caption-y <printed value>` | Title and cards: `TITLE`, `CARDS`, `ACCENT`, and the `font-family:'Inter Tight'` rules in `PAGE`. Caption band: `CAP_Y`, `CAP_H` |
| UI World | the caption line repeats speech. The screen and the tags are the effect | `CAPTIONS=0` for the caption line (the default in a reel), then `fx_add.py --caption-y <printed value>` | Tags: `LABELS`, `HILITE`. Screen: `ACCENT`, `INK`, and the font rules of the screen css. Caption line: the `.cap` css rule, `CAP_Y` |
| Checklist | the effect (a title and rows) | none | `TITLE` (drawn in caps by `.upper()` in the eyebrow line), `ROWS` (`*word*` = accent word), `ACCENT`, `GLASS`, row size `FS`, place `CARD_BOX`. Typeface: `font:600 26px ... Montserrat` (eyebrow) and the two `font:800 ... 'Inter Tight'` rules (rows, pill) |
| Comment Bubble | the effect (the typed keyword, the comment, the reply, the chip) | none | The style lines at the end of the CLIP block: `WORD_FONT`, `TEXT_FONT` (css family, weight, font file), `UPPER`, `ACCENT_COL`, `LIGHT_COL`, `DARK_COL`. Size and place: `SCALE`, `DROP`, `X_CENTER` |
| Freeze Sticker | the effect (handwritten notes, a stamp) | `CAPTIONS=0` = no notes or doodles | `NOTES`, `STAMP`, `INK`, `ACCENT`, `PAGE`, `SIZE`, `PLACE`. Typeface: `.note{font-family:'Caveat'}` and the stamp rule (`'Inter Tight'`, `text-transform:uppercase`) |
| Green Screen | repeat speech. The speaker is shrunk to the bottom, so the reel's normal caption line would land on the face | `CAPTIONS=0` (the default in a reel), then `fx_add.py --caption-y <printed value>`: the reel's captions move to the line above the head | Own captions, only for a reel with no captions: `CAPS`, `CAP_KEY`, `CAP_WORDS`, `CAP_PLATE`, `CAP_PX`, `CAP_GAP` (lowercase, typeface in the `.cap` css rule). More room above the head: `SIZE = 'small'` |
| Blackout | the effect: one punch word behind the head, a word the speaker says | `CAPTIONS=0` = no word (the dim, flash, kick and snap stay, the reel's captions say the word). With the word on, hide the reel's caption for that one word (`--hide-captions a-b`) | the `WORD STYLE` block under the CLIP block in `build.py`: `WORD_FONT`, `WORD_FONT_FILE`, `WORD_WEIGHT`, `WORD_ITALIC`, `WORD_CASE`, `WORD_TRACK`, `WORD_COLOUR`, `WORD_GLOW`, `WORD_PLACE`, `WORD_SIZE` |
| Knockout Tiles | the effect (name tiles, receipts, total). The reel's captions keep running | none needed: nothing covers the captions | the `STYLE` block at the top of `build.py`: `name_*` and `small_*` (typeface, weight, case, tracking), `tile_bg`, `tile_text`, `label_color`, `strike`, `paper`, `paper_ink`, `radius`, `order`. Another typeface may need `width_factor` |
| Pull-Back Reveal | the effect (window title, checklist, counter, label). It also draws the spoken words on the small card, because the reel's captions are hidden while the slot plays | `CAPTIONS=0` = no spoken words on the card | the `STYLE` block at the top of `build.py`: `ui_font`, `ui_weight`, `ui_case`, `label_font`, `label_case`, the colours (`page`, `window`, `panel`, `ink`, `accent`, `done`, `highlight`), and for the spoken words `cap_font`, `cap_weight`, `cap_case`, `cap_size`, `cap_color`, `cap_mark`: set those to the buyer's caption style. Limit: the words on the card take typeface, case, size and colour, not a plate behind them and not a word that lights up as it is said. Tell the buyer when their style has one of those |
| Timeline Burn | the effect (track labels, timecodes). The reel's captions keep running | none needed. The timeline sits in the chest band: add the slot with the `--caption-y` value `build.py` prints, or `--captions hide` when it says there is no room | the `STYLE` block at the top of `build.py`: `FONT`, `WEIGHT`, `CASE`, `TEXT`, `LABEL_PX`, `NAME_PX`, `ACCENT`, `PANEL`, `PANEL_EDGE`, `PALETTE`. Set `DIM = 0` when the buyer's style is already dark or they do not want the room dimmed |
| Type Wall | the effect (the wall of words) | none | `PHRASES`, `FS`, `INK`, `ACCENT`, `GROUND`, `ACCENT_Y`. Typeface: its own `@font-face` (`'Inter Tight Wall'`) and the `.wd` rule. The wall is drawn in capitals |
| Depth Scatter, Stat Stack, Dot Counter, Chip Row, Prompt Box, Serif Flow | the effect (the words are what the effect shows; the reel's captions are hidden only while they are up, Chip Row keeps them on) | none needed | the `STYLE` block at the top of `build.py`, the same in all six: `font`, `weight`, `tracking`, `big_weight`, `big_tracking`, `case`, `small_font`, `small_weight`, `serif_font`, `serif_italic`, `ink`, `accent`, `card`, `shadow`. Colours as 6-digit hex. Their default is the house look |

Comment Bubble is the one with a ready style block. In the other effects made of words the typeface sits in css
rules inside `build.py`: change the family and weight there, keep the size variables, and look at the slot
snapshot, because text widths were tuned for the default typeface (lower `FS` or the size value when a word no
longer fits). Every font the Studio's styles use is already in the slot: `<slot>/assets/fonts/`, named
`<Family>-<weight>-<normal or italic>.woff2`, declared in `assets/fonts/fonts.css`.

Every caption style of the Studio is a spec: the reel's saved style (`references/my-styles.md`; one of the 20 NKB
caption styles or 10 ready styles from `nkb-styles/`, or one built from an example, `references/replicate.md`), with
this reel's plan.json on top. Restyle an effect's words to the values in that spec (`font`, `weight`, `case`,
`color`, `accent`, `plate`, `tracking`), and match its `motion` where the effect's words animate in.

## The list

<!-- LIST:START (generated from index.json, do not edit by hand) -->
42 ready, 0 recipe.

| # | Effect | Key | Kind | What it does | The buyer says | Framing | Camera | Wall | Cutout | Tracking | Extra packages |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Orbita | `orbit` | ready | Your own reels circle around you, passing behind and in front. | "put my reels in orbit around me" | wide or medium | still or drifting | no need | clean | none (prep.py measures the ring from the cutout; the ring follows the head) | none |
| 2 | Ściana okładek | `couch-wall` | ready | Your reel covers become a grid on the wall behind you. | "put my reels as a grid on the wall behind me" | wide or medium | still or drifting | clear wall above the head | clean | room track, wall and furniture found by colour (prep.py) | scipy |
| 3 | Ekran za Tobą | `ui-world` | ready | An app screen fills the frame and you stand in front of it. | "put me in front of the Claude screen" | wide or medium | still or drifting | no need | clean | none (laid out for the speaker's highest position) | scipy |
| 4 | Naklejka | `freeze-sticker` | ready | Your freeze frame becomes a die-cut sticker with handwritten notes. | "turn me into a sticker on this line" | any | any | no need | clean | none (one frame is frozen; bake.py measures its outline) | scipy |
| 5 | Wyjście z ramki | `frame-break` | ready | The video shrinks into a card and your head and hands pop out of it. | "shrink the video into a card and let me break out of it" | wide or medium | any | no need | clean | none (prep.py measures head, body and hands from the cutout) | none |
| 6 | Ściana słów | `type-wall` | ready | Giant words march behind you and swap on the word you say. | "put giant words behind me that change as I talk" | wide or medium | still | clear wall above the head | clean | none (prep.py measures the head; the wall is locked) | scipy |
| 7 | Karty z danymi | `the-stack` | ready | Data cards with racing bars stack above you, you sit in a window below. | "do the stacked data card layout on this line" | any | any | no need | clean | none (measure.py finds the head from the cutout; the window follows it) | none |
| 8 | Najazd | `digital-zoom` | ready | A slow creep onto your face, a hard snap on a key word, a whip back out. | "punch in on my face when I say X" | any | any | no need | clean | face (track.py) | none |
| 9 | Przyklejona etykieta | `sticky-text` | ready | A tag glued to your cap or chest that moves, tilts and scales with you. | "stick a tag that says X to my cap" | any | any | no need | clean | head and chest followed frame by frame from the cutout (track.py) | scipy |
| 10 | Licznik | `odometer` | ready | Numbers roll up digit by digit like a mileage counter. | "roll the numbers up like an odometer when I say X" | any | any | no need | clean | none | none |
| 11 | Komentarz | `comment-bubble` | ready | The comment keyword types itself, posts, and your reply with the link lands. | "show the comment being typed and my reply when I say comment X" | any | any | no need | clean | none | none |
| 12 | Stop-klatka z podpisami | `freeze-and-label` | ready | The picture freezes while you keep talking, tagged lines point at you. | "freeze the frame on X and label me: A, B" | any | any | no need | clean | none (the picture is frozen: everything is measured once on the held frame) | scipy |
| 13 | Telefon | `phone-mockup` | ready | A 3D phone flies in beside you playing a screen, taps land on your words. | "put a phone next to me showing the app" | any | still or drifting | no need | clean | none (build.py finds the side with more room from the cutout) | scipy |
| 14 | Lista kroków | `checklist` | ready | A card builds on the wall and each step ticks as you say it. | "put a checklist on screen for these three steps" | any | any | no need | clean | none (prep.py measures the clip) | none |
| 15 | Ściana nagłówków | `headline-wall` | ready | The wall behind you fills with headline and post cards, the key word highlighted. | "fill the wall behind me with headlines about X" | wide or medium | any | open wall beside the speaker | clean | room track (prep.py) | scipy |
| 16 | Przejście przez Ciebie | `zoom-through-cut` | ready | The camera dives through you and comes out in the next shot. | "make that cut a zoom-through" | any, two shots back to back | any | no need | clean | none (prep.py finds the dive points) | scipy |
| 17 | Klony | `clone` | ready | More of you pop up beside you on the words, then sync up for the payoff. | "sklonuj mnie na tych słowach" | wide | still | open room on both sides | clean | room drift lock (bake.py) | scipy |
| 18 | Przed i po | `before-and-after` | ready | A wipe line sweeps across your raw clip to reveal the edited version. | "do a before/after wipe on this line" | any | any | no need | clean | none (measure.py finds the head; both sides are the same frames) | none |
| 19 | Rosnący wykres | `chart-grow` | ready | A line chart draws on the wall behind you and kicks up on your word. | "draw a growth chart behind me that takes off when I say scale" | wide or medium | still or drifting | open room on both sides | clean | wall track for a drifting or handheld shot (measure.py); pinned on a still camera | scipy |
| 20 | Zaciemnienie | `blackout` | ready | The room dims on your line while you stay lit, the punch word slams in behind your head, and the lights snap back on the next line. | "dim the room when I say X and bring the lights back on the next line" | any | any | no need | clean | none (prep.py measures the head while the room is dim; the word is fixed on screen) | scipy |
| 21 | Płonąca oś | `timeline-burn` | ready | A video-editing timeline assembles in front of you, overheats, catches fire on your word and crumbles into embers. | "put an editing timeline on screen and burn it when I say X" | wide or medium | any | no need | clean | none (build.py reads the head box from the cutout; the timeline is a screen overlay) | scipy |
| 22 | Okno montażu | `pull-back-reveal` | ready | The live video shrinks into a card inside an app window: a checklist of the real edit ticks off, the shot timeline plays, a counter rolls up to the number you say. | "pull back and show this video being edited" | any | any | no need | none | none (the whole picture goes into the card; nothing is measured) | none |
| 23 | Skreślane nazwy | `knockout-tiles` | ready | Name tiles slam onto the wall behind you one per word, each gets struck out and knocked away; receipts can then stack up with a running total. | "put these names on the wall behind me and knock each one out as I say it" | wide or medium | still or drifting | open wall beside the speaker | clean | none (prep.py reads the head, its movement and the clear wall from the cutout) | none |
| 24 | Zielone tło | `green-screen` | ready | You are cut out and shrunk to the bottom of the frame, and the whole screen behind you becomes the thing you are talking about. | "green screen me over this video" | wide or medium | any | no need | clean | none (prep.py reads head top, chin, head width and the body's cut-off row from the cutout) | scipy |
| 25 | Pękające szkło | `shatter-3d` | ready | The frame fractures into tiles at different depths, jolts on your key word, then shatters like glass to reveal the clean shot. | "shatter the frame when I say X" | any | still or drifting | no need | clean | the face tile follows the head measured on the cutout | opencv-python-headless |
| 26 | Kolaż z papieru | `paper-cut` | ready | The room rips away to torn paper, you stay live as a white-edged cutout, and your phrase lands in cut-out letters before the collage tears back. | "turn this line into a paper collage and spell X in cut-out letters" | any | still or drifting | no need | clean | the cutout is live; the paper replaces the room | opencv-python-headless |
| 27 | Kredowy kontur | `doodle-boil` | ready | A hand-drawn chalk line traces your outline and boils, and chalk doodles draw on the words you pick. | "draw a chalk outline around me and doodle a heart when I say X" | any | still or drifting | no need | clean | the outline and the doodles follow the cutout every frame | opencv-python-headless |
| 28 | Kod | `code-scan` | ready | The picture resolves into readable code with you as a brighter figure, a small terminal types your two lines, and it resolves back. | "turn me into code when I say X" | any | still or drifting | no need | clean | every frame is redrawn from the cutout | opencv-python-headless |
| 29 | Spadające klocki | `word-pile` | ready | The things you name drop as solid slabs with real physics, glance off your head, land on a line with a thud, then blow away. | "drop these three names as blocks and pile them on a line" | any | still or drifting | no need | clean | the head is re-measured every frame (colliders) | opencv-python-headless |
| 30 | Okno w sylwetce | `inside-out` | ready | Your body becomes a window showing a clip you choose, then it flips: you are solid and the clip becomes the room. | "play this clip inside me, then swap the room to it" | any | still or drifting | no need | clean | the window follows the cutout every frame | opencv-python-headless |
| 31 | Tapeta ze słowa | `scene-text` | ready | A word prints across your real wall like wallpaper, behind you and the things on the wall, then two big words land on it. | "print X all over my wall and paint Y on it" | any | still or drifting | open wall beside the speaker | clean | camera track pins the print to the wall | opencv-python-headless |
| 32 | Okładka magazynu | `cover-story` | ready | The live shot becomes a magazine cover: a serif masthead behind your head, a hairline border, small labels and one italic cover line. | "make this line a magazine cover" | any | still or drifting | clear wall above the head | clean | none (the page is fixed to the screen; the cutout follows the speaker) | opencv-python-headless |
| 33 | Neon | `neon-sign` | ready | Your phrase as a neon tube on your wall: it flickers on, the room dims and the sign lights the wall. | "hang a neon sign that says X on my wall" | wide or medium | still or drifting | open wall beside the speaker | clean | camera track (shift, roll, scale) pins the sign to the wall | opencv-python-headless |
| 34 | Szklane panele | `spatial-glass` | ready | Three frosted glass panes float at different depths around you, one behind you, one for each step you name. | "float three glass panels around me for these three steps" | any | still or drifting | open wall beside the speaker | clean | the room is tracked and the panes ride it | opencv-python-headless |
| 35 | Ostrość na tytuł | `rack-focus` | ready | A title starts as soft lens bokeh, focus pulls to it while you and the room go into real lens blur, then racks back. | "rack focus to a title when I say X" | any | still or drifting | no need | clean | the title is glued to the lens | opencv-python-headless |
| 36 | Szklane słowo | `glass-type` | ready | One word as thick clear glass letters on your wall, bending the light behind them. | "put the word X in glass on my wall" | any | still or drifting | clear wall above the head | clean | camera track pins the glass to the wall | opencv-python-headless |
| 37 | Rozsypane słowa | `depth-scatter` | ready | Your opening words land one by one at different sizes and heights, and each earlier word goes soft as the next one lands. | "scatter my opening words" | any | any | no need | none | none (screen-fixed, placed from layout.json) | none |
| 38 | Wielka liczba | `stat-stack` | ready | The number you say lands huge over your chest, and a tiny caps line under it swaps on the words that follow. | "make the number huge on this line" | any | any | no need | none | none (screen-fixed, placed from layout.json) | none |
| 39 | Kropki postępu | `dot-counter` | ready | A row of dots pops in when you say how many things are coming; filled dots show how far along you are. | "pop a dot for each of the 3 things" | any | any | no need | none | none (screen-fixed, placed from layout.json) | none |
| 40 | Pigułki listy | `chip-row` | ready | As you list things, an outlined pill pops in for each one in a row under your captions. | "pop a pill for each thing I list" | any | any | no need | none | none (screen-fixed, placed from layout.json) | none |
| 41 | Pole promptu | `prompt-box` | ready | A glass input box appears over your chest and what you say you type into it types itself in, caret and all. | "type my prompt on screen" | any | any | no need | none | none (screen-fixed, placed from layout.json) | none |
| 42 | Proces na karcie | `serif-flow` | ready | The picture cuts to a dark card and your process builds down it: serif italic steps, bold steps, thin lines drawing between them. | "draw the process on a card" | any | any | no need | none | none (screen-fixed, placed from layout.json) | none |

## Per effect: what the buyer has to give you, and what to watch

- **Orbit** (READY, `effects/orbit/`: build.py, effect.md, onsets.py, prep.py, slot.json). Needs from the buyer: a folder of the buyer's own reel cover images (at least 4, 6 fills the default ring). Real view counts only if the buyer gives them. Speaker centred, wide or medium, chin above about y 1000 so a card fits under the face. Fails on a close-up selfie, a speaker who fills the frame width or sits far off centre, a hand held above the head, a weak cutout and a walking camera. Without the buyer's own covers the effect is left out.
- **Couch Wall** (READY, `effects/couch-wall/`: build.py, effect.md, onsets.py, prep.py, slot.json). Needs from the buyer: a folder of the buyer's own reel cover images (at least 4, 9 or more looks best). Real view counts only if the buyer gives them. Needs a plain one-colour wall in the upper frame. Fails on a tight selfie, a patterned wall (wallpaper, brick, shelves, a window) and furniture or floor the same colour as the wall (draw those in IN_FRONT). Without the buyer's own covers the effect is left out.
- **UI World** (READY, `effects/ui-world/`: build.py, effect.md, example, onsets.py, prep.py, slot.json). Needs from the buyer: what the screen shows: the buyer's words for the packaged chat screen, or the buyer's own picture or screen recording. Any names on it are generic placeholders. Still or near-still speaker facing the camera, head and shoulders in frame, one continuous shot. Nothing is tracked: a speaker who moves up and down a lot, walks, or raises hands above the head breaks it. Needs a clean cutout with both shoulders intact. A tight selfie leaves no room.
- **Freeze Sticker** (READY, `effects/freeze-sticker/`: bake.py, build.py, check.py, effect.md, onsets.py, slot.json). Needs from the buyer: the notes. Medium or wide is best (head and chest with air around them); a close-up gives a large sticker with room for one or two short notes. Breaks on a freeze frame with motion blur, closed eyes or a hand across the face, a cutout that lost hair or fingers on that frame, a speaker cut by both sides of the frame, and a head cut by the top of the frame.
- **Frame Break** (READY, `effects/frame-break/`: build.py, check.py, effect.md, onsets.py, prep.py, slot.json). Needs nothing from the buyer. One continuous shot, 3 to 6 s, head in the upper half with room above it. Best with a hand gesture that reaches sideways at chest height or higher; without one it still works as a head pop-out. Weak on a tight close-up and when the head touches the top of the frame. Needs a cutout that keeps hair and fingers. A hood or long hair over the shoulders needs HEAD typed in.
- **Type Wall** (READY, `effects/type-wall/`: assets_fx, build.py, effect.md, example, onsets.py, prep.py, slot.json). Needs nothing from the buyer. Locked camera only. Needs clear room above the head (head top at y 250 or lower in the frame). It replaces everything behind the speaker: furniture the speaker sits on has to be drawn in KEEP. Best on a short line with one word that matters; a word over about 7 letters does not fit.
- **The Stack** (READY, `effects/the-stack/`: build.py, effect.md, measure.py, onsets.py, slot.json). Needs from the buyer: the buyer's own figures: titles, labels, values and units for one to three small cards. One speaker, head and shoulders in frame, one continuous take of 3 to 6 s. A very tight selfie holds about 5 rows in all (build.py stops and says how much to drop). A far-away wide shot is enlarged and goes soft. Hands above the head, a hood or two people give a wrong head box: type HEAD. Without the buyer's own figures the effect is left out.
- **Digital Zoom** (READY, `effects/digital-zoom/`: bake.py, build.py, clipblock.py, effect.md, example, onsets.py, post.py, slot.json, track.py). Needs nothing from the buyer. One continuous shot with the face visible the whole time. With --hi a 1728 px source stays sharp to 1.6x; from a 1080 source every zoom is an upscale (capped at 1.5x).
- **Sticky Text** (READY, `effects/sticky-text/`: build.py, check.py, effect.md, slot.json, track.py). Needs nothing from the buyer. Works on handheld. 'cap' and 'chest' want a medium or close shot, 'head' (beside the head) wants room beside it. Breaks on a hand on or above the head, a hood or long hair hiding the neck, a second person, a head turn past about 40 degrees. When the cap is inside the top 220 px, 'cap' and 'head' are refused: use 'chest'.
- **Odometer** (READY, `effects/odometer/`: build.py, check.py, effect.md, example, measure.py, slot.json). Needs from the buyer: the real number, from the buyer. The panel sits behind the speaker, in open background beside or above the head. It stops with a clear message when the speaker fills the frame. Only a number the speaker actually says.
- **Comment Bubble** (READY, `effects/comment-bubble/`: build.py, check.py, effect.md, example, measure.py, slot.json). Needs from the buyer: the comment keyword (the cta mark in words.json). The commenter is a generic placeholder, never a real person. The cutout is only used to measure the chin and the avatar crop (fx_new.py --no-cutout and CHIN_Y by hand skips it). Needs the top of the head in frame and about 1.5 s of the same shot after the line.
- **Freeze and Label** (READY, `effects/freeze-and-label/`: bake_freeze.py, build.py, check.py, effect.md, slot.json). Needs from the buyer: the labels. Best wide or medium with room beside or above the speaker. The hold needs about 1 s per label. A tight selfie fits 1 or 2 short labels (build.py stops and says how many fit). Breaks on a blink or motion blur on the freeze word, a hood or long hair over the neck, a hand on the head, a second person. Hand points are found by skin colour and can miss a hand in front of the chest.
- **Phone Mockup** (READY, `effects/phone-mockup/`: build.py, check.py, effect.md, measure.py, prep.py, slot.json). Needs from the buyer: the buyer's own screen recording or picture for the phone, or the words for the packaged card. Medium or wide is best; close works with 300 px or more of background beside the head, and a close-up that fills the frame stops with 'no room for a phone'. Needs a slot of 2 s or more, the tap word not in the first 0.6 s or last 0.5 s, and no hand parked over the tap point. Not for a speaker walking across the frame.
- **Checklist** (READY, `effects/checklist/`: build.py, check.py, effect.md, example, onsets.py, prep.py, slot.json). Needs from the buyer: 2 to 4 steps, in the speaker's own words. Needs open room above or beside the speaker. A close-up gives a small card. On a moving camera it switches to an opaque card by itself.
- **Headline Wall** (READY, `effects/headline-wall/`: build.py, cards.py, effect.md, example, onsets.py, prep.py, slot.json). Needs from the buyer: the topic. Card text is written for the reel: generic outlets and placeholder names, never a real publication, person, number or made-up proof. One continuous shot, 3 to 6 s, with visible wall beside or above the head. A moving camera is tracked. A window, mirror or open doorway behind the speaker breaks the track. A tight selfie has no room for the big cards.
- **Zoom-Through Cut** (READY, `effects/zoom-through-cut/`: bake.py, build.py, effect.md, example, prep.py, slot.json, two_shot.py). Needs nothing from the buyer. Needs two different shots back to back (a real cut in the edit, not one continuous take), the speaker in both, and something dark and plain on the speaker to dive into. A cut in the middle of a word fights the move.
- **Clone** (READY, `effects/clone/`: bake.py, build.py, check.py, effect.md, example, prep.py, slot.json). Needs nothing from the buyer. Needs room on both sides and a furniture edge (sofa back, desk, counter) with wall above it for the clones to stand behind. No close-ups, no moving camera.
- **Before and After** (READY, `effects/before-and-after/`: build.py, check.py, effect.md, measure.py, prep_after.py, slot.json). Needs from the buyer: nothing needed. Optional: the buyer's own finished version of the same frames. Any shot, any camera. Needs a line that is about a change. Weak when the payoff word comes in the first 0.3 s or less than 1.5 s of slot follows the sweep. On footage that is already dark the default grade may be too quiet: raise AFTER_GRADE. The buyer's own after file must be the same take with no punch-in, reframe or speed change.
- **Chart Grow** (READY, `effects/chart-grow/`: build.py, check.py, effect.md, measure.py, slot.json). Needs from the buyer: nothing needed. Optional: the buyer's own real figures and labels for the chart. Needs open wall beside or above the head, best up and to the right where the line ends. A tight selfie stops with NO OPEN WALL. Breaks on a walking or panning camera, a wall with no texture on a handheld shot, hands flying through the top right during the kick, and a kick word in the first second of the slot.
- **Blackout** (READY, `effects/blackout/`: build.py, check.py, effect.md, onsets.py, prep.py, slot.json). Needs nothing from the buyer. One person, a line of 1 to 3 s that ends on one punch word, then a cut or the next line. Best wide or medium with room above the head; on a close shot the word sits just above the head. Needs a clean cutout: background the cutout keeps stays lit, lost hair or fingers dim with the room. Breaks on a hand above the head, two people, a head that reaches the top of the safe zone (no room for the word: move it or turn it off) and a room that is already dark.
- **Timeline Burn** (READY, `effects/timeline-burn/`: build.py, check.py, effect.md, slot.json). Needs nothing from the buyer. Wide or medium shot with the chin above about y 980 (y 1100 without a caption line): the timeline sits under the chin in the lower third. A tight selfie stops with 'No room for the timeline'. Needs 1 s or more of the slot before the burn word and 1 s after it. Reads best on a dark or dimmed picture (DIM). Only a wide shot on a still camera was tested.
- **Pull-Back Reveal** (READY, `effects/pull-back-reveal/`: build.py, check.py, effect.md, onsets.py, slot.json). Needs from the buyer: the reel's own edit list (steps really done, each shot's length in frames) and, for the counter, a number the speaker says. Any shot, any camera, no cutout. The checklist covers up to 170 px of the card's left edge: a face in the left quarter of the picture at mid height needs FACE set or shorter steps. The title bar covers the top 68 px of the clip, the timeline strip the bottom 240 px. Needs a slot of about 3.5 s or more. Only a handheld close-up was tested.
- **Knockout Tiles** (READY, `effects/knockout-tiles/`: build.py, check.py, effect.md, prep.py, slot.json). Needs from the buyer: the names the speaker lists; for receipts, the amounts they say. Wide or medium shot with about 400 x 150 px of clear wall beside the head, inside the safe zone. Still camera: the pieces are not tracked to the room. Needs the clean cutout. The running total needs about 150 px of wall above the head. A close-up stops with 'no clear wall'. Only a still wide shot was tested.
- **Green Screen** (READY, `effects/green-screen/`: build.py, check.py, effect.md, prep.py, slot.json). Needs from the buyer: the buyer's own video or picture of the thing they are talking about (at least one file in bg/). Medium is best (head, shoulders and chest). Wide works but the speaker is enlarged and turns soft above 1.3x. A close-up with less than about one head height of body under the chin stops with 'too tight'. Needs a clean cutout (the new background shows every matte fault), one speaker, a slot of 36 frames or more. Only a still camera was tested.
- **Shatter 3D** (READY, `effects/shatter-3d/`: bake.py, build.py, effect.md, example, fxio.py, onsets.py, post.py, requirements.txt, shcore.py, slot.json). Needs nothing from the buyer. Needs about 0.6 to 1.5 s between the break word and the punch word and about 1.2 s after it. The face tile always stays whole. Declines on a zoom while the frame is fractured.
- **Paper Cut** (READY, `effects/paper-cut/`: bake.py, build.py, collage.py, effect.md, example, fxio.py, onsets.py, post.py, requirements.txt, slot.json). Needs nothing from the buyer. Picks above / below / beside from the head and chin. Declines when the face fills the frame both ways or the source zooms inside the slot.
- **Doodle Boil** (READY, `effects/doodle-boil/`: bake.py, build.py, chalk.py, doodles.py, effect.md, example, post.py, requirements.txt, slot.json). Needs nothing from the buyer. Pick a doodle per word from the library in effect.md. build.py places them in open space off the face; it stops only when no space fits anywhere.
- **Code Scan** (READY, `effects/code-scan/`: bake.py, build.py, effect.md, example, fxio.py, onsets.py, post.py, requirements.txt, scan.py, slot.json). Needs nothing from the buyer. Hook or a 'this is how' beat. Without a cutout the whole picture becomes room code (voice-over). Declines on a hold under 0.6 s or a zoom inside the beat.
- **Word Pile** (READY, `effects/word-pile/`: bake.py, build.py, effect.md, example, fxio.py, onsets.py, pile_search.py, pile_sim.py, post.py, requirements.txt, slabs.py, slot.json). Needs nothing from the buyer. Fill the slab words with the things the speaker names. Declines when the chin is so low no slab fits above the line.
- **Inside Out** (READY, `effects/inside-out/`: bake.py, build.py, effect.md, example, fxio.py, onsets.py, post.py, requirements.txt, slot.json). Needs from the buyer: one b-roll clip or picture from the buyer. Needs the buyer's own b-roll in fill/ (never a person). Needs the chest in shot. Declines on a zoom inside the slot.
- **Scene Text** (READY, `effects/scene-text/`: build.py, effect.md, example, onsets.py, post.py, requirements.txt, scene.py, slot.json). Needs nothing from the buyer. Needs some plain wall behind or beside the speaker. Goes behind things on the wall by itself. Declines on a camera that travels.
- **Cover Story** (READY, `effects/cover-story/`: bake.py, build.py, cover.py, effect.md, example, fxio.py, onsets.py, post.py, requirements.txt, slot.json). Needs nothing from the buyer. Hook line said to camera. Picks the layout from the head: behind the head (medium), above it (selfie), clear above (wide). Declines when the head reaches the very top of the frame.
- **Neon Sign** (READY, `effects/neon-sign/`: bake.py, build.py, effect.md, example, fxio.py, neon.py, onsets.py, post.py, requirements.txt, scene.py, slot.json). Needs nothing from the buyer. Needs plain wall beside or above the speaker that stays clear. Tries beside, above, a corner, one line, then declines. A punch-in zoom inside the slot breaks the tracking.
- **Spatial Glass** (READY, `effects/spatial-glass/`: bake.py, build.py, effect.md, example, fxio.py, glass.py, onsets.py, post.py, requirements.txt, slot.json). Needs nothing from the buyer. Three steps the speaker names. Wide or medium gets three panes, a tight shot two smaller ones. Declines when the face fills the frame with no wall either side, or when the camera swings so far the face would cross the panes.
- **Rack Focus** (READY, `effects/rack-focus/`: bake.py, build.py, effect.md, example, fxio.py, onsets.py, post.py, rack.py, requirements.txt, slot.json). Needs nothing from the buyer. The title goes to the darkest calm spot off the face. Declines when the face fills every spot or the title would be sharp for under 0.55 s.
- **Glass Type** (READY, `effects/glass-type/`: build.py, effect.md, example, glass.py, onsets.py, post.py, requirements.txt, slot.json). Needs nothing from the buyer. Needs some open wall above or beside the head. Best with something behind to bend (window, lamp, panels); a plain wall still reads. Declines on a zoom inside the slot or a camera that travels.
- **Depth Scatter** (READY, `effects/depth-scatter/`: build.py, check.py, effect.md, slot.json, vgfx.py). Needs from the buyer: none (a spoken opening phrase of 2 to 6 words). Any framing. Close-up selfie with a low chin: the cluster moves above the head; no room above or below the face: it declines.
- **Stat Stack** (READY, `effects/stat-stack/`: build.py, check.py, effect.md, slot.json, vgfx.py). Needs from the buyer: none (a number the speaker says). Any framing. A number that is only passing (a year, 'one of the') is not a stat: leave it out.
- **Dot Counter** (READY, `effects/dot-counter/`: build.py, check.py, effect.md, slot.json, vgfx.py). Needs from the buyer: none (a spoken count from 2 to 8). Any framing. Needs a real count ('3 things', 'five steps').
- **Chip Row** (READY, `effects/chip-row/`: build.py, check.py, effect.md, slot.json, vgfx.py). Needs from the buyer: none (a spoken list of 2 to 4 short things). Any framing. Long items shrink the row to the safe width.
- **Prompt Box** (READY, `effects/prompt-box/`: build.py, check.py, effect.md, slot.json, vgfx.py). Needs from the buyer: none (a spoken instruction of up to about 60 characters). Any framing. A plain glass field, never a real app's screen.
- **Serif Flow** (READY, `effects/serif-flow/`: build.py, check.py, effect.md, slot.json, vgfx.py). Needs from the buyer: none (a line that describes 2 to 4 steps). Any framing: the card is full frame, so the face is never covered.
<!-- LIST:END -->
