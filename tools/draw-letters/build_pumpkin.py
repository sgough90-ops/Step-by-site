"""P is for Pumpkin (dx_pumpkin_p), Food and drink A to Z, slot P (22 Nov 2026).
From his pick "Pumpkin 2: leaf on the stalk" (Claude's round 2 sketches, claude/step-by-draw-food-11-ideas-4-versions.md).

A big pumpkin with a green stalk, and one round leaf sitting across the stalk. The P is the right edge of the stalk
(its stick) and the right half of the leaf (its bump).

    python3 build_pumpkin.py
"""
import math
from fkit import *

GREEN, ORANGE = FILL['green'], FILL['orange']
CX, CY, HW, HH = 50.0, 66.5, 41.0, 28.0            # the pumpkin: middle, half its width, half its height
X1, WD, FL = 52.8, 5.6, 2.8                        # the right edge of the stalk (the P's stick), how thick it is, its foot
X0 = X1 - WD
TOPY, MIDY, BW = 9.0, 27.5, 16.5                   # the top of the P, the bottom of its bump, how far the bump sticks out
BASE = CY - 0.86 * HH + 0.8                        # the bottom of the P's stick, just inside the dip in the top of the pumpkin

PUM = [(0, -0.86), (0.26, -1.0), (0.58, -0.9), (0.86, -0.56), (1.0, 0), (0.9, 0.56), (0.6, 0.9), (0.26, 1.0), (0, 0.96),
       (-0.26, 1.0), (-0.6, 0.9), (-0.9, 0.56), (-1.0, 0), (-0.86, -0.56), (-0.58, -0.9), (-0.26, -1.0)]

net = Net()
net.add('stem', Seg((X1, TOPY), (X1, BASE)))                                        # 1: the P
net.add('bowl', half_leaf(X1, TOPY, MIDY, BW, 1))
net.add('stalk', Seg((X1, BASE), (X1 - 2, BASE + 1.6), (X0 - FL + 1, BASE + 1.8), (X0 - FL, BASE + 0.6)),      # 2: the rest of the stalk
        Seg((X0 - FL, BASE + 0.6), (X0 - 0.4, BASE - 2.5), (X0, BASE - 6), (X0, BASE - 9)),
        Seg((X0, BASE - 9), (X0, TOPY)), Seg((X0, TOPY), (X1, TOPY)))
net.add('leafL', half_leaf(X0, TOPY, MIDY, BW, -1))                                 # 3: the other half of the leaf
net.region('stalkR', net.all('stem'), net.all('stalk'))
net.add('pump', smooth([(CX + x * HW, CY + y * HH) for x, y in PUM], closed=True))  # 4: the pumpkin
# 5: the curved lines down the pumpkin (drawn a little too long, then trimmed at the edge of the pumpkin and the stalk)
for k, sx in enumerate((1, -1)):
    net.add('ribA%d' % k, Seg((CX + sx * 0.05 * 2 * HW, CY - 0.92 * HH), (CX + sx * 0.48 * HW, CY - 0.6 * HH), (CX + sx * 0.48 * HW, CY + 0.68 * HH), (CX + sx * 0.16 * HW, CY + 1.04 * HH)))
    net.add('ribB%d' % k, Seg((CX + sx * 0.42 * HW, CY - 1.04 * HH), (CX + sx * 0.9 * HW, CY - 0.6 * HH), (CX + sx * 0.88 * HW, CY + 0.64 * HH), (CX + sx * 0.52 * HW, CY + 1.0 * HH)))
net.node()
net.hide('pump', 'stalkR')
RIBS = ['ribA0', 'ribB0', 'ribA1', 'ribB1']
for r in RIBS:
    net.hide(r, 'stalkR'); net.keep_in(r, 'pump')


def veins(x, sg):
    out = []
    for t in (0.36, 0.62):
        y = TOPY + (MIDY - TOPY) * t
        out.append(line(Seg((x + sg * 2.2, y), (x + sg * BW * 0.62, y - (MIDY - TOPY) * 0.17))))
    return out


steps = [
    step('Start with a P', 'Draw a capital P: a straight line down, with a round bump at the top. This P is hiding in the pumpkin.',
         net.lines('stem', 'bowl')),
    step('The stalk', 'Make the line of the P thick. Go across its top, down its left side, and curve out into a little foot at the bottom.',
         net.lines('stalk')),
    step('The leaf', 'Draw a round bump on the left of the stalk, the same as the bump of the P. Now it is a leaf. Add two little lines on each side.',
         net.lines('leafL') + veins(X0, -1) + veins(X1, 1)),
    step('The pumpkin', 'Start at the bottom of the stalk. Draw a big, wide, round pumpkin, all the way round to the other side of the stalk.',
         net.lines('pump')),
    step('The lines', 'Draw four curved lines down the pumpkin, from the top to the bottom: two on each side.', net.lines(*RIBS)),
    step('Colour green', 'Colour the stalk and both halves of the leaf green.',
         [net.fill(GREEN, ((X0 + X1) / 2, (MIDY + BASE) / 2), names=['stem', 'stalk']),
          net.fill(GREEN, (X0 - BW / 2, (TOPY + MIDY) / 2), names=['stalk', 'leafL']),
          net.fill(GREEN, (X1 + BW / 2, (TOPY + MIDY) / 2), names=['stem', 'bowl'])], use='green'),
    step('Colour orange', 'Colour the pumpkin orange.', [net.fill(ORANGE, (CX, CY + 6), names=['pump', 'stem', 'stalk'])], use='orange'),
]

D = drawing('dx_pumpkin_p', 'P is for Pumpkin', 2, 10, 'things', ['Letters', 'Around the house'],
            'A big orange pumpkin with a leaf on its stalk. The capital P is hiding in it: the stalk is its stick and half of the leaf is its bump.',
            steps, ['green', 'orange'])
save('pumpkin', D, {'set': 'house-AZ', 'slot': 'P', 'kind': 'key', 'age_from': 4})
