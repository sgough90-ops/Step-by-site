"""B is for Broad beans (dx_broadbeans_b), Food and drink A to Z, slot B.

22 Nov 2026: from his pick "B1 Open pod, four beans" (claude/step-by-draw-food-11-ideas-4-versions.md): half an open
pod with four beans in a row along its straight edge, a green skin and a white lining.

25 Nov 2026: he sent step 1 from the live app and said "Make the beans better maybe put a lighter Green on the white
pot in the centre ... just do four variations", then picked number 2, "Whole pod". Now you see both sides of a slimmer
pod: the near side on the left of the straight edge, and the open side on the right with the beans in it. The inside
is light green (a new pencil, 'lgreen'). The straight edge now runs to the two points of the pod, so the pod is two
curves from the top of the line to the bottom, one each side.

The B has not changed its shape: it is the middle two beans and the bit of the straight edge behind them.

    python3 build_broadbeans.py
"""
import math, os
from fkit import *
import check as CK
import ncommon

GREEN, LIGHT = FILL['green'], FILL['lgreen']
X = 46.0                                       # the straight edge of the pod
YS = [20.0, 37.5, 55.0, 72.5, 90.0]            # where the four beans start and end
WB = [12.5, 18.5, 20.0, 12.5]                  # how far each bean sticks out (the end ones are smaller, to stay inside the skin)
G, K, WL = 29.0, 24.0, 10.0                    # how far the open side bulges, its inside edge, and the near side
TOP, BOT = (X, 13.5), (X, 96.5)                # the two points of the pod


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
# 2: the stick made longer, to the two points of the pod, and a bean above and below
net.add('up', Seg((X, YS[1]), (X, YS[0])), Seg((X, YS[0]), TOP))
net.add('down', Seg((X, YS[3]), (X, YS[4])), Seg((X, YS[4]), BOT))
net.add('bean1', bump(YS[0], YS[1], WB[0], lean=1.3))
net.add('bean4', bump(YS[3], YS[4], WB[3], lean=1.3))
# 3: the open side of the pod, from the top point round all four beans to the bottom point
right = [Seg(TOP, (X + G * 0.66, 17.5), (X + G, 36), (X + G, 55)), Seg((X + G, 55), (X + G, 74), (X + G * 0.66, 92.5), BOT)]
net.add('pod', right)
# 4: the inside edge of the pod's skin
net.add('skin', Seg((X, YS[0]), (X + K * 0.5, 15.6), (X + K, 32), (X + K, 55)), Seg((X + K, 55), (X + K, 78), (X + K * 0.5, 94.4), (X, YS[4])))
# 5: the near side of the pod, on the other side of the line
left = [Seg(TOP, (X - 3, 22), (X - WL, 37), (X - WL, 55)), Seg((X - WL, 55), (X - WL, 73), (X - 3, 88), BOT)]
net.add('near', left)
# 6: a curly stalk and a leaf at the top
net.add('curl', Seg(TOP, (X + 2.5, 11.5), (X + 5.5, 9.2), (X + 10, 9.6)))
net.add('leaf', leaf2(TOP, (X - 19, 4.5), 10))
net.region('podR', left + [Seg(*reversed(s.p)) for s in reversed(right)])
net.node()
net.hide('leaf', 'podR')                       # the leaf tucks in behind the point of the pod
rib = Seg((X - 3.4, 12.0), (X - 7.5, 10.2), (X - 11.5, 8.4), (X - 15.2, 6.5))
marks = [mark(YS[k], YS[k + 1], WB[k]) for k in range(4)]
SK = ('curl', 'leaf')

steps = [
    step('Start with a B', 'Draw a capital B: a straight line with two round bumps. This B is hiding in the broad beans.', net.lines('B')),
    step('Two more beans', 'Make the straight line longer at the top and the bottom. Draw one more bump above the B and one more below.',
         net.lines('up', 'bean1', 'down', 'bean4')),
    step('The pod', 'From the top of the line, draw a big curve round all four beans, down to the bottom of the line.', net.lines('pod')),
    step('The skin', 'Draw another big curve just inside the pod, from the top bean round to the bottom bean.', net.lines('skin')),
    step('The other side', 'On the other side of the line, draw a smaller curve from the top to the bottom. Now it is a whole pod.', net.lines('near')),
    step('Stalk and leaf', 'At the top point, draw a little curly stalk and a pointed leaf. Draw a line along the middle of the leaf.',
         net.lines('curl', 'leaf') + [line(rib)]),
    step('Bean marks', 'Draw a little curved line inside each bean.', [line(m) for m in marks]),
    step('Colour green', 'Colour the four beans green. Colour both sides of the pod and the leaf green too. Leave the inside of the pod.',
         [net.fill(GREEN, (X + 5, (YS[k] + YS[k + 1]) / 2), skip=SK) for k in range(4)]
         + [net.fill(GREEN, (X + (G + K) / 2, 55), skip=SK), net.fill(GREEN, (X - WL / 2, 55), skip=SK), net.fill(GREEN, (X - 10, 8.6), names=['leaf', 'near'])], use='green'),
    step('Colour light green', 'Colour the inside of the pod light green, round the beans.', [net.fill(LIGHT, (X + 22, 55), skip=SK)], use='lgreen'),
]

D = drawing('dx_broadbeans_b', 'B is for Broad beans', 1, 10, 'things', ['Letters', 'Around the house'],
            'Four broad beans in their pod. The capital B is hiding in them: it is the two beans in the middle.',
            steps, ['green', 'lgreen'])
save('broadbeans', D, {'set': 'house-AZ', 'slot': 'B', 'kind': 'key', 'age_from': 4})
if __name__ == '__main__':
    r, info = CK.check(D, verbose=False)
    for n, g, dtl in r:
        if not g: print('   FAIL', n, '->', dtl)
    for i in info: print('   ', i)
    print('    on the paper: x %.1f to %.1f, y %.1f to %.1f' % tuple(ncommon.extent(D)[i] for i in (0, 2, 1, 3)))
    print('   broadbeans: %d steps, %s' % (len(steps), 'ALL 9 CHECKS PASS' if all(g for _, g, _ in r) else 'CHECKS FAILED'))
    from vkit import preview
    preview(D, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out', 'broadbeans-look.png'), px=700)
