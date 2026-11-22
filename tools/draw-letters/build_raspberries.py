"""R is for Raspberries (dx_raspberries_r), Food and drink A to Z, slot R (22 Nov 2026).
From his pick "R4 Small R on a giant berry" (Claude's sketches, claude/step-by-draw-food-11-ideas-4-versions.md).

One giant raspberry hanging from its stalk. The R is at the top: its stick is the right edge of the green stalk, its
bump is the right half of a round leaf, and its leg is the middle line of a second, pointed leaf.

    python3 build_raspberries.py
"""
import math
from fkit import *

GREEN, RED = FILL['green'], FILL['red']
X1, WD = 50.5, 4.4                               # the R's stick (the right edge of the stalk), how thick the stalk is
X0 = X1 - WD
TOPY, MIDY, BW = 4.0, 22.0, 12.5                 # the top of the R, the bottom of its bump, how far the bump sticks out
TIP = (X1 + 17.0, MIDY + 21.5)                   # the tip of the second leaf
LEG = P(X1 + 0.667 * 17.0, MIDY + 0.667 * 21.5)  # the end of the R's leg, two thirds of the way along that leaf
BX, BY, S = X1 - 1.5, 37.0, 1.9                  # the berry: middle, top, size
R = 4.3 * S


def lens(base, tip, ang=28.0, k=0.42):
    """a pointed leaf from base to tip whose two edges leave the base close to its middle line"""
    dx, dy = tip[0] - base[0], tip[1] - base[1]; L = math.hypot(dx, dy); a = math.atan2(dy, dx)
    def off(p, direction, turn):
        t = a + math.radians(turn) + (math.pi if direction < 0 else 0)
        return (p[0] + k * L * math.cos(t), p[1] + k * L * math.sin(t))
    return [Seg(base, off(base, 1, -ang), off(tip, -1, ang), tip), Seg(tip, off(tip, -1, -ang), off(base, 1, ang), base)]


def star(cx, cy, r_out, r_in, squash, k=5, rot=90):
    pts = []
    for i in range(2 * k):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(rot + i * 180 / k)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a) * squash))
    return poly(*pts, closed=True)


net = Net()
net.add('stem', Seg((X1, TOPY), (X1, BY + 1)))                                 # 1: the R (the stick is trimmed at the star below)
net.add('bowl', half_leaf(X1, TOPY, MIDY, BW, 1))
net.add('leg', Seg((X1, MIDY), LEG))
net.add('stalkL', poly((X1, TOPY), (X0, TOPY), (X0, BY + 1)))                  # 2: the rest of the stalk, and the other half of the leaf
net.add('leafL', half_leaf(X0, TOPY, MIDY, BW, -1))
net.add('leaf2', lens((X1, MIDY), TIP))                                        # 3: the leaf round the leg
net.add('star', star(BX, BY + 2.5, 12.0, 6.2, 0.7))                            # 4: the green star on top of the berry
# 5 and 6: the round bumps of the berry, front ones first
ROWS = [(4.5, [0, 6.4, -6.4]), (10.0, [3.2, -3.2, 9.4, -9.4]), (15.8, [0, 6.6, -6.6]), (21.0, [3.6, -3.6]), (25.2, [0])]
DR = []
for y, xs in ROWS:
    for x in xs:
        DR.append('d%d' % len(DR))
        net.add(DR[-1], ell(BX + x * S, BY + y * S, R))
net.node()
net.hide('stem', 'star'); net.hide('stalkL', 'star'); net.hide('star', 'leaf2')
for i, nm in enumerate(DR):
    net.hide(nm, 'leaf2', 'star', *DR[:i])
ALL = ['stem', 'bowl', 'stalkL', 'leafL', 'leaf2', 'star'] + DR

steps = [
    step('Start with an R', 'Draw a capital R: a straight line down, a round bump at the top, and a leg going down to the right. It is hiding in the raspberry.',
         net.lines('stem', 'bowl', 'leg')),
    step('Stalk and leaf', 'Make the straight line thick, for the stalk. Then draw a round bump on its left, the same as the bump of the R. Now it is a leaf.',
         net.lines('stalkL', 'leafL')),
    step('Another leaf', 'Draw a long pointed leaf round the leg of the R. The leg is the line down its middle.', net.lines('leaf2')),
    step('A star', 'At the bottom of the stalk, draw a star with five points. It goes behind the pointed leaf.', net.lines('star')),
    step('The top of the berry', 'Draw round bumps peeping out under the star. Then draw a row of four round bumps below them.',
         net.lines(*DR[:7])),
    step('The rest of the berry', 'Draw three more rows of round bumps, each tucked in behind the row above: three, then two, then one.',
         net.lines(*DR[7:])),
]
green = [net.fill(GREEN, ((X0 + X1) / 2, 28), names=ALL), net.fill(GREEN, (X0 - BW / 2, 13), names=ALL), net.fill(GREEN, (X1 + BW / 2, 13), names=ALL),
         net.fill(GREEN, (X1 + 8.6, MIDY + 9.2), names=ALL)]
green += net.visible_fills(GREEN, 'star', ['leaf2'], names=ALL)
red = []
for i, nm in enumerate(DR):
    red += net.visible_fills(RED, nm, ['leaf2', 'star'] + DR[:i], names=ALL)
steps += [
    step('Colour green', 'Colour the stalk, both leaves and the star green.', green, use='green'),
    step('Colour red', 'Colour every round bump of the raspberry red.', red, use='red'),
]
print('green parts', len(green), 'red parts', len(red))

D = drawing('dx_raspberries_r', 'R is for Raspberries', 2, 14, 'things', ['Letters', 'Around the house'],
            'One giant raspberry on its stalk. The capital R is hiding at the top: in the stalk and the two leaves.',
            steps, ['green', 'red'])
save('raspberries', D, {'set': 'house-AZ', 'slot': 'R', 'kind': 'key', 'age_from': 4})
