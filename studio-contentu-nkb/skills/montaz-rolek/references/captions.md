# Captions: the styles, the word marks, where they sit

One engine (`SK/engine/captions.py`), driven by `words.json`. Every caption style of the Studio is a SPEC that engine
renders: the 20 NKB caption styles and the captions of the 10 ready styles (`nkb-styles/<key>/style.json`,
"caption"), and a style built from the buyer's example or description (`references/replicate.md`). There are no
other caption styles. `build_reel.py` takes the spec from the reel's saved style (`references/my-styles.md`), with
this reel's plan.json on top. You never edit the engine for a reel: you clean the words, mark them, and write the title.

## The 20 NKB caption styles

The catalog shows them in four families (Spokojne, Wyraziste, Dynamiczne, Edytorskie), five each. The keys are the
folder names in `nkb-styles/` (their `style.json` has `"nkb": {"kind": "captions"}`); `style.md` beside it says what
each one is for. A one-off build in another of them: `build_reel.py "<project>" --caption <key>` (in the colour of
her saved style). `--caption none` = no captions at all (titles and effects only).

## Marking the words (do this for every reel)

Each word in `words.json` can carry one mark in its `e` field. The marks are what make a caption style look
designed instead of typed.

| Mark | Meaning | Mark it when |
|---|---|---|
| `num` | a number worth showing big | the number IS the point of the line: "7 video effects", "$500 a day", "10x". Not for passing numbers ("one of the things", a year, a time of day). |
| `key` | a name or brand | every product, app, company or person said by name: "Claude", "Instagram". It keeps its capital in lowercase styles and turns yellow in Keyword. |
| `emph` | the word the line leans on | a sentence has no number and no comment keyword, and one word carries it ("never", "automatically", "everything"). The word you would stress out loud. |
| `cta` | the comment keyword | the word they ask people to comment: "comment EDIT". Exactly one per reel. |

The rule:
1. Run `PY "SK/scripts/marks.py" "<project>"` AFTER fixing mishearings. It guesses `num` (digits and number words),
   `cta` (the word after "comment") and `key` (capitalised words that do not start a sentence). It never guesses `emph`.
2. Then go through the transcript sentence by sentence:
   - at most ONE of `num` / `emph` per sentence (they are the punch; two punches fight). Keep the one the
     sentence is about and remove the other. A long sentence counts part by part: a comma, "and", "then" or "so"
     starts a new part.
   - the comment keyword ALWAYS keeps its `cta` mark, also when its sentence already has a `num` or an `emph`
     (a one-sentence reel: "get all 21 effects, then just comment VIDEO" keeps `21` num and `VIDEO` cta).
   - `key` on every name, as many as there are. Check sentence openers by hand: the script cannot tell a name that
     starts a sentence from a normal word (it lists them).
   - add `emph` where a sentence has no punch yet and one word clearly carries it. Not every sentence needs one.
   - never mark filler ("the", "and", "so", "that", "for").
3. A short reel (under 10 seconds) usually ends up with 2 to 5 marks. More than one mark every 4 words is too many.

Example: "Everybody's talking about Claude editing videos, so here are seven video effects that Claude created
for me." -> `Claude` key, `seven` num (write it as `7` if the buyer's style shows numbers big), second `Claude` key.

```json
{"text": "seven", "start": 3.18, "end": 3.52, "e": "num"}
```

## Titles come from the hook

`plan.json` (started by `init_project.py` with a first guess, rewrite it):
- `"title": ["line one", "line two"]`: the reel's hook as two short lines, up to about 26 characters each, sentence
  case. A style or layer that pins a headline uses it, and so do the ready styles as their fallback headline.
- `"swash": ["Line One", "Line Two"]`: the same idea, shorter (up to about 16 characters a line), Title Case.
Write what the reel promises, in the speaker's own words: "7 video effects" / "Claude made for me". Not a summary,
not clickbait they did not say.

## Where captions sit (worked out per clip, never typed in)

`PY "SK/scripts/layout.py" "<project>"` samples the reel, cuts the speaker out of just those frames, reads the head
off the silhouette and writes `layout.json`. Look at `work/layout/check.jpg` once (up to four frames, half size):
the green box has to run from the top of the head to the chin, and its numbers are printed under it. Blue lines are
the bands, red is the Reels safe zone. When the clean cutout is installed (`setup.py --matting`) the samples are cut
out with it, which takes about a minute and is not fooled by what hangs behind the head.

| Band | In `bands` | Rule | When there is no room |
|---|---|---|---|
| Above the head | `Y_ABOVE_HEAD` | 104px above the highest head position, never above y 236 | `null`: anything placed above the head goes over the chest |
| Behind the head | `HEAD_TOP` | a big word behind the head shows 72% of its height above it, shrinking to fit under y 226 | under 110px of type: the word lands over the chest, in front |
| Chest | `Y_CHEST` | y 1170, as long as the chin is at least 100px above it | the face is low or fills the frame: the picture is lifted (up to 260px, `lift`) and the captions take the collar band under the chin. `fits.chest` says `tight`: one-line styles only |
| Lower third | `Y_LOWER` | y 1376 (one line ends at 1452) | same lift |
| Open wall | `WALL_LEFT`, `WALL_RIGHT` | beside the speaker at face height, at least 240px wide | `null`: layers placed beside the speaker use the spots that exist |

Punch-ins move the head between segments: the bands are the ones that are safe in every segment, and words behind
the head read the head height of the segment each word falls in.

The quick cutout can be fooled: a framed picture, poster or lamp right behind the head joins the outline and the
box starts about 100px too high and stops at the nose. `layout.py` prints `CHECK THE HEAD BOX` when it could not
find a neck under the head (the usual sign, also normal with long hair or a hood), and `fx_new.py` / `fx_add.py`
print `CHECK layout.json` when an effect's own clean cutout disagrees with it by more than 60px. Either way: if
`check.jpg` shows the green box off the face (too high, a poster, a second person), run `setup.py --matting` once
and `layout.py` again, or correct `head` and `bands` in `layout.json` by hand. They are plain numbers in the
1080x1920 frame. The caption placement, words behind the head and the face box of the self-check all read them.

Styles that stack two or three lines (Duet, Gabinet, Notatnik, Elegancki) start about 70px above `Y_CHEST`. On a
`tight` chest band tell the buyer and keep that reel to one line ("lines": 1 in the plan's caption).
