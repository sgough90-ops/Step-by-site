"""F is for Fruit (dx_fruit_f), Food and drink A to Z, slot F (22 Nov 2026).
From his pick "F1 Fruit bowl, pear on top" (Claude's sketches, claude/step-by-draw-food-11-ideas-4-versions.md).

A bowl of fruit: an apple, a pear, an orange, a banana and three grapes. The F is at the top, in the pear's stalk:
its stick is the right edge of the green stalk, and its two bars are the middle lines of the two leaves.

    python3 build_fruit.py
"""
import math
from fkit import *

GREEN, RED, ORANGE, YELLOW, PURPLE, LBLUE = FILL['green'], FILL['red'], FILL['orange'], FILL['yellow'], FILL['purple'], FILL['lblue']
K, Y0 = 0.885, 3.2                                # the sketch (about 106 tall) is made a little smaller to fit the paper


def T(x, y):
    return P(50 + (x - 50) * K, Y0 + (y + 8.8) * K)


def q2c(p0, q, p2):
    return Seg(p0, (p0[0] + 2 / 3 * (q[0] - p0[0]), p0[1] + 2 / 3 * (q[1] - p0[1])), (p2[0] + 2 / 3 * (q[0] - p2[0]), p2[1] + 2 / 3 * (q[1] - p2[1])), p2)


APP = [(0, -0.74), (0.4, -0.98), (0.88, -0.74), (1.03, -0.1), (0.84, 0.62), (0.4, 0.98), (0, 0.88), (-0.4, 0.98), (-0.84, 0.62), (-1.03, -0.1), (-0.88, -0.74), (-0.4, -0.98)]
PEA = [(0, -1.72), (0.3, -1.6), (0.44, -1.15), (0.56, -0.6), (0.9, -0.05), (1.0, 0.5), (0.74, 0.98), (0.3, 1.14), (0, 1.1),
       (-0.3, 1.14), (-0.74, 0.98), (-1.0, 0.5), (-0.9, -0.05), (-0.56, -0.6), (-0.44, -1.15), (-0.3, -1.6)]
SX, FT, FM, WD = 50.0, -4.0, 6.5, 4.2             # the F's stick, its top bar, its middle bar; how thick the stalk is
TOPBAR, MIDBAR = 13.0, 10.5

net = Net()
# 1: the F (the stick runs on into the pear and is trimmed at its edge below)
net.add('stem', Seg(T(SX, FT), T(SX, 21)))
net.add('bar1', Seg(T(SX, FT), T(SX + TOPBAR, FT)))
net.add('bar2', Seg(T(SX, FM), T(SX + MIDBAR, FM)))
# 2: the stalk made thick, and a leaf round each bar
net.add('stalkL', poly(T(SX, FT), T(SX - WD, FT), T(SX - WD, 21)))
net.add('leafA', leaf2(T(SX, FT), T(SX + TOPBAR + 6.5, FT), 9.5 * K))
net.add('leafB', leaf2(T(SX, FM), T(SX + MIDBAR + 6, FM), 8.5 * K))
# 3: the bowl and its foot
RIM, DEPTH = 68.0, 26.0
net.add('bowl', Seg(T(10, RIM), T(90, RIM)), Seg(T(90, RIM), T(88, RIM + DEPTH * 0.72), T(68, RIM + DEPTH), T(50, RIM + DEPTH)),
        Seg(T(50, RIM + DEPTH), T(32, RIM + DEPTH), T(12, RIM + DEPTH * 0.72), T(10, RIM)))
net.add('foot', poly(T(40, RIM + DEPTH - 3), T(37, RIM + DEPTH + 2.8), T(63, RIM + DEPTH + 2.8), T(60, RIM + DEPTH - 3)))
# 4: the banana, lying across the front, and three grapes
B1, B2 = T(16, 53), T(66, 58)
BA, BB = T(39.2, 73.4), T(40.9, 56.5)
net.add('banana', q2c(B1, BA, B2), q2c(B2, BB, B1))
GR = 4.6 * K
for i, gx in enumerate((71.6, 79.0, 86.4)):
    net.add('g%d' % i, ell(*T(gx, 64.6), GR))
