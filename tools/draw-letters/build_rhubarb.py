"""r is for Rhubarb (dx_rhubarb_r), Food and drink a to z, slot r (22 Nov 2026).
From his pick "r1 A bunch tied with string" (Claude's sketches, claude/step-by-draw-food-small-11-ideas-4-versions.md).

Three sticks of rhubarb tied in a bunch with string and a bow, each with a big crinkly leaf at the top.
The r is the right edge of the right-hand stick (its line) and the middle of that stick's leaf (its arm).

    python3 build_rhubarb.py
"""
import math
from fkit import *

RED, GREEN, LBROWN = FILL['red'], FILL['green'], FILL['lbrown']
X, RT, RB = 60.0, 48.0, 92.0                      # the r's line: the right edge of the right-hand stick
ARM0, ARM1 = P(X, 54.5), P(79, 47.5)              # the r's arm: the middle of the leaf
SW = 8.0                                          # how wide a stick is
S1, S2 = 72.0, 76.5                               # the string, top and bottom
STICKS = {'A': (X - SW, RT, RB), 'B': (40.0, 30.0, 94.0), 'C': (29.0, 50.0, 90.0)}   # left edge, top, bottom


def crinkle(pts, k=0.9, closed=False):
    cx = sum(p[0] for p in pts) / len(pts); cy = sum(p[1] for p in pts) / len(pts)
    out = []; pairs = list(zip(pts, pts[1:] + pts[:1])) if closed else list(zip(pts, pts[1:]))
    for a, b in pairs:
        out.append(a); m = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
        out.append((cx + (m[0] - cx) * k, cy + (m[1] - cy) * k))
    if not closed: out.append(pts[-1])
    return out


def leaf_line(pts):
    pts = crinkle(pts); pts[0] = P(*pts[0]); pts[-1] = P(*pts[-1])
    return snap_end(smooth(pts), pts[-1])


net = Net()
net.add('r', Seg((X, RT), (X, RB)))                                                        # 1: the r
net.add('arm', Seg(ARM0, (X + 1, 49.5), (X + 7, 46.6), ARM1))
LA = [(X, RT), (57.5, 40), (60.5, 31.5), (70, 26.5), (82, 27.5), (91.5, 34), (95.5, 44.5), (93, 54.5), (84, 60.5), (72, 63), (64, 64), (X, 63)]
net.add('leafA', leaf_line(LA))                                                           # 2: the leaf
net.add('ribA', Seg(ARM1, (83, 46.2), (87.5, 46.6), (91, 47.4)))
veinsA = [((70, 45.9), (73.5, 37)), ((81, 45.4), (85.5, 35.5)), ((70, 49.2), (73, 59)), ((83, 48.2), (86, 56.5))]
net.add('str1', Seg((X, S1), (STICKS['C'][0] - 2, S1))); net.add('str2', Seg((X, S2), (STICKS['C'][0] - 2, S2)))   # 3: the string
XE = STICKS['C'][0] - 2
net.add('strE', Seg((XE, S1), (XE, S2)))
net.add('bowU', Seg((XE, S1 + 0.6), (XE - 3, S1 - 3.4), (XE - 8.5, S1 - 4.4), (XE - 8, S1 + 0.4)), Seg((XE - 8, S1 + 0.4), (XE - 7.6, S1 + 3.2), (XE - 3, S1 + 2.6), (XE, S1 + 1.6)))
net.add('bowD', Seg((XE, S2 - 1.2), (XE - 3, S2 + 0.2), (XE - 6.5, S2 + 4.6), (XE - 4.5, S2 + 6.4)), Seg((XE - 4.5, S2 + 6.4), (XE - 2.5, S2 + 8), (XE - 0.6, S2 + 3), (XE, S2 - 0.4)))
for k, (x0, top, bot) in STICKS.items():                                                  # 4-5: the sticks
    x1 = x0 + SW
    segs = [Seg((x0, bot), (x0, top)), Seg((x0, top), (x1, top))] + ([] if k == 'A' else [Seg((x1, top), (x1, bot))]) + [Seg((x1, bot), (x0, bot))]
    if k == 'A': segs = [Seg((x1, bot), (x0, bot)), Seg((x0, bot), (x0, top)), Seg((x0, top), (x1, top))]
    net.add('stick' + k, segs)
