"""h is for Hot cross bun (dx_hotcrossbun_h), Food and drink a to z, slot h (22 Nov 2026).
From his pick "h3 With a carton of milk", changed at his ask to a glass of milk.

A hot cross bun on the table next to a tall glass of milk. The h is the right side of the glass (its tall line) and
the round top and side of the bun (its hump).

    python3 build_hotcrossbun.py
"""
import math
from fkit import *

BROWN, LBLUE = FILL['brown'], FILL['lblue']
X, GTOP, BASE = 40.0, 31.0, 86.0                 # the h's tall line (the glass's right side), its top, the table
X1, BTOP, BRY = 84.0, 46.0, 18.0                 # the bun: its right side, its top, how tall its round top is
XM, BRX = (X + X1) / 2, (X1 - X) / 2
SH = BTOP + BRY
GL = 14.0                                        # the glass's left side
CW = 3.2                                         # half the width of the cross
YA = 66.0                                        # the cross line across the bun, at its ends

net = Net()
net.add('stem', Seg((X, GTOP), (X, BASE)))                                                    # 1: the h
HUMP = [Seg((X, SH - 1), (X + 4, BTOP + 6.5), (X + 11, BTOP), (XM, BTOP))] + arc(XM, SH, BRX, BRY, 270, 360, start=P(XM, BTOP), end=P(X1, SH)) + [Seg((X1, SH), (X1, BASE))]
net.add('hump', HUMP)
net.add('glass', Seg((X, GTOP), (GL, GTOP)), Seg((GL, GTOP), (GL, BASE)))                     # 2: the glass
milk = smooth([(GL, 40.6), (18, 39.2), (23, 41.2), (28, 39.2), (33, 41.2), (36.6, 39.8), (X, 40.6)])
net.add('milk', milk)                                                                         # 3: the milk and the thick bottom
net.add('gbase', Seg((GL, 81.0), (X, 81.0)))
net.add('table', Seg((12, BASE), (88, BASE)))                                                  # 4: the table
q = lambda y0, dip: [Seg((X, y0), (X + BRX * 2 / 3, y0 - dip * 2 / 3), (X1 - BRX * 2 / 3, y0 - dip * 2 / 3), (X1, y0))]
net.add('htop', q(YA, 9)); net.add('hbot', q(YA + 6, 9))                                     # 5: the cross
net.add('vL', Seg((XM - CW, BTOP - 1), (XM - CW, BASE))); net.add('vR', Seg((XM + CW, BTOP - 1), (XM + CW, BASE)))
net.region('bun', HUMP, Seg((X1, BASE), (X, BASE)), Seg((X, BASE), (X, SH - 1)))
net.region('vband', poly((XM - CW, 40), (XM + CW, 40), (XM + CW, 90), (XM - CW, 90), closed=True))
net.region('hband', q(YA, 9), Seg((X1, YA), (X1, YA + 6)), rev(q(YA + 6, 9)), Seg((X, YA + 6), (X, YA)))
net.node()
for nm in ('vL', 'vR'): net.keep_in(nm, 'bun'); net.hide(nm, 'hband')
for nm in ('htop', 'hbot'): net.hide(nm, 'vband')
CROSS = ['htop', 'hbot', 'vL', 'vR']
cur = [dot(x, y, w=2.6) for x, y in ((47, 81), (52, 56), (71, 54.5), (78, 79), (52, 78), (72.5, 82.5), (79, 61))]
shine = line(Seg((19, 47), (19, 70)))

steps = [
    step('Start with an h', 'Draw a small letter h: a tall line down, then a round hump on the right.', net.lines('stem', 'hump')),
    step('The glass', 'The tall line of the h is the side of a glass. Draw a line across its top, then a line down for the other side.', net.lines('glass')),
    step('The milk', 'Draw a wavy line near the top of the glass for the milk. Draw a line across near the bottom.', net.lines('milk', 'gbase')),
    step('The table', 'Draw a long line across the bottom, under the glass and the bun.', net.lines('table')),
    step('The cross', 'The hump of the h is a bun. Draw a cross on it with two lines going down and two curved lines across.', net.lines(*CROSS)),
    step('Currants', 'Draw some dots on the bun for the currants. Draw a line on the glass to make it shine.', cur + [shine]),
    step('Colour brown', 'Colour the bun brown, all round the white cross.',
         [net.fill(BROWN, s, names=['stem', 'hump', 'table'] + CROSS) for s in ((50, 57), (73, 57), (49, 81.5), (75, 81.5))], use='brown'),
    step('Colour light blue', 'Colour the top of the glass, above the milk, light blue. Colour the thick bottom of the glass too.',
         [net.fill(LBLUE, (27, 35), names=['stem', 'glass', 'milk']), net.fill(LBLUE, (27, 83.5), names=['stem', 'glass', 'gbase', 'table'])], use='lblue'),
]

D0 = drawing('dx_hotcrossbun_h', 'h is for Hot cross bun', 2, 10, 'things', ['Letters', 'Around the house'],
            'A hot cross bun next to a glass of milk. The small letter h is hiding in it: the side of the glass and the top of the bun.',
            steps, ['brown', 'lblue'])
D = scale(D0, 1.25, 50.0, 90.0)                     # the whole picture a bit bigger, to fill the paper
save('hotcrossbun', D, {'set': 'house-az', 'slot': 'h', 'kind': 'key', 'age_from': 4})
