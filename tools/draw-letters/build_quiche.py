"""Q is for Quiche (dx_quiche_q), Food and drink A to Z, slot Q (22 Nov 2026).
From his pick "Q2 Cutting a slice" (Claude's sketches, claude/step-by-draw-food-11-ideas-4-versions.md).

A round quiche seen from above, with a knife cutting a slice. The Q's ring is the outside of the quiche, and the Q's
tail is the straight back of the knife, running from inside the quiche out to the handle.

    python3 build_quiche.py
"""
import math
from fkit import *

YELLOW, LBROWN, RED, GREEN = FILL['yellow'], FILL['lbrown'], FILL['red'], FILL['green']
C, RQ, RI = (45.0, 45.0), 35.0, 29.0                 # the middle, the outside of the quiche, the inside of the crust
TIP, HEEL, TEND = (55.0, 55.0), (68.0, 68.0), (81.5, 81.5)     # the knife: its tip, the end of its blade, the end of the Q's tail
U = 2.05                                             # half the handle's width, measured along x and y


def on(r, deg):
    return P(C[0] + r * math.cos(math.radians(deg)), C[1] + r * math.sin(math.radians(deg)))


net = Net()
net.add('ring', ell(C[0], C[1], RQ))                                           # 1: the Q
net.add('tail', Seg(TIP, TEND))
net.add('blade', Seg(HEEL, (64.3, 71.8), (54.9, 63.4), TIP))                   # 2: the knife
A, B, A2, B2 = P(TEND[0] + U, TEND[1] - U), P(TEND[0] - U, TEND[1] + U), P(TEND[0] + 10 + U, TEND[1] + 10 - U), P(TEND[0] + 10 - U, TEND[1] + 10 + U)
net.add('handle', Seg(TEND, A), Seg(A, A2), arc(TEND[0] + 10, TEND[1] + 10, U * math.sqrt(2), U * math.sqrt(2), -45, 135, start=A2, end=B2), Seg(B2, B), Seg(B, TEND))
net.region('bladeR', net.all('blade'), Seg(TIP, HEEL))
net.add('inner', ell(C[0], C[1], RI))                                          # 3: the inside edge of the crust
net.add('cut1', Seg(C, TIP))                                                   # 4: the cuts
net.add('cut2', Seg(C, on(RI, 105)))
TOMS = [(31.0, 28.0, 4.8), (24.0, 50.0, 4.4), (61.0, 46.0, 4.4)]               # 5: tomato slices and leaves
LEAVES = [((41, 38), (48.5, 29)), ((35, 59), (26.5, 63.5)), ((58, 36), (65, 30))]
for i, (x, y, r) in enumerate(TOMS): net.add('tom%d' % i, ell(x, y, r))
for i, (b, t) in enumerate(LEAVES): net.add('leaf%d' % i, leaf2(b, t, 6.5))
net.node()
net.hide('inner', 'bladeR')                                                    # the knife lies on top of the crust


def ymark(x, y, r):
    """a Y inside a tomato slice, as two pencil lines: the V across the top, then the line down.
    (As three lines, step 5 had 15 lines, one more than the app's own checker allows in a step.)"""
    e = lambda a: (x + r * 0.62 * math.cos(math.radians(a)), y + r * 0.62 * math.sin(math.radians(a)))
    return [line(Seg(e(210), (x, y)), Seg((x, y), e(330))), line(Seg((x, y), e(90)))]


holes = [d_fill(*net.all('tom%d' % i)) for i in range(len(TOMS))] + [d_fill(*net.all('leaf%d' % i)) for i in range(len(LEAVES))]
S = ['ring', 'tail', 'blade', 'inner']
steps = [
    step('Start with a Q', 'Draw a capital Q: a big round O, with a straight tail going from inside the O down and out to the right. It is hiding in the quiche.',
         net.lines('ring', 'tail')),
    step('The knife', 'The tail is a knife. Draw a curved blade under the first part of the tail. Draw a long handle on the far end, with a round end.',
         net.lines('blade', 'handle')),
    step('The crust', 'Draw a circle just inside the O. Start at one side of the knife, go all the way round, and stop at the other side.',
         net.lines('inner')),
    step('Cut a slice', 'Draw a line from the tip of the knife to the middle. Draw one more line from the middle down to the crust.',
         net.lines('cut1', 'cut2')),
    step('On the top', 'Draw three small circles for slices of tomato, with a Y inside each one. Draw three little leaves.',
         net.lines(*['tom%d' % i for i in range(len(TOMS))]) + sum([ymark(*t) for t in TOMS], []) + net.lines(*['leaf%d' % i for i in range(len(LEAVES))])),
    step('Colour yellow', 'Colour the inside of the quiche yellow, round the tomatoes, the leaves and the knife.',
         [net.fill(YELLOW, (45, 50.5), names=S, cut=holes)], use='yellow'),
    step('Colour light brown', 'Colour the crust light brown, all the way round the edge. Colour the handle of the knife light brown too.',
         [net.fill(LBROWN, (45, 13), names=S), net.fill(LBROWN, (TEND[0] + 5, TEND[1] + 5), names=['handle'])], use='lbrown'),
    step('Colour red', 'Colour the three slices of tomato red.', [fill(RED, *net.all('tom%d' % i)) for i in range(len(TOMS))], use='red'),
    step('Colour green', 'Colour the three leaves green.', [fill(GREEN, *net.all('leaf%d' % i)) for i in range(len(LEAVES))], use='green'),
]

D = drawing('dx_quiche_q', 'Q is for Quiche', 2, 14, 'things', ['Letters', 'Around the house'],
            'A round quiche with a knife cutting a slice. The capital Q is hiding in it: the O is the edge of the quiche and the tail is the knife.',
            steps, ['yellow', 'lbrown', 'red', 'green'])
save('quiche', D, {'set': 'house-AZ', 'slot': 'Q', 'kind': 'key', 'age_from': 4})