LB = [(40, 31), (41, 23), (35, 17), (25, 15.5), (16.5, 18.5), (11, 26), (11.5, 35), (18, 41), (28, 43.5), (36, 44), (40, 43)]
LC = [(29, 50), (26, 46.5), (17.5, 46.5), (9, 51), (6, 59), (10, 66), (18, 67.5), (25, 65.5), (29, 62)]
net.add('leafB', leaf_line(LB)); net.add('leafC', leaf_line(LC))                          # 6: the other leaves
net.region('string', poly((XE, S1), (X, S1), (X, S2), (XE, S2), closed=True))
net.node()
for k in STICKS: net.hide('stick' + k, 'string')
ribs = [line(Seg((39.2, 37), (33, 33), (25, 29), (18, 28.5))), line(Seg((28.2, 56), (22, 55.5), (16, 56.5), (11, 58.5)))]
veins = [line(Seg(a, b), w=1.2) for a, b in veinsA + [((31, 32.4), (30, 22)), ((23, 29.3), (20.5, 21)), ((30, 33.2), (31, 40)), ((22, 29.4), (21, 37)),
                                                        ((21, 55.5), (19, 49.5)), ((16, 56.5), (13.5, 51.5)), ((20, 55.8), (20.5, 63)), ((14.5, 57.2), (14, 63.5))]]
shine = [line(Seg((x0 + 3, a), (x0 + 3, b)), w=1.2) for x0, a, b in ((STICKS['A'][0], 53, 69), (STICKS['A'][0], 80, 88), (40, 36, 69), (40, 80, 90), (29, 55, 69), (29, 80, 87))]
ALL = ['r', 'arm', 'leafA', 'ribA', 'str1', 'str2', 'strE', 'bowU', 'bowD', 'stickA', 'stickB', 'stickC', 'leafB', 'leafC']

steps = [
    step('Start with an r', 'Draw a small letter r: a line down, then a short curved arm at the top. This r is hiding in the rhubarb.', net.lines('r', 'arm')),
    step('The leaf', 'Round the arm of the r, draw a big crinkly leaf. Carry the arm on to the middle of the leaf, and add some little lines.',
         net.lines('leafA', 'ribA') + [line(Seg(a, b), w=1.2) for a, b in veinsA]),
    step('The string', 'Draw two lines going left from the r, for the string. Close the end and add a bow.', net.lines('str1', 'str2', 'strE', 'bowU', 'bowD')),
    step('The stick', 'Next to the r, draw a stick of rhubarb: across the top, down the side and across the bottom. Stop at the string.', net.lines('stickA')),
    step('Two more sticks', 'Draw two more sticks of rhubarb on the left: a tall one and a short one.', net.lines('stickB', 'stickC')),
    step('More leaves', 'Draw a crinkly leaf at the top of each new stick, with a line down its middle.', net.lines('leafB', 'leafC') + ribs),
    step('Shine', 'Draw a thin line down each stick, and some little lines on the leaves.', shine + veins[4:]),
    step('Colour red', 'Colour the sticks of rhubarb red, above and below the string.',
         [net.fill(RED, (x0 + 1.4, y), names=ALL) for x0, top, bot in STICKS.values() for y in ((top + S1) / 2 + 1, (S2 + bot) / 2)], use='red'),
    step('Colour green', 'Colour the leaves green.',
         [net.fill(GREEN, (76, 34), names=ALL), net.fill(GREEN, (26, 36), names=ALL), net.fill(GREEN, (14, 60), names=ALL)], use='green'),
    step('Colour the string', 'Colour the string and the bow light brown.',
         [net.fill(LBROWN, (44, (S1 + S2) / 2), names=ALL), net.fill(LBROWN, (XE - 6, S1 - 1), names=ALL), net.fill(LBROWN, (XE - 3.4, S2 + 4.4), names=ALL)], use='lbrown'),
]

D = drawing('dx_rhubarb_r', 'r is for Rhubarb', 2, 12, 'things', ['Letters', 'Around the house'],
            'A bunch of rhubarb tied with string. The small letter r is hiding in it: the edge of a stick and the middle of its leaf.',
            steps, ['red', 'green', 'lbrown'])
save('rhubarb', D, {'set': 'house-az', 'slot': 'r', 'kind': 'key', 'age_from': 4})
