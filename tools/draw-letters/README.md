# Step by Draw letter drawings: the build tools

Not published (only `public/` is). These scripts write a letter drawing as code, check it and add it to the app page.

- `kit.py`: the drawing kit (lines, curves, colours, the stepby/1 format).
- `build_<name>.py`: one drawing each. Writes `out/<name>.json` (the drawing), `out/<name>.place.json` (set, slot, Make it move kind, age) and sometimes `out/<name>.white.json` (holes meant to stay white).
- `check.py out/<name>.json`: the line and colour checks (9 checks; every one must pass).
- `sheet.py out/<name>.json out/<name>-steps.png` draws the numbered step sheet; add `--pair` for lines beside the finished picture.
- `apply.py ../../public/draw/index.html name1 name2 ...`: adds built drawings to the app page (data and card, level, Make it move kind, set slot). Stops if a key or slot is already taken.
- `famkit.py`: extra helpers for the family drawings (16 Nov 2026): a peach pencil, circle and arm helpers, and a curve offset for wide ribbons.
- `reapply.py ../../public/draw/index.html name1 ...`: puts a rebuilt drawing back into the app page in place of the old one (same key).
- `apptest.py ../../public <port> out/app/<prefix> key1 key2 ...`: opens the app in headless Chrome (phone and Chromebook size) and goes through every step of each drawing.

To add a new drawing:

```
mkdir -p out/app
python3 build_<name>.py && python3 check.py out/<name>.json
python3 sheet.py out/<name>.json out/<name>-pair.png --pair
python3 apply.py ../../public/draw/index.html <name>
python3 apptest.py ../../public 8801 out/app/after <key>
```

Rules the drawings follow: the letter is drawn first and whole, as it is written; nothing crosses it (lines may only touch it); every colour edge is on a drawn line; no colour goes over another colour; one pencil a step; all the line steps come before the colour steps.

Needs Python 3 with numpy, scipy, scikit-image and playwright, and Chrome at `/usr/bin/google-chrome`.
