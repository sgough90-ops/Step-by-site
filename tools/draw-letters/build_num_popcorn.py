"""7 is for Popcorn (dx_popcorn_7), Food and drink 1 to 9, slot 7 (23 Nov 2026).
From his pick "7: 4 Popcorn" (claude/step-by-draw-food-numbers-1-to-9-36-sketches.md).

A pointed paper cone of popcorn with red stripes. The 7 is the top edge of the cone and its right-hand side.
Written in the sketch's numbers.

    python3 build_num_popcorn.py
"""
from ncommon import *

p = Pic(s=0.96, dx=2.0, dy=3.6)
TL, TR, TIP = (26, 35), (74, 35), (50, 95)
RIM = [TL[0] + (TR[0] - TL[0]) * i / 5 for i in range(6)]            # where the stripes meet the top edge

# ---- the popcorn: a row of round bumps from one end of the top edge, over, to the other end ----
B = [TL, (22.5, 25.5), (28.5, 16), (39, 9.5), (51, 7.5), (62.5, 10.5), (72, 17.5), (77, 26.5), TR]
p.stroke('pop', [bump(a, b, 0.62) for a, b in zip(B, B[1:])], step=3)
for i, (x, y, r, a0, a1) in enumerate(((35, 24, 3.4, 150, 330), (47.5, 18, 3.6, 170, 350), (60, 22, 3.4, 200, 380), (67.5, 30, 2.8, 180, 360), (43, 30, 2.8, 20, 200), (30.5, 31, 2.2, 190, 350))):
    p.stroke('curl%d' % i, arc(x, y, r, r, a0, a1), step=4, deco=True)

# ---- the cone: its left side and four stripe lines down to the point ----
p.stroke('side_l', Seg(TL, TIP), step=2)
for i in range(1, 5):
    p.stroke('stripe%d' % i, Seg((RIM[i], TL[1]), TIP), step=5)

# ---- the 7, in front of everything ----
p.stroke('seven', poly(TL, TR, TIP), step=1)
p.build()

mid = lambda i: ((RIM[i] + RIM[i + 1]) / 2 + (50 - (RIM[i] + RIM[i + 1]) / 2) / 6, 45)      # a point inside stripe i
steps = [
    step('Start with a 7', 'Draw a big number 7: a straight line across the top, then a long slanted line down to the left. This 7 is hiding in the popcorn.', p.step(1)),
    step('The cone', 'From the left end of the top line, draw a slanted line down to the bottom of the 7. Now you have a pointed cone.', p.step(2)),
    step('Popcorn', 'Draw fluffy popcorn on top: a row of round bumps going up from one end of the top line, over, and down to the other end.', p.step(3)),
    step('More popcorn', 'Draw a few little curved lines inside the popcorn.', p.step(4)),
    step('Stripes', 'Draw four lines from the top of the cone down to its point, to make five stripes.', p.step(5)),
    step('Colour red', 'Colour three stripes red: the two outside ones and the middle one. The other two stay white.', [p.face('red', mid(i)) for i in (0, 2, 4)], use='red'),
    step('Colour yellow', 'Colour the popcorn yellow.', [p.face('yellow', (50, 26))], use='yellow'),
]
D = drawing('dx_popcorn_7', '7 is for Popcorn', 1, 8, 'things', TAGS,
            'A stripy paper cone full of popcorn. The number 7 is hiding in it: the top edge of the cone and its right side.',
            steps, ['red', 'yellow'])
ok = finish('num7popcorn', D, {'set': SET, 'slot': '7', 'kind': 'key', 'age_from': 4}, p)
