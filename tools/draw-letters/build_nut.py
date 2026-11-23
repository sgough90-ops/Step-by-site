"""n is for Nut (dx_nut_n), Food and drink a to z, slot n (23 Nov 2026).
From his pick, "acorn shape" number 1 "Narrow acorn" (Claude's sketches,
claude/step-by-draw-nuts-acorn-waffle-round3-sketches.py). His words for that round, with a photo of an acorn hanging by its
cap: "more like this shape but make it narrow, happy with your existing colours".

A long narrow nut hanging from a branch by a short stalk, in a green cap, with a leaf on each side.
The n is the cap: up its left side, over the top in a round arch and down its right side (28 wide, 29 tall).
Different from the sketch: the branch sits lower, so nothing is under the step number, and it stops short of the edges of
the paper; the nut is a little shorter to make room. The cap and the leaves are the same green (the app has one green).
The app calls it a nut, not an acorn, because it is in the food set and people do not eat acorns.

    python3 build_nut.py
"""
from bcommon import *

p = Pic(s=1.0, dx=0.0, dy=0.0)
CX, RX = 50, 14                                                # the middle of the n, half its width
X0, X1 = CX - RX, CX + RX
APEX, RIM, BOT, BR = 29, 58, 96, 20.5                          # the top of the n, its feet, the tip of the nut, the middle of the branch
TOP = APEX + RX                                                # where the arch of the n starts
BRIM = 2.2                                                     # how far the cap sticks out past the nut on each side
L = BOT - RIM

N = [Seg((X0, RIM), (X0, TOP))] + arc(CX, TOP, RX, RX, 180, 360, start=P(X0, TOP), end=P(X1, TOP)) + [Seg((X1, TOP), (X1, RIM))]
EDGE = one("M%s,%s Q%s,%s %s,%s" % (X1, RIM, CX, RIM + 3.4, X0, RIM))                # the cap's bottom edge, right to left
A, B = X0 + BRIM, X1 - BRIM
NUT = one("M%s,%s C%s,%s %s,%s %s,%s L%s,%s L%s,%s C%s,%s %s,%s %s,%s Z" % (
    A, RIM - 2, A - 0.3, RIM + L * 0.58, CX - RX * 0.8, RIM + L * 0.93, CX - 1.6, BOT - 2.4, CX, BOT, CX + 1.6, BOT - 2.4,
    CX + RX * 0.8, RIM + L * 0.93, B + 0.3, RIM + L * 0.58, B, RIM - 2))
TOPS = [(6, BR - 2.2), (27, BR - 4.2), (50, BR - 2.2), (73, BR - 4.7), (94, BR - 2.2)]
BT, BB = smooth(TOPS), smooth([(x, y + 4.4) for x, y in reversed(TOPS)])       # the branch's top edge, then its bottom edge back again
BRANCH = (BT + arc(94, BR, 2.2, 2.2, -90, 90, start=BT[-1].b, end=BB[0].a) + BB + arc(6, BR, 2.2, 2.2, 90, 270, start=BB[-1].b, end=BT[0].a))   # round ends
LEAVES = (((31, BR - 1), (12, BR + 13.5)), ((71, BR - 2), (90, BR + 11.5)))


def at(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


for i, (base, tip) in enumerate(LEAVES):
    p.shape('leaf%d' % i, leaf2(base, tip, 10), step=5)
    p.stroke('vein%d' % i, Seg(at(base, tip, 0.3), at(base, tip, 0.82)), step=5, deco=True)
p.shape('stalk', box(CX - 2.1, BR, CX + 2.1, APEX + 3), step=4)
p.shape('branch', BRANCH, step=4)
p.shape('nut', NUT, step=3)
p.region('capR', N, EDGE)
p.stroke('edge', EDGE, step=2)
for i, (dx, y0) in enumerate(((-RX * 0.5, APEX + RX * 0.42), (0, APEX + 3.6), (RX * 0.5, APEX + RX * 0.42))):
    p.stroke('rib%d' % i, Seg((CX + dx, y0), (CX + dx * 1.12, RIM - 3)), step=2, deco=True)
p.stroke('n', N, step=1)
p.build()

steps = [
    step('Start with an n', 'Draw a small letter n: a short line up, over in a round arch and straight down the other side.', p.step(1)),
    step('The cap', 'Join the two feet of the n with a line that dips a little in the middle. Draw three lines down the inside of the cap.', p.step(2)),
    step('The nut', 'Under the cap draw a long nut: down one side, round to a little point at the bottom, and back up the other side.', p.step(3)),
    step('The branch', 'Draw a short stalk up from the top of the n: two lines close together. Across the top of it draw a long wavy branch with round ends.', p.step(4)),
    step('Two leaves', 'Draw a pointed leaf hanging down from each side of the branch. Draw a line down the middle of each leaf.', p.step(5)),
    step('Colour green', 'Colour the cap green. Colour the two leaves green too.',
         [p.face('green', (CX + 3.5, RIM - 6)), p.face('green', at(*LEAVES[0], 0.6)[0:1] + (at(*LEAVES[0], 0.6)[1] + 1.6,)),
          p.face('green', at(*LEAVES[1], 0.6)[0:1] + (at(*LEAVES[1], 0.6)[1] + 1.6,))], use='green'),
    step('Colour brown', 'Colour the nut brown. Colour the branch and the little stalk brown too.',
         [p.face('brown', (CX, RIM + L * 0.55)), p.ring('brown', 'branch'), p.face('brown', (CX, (BR + 2.2 + APEX) / 2 + 0.4))], use='brown'),
]
D = drawing('dx_nut_n', 'n is for Nut', 2, 10, 'things', ['Letters', 'Around the house'],
            'A nut hanging from a branch in its green cap. The small letter n is hiding in the cap: up one side, over the top and down the other.',
            steps, ['green', 'brown'])
ok = finish('nut', D, {'set': 'house-az', 'slot': 'n', 'kind': 'key', 'age_from': 4}, p)
