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
- `vkit.py` (22 Nov 2026): a painter's layer over `fkit`, for the five Vehicles capitals built from Claude's sketches (oiltanker, ketch, nuclearsub, yacht, vikingboat). A `Pic` takes its parts back to front: `shape()` is a closed part that hides the lines of everything behind it, `stroke()` is a line that hides nothing (`deco=True` for a line that is only decoration), `region()` hides without drawing. `build()` cuts and trims; `step(k)` gives a step's lines; `ring()` colours a whole part and `face()` colours the space round a point, with `holes` for parts that sit inside the colour. The drawing is written in its sketch's numbers and the `Pic` moves and scales it onto the paper in one place. Two parts that share a wall must not both draw it: give one of them a `region()` and separate `stroke()` sides (see the top box of the oil tanker's cabin).
- `sheet_phone.py out/<name>.json out/<name>-phone.png`: a tall step sheet that reads well on a phone (the letter in red and the finished picture on top, then every step, two across).
- `bcommon.py` (23 Nov 2026): the few things the seven small-letter Vehicles builds share (excavator, narrowboat, rocket, unicycle, van, xebec, ziplinecar): a cloud, a star, a wavy line, and `finish()`, which saves the drawing, runs the 9 checks and draws a quick look (`out/<name>-look.png`). These seven are written with `vkit` from Claude's sketches. `build_van.py yellow` makes the van with a yellow top instead of a white one (`out/van-yellow.json`, not in the app). The rocket's step 1 draws only the top part of its straight side, so the r has a normal shape; step 2 carries that line on down.
- Seven small-letter Food and drink builds (23 Nov 2026), written with `vkit` from Claude's sketches: blueberry, icedtea, kale, onion, quinoa, sushi, teapot. In the iced tea, step 2 is only the short line that joins the i's dot to its line (his ask); the dot ends up as the straw's top corner. The kale's tall line is drawn to the bottom of the leaf in step 1 and carried on as the stalk in step 3; all its leaf lines are pencil. The sushi's s is two strokes (the left edge of the top roll, then the right edge of the roll under it); the rolls stay white, so the board's colour has two holes meant to stay white (`out/sushi.white.json`) and the app checker lists them as gaps. Two things the app's own checker tests that `check.py` does not: no more than 14 new lines in a step (so the quinoa has 14 dots and the sushi 10 seeds), and every number in a path on the paper, a curve's guide points included (the teapot's handle).
- `look.py build_<name>.py`: a quick look at a build without the checks (writes the drawing and `out/<name>-look.png`). The kale's checks take about four minutes.
- Nine more from Claude's sketches (23 Nov 2026), written with `vkit` and `bcommon.finish()`: the Food and drink capitals avocado (A), drumstick (D), hotdog (H), kingprawn (K), nachos (N) and salad (S), and the small-letter Vehicles golfcart (g), mailvan (m) and offroader (o). The golf cart's headlight (the round of the g) is a nearly full circle that meets the front edge at two points: a full circle that only touches the stick fails "no line runs along another". The mail van's m is 38 wide and 21 tall (he asked for it to be less tall than in the sketch). The off-roader is written level and facing right, and its `F()` turns it to face left with its nose up.

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
