"""G is for Grapes (dx_grapes_g), Food and drink A to Z, slot G (21 Nov 2026).
From the 'Grapes' card on the capital Food and drink catalogue page (also found online: Vikash Drawing Shorts).
Drawn fresh in our style.

Version 7 (22 Nov, 06:45: "much better but I feel like it needs another 5 degrees more"): the G turned 5 degrees
more the same way (the next grape at -30 degrees), the grapes near it eased round again (up to about 2.5).

Version 6 (22 Nov, 06:17: "the G looks like it's been rotated like 10 degrees too much ... get it back into its more
natural place and just move the connecting grape down a bit"): the G is turned back 10 degrees, so its gap is at the top
right and its bar comes out at the middle of its right side; the next grape sits a little lower (at -35 degrees, was -45).
The grapes near the G grape moved with it (up to about 2), the rest of the bunch is as before.

Version 5 (21 Nov, 21:14: "they should be able to fit in naturally ... it doesn't have to be completely straight. It
could be the little bend for the grape next to it"): the G's bar is not a straight line. It is the start of the next
grape's round edge: from the end of the G's curve it bends a little way along the bottom of the next grape. So the G
grape is just a grape tucked in behind the next grape, with grapes all round it. The G: its round curve is the G
grape's outline, and its short bendy bar goes OUT to the right (his drawing); the next grape loops round from the end
of the bar, touches the top of the G and comes back down to where the bar starts. The grapes round the G grape peek
out from behind it. Then a short brown stalk on the top grape and a green vine leaf.

The grapes overlap: each one peeks out from behind the grapes in front of it, so only the part you can see is drawn,
and each grape is coloured on its own. The hiding is worked out by grapekit.py. Versions 1 to 6 are described in
claude/step-by-draw-letter-builders-24.md.

    python3 build_grapes.py
"""
import math
from r5kit import *
from grapekit import Bunch

PURPLE, GREEN, BROWN = FILL['purple'], FILL['green'], FILL['brown']
R, RG = 7.5, 8.5                      # every grape, and the G grape (a little bigger, so the G is 17 tall)
G0 = (40.0, 62.0)
F_DIR, F_DIST, BAR = -30.0, 13.0, 5.5  # the next grape: up and to the right of the G grape; the bar's length

# the grapes behind, front first: version 5's honeycomb, eased round the G grape when it turned back 10 then 5 degrees
# (the grapes near it turned with it, the far ones stayed; worked out by a small spring layout, then checked)
BEHIND = [('H', 52.33, 67.55), ('B', 41.45, 74.98), ('UL', 28.16, 56.92), ('U1', 38.97, 49.32),      # round the G grape
          ('R1', 62.59, 59.19), ('ML', 26.68, 45.16), ('M1', 48.89, 42.68), ('M2', 60.15, 46.23),    # the next ring out
          ('M0', 35.98, 37.7), ('MLL', 23.35, 33.65), ('T1', 45.51, 30.37), ('T2', 56.89, 33.41), ('T0', 32.35, 25.61)]  # the top
NAMES = [n for n, _, _ in BEHIND]

# ---- 1: the G (curve from its top end round anticlockwise) and its bar, bending along the bottom of the next grape ----
B = Bunch([(x, y) for _, x, y in BEHIND], G0, RG, F_DIR, F_DIST, R, BAR)
for i in range(2, len(B.C)):
    assert B.ok(i, B.lines[i]), ('a grape has a tiny bit peeking out, or overlaps too much', NAMES[i - 2])
for i in range(2, 6):                 # the four round the G grape touch it; nothing else does (the next grape is in front)
    assert math.dist(B.C[i][:2], G0) < R + RG, NAMES[i - 2]
for i in range(6, len(B.C)):
    assert math.dist(B.C[i][:2], G0) > R + RG + 0.8, NAMES[i - 2]

ROUND_G = [l for i in range(2, 6) for l in B.lines[i]]
NEXT_RING = [l for i in range(6, 10) for l in B.lines[i]]
TOP = [l for i in range(10, 15) for l in B.lines[i]]

# ---- the stalk: on the middle top grape, a short thick stalk going up, leaning a little to the right ----
TOPG = 2 + NAMES.index('T1')
BX, BY, BR_ = B.C[TOPG]
SW = 2.1                              # half the stalk's width
SX_BOT, SX_TOP = BX + 0.6, BX + 1.8
SY_TOP = BY - BR_ - 10.0               # about 10 tall


def on_top_grape(x):
    return P(x, BY - math.sqrt(BR_ * BR_ - (x - BX) ** 2))


S_LB, S_RB = on_top_grape(SX_BOT - SW), on_top_grape(SX_BOT + SW)
S_LT, S_RT = P(SX_TOP - SW, SY_TOP), P(SX_TOP + SW, SY_TOP)
stalk_l = [Seg(S_LB, (S_LB[0], SY_TOP + 8.0), (S_LT[0] - 0.1, SY_TOP + 3.5), S_LT)]
stalk_r = [Seg(S_RB, (S_RB[0], SY_TOP + 8.0), (S_RT[0] - 0.1, SY_TOP + 3.5), S_RT)]
stalk_top = Seg(S_LT, (S_LT[0] + 0.5, SY_TOP - 1.5), (S_RT[0] - 0.5, SY_TOP - 1.5), S_RT)
stalk_r, (LA, LM, LB) = cut_at_points(stalk_r, [(SX_TOP + SW - 0.1, SY_TOP + 2.0), (SX_TOP + SW - 0.15, SY_TOP + 4.2), (SX_TOP + SW - 0.25, SY_TOP + 6.4)])

