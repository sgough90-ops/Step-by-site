"""B is for Broad beans (dx_broadbeans_b), Food and drink A to Z, slot B (22 Nov 2026).
From his pick "B1 Open pod, four beans" (Claude's sketches, claude/step-by-draw-food-11-ideas-4-versions.md).

An open pod with four beans in a row along its straight edge. The B is the middle two beans and the bit of the
straight edge behind them. The pod has a thick green skin and a white lining, as a real broad bean pod has.

    python3 build_broadbeans.py
"""
import math
from fkit import *

GREEN = FILL['green']
X = 40.0                                       # the straight edge of the pod
YS = [20.0, 37.5, 55.0, 72.5, 90.0]            # where the four beans start and end
WB = [16.0, 18.5, 20.0, 16.0]                  # how far each bean sticks out


def bump(y0, y1, w, lean=0.0):
    """a bean: from the straight edge round and back. lean: how much its two ends tip in (0 = flat, as a B's bowl)"""
    h = y1 - y0
    return [Seg((X, y0), (X + w * 0.55, y0 + lean), (X + w, y0 + h * 0.17), (X + w, y0 + h / 2)),
            Seg((X + w, y0 + h / 2), (X + w, y1 - h * 0.17), (X + w * 0.55, y1 - lean), (X, y1))]


def mark(y0, y1, w):
    h = y1 - y0
    return Seg((X + w * 0.36, y0 + h * 0.2), (X + w * 0.62, y0 + h * 0.2), (X + w * 0.78, y0 + h * 0.34), (X + w * 0.8, y0 + h * 0.5))


net = Net()
# 1: the B, in one go: up the stick, round the top bowl, round the bottom bowl
net.add('B', Seg((X, YS[3]), (X, YS[2])), Seg((X, YS[2]), (X, YS[1])), bump(YS[1], YS[2], WB[1]), bump(YS[2], YS[3], WB[2]))
# 2: the stick made longer, and a bean above and below
net.add('up', Seg((X, YS[1]), (X, YS[0])))
net.add('down', Seg((X, YS[3]), (X, YS[4])))
net.add('bean1', bump(YS[0], YS[1], WB[0], lean=1.3))
net.add('bean4', bump(YS[3], YS[4], WB[3], lean=1.3))
# 3: the pod, from the top of the stick up to a point, round, and back to the bottom of the stick
TOP, BOT = (X + 5.5, 13.5), (X + 5.5, 96.5)
net.add('pod', Seg((X, YS[0]), (X, 17), (X + 2, 14.6), TOP),
        Seg(TOP, (X + 22, 19), (X + 36, 37), (X + 36, 55)), Seg((X + 36, 55), (X + 36, 73), (X + 22, 91), BOT),
        Seg(BOT, (X + 2, 95.4), (X, 93), (X, YS[4])))
# 4: the inside edge of the pod's skin
net.add('skin', Seg((X, YS[0]), (X + 11, 15.6), (X + 30.6, 32), (X + 30.6, 55)), Seg((X + 30.6, 55), (X + 30.6, 78), (X + 11, 94.4), (X, YS[4])))
# 5: a curly stalk and a leaf at the top
net.add('curl', Seg(TOP, (X + 6.4, 10.4), (X + 9.6, 7.8), (X + 14.6, 7)))
net.add('leaf', leaf2(TOP, (X - 16.5, 8.5), 10))
net.region('podR', net.all('pod'), Seg((X, YS[4]), (X, YS[0])))
net.node()
net.hide('leaf', 'podR')                       # the leaf tucks in behind the point of the pod
rib = Seg((X + 1.2, 12.6), (X - 3.5, 11.3), (X - 8, 10.4), (X - 12, 9.5))
marks = [mark(YS[k], YS[k + 1], WB[k]) for k in range(4)]

steps = [
    step('Start with a B', 'Draw a capital B: a straight line with two round bumps. This B is hiding in the broad beans.', net.lines('B')),
    step('Two more beans', 'Make the straight line longer at the top and the bottom. Draw one more bump above the B and one more below.',
         net.lines('up', 'bean1', 'down', 'bean4')),
    step('The pod', 'From the top of the line go up to a point, then draw a big curve round all four beans, down to a point and back to the line.',
         net.lines('pod')),
    step('The skin', 'Draw another big curve just inside the pod, from the top of the line round to the bottom.', net.lines('skin')),
    step('Stalk and leaf', 'At the top point, draw a little curly stalk and a pointed leaf. Draw a line along the middle of the leaf.',
         net.lines('curl', 'leaf') + [line(rib)]),
    step('Bean marks', 'Draw a little curved line inside each bean.', [line(m) for m in marks]),
    step('Colour green', 'Colour the four beans, the skin round the edge of the pod and the leaf green. Leave the inside of the pod white.',
         [net.fill(GREEN, (X + 5, (YS[k] + YS[k + 1]) / 2), skip=('curl', 'leaf')) for k in range(4)]
         + [net.fill(GREEN, (X + 33.3, 55), skip=('curl', 'leaf')), net.fill(GREEN, (X - 6, 10.6), names=['leaf', 'pod'])], use='green'),
]

D = drawing('dx_broadbeans_b', 'B is for Broad beans', 1, 8, 'things', ['Letters', 'Around the house'],
            'Four broad beans in their open pod. The capital B is hiding in them: it is the two beans in the middle.',
            steps, ['green'])
save('broadbeans', D, {'set': 'house-AZ', 'slot': 'B', 'kind': 'key', 'age_from': 4})
