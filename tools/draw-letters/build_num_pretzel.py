"""3 is for Pretzel (dx_pretzel_3), Food and drink 1 to 9, slot 3 (23 Nov 2026).
From his pick "3: 4 Pretzel" (claude/step-by-draw-food-numbers-1-to-9-36-sketches.md).

A big soft pretzel lying on its side. The 3 is the outside edge of its two loops on the right, which meet in a point
where the dough twists. The dough is one long band: it starts at the tip of the first arm (bottom left), goes through
the twist, round the top loop, down the left side, round the bottom loop, back through the twist and out to the tip of
the second arm (top left). The first arm lies in front of the second arm; both arm tips lie in front of the left side.
Written in the sketch's numbers.

    python3 build_num_pretzel.py
"""
from ncommon import *

p = Pic(s=1.0, dx=2.5, dy=0.0)
OFF = 5.15                                                       # half the width of the dough
MID = [(25, 67), (38, 60), (52, 53), (61, 50), (72, 45), (80, 37), (81, 26), (72, 16), (56, 11), (38, 13), (24, 23), (16, 38), (14, 50),
       (16, 62), (24, 77), (38, 87), (56, 89), (72, 84), (81, 74), (80, 63), (72, 55), (61, 50), (52, 47), (38, 40), (25, 33)]


def dense(pts, k=10):
    """points along the smooth middle line of the dough, k for each stretch between two of the points above"""
    m = len(pts); g = lambda i: pts[max(0, min(m - 1, i))]; out = []
    for i in range(m - 1):
        p0, p1, p2, p3 = g(i - 1), g(i), g(i + 1), g(i + 2)
        s = Seg(p1, (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6), (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6), p2)
        s.p = [p1, (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6), (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6), p2]   # not rounded
        out += [s.at(j / k) for j in range(k)]
    return out + [pts[-1]]


C = dense(MID)                                                   # 241 points; point 10 * i is MID[i]


def edge(side):
    """the dough's edge: side +1 is on the right of someone walking along the middle line (the outside of the loops), -1 the left"""
    out = []
    for i, (x, y) in enumerate(C):
        (ax, ay), (bx, by) = C[max(0, i - 1)], C[min(len(C) - 1, i + 1)]
        L = math.hypot(bx - ax, by - ay)
        out.append((x - (by - ay) / L * OFF * side, y + (bx - ax) / L * OFF * side))
    return out


OUT, IN = edge(1), edge(-1)
k = next(i for i in range(30, 45) if OUT[i + 1][1] <= 50)        # the outside edge crosses itself on the line y = 50 (the twist)
t = (50 - OUT[k][1]) / (OUT[k + 1][1] - OUT[k][1])
DIP = (OUT[k][0] + (OUT[k + 1][0] - OUT[k][0]) * t, 50)          # the point of the 3

# the two edges as smooth pieces, through every fifth point (the outside edge goes through the point of the 3 twice)
SO = smooth([OUT[i] for i in range(0, 40, 5)] + [DIP] + [OUT[i] for i in range(45, 200, 5)] + [DIP] + [OUT[i] for i in range(205, 245, 5)])
SI = smooth([IN[i] for i in range(0, 245, 5)])
A_LO, UP3, LEFT, LO3, B_HI = SO[0:8], SO[8:17], SO[17:31], SO[31:40], SO[40:48]     # tip A..dip, dip..85, 85..155, 155..dip, dip..tip B
A_HI, LOOP_IN, B_LO = SI[0:9], SI[9:42], SI[42:48]                                 # tip A..45, 45..210, 210..tip B


def cap(c, a, b, away):
    """the round tip of an arm: half a circle about c from a to b, bulging the way of the angle `away`"""
    a0 = math.degrees(math.atan2(a[1] - c[1], a[0] - c[0])); a1 = math.degrees(math.atan2(b[1] - c[1], b[0] - c[0]))
    a1 = min((a1 - 360, a1, a1 + 360), key=lambda v: abs(((a0 + v) / 2 - away + 180) % 360 - 180) + (0 if 90 < abs(v - a0) < 270 else 999))
    return arc(c[0], c[1], OFF, OFF, a0, a1, start=P(*a), end=P(*b))


away_a = math.degrees(math.atan2(C[0][1] - C[1][1], C[0][0] - C[1][0]))
away_b = math.degrees(math.atan2(C[240][1] - C[239][1], C[240][0] - C[239][0]))
CAP_A = cap(C[0], A_LO[0].a, A_HI[0].a, away_a)                  # from the outside edge round to the inside edge
CAP_B = cap(C[240], B_HI[-1].b, B_LO[-1].b, away_b)

# ---- the back: the left side of the pretzel and the inside edge of the loops ----
p.stroke('left', LEFT, step=2)
p.stroke('inner', LOOP_IN, step=5)

# ---- the second arm (in front of the left side, behind the first arm) ----
p.region('armB_R', B_HI, CAP_B, rev(B_LO), Seg(B_LO[0].a, B_HI[0].a))
p.stroke('armB', B_HI, CAP_B, rev(B_LO), step=4)

# ---- the first arm (in front) ----
p.region('armA_R', A_LO, UP3[0:1], Seg(UP3[0].b, A_HI[-1].b), rev(A_HI), rev(CAP_A))
p.stroke('armA', rev(A_LO), CAP_A, A_HI, step=3)

# ---- the 3, in front of everything: the top bump, down to the point, then the bottom bump ----
p.stroke('three', rev(UP3), rev(LO3), step=1)
p.build()

salt = [pdot(p, *C[i]) for i in (12, 58, 72, 92, 110, 128, 148, 166, 186, 226)]
steps = [
    step('Start with a 3', 'Draw a big number 3: two round bumps, one on top of the other, meeting in a point in the middle. This 3 is hiding in the pretzel.', p.step(1)),
    step('The outside', 'From the top of the 3, draw a big curve round to the left and back to the bottom of the 3, like a letter C.', p.step(2)),
    step('The first arm', 'From the point of the 3 draw a line down to the left. Go round a little round tip and come back beside it. Stop just above the point of the 3.', p.step(3)),
    step('The second arm', 'Draw the other arm going up to the left with a round tip. It starts and ends on the first arm, as it goes behind it.', p.step(4)),
    step('Inside the loops', 'Draw a line inside the pretzel, the same distance from the outside all the way round. Stop each time you reach an arm.', p.step(5)),
    step('Salt', 'Draw little dots on the pretzel for the salt.', salt),
    step('Colour light brown', 'Colour the whole pretzel light brown. Leave the three holes white.', [p.face('lbrown', C[70]), p.face('lbrown', C[226 + 4])], use='lbrown'),
]
D = drawing('dx_pretzel_3', '3 is for Pretzel', 2, 12, 'things', TAGS,
            'A big soft pretzel lying on its side. The number 3 is hiding in it: the outside of its two loops.',
            steps, ['lbrown'])
ok = finish('num3pretzel', D, {'set': SET, 'slot': '3', 'kind': 'key', 'age_from': 5}, p)