# ---- the vine leaf, with three rounded points, growing from the right of the stalk (the top right grape is lower) ----
LTH = math.radians(-36)               # the leaf points up and to the right, clear of the top grapes


def Lp(u, v):
    """a point in leaf space (u along the leaf from its base on the stalk, v across it) on the paper"""
    return (LM[0] + u * math.cos(LTH) - v * math.sin(LTH), LM[1] + u * math.sin(LTH) + v * math.cos(LTH))


def leaf_half(sign):
    """one side of the leaf in leaf space, from its join on the stalk out round a side point to the dip, then out to
    the middle point (sign -1: the top side, +1: the bottom side, drawn the other way round)"""
    k = sign
    tip = (12.0, 16.0 * k)                                # the side point
    t = (0.87, -0.5 * k)                                  # across the side point, going away from the stalk
    dip, mid = (17.0, 5.6 * k), (30.0, 0.0)
    return [((0.0, 2.4 * k), (7.0, 6.0 * k), (tip[0] - t[0] * 4.2, tip[1] - t[1] * 4.2), tip),
            (tip, (tip[0] + t[0] * 4.2, tip[1] + t[1] * 4.2), (dip[0] - 0.4, dip[1] + 3.6 * k), dip),
            (dip, (dip[0] + 4.6, dip[1] + 2.4 * k), (mid[0], mid[1] + 3.6 * k), mid)]


def leaf_segs():
    top, bot = leaf_half(-1), leaf_half(1)
    parts = top + [tuple(reversed(p)) for p in reversed(bot)]
    out = []
    for p in parts:
        pts = [Lp(*q) for q in p]
        if out: pts[0] = out[-1].b
        out.append(Seg(*pts))
    out[0].p[0] = LA; out[-1].p[-1] = LB
    return out


leaf = leaf_segs()
chain_ok(leaf)
VJ = P(*Lp(7.0, 0))
veins = [Seg(LM, VJ), Seg(VJ, P(*Lp(25.0, 0))), Seg(VJ, P(*Lp(11.2, -12.0))), Seg(VJ, P(*Lp(11.2, 12.0)))]

steps = [
    step('Start with a G', 'Draw a capital G: a round curve like a C, then a short bendy line going out to the right. This G is one of the grapes.',
         [line(*B.G_CURVE), line(*B.G_BAR)]),       # two strokes, like writing a G: the round, then the bar
    step('The next grape', 'Keep going from the end of the bendy line: loop round to make the next grape, touch the top of the G, and come back to where the line began.',
         [line(*B.FR_REST)]),
    step('Round the G', 'Draw four grapes round the G grape: on its right, under it, on its left and above it. They peek out from behind it.',
         [line(*l) for l in ROUND_G]),
    step('More grapes', 'Draw four more grapes round the outside, each one peeking out from behind the grapes in front.',
         [line(*l) for l in NEXT_RING]),
    step('Top grapes', 'Draw five grapes along the top, peeking out from behind the others.',
         [line(*l) for l in TOP]),
    step('The stalk', 'From the middle top grape, draw a short thick stalk going up.',
         [line(*stalk_l, stalk_top, *rev(stalk_r))]),
    step('The leaf', 'On one side of the stalk, draw a big leaf with three round points.',
         [line(*leaf)]),
    step('The veins', 'Draw a line along the middle of the leaf, and a line out to each of its other two points.',
         [line(*veins[:2]), line(veins[2]), line(veins[3])]),
]

stalk_fill = fill(BROWN, *(stalk_l + [stalk_top] + rev(stalk_r) + B.carc(TOPG, S_RB, S_LB, False)))
leaf_fill = fill(GREEN, *(leaf + piece(stalk_r, LB, LA)))
grape_fills = [B.FR_RING, B.G_FILL] + [B.fills[i] for i in range(2, len(B.C))]
steps += [
    step('Colour purple', 'Colour all the grapes purple, the G grape too.', [fill(PURPLE, *g) for g in grape_fills], use='purple'),
    step('Colour green', 'Colour the leaf green.', [leaf_fill], use='green'),
    step('Colour brown', 'Colour the stalk brown.', [stalk_fill], use='brown'),
]

D = drawing('dx_grapes_g', 'G is for Grapes', 2, 14, 'things', ['Letters', 'Around the house'],
            'A bunch of purple grapes with a leaf. The capital G is hiding in it: it is one of the grapes near the bottom.',
            steps, ['purple', 'green', 'brown'])
move(D, dx=6.0, dy=10.5)              # into the middle of the paper
save('grapes', D, {'set': 'house-AZ', 'slot': 'G', 'kind': 'key', 'age_from': 4})
