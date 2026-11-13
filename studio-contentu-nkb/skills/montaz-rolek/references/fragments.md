# The fragment picker (before the cut)

The buyer decides what goes into the reel before anything is cut. After `ingest.py`, open the picker:

```
PY "SK/scripts/fragments.py" "<project>" --until-saved      IN THE BACKGROUND
```

## It is a gate

`assemble.py` stops with `STOP fragments MISSING` when there is no `fragments.json`, and with `STOP fragments STALE`
when `transcript.txt` is newer (the clips were ingested again). Go back to the picker. Never work around the stop.

The picker is skipped too often for reasons that do not count. None of these skips it:
- `ingest.py` already ran in an earlier turn (an analysis of the content, a b-roll concept, another chat).
- One clip, one take, nothing said twice. She still drops lines and changes their order on the page.
- A concept or b-roll plan was agreed, or she wrote "użyj koncepcji i zmontuj", "działaj", "edytuj".
- The reel is long, or you are sure which lines are best.

Only two things skip it, and both are recorded:
```
PY "SK/scripts/fragments.py" "<project>" --auto buyer        she said "wybierz sam" / "nie chcę wybierać" in this edit
PY "SK/scripts/fragments.py" "<project>" --auto no-browser   the page cannot open on this computer
```
Both write `fragments.json` with `"by": "claude"` and the pre-ticked lines, and you pick the takes as
`references/cutting.md` says. A reel cut before the picker existed (it has `segments.json` but no `fragments.json`)
goes on in a notes round without it.

- The page lists every line of every clip with its time (minutes:seconds), a play button that plays just that line,
  and a badge "ujęcie 2 z 3" on lines she said more than once.
- Pre-ticked: the last complete take of every repeated line, and every single line of three words or more said only
  once. Never pre-ticked: one or two word lines (fillers, "jeszcze raz", "dobra").
- She can change ticks, reorder the reel in the side panel and write a note to the edit. Save writes
  `<project>/fragments.json` and prints `STATUS fragments SAVED ... picked=<n> of <total>`, plus a `NOTE` line with
  her note when she wrote one. Treat that note like any other instruction from her.

Tell her once, in her language: "W przeglądarce otworzyła się strona z Twoją transkrypcją. Zaznacz fragmenty, które
mają wejść do rolki, i kliknij Zapisz." Then wait for the SAVED line. Do not start edl.json before it.

## From fragments.json to edl.json

- One EDL segment per picked line, in the order of `picked` (her order, not the clips' order).
- `in` / `out` in fragments.json are word edges. Trim them as `references/cutting.md` says (start about 0.05 to
  0.07 s before the first word, end at the silence after the last word). Two picked lines that follow each other in
  the same clip with a short pause between them may stay one segment.
- Her ticks win over your own judgement of the best take. If a ticked line has a clear flaw (a cough, a word cut
  off, the take breaks off), keep it, and say in one line what you noticed and which other take would fix it.
- She ticked nothing new and saved the defaults: that is a yes to the pre-ticked takes.
- `assemble.py` prints a `NOTE` for every segment that is not one of her ticked lines. Fix `edl.json`, unless she
  asked for that line in chat.
- A notes round that changes takes ("weź jednak pierwsze ujęcie hooka") does not need the picker again: edit
  edl.json directly. She asks to see the list again: run the picker again; it starts from the default ticks.

Nothing leaves the computer: the page is served on 127.0.0.1 only and plays the clips' own audio from `work/`.
