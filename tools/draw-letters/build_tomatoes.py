"""T is for Tomatoes (dx_tomatoes_t), Food and drink A to Z, slot T (22 Nov 2026).
From his pick "Tomatoes 2: green stalk with side stalks" (Claude's round 2 sketches,
claude/step-by-draw-food-11-ideas-4-versions.md). He asked for the T to be a real green stalk, not a bare black line.

Cherry tomatoes on the vine. The stalk is a thin green band shaped like a T. The T itself is two plain lines: the top
edge of the band, and the top part of the left edge of the long piece (step 1 draws a T of a normal shape, 38 wide and
48 tall, and step 2 carries its line on down: the step 1 rule in the README). Four side stalks go out to four tomatoes, and one more tomato
hangs on the bottom of the stalk.

    python3 build_tomatoes.py
"""
import math
from fkit import *

GREEN, RED = FILL['green'], FILL['red']
SX, TOP, TH = 50.0, 6.0, 5.0                  # the T's stick, its top line, how thick the stalk is
BL, BR = 31.0, 69.0                           # the ends of the T's top line
MID = SX + TH / 2                             # the middle of the long piece (the picture is the same both sides of it)
TEND = 54.0                                   # step 1's T ends here (38 wide, 48 tall: a normal T); step 2 carries the line on down
RX, RY = 10.0, 9.4
TOMS = [(-1, 15.0), (1, 27.0), (-1, 39.0), (1, 51.0)]      # side (left or right) and how far down each side stalk starts
BOT = (MID, 86.0, 10.5, 9.8)                  # the tomato on the bottom of the stalk

net = Net()
net.add('bar', Seg((BL, TOP), (BR, TOP)))                                           # 1: the T
net.add('stem', Seg((SX, TOP), (SX, TEND)))
net.add('stem2', Seg((SX, TEND), (SX, BOT[1] - 4)))                                  # 2: the line carried on, and the stalk made thick
net.add('thickL', poly((BL, TOP), (BL, TOP + TH), (SX, TOP + TH)))
net.add('thickR', poly((BR, TOP), (BR, TOP + TH), (SX + TH, TOP + TH), (SX + TH, BOT[1] - 4)))


def on(cx, cy, rx, ry, deg):
    return P(cx + rx * math.cos(math.radians(deg)), cy + ry * math.sin(math.radians(deg)))


def zigzag(cx, cy, rx, ry):
    """the green top of a tomato: a zigzag from one side of the top to the other, with three points hanging down"""
    a, b = on(cx, cy, rx, ry, -127), on(cx, cy, rx, ry, -53)
    k = ry / 9.4
    return poly(a, (cx - 3.7, cy - 3.9 * k), (cx - 1.9, cy - 6.5 * k), (cx, cy - 2.8 * k), (cx + 1.9, cy - 6.5 * k), (cx + 3.7, cy - 3.9 * k), b)


cents = []
for i, (side, ya) in enumerate(TOMS):
    tx, cy = MID + side * 14.9, ya + 15.4
    cents.append((tx, cy))
    x0 = SX if side < 0 else SX + TH                                                # the edge of the long piece it grows from
    # the two edges of the side stalk run on a little way into the tomato, and are trimmed at its edge below
    net.add('up%d' % i, Seg((x0, ya), (tx - side * 0.2, cy - 7.6)))
    net.add('lo%d' % i, Seg((x0, ya + 3.6), (tx - side * 3.9, cy - 6.6)))
    net.add('tom%d' % i, ell(tx, cy, RX, RY))
    net.add('zig%d' % i, zigzag(tx, cy, RX, RY))
cents.append((BOT[0], BOT[1]))
net.add('tom4', ell(*BOT))
net.add('zig4', zigzag(*BOT))
net.node()
for i in range(4):
    net.hide('up%d' % i, 'tom%d' % i); net.hide('lo%d' % i, 'tom%d' % i)
net.hide('stem2', 'tom4'); net.hide('thickR', 'tom4')

S = ['bar', 'stem', 'stem2', 'thickL', 'thickR']
steps = [
    step('Start with a T', 'Draw a capital T near the top: a line across, then a line down from its middle. This T is hiding in the tomatoes.',
         net.lines('bar', 'stem')),
    step('The stalk', 'Make the line of the T longer, a long way down. Then make it thick: a line under its top line, with short ends, and a long line down beside it.',
         net.lines('stem2', 'thickL', 'thickR')),
    step('Side stalks', 'Draw four little side stalks going down a bit: two on the left and two on the right. Each one is two lines close together.',
         net.lines(*['%s%d' % (a, i) for i in range(4) for a in ('up', 'lo')])),
    step('Tomatoes', 'Draw a round tomato on the end of each side stalk. Draw one more on the bottom of the stalk.',
         net.lines(*['tom%d' % i for i in range(5)])),
    step('Leafy tops', 'Draw a zigzag across the top of each tomato, with three little points hanging down.',
         net.lines(*['zig%d' % i for i in range(5)])),
]
green = [net.fill(GREEN, ((BL + SX) / 2, TOP + TH / 2), names=S), net.fill(GREEN, ((SX + TH + BR) / 2, TOP + TH / 2), names=S + ['tom4'])]
for i, (side, ya) in enumerate(TOMS):
    tx, cy = cents[i]
    green.append(net.fill(GREEN, (MID + side * 6.5, ya + 3.8), names=S + ['up%d' % i, 'lo%d' % i, 'tom%d' % i]))
green += [net.fill(GREEN, (cx, cy - 0.83 * (RY if i < 4 else BOT[3])), names=['tom%d' % i, 'zig%d' % i]) for i, (cx, cy) in enumerate(cents)]
red = [net.fill(RED, (cx, cy + 2), names=['tom%d' % i, 'zig%d' % i]) for i, (cx, cy) in enumerate(cents)]
steps += [
    step('Colour green', 'Colour the stalk, the four side stalks and the leafy top of every tomato green.', green, use='green'),
    step('Colour red', 'Colour the five tomatoes red.', red, use='red'),
]

D = drawing('dx_tomatoes_t', 'T is for Tomatoes', 2, 12, 'things', ['Letters', 'Around the house'],
            'Cherry tomatoes on the vine. The capital T is hiding in the top of the green stalk: its top line, and the line down.',
            steps, ['green', 'red'])
save('tomatoes', D, {'set': 'house-AZ', 'slot': 'T', 'kind': 'key', 'age_from': 4})
