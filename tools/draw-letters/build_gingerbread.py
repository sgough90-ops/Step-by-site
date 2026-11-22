"""g is for Gingerbread (dx_gingerbread_g), Food and drink a to z, slot g (22 Nov 2026).
From his pick "g3 A gingerbread house" (Claude's sketches, claude/step-by-draw-food-small-11-ideas-4-versions.md).

A gingerbread house in the snow, with an icing roof covered in sweets, a red door and a window. Stuck on the wall
are a round peppermint and a candy cane. The g is the peppermint (its round part) and the inside edge of the candy cane
(its tail).

    python3 build_gingerbread.py
"""
import math
from fkit import *

BROWN, RED, GREEN, LBLUE = FILL['brown'], FILL['red'], FILL['green'], FILL['lblue']
XS, GT, GB, HR = 76.6, 60.0, 82.0, 5.0          # the g's tail: its line, top, bottom of the straight part, the hook
BC, BR = P(69.5, 68.0), 8.0                       # the g's round part (the peppermint); its edge goes just past the tail
CW = 3.4                                          # how thick the candy cane is
XW = XS + CW                                      # the house's right wall (the cane's other edge)
HC = P(XS - HR, GB)                               # the middle of the hook
XL, WB = 20.0, 92.0                               # the house's left wall and bottom
APO, API = P(50, 9), P(50, 19)                    # the top of the roof, outside and inside
EO, EI = P(93, 53.5), P(88.5, 58)                 # the right end of the roof, outside and inside


def inner_y(x):
    return API[1] + abs(x - API[0]) * (EI[1] - API[1]) / (EI[0] - API[0])


def on(c, r, deg):
    a = math.radians(deg); return P(c[0] + r * math.cos(a), c[1] + r * math.sin(a))


net = Net()
net.add('bowl', ell(BC[0], BC[1], BR, start=0))                                          # 1: the g
net.add('tail', Seg((XS, GT), (XS, BC[1])), Seg((XS, BC[1]), (XS, GB)), arc(HC[0], HC[1], HR, HR, 0, 180, start=P(XS, GB), end=P(XS - 2 * HR, GB)))
net.add('cane', Seg((XS, GT), (XW, GT)), Seg((XW, GT), (XW, GB)),                         # 2: the candy cane
        arc(HC[0], HC[1], HR + CW, HR + CW, 0, 180, start=P(XW, GB), end=P(HC[0] - HR - CW, GB)), Seg((HC[0] - HR - CW, GB), (XS - 2 * HR, GB)))
WEDGE = (35, 115, 195, 275)
RAD = []
for k, a in enumerate([a for w in WEDGE for a in (w, w + 42)]):                            # 3: the peppermint
    net.add('r%d' % k, Seg(BC, on(BC, BR, a))); RAD.append('r%d' % k)
STR = []
for k, y in enumerate((63.0, 74.0, 79.5)):                                                 # 4: the stripes
    net.add('st%d' % k, Seg((XS, y), (XW, y - 1.8))); STR.append('st%d' % k)
for k, a in enumerate((40, 90, 140)):
    net.add('sh%d' % k, Seg(on(HC, HR, a), on(HC, HR + CW, a + 12))); STR.append('sh%d' % k)
roof = [Seg((EI[0] - 2 * (EI[0] - 50), EI[1]), (EO[0] - 2 * (EO[0] - 50), EO[1])), Seg((EO[0] - 2 * (EO[0] - 50), EO[1]), APO), Seg(APO, EO),
        Seg(EO, EI), Seg(EI, API), Seg(API, (EI[0] - 2 * (EI[0] - 50), EI[1]))]
net.add('roof', roof)                                                                      # 5: the roof
yw = inner_y(XL)
net.add('wallL', Seg((XL, yw), (XL, WB)), Seg((XL, WB), (XW, WB)), Seg((XW, WB), (XW, GB)))  # 6: the walls
net.add('wallR', Seg((XW, inner_y(XW)), (XW, GT)))
net.add('door', Seg((31, WB), (31, 73)), arc(39, 73, 8, 8, 180, 360, start=P(31, 73), end=P(47, 73)), Seg((47, 73), (47, WB)))   # 7: door, window
win = rrect(43.5, 33, 56.5, 45, 1.5)
net.add('win', win)
WC = P(50, 39)
BARS = []
for k, e in enumerate(((50, 33), (56.5, 39), (50, 45), (43.5, 39))):
    net.add('bar%d' % k, Seg(WC, e)); BARS.append('bar%d' % k)
