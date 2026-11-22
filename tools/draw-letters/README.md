# Step by Draw letter drawings: the build tools

Not published (only `public/` is). These scripts write a letter drawing as code, check it and add it to the app page.

- `kit.py`: the drawing kit (lines, curves, colours, the stepby/1 format).
- `build_<name>.py`: one drawing each. Writes `out/<name>.json` (the drawing), `out/<name>.place.json` (set, slot, Make it move kind, age) and sometimes `out/<name>.white.json` (holes meant to stay white).
- `check.py out/<name>.json`: the line and colour checks (9 checks; every one must pass).
- `sheet.py out/<name>.json out/<name>-steps.png` draws the numbered step sheet; add `--pair` for lines beside the finished picture.
- `apply.py ../../public/draw/index.html name1 name2 ...`: adds built drawings to the app page (data and card, level, Make it move kind, set slot). Stops if a key or slot is already taken.
- `famkit.py`: extra helpers for the family drawings (16 Nov 2026): a peach pencil, circle and arm helpers, and a curve offset for wide ribbons.
- `reapply.py ../../public/draw/index.html name1 ...`: puts a rebuilt drawing back into the app page in place of the old one (same key).
- `carkit.py` and `build_racecars.py` (19 Nov 2026): the Vehicles 1 to 9 race cars (`car1` ... `car9`). The cars were sketched on a 200-wide page and `carkit.T` moves them onto the app's paper, so every car is the same size and sits on the same road. Live from 19 Nov 2026: 1, 2, 4, 5, 6, 7 and 9 (4 is for Jet car added at 09:3x). Its white stripe is a hole meant to stay white (`out/car4.white.json`), so the app checker lists it as a gap, like other drawings with white bits.
- `apptest.py ../../public <port> out/app/<prefix> key1 key2 ...`: opens the app in headless Chrome (phone and Chromebook size) and goes through every step of each drawing.
- `fkit.py` (22 Nov 2026): for drawings where shapes sit in front of each other (the nine Food and drink drawings: orange, broadbeans, loaf, tomatoes, pumpkin, jasminetea, quiche, raspberries, fruit). A `Net` holds named lines; `node()` cuts every line where it meets another and makes both share the very same point, `hide()` takes away the parts behind a shape in front, and `fill()` walks round the drawn lines that close in a point (like a paint bucket), so each colour edge is made of the very same pieces as the lines.
- `qcheck.py out/<name>.json`: the same 9 checks as `check.py`, much quicker on drawings with many lines (it skips pairs of lines that are far apart when looking for crossings).

To add a new drawing:

```
mkdir -p out/app
python3 build_<name>.py && python3 check.py out/<name>.json
python3 sheet.py out/<name>.json out/<name>-pair.png --pair
python3 apply.py ../../public/draw/index.html <name>
python3 apptest.py ../../public 8801 out/app/after <key>
```

Rules the drawings follow: the letter is drawn first and whole, as it is written, with a normal letter shape (not stretched wide, tall or flat: if the picture needs longer lines, step 1 draws the first part and a later step carries them on); nothing crosses it (lines may only touch it); every colour edge is on a drawn line; no colour goes over another colour; one pencil a step; all the line steps come before the colour steps.

Needs Python 3 with numpy, scipy, scikit-image and playwright, and Chrome at `/usr/bin/google-chrome`.

Step 1 fixes (18 Nov 2026): 16 live drawings had their step 1 cut so the letter looks natural, with the finished picture unchanged (see `step1fix.py`). If one of them is rebuilt from its build script (tap, toiletroll, electrictrain, num_swan, num_shark, num_pig), run `python3 step1fix.py out/<name>.json` before `apply.py` or `reapply.py`.