# 5: the apple and the orange
AY = 54.8                                         # low enough for the dip in the bottom of the apple to be hidden by the bowl
net.add('apple', smooth([T(27 + x * 16, AY + y * 16) for x, y in APP], closed=True))
net.add('orange', ell(*T(74, 54), 15.5 * K))
# 6: the pear, behind them
net.add('pear', smooth([T(50 + x * 15.5, 44 + y * 15.5) for x, y in PEA], closed=True))
net.node()
net.hide('stem', 'pear'); net.hide('stalkL', 'pear'); net.hide('foot', 'bowl')
FRONT = {'banana': ['bowl'], 'g2': ['bowl', 'banana'], 'g1': ['bowl', 'banana', 'g2'], 'g0': ['bowl', 'banana', 'g2', 'g1'],
         'apple': ['bowl', 'banana'], 'orange': ['bowl', 'banana', 'g0', 'g1', 'g2'], 'pear': ['bowl', 'banana', 'apple', 'orange']}
for nm, fr in FRONT.items():
    net.hide(nm, *fr)
ALL = ['stem', 'stalkL', 'leafA', 'leafB', 'bowl', 'foot', 'banana', 'g0', 'g1', 'g2', 'apple', 'orange', 'pear']


def stub(p, away, n=2.2 * K):
    d = math.dist(p, away)
    return line(Seg(p, (p[0] + (p[0] - away[0]) / d * n, p[1] + (p[1] - away[1]) / d * n)))


apple_stalk = q2c(T(27, AY - 0.74 * 16), T(27.96, AY - 1.08 * 16), T(31.16, AY - 1.3 * 16))
steps = [
    step('Start with an F', 'Draw a small capital F near the top: a line down, a bar across the top and a shorter bar in the middle. It is hiding in the fruit.',
         net.lines('stem', 'bar1', 'bar2')),
    step('Stalk and leaves', 'Make the line down thick, for the stalk. Draw a pointed leaf round each bar. The bars are the lines down their middles.',
         net.lines('stalkL', 'leafA', 'leafB')),
    step('The bowl', 'Lower down, draw a long line across. Draw a deep curve under it, from one end to the other. Add a little foot.',
         net.lines('bowl', 'foot')),
    step('Banana and grapes', 'Just above the bowl, draw a long curved banana. On the right, draw three little grapes sitting on the edge of the bowl.',
         net.lines('banana') + [stub(B1, BA), stub(B2, BA)] + net.lines('g2', 'g1', 'g0')),
    step('Apple and orange', 'Behind the banana, draw an apple on the left, with a dip in the top and a little stalk. Draw a round orange on the right.',
         net.lines('apple', 'orange') + [line(apple_stalk)]),
    step('The pear', 'From the bottom of the stalk, draw the pear: narrow at the top and wide lower down. It is behind the other fruit.',
         net.lines('pear')),
]
vf = lambda col, nm: net.visible_fills(col, nm, FRONT[nm], names=ALL)
green = [net.fill(GREEN, T(SX - WD / 2, 8), names=ALL), net.fill(GREEN, T(SX + 9, FT - 2), names=ALL), net.fill(GREEN, T(SX + 8, FM - 2), names=ALL)] + vf(GREEN, 'pear')
purple = vf(PURPLE, 'g0') + vf(PURPLE, 'g1') + vf(PURPLE, 'g2')
parts = {'pear': len(green) - 3, 'apple': len(vf(RED, 'apple')), 'orange': len(vf(ORANGE, 'orange')), 'banana': len(vf(YELLOW, 'banana')), 'grapes': len(purple)}
print(parts)
steps += [
    step('Colour green', 'Colour the pear, its stalk and the two leaves green.', green, use='green'),
    step('Colour red', 'Colour the apple red.', vf(RED, 'apple'), use='red'),
    step('Colour orange', 'Colour the orange orange.', vf(ORANGE, 'orange'), use='orange'),
    step('Colour yellow', 'Colour the banana yellow.', vf(YELLOW, 'banana'), use='yellow'),
    step('Colour purple', 'Colour the three grapes purple.', purple, use='purple'),
    step('Colour light blue', 'Colour the bowl and its foot light blue.',
         [net.fill(LBLUE, T(50, RIM + 12), names=ALL), net.fill(LBLUE, T(50, RIM + DEPTH + 1.2), names=ALL)], use='lblue'),
]

D = drawing('dx_fruit_f', 'F is for Fruit', 3, 18, 'things', ['Letters', 'Around the house'],
            'A bowl of fruit with a pear on top. The capital F is hiding in the pear: in its green stalk and its two leaves.',
            steps, ['green', 'red', 'orange', 'yellow', 'purple', 'lblue'])
save('fruit', D, {'set': 'house-AZ', 'slot': 'F', 'kind': 'key', 'age_from': 5})