snow = [Seg((2, 94), (10, 88), (30, 90), (50, 90)), Seg((50, 90), (70, 90), (90, 88), (98, 94)), Seg((98, 94), (98, 98), (2, 98), (2, 94))]
net.add('snow', snow)                                                                      # 9: the snow
net.region('house', poly((XL, WB), (XL, yw), API, (XW, inner_y(XW)), (XW, WB), closed=True))
net.node()
net.hide('snow', 'house')
dots = []                                                                                  # 8: the sweets on the roof
for k, t in enumerate((0.2, 0.42, 0.64, 0.86)):
    for sg in (1, -1):
        o = (50 + sg * (EO[0] - 50) * t, APO[1] + (EO[1] - APO[1]) * t); i = (50 + sg * (EI[0] - 50) * t, API[1] + (EI[1] - API[1]) * t)
        c = ((o[0] + i[0]) / 2, (o[1] + i[1]) / 2)
        dots.append((ell(c[0], c[1], 2.2), RED if (k + (sg > 0)) % 2 == 0 else GREEN))
win_fill = fill(LBLUE, *win)
ALL = ['bowl', 'tail', 'cane'] + RAD + STR + ['roof', 'wallL', 'wallR', 'door', 'win'] + BARS
mid = lambda a, r: on(BC, r, a)

steps = [
    step('Start with a g', 'Draw a small letter g: a round circle, then a line down its right side with a hook at the bottom.', net.lines('bowl', 'tail')),
    step('The candy cane', 'The tail of the g is a candy cane. Draw a second line beside it, all the way round the hook.', net.lines('cane')),
    step('The peppermint', 'The circle is a round sweet. Draw lines from the middle out to the edge, like slices of a cake.', net.lines(*RAD)),
    step('The stripes', 'Draw little lines across the candy cane, for its stripes.', net.lines(*STR)),
    step('The roof', 'Above the g, draw a big pointed roof: two thick lines that meet at the top.', net.lines('roof')),
    step('The walls', 'From the roof, draw the walls of the house down to the bottom, and a line along the bottom.', net.lines('wallL', 'wallR')),
    step('Door and window', 'Draw a door with a round top, and a little window at the top of the house.',
         net.lines('door', 'win', *BARS) + [dot(44, 83, w=2.6)]),
    step('Sweets', 'Draw some little round sweets along the roof.', [ring(*c) for c, _ in dots]),
    step('The snow', 'Draw the snow on the ground, under the house.', net.lines('snow')),
    step('Colour brown', 'Colour the gingerbread house brown. Leave the roof, the door, the window and the sweets.',
         [net.fill(BROWN, (30, 60), names=ALL, cut=[win_fill['d']])], use='brown'),
    step('Colour red', 'Colour the door red. Colour every other slice of the peppermint, every other stripe of the cane, and some sweets red.',
         [net.fill(RED, mid(w + 21, 5), names=['bowl'] + RAD) for w in WEDGE] +
         [net.fill(RED, s, names=ALL) for s in ((78.3, 61), (78.3, 75.8), on(HC, HR + CW / 2, 66), on(HC, HR + CW / 2, 162))] +
         [net.fill(RED, (39, 80), names=ALL)] + [fill(RED, *c) for c, col in dots if col == RED], use='red'),
    step('Colour green', 'Colour the other sweets green.', [fill(GREEN, *c) for c, col in dots if col == GREEN], use='green'),
    step('Colour the window', 'Colour the window light blue.', [win_fill], use='lblue'),
]

D = drawing('dx_gingerbread_g', 'g is for Gingerbread', 3, 14, 'things', ['Letters', 'Around the house'],
            'A gingerbread house in the snow with sweets on the roof. The small letter g is hiding in it: a round peppermint and a candy cane on the wall.',
            steps, ['brown', 'red', 'green', 'lblue'])
save('gingerbread', D, {'set': 'house-az', 'slot': 'g', 'kind': 'key', 'age_from': 5})
