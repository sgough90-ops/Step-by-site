"""L is for Loaf of bread (dx_loaf_l), Food and drink A to Z, slot L (22 Nov 2026).
From his pick "L2 Loaf with its end cut" (Claude's sketches, claude/step-by-draw-food-11-ideas-4-versions.md).

A long loaf seen from the front, with its cut end on the left and one slice lying in front. The L is the near
corner of the loaf: the straight edge between the cut end and the long side, and the first part of the bottom edge of
the long side (step 1 draws an L of a normal shape; step 2 carries its bottom line on: the step 1 rule in the README).

    python3 build_loaf.py
"""
import json, math, os
from fkit import *

BROWN, LBROWN = FILL['brown'], FILL['lbrown']
NX, BY, SH, LEN = 52.0, 76.0, 42.0, 36.0          # the corner of the L, how tall it is, how long the loaf is
TOPY = BY - SH


def shift(segs, dx, dy=0.0):
    out = []
    for s in segs:
        m = Seg.__new__(Seg); m.p = [P(x + dx, y + dy) for x, y in s.p]; out.append(m)
    return out


# the shape of the end of the loaf, from the top of the L, out and up over the top, and down the far side
prof = smooth([(NX, TOPY), (NX + 2, TOPY - 3.8), (NX + 1, TOPY - 11.65), (NX - 4, TOPY - 18.9), (NX - 10, TOPY - 23),
               (NX - 16, TOPY - 23.1), (NX - 21, TOPY - 19.35), (NX - 22, TOPY - 12.2), (NX - 20, TOPY - 7)])
near_r, near_l = prof[:4], prof[4:]                # up to the top of the loaf; from the top down the far side of the end
far_r = shift(near_r, LEN)
PEAK, FPEAK = near_r[-1].b, far_r[-1].b
END_TL, END_BL = near_l[-1].b, P(NX - 20, BY - 7)

net = Net()
FOOT = 24.0                                       # step 1's L: 42 tall with a foot 24 long (a normal L); step 2 carries the bottom line on
net.add('L', Seg((NX, TOPY), (NX, BY)), Seg((NX, BY), (NX + FOOT, BY)))                                     # 1: the L
net.add('side', Seg((NX + FOOT, BY), (NX + LEN - 4, BY)),                                                    # 2: the bottom line carried on, and the far end
        Seg((NX + LEN - 4, BY), (NX + LEN - 1.8, BY), (NX + LEN, BY - 1.8), (NX + LEN, BY - 4)),
        Seg((NX + LEN, BY - 4), (NX + LEN, TOPY)))
net.add('top', near_r, Seg(PEAK, FPEAK), rev(far_r))                                                         # 3: the crust
net.add('crust', Seg((NX, TOPY), (NX + 11, TOPY - 2.4), (NX + LEN - 11, TOPY - 2.4), (NX + LEN, TOPY)))
net.add('end', near_l, Seg(END_TL, END_BL), Seg(END_BL, (NX, BY)))                                           # 4: the cut end


def slice_ring(cx, cy, w, h, deg, s=1.0):
    """a slice of bread standing up, bottom middle at (cx, cy), leaning by deg; s shrinks it about its middle"""
    x0, x1, ys, top = -w / 2, w / 2, -0.6 * h, -h
    dome = [(x1, ys), (x1 + 0.08 * w, ys - 0.10 * h), (x1 + 0.02 * w, ys - 0.27 * h), (0.26 * w, top + 0.03 * h), (0, top),
            (-0.26 * w, top + 0.03 * h), (x0 - 0.02 * w, ys - 0.27 * h), (x0 - 0.08 * w, ys - 0.10 * h), (x0, ys)]
    a = math.radians(deg)

    def T(x, y):
        x, y = x * s, (y + h / 2) * s - h / 2
        return P(cx + x * math.cos(a) - y * math.sin(a), cy + x * math.sin(a) + y * math.cos(a))
    d = smooth([T(*q) for q in dome])
    bl, br = T(x0, 0), T(x1, 0)
    return [Seg(bl, br), Seg(br, d[0].a)] + d + [Seg(d[-1].b, bl)]


SL = slice_ring(26, 93.5, 21, 25, -10)
SL_IN = slice_ring(26, 93.5, 21, 25, -10, 0.78)
net.add('slice', SL)                                                                                         # 6: the slice
net.add('slice_in', SL_IN)
net.node()
net.hide('end', 'slice')                               # the slice lies in front of the corner of the cut end

marks = [Seg((x - 3, TOPY - 17), (x + 3.5, TOPY - 5)) for x in (NX + 7, NX + 18, NX + 29)]
dots = [dot(x, y, w=2.4) for x, y in [(NX - 8, TOPY + 2), (NX - 14, TOPY + 14), (NX - 7, TOPY + 22), (NX - 13, TOPY + 31), (NX - 9, TOPY - 9)]]

white = [d_fill(*net.all('slice_in'))]
steps = [
    step('Start with an L', 'Draw a capital L: a straight line down, then a shorter line along the bottom. This L is hiding in the loaf.', net.lines('L')),
    step('The far end', 'Make the bottom line a little longer. Then go round a little corner and draw a straight line up, as tall as the L.', net.lines('side')),
    step('The crust', 'From the top of the L, bulge out and go up over the top, straight along, and down to the other side. Join the two sides with a curved line.',
         net.lines('top', 'crust')),
    step('The cut end', 'From the top, curve down on the left, draw a straight line down, then a line back to the corner of the L.', net.lines('end')),
    step('Marks and holes', 'Draw three slanting marks on the crust. Add a few dots on the cut end, for the little holes in the bread.',
         [line(m) for m in marks] + dots),
    step('A slice', 'In front, draw a slice of bread: flat at the bottom, with a round top. Draw the same shape again, smaller, inside it.',
         net.lines('slice', 'slice_in')),
    step('Colour brown', 'Colour the crust on top of the loaf brown. Colour round the edge of the slice brown too.',
         [net.fill(BROWN, (NX + 18, TOPY - 12), names=['top', 'crust']), fill(BROWN, *net.all('slice'), cut=white)], use='brown'),
    step('Colour light brown', 'Colour the long side of the loaf light brown. Leave the cut end and the middle of the slice white.',
         [net.fill(LBROWN, (NX + 18, TOPY + 20), names=['L', 'side', 'crust'])], use='lbrown'),
]

D = drawing('dx_loaf_l', 'L is for Loaf of bread', 2, 10, 'things', ['Letters', 'Around the house'],
            'A loaf of bread with one slice cut. The capital L is hiding in it: it is the near corner of the loaf.',
            steps, ['brown', 'lbrown'])
save('loaf', D, {'set': 'house-AZ', 'slot': 'L', 'kind': 'key', 'age_from': 4})
json.dump(white, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out', 'loaf.white.json'), 'w'))
