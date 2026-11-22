"""f is for Fizzy drink (dx_fizzydrink_f), Food and drink a to z, slot f (22 Nov 2026).
From his pick "f2 A tall glass with ice and lemon" (Claude's sketches, claude/step-by-draw-food-small-11-ideas-4-versions.md).

A tall glass of orange fizzy drink with two ice cubes, a slice of lemon on the rim and a stripy bendy straw.
The f is the outside edge of the straw (its tall line and its hook) and the middle of the rim of the glass (its cross line).

    python3 build_fizzydrink.py
"""
import math
from fkit import *

ORANGE, RED, LBLUE, YELLOW = FILL['orange'], FILL['red'], FILL['lblue'], FILL['yellow']
X, SBOT, TOPY, R, RUN, SW = 44.0, 84.0, 6.0, 11.0, 5.0, 4.2      # the straw: its outside edge, bottom, top, bend, end, width
RIM = 38.0
LC, LR = (73.0, 32.0), 9.5                                       # the lemon slice


def rot_square(c, half, deg):
    a = math.radians(deg); pts = []
    for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
        x, y = sx * half, sy * half
        pts.append(P(c[0] + x * math.cos(a) - y * math.sin(a), c[1] + x * math.sin(a) + y * math.cos(a)))
    return poly(*pts, closed=True)


net = Net()
hook = arc(X + R, TOPY + R, R, R, 180, 270, start=P(X, TOPY + R), end=P(X + R, TOPY))
net.add('fstem', Seg((X, SBOT), (X, TOPY + R)), hook, Seg((X + R, TOPY), (X + R + RUN, TOPY)))   # 1: the f
net.add('fbar', Seg((34, RIM), (58, RIM)))
net.add('lemon', ell(LC[0], LC[1], LR))                                                    # 2: the lemon
inner = ell(LC[0], LC[1], LR - 2.4)
spokes = []
for k in range(8):
    a = math.radians(22.5 + 45 * k)
    spokes.append(line(Seg((LC[0] + 1.0 * math.cos(a), LC[1] + 1.0 * math.sin(a)), (LC[0] + 5.6 * math.cos(a), LC[1] + 5.6 * math.sin(a))), w=1.2))
net.add('rimL', Seg((24, RIM), (34, RIM)))                                                 # 3: the glass
net.add('glass', Seg((58, RIM), (76, RIM)), Seg((76, RIM), (69.5, 90)), Seg((69.5, 90), (69.17, 92.67), (67.67, 94), (65, 94)),
        Seg((65, 94), (35, 94)), Seg((35, 94), (32.33, 94), (30.83, 92.67), (30.5, 90)), Seg((30.5, 90), (24, RIM)))
XI = X + SW
inner_hook = arc(X + R, TOPY + R, R - SW, R - SW, 180, 270, start=P(XI, TOPY + R), end=P(X + R, TOPY + SW))
net.add('strawA', Seg((X, SBOT), (XI, SBOT)), Seg((XI, SBOT), (XI, RIM)))                  # 4: the straw
net.add('strawB', Seg((XI, RIM), (XI, TOPY + R)), inner_hook, Seg((X + R, TOPY + SW), (X + R + RUN, TOPY + SW)),
        Seg((X + R + RUN, TOPY + SW), (X + R + RUN, TOPY)))
SY = [78, 71, 64, 57, 50, 43, 33, 26]
STRIPES = []
for k, y in enumerate(SY):                                                                 # 5: the stripes
    net.add('s%d' % k, Seg((X, y), (XI, y - 2.4))); STRIPES.append('s%d' % k)
cubes = [rot_square((62, 50), 5.5, 12), rot_square((57, 66.5), 5.5, -16)]                 # 6: the ice
net.region('lemR', ell(LC[0], LC[1], LR))
net.node()
net.hide('glass', 'lemR')
cube_fills = [fill(LBLUE, *c) for c in cubes]
dashes = [line(Seg(a, b)) for a, b in (((85, 17), (89, 12.5)), ((88.5, 23.5), (94, 21.5)), ((80.5, 13), (82, 8)))]
STRAW = ['fstem', 'fbar', 'strawA', 'strawB'] + STRIPES


def red_bands():
    out = []
    for y1, y2 in ((78, 71), (64, 57), (50, 43), (33, 26)):
        out.append(net.fill(RED, (X + SW / 2, (y1 + y2) / 2 - 1.2), names=STRAW))
    return out


steps = [
    step('Start with an f', 'Draw a small letter f: a tall line with a hook at the top, and a short line across.', net.lines('fstem', 'fbar')),
    step('The lemon', 'Next to the f, draw a round slice of lemon. Draw a ring inside it, and little lines like the spokes of a wheel.',
         net.lines('lemon') + [ring(*inner, w=1.2)] + spokes),
    step('The glass', 'Make the cross line of the f longer on both sides. Then draw the glass down from it, behind the lemon.', net.lines('rimL', 'glass')),
    step('The straw', 'The tall line of the f is a bendy straw. Draw a second line beside it, all the way round the hook.', net.lines('strawA', 'strawB')),
    step('The stripes', 'Draw little slanting lines across the straw.', net.lines(*STRIPES)),
    step('Ice cubes', 'Draw two ice cubes in the drink. Add three little lines by the lemon.', [ring(*c) for c in cubes] + dashes),
    step('Colour the drink', 'Colour the drink orange, all round the straw and the ice.',
         [net.fill(ORANGE, (38, 60), names=['rimL', 'glass', 'lemon'] + STRAW, cut=[f['d'] for f in cube_fills])], use='orange'),
    step('Colour the stripes', 'Colour every other stripe on the straw red.', red_bands(), use='red'),
    step('Colour the ice', 'Colour the ice cubes light blue.', cube_fills, use='lblue'),
    step('Colour the lemon', 'Colour the lemon slice yellow.', [net.fill(YELLOW, (LC[0] + 8.2, LC[1]), names=['lemon'])], use='yellow'),
]

D = drawing('dx_fizzydrink_f', 'f is for Fizzy drink', 3, 12, 'things', ['Letters', 'Around the house'],
            'A tall glass of fizzy orange with ice, a lemon slice and a bendy straw. The small letter f is hiding in it: the straw and the rim of the glass.',
            steps, ['orange', 'red', 'lblue', 'yellow'])
save('fizzydrink', D, {'set': 'house-az', 'slot': 'f', 'kind': 'key', 'age_from': 5})
