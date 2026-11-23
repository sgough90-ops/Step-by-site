"""2 is for Toast (dx_toast_2), Food and drink 1 to 9, slot 2 (23 Nov 2026).
From his pick "2: 1 Toast" (claude/step-by-draw-food-numbers-1-to-9-36-sketches.md).

A slice of toast and jam, cut in two from corner to corner. The 2 is the round top of the slice, the cut, and the
bottom crust. The jam is drawn in two parts, one each side of the cut, so no line crosses the 2. The little shoulder on
the right is steep, so it leaves the top of the cut cleanly and the side never crosses the cut.
Written in the sketch's numbers.

    python3 build_num_toast.py
"""
from ncommon import *

p = Pic(s=1.0, dx=0.0, dy=1.0)
CX, CY, R, XL, XR, BOT, SH = 50, 40, 30, 22.5, 77.5, 88, 45
on_cut = lambda t: (80 + (XL - 80) * t, CY + (BOT - CY) * t)        # a point on the cut (the slanted line of the 2)
A, B = on_cut(0.2), on_cut(0.8)                                     # where the jam meets the cut

# ---- the sides of the slice: a little shoulder in, then straight down ----
p.stroke('side_l', poly((20, 40), (XL, SH), (XL, BOT)), step=2)
p.stroke('side_r', poly((80, 40), (XR, SH), (XR, BOT)), step=2)

# ---- the jam: one part each side of the cut ----
p.stroke('jam_a', smooth([B, (31.5, 68), (34.5, 54), (33.5, 41), (37, 28.5), (50, 22.5), (63, 27), (68.5, 39), A]), step=3)
p.stroke('jam_b', smooth([A, (66, 58), (68.5, 69), (61.5, 78.5), (49, 75.5), (41, 80.5), B]), step=3)

# ---- the 2, in front of everything: round top, the cut, the bottom ----
p.stroke('two', arc(CX, CY, R, R, 180, 360, start=P(20, 40), end=P(80, 40)), Seg((80, 40), (XL, BOT)), Seg((XL, BOT), (XR, BOT)), step=1)
p.build()

crumbs = [pdot(p, 12.5, 81), pdot(p, 87.5, 73), pdot(p, 90, 85, 2.2), pdot(p, 10, 68, 2.2)]
steps = [
    step('Start with a 2', 'Draw a big number 2: a round top, a straight slanted line down to the left, and a straight line along the bottom.', p.step(1)),
    step('The sides', 'From each end of the round top draw a tiny line sloping in. Then draw a straight line down each side to the bottom.', p.step(2)),
    step('The jam', 'Draw a wobbly blob of jam in the middle. Draw it in two parts, one each side of the slanted line.', p.step(3)),
    step('Crumbs', 'Draw a few little dots beside the toast for crumbs.', crumbs),
    step('Colour red', 'Colour the jam red, on both sides of the slanted line.', [p.face('red', (50, 40)), p.face('red', (58, 68))], use='red'),
    step('Colour light brown', 'Colour the toast light brown, all round the jam.', [p.face('lbrown', (27, 50)), p.face('lbrown', (73, 75))], use='lbrown'),
]
D = drawing('dx_toast_2', '2 is for Toast', 1, 8, 'things', TAGS,
            'A slice of toast and jam, cut in two. The number 2 is hiding in it: the round top, the cut and the bottom crust.',
            steps, ['red', 'lbrown'])
ok = finish('num2toast', D, {'set': SET, 'slot': '2', 'kind': 'key', 'age_from': 4}, p)
