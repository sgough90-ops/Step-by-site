"""M is for Muffin (dx_muffin_m), Food and drink A to Z, slot M (21 Nov 2026).
From the 'Muffin' card on the capital Food and drink catalogue page (also found online: a muffin drawn from an M,
Art with Vered). Drawn fresh in our style.

Version 2 (20:05: he didn't like the big M as the whole case; the M should be between the zigzag lines, as part of the
paper case, so quite a small M): a blueberry muffin in a pleated paper case. The case's top edge is a zigzag, and its
folds go from each top point of the zigzag down to the bottom. The middle part of the case is the M: its two sides are
two folds, and the V between them is one dip of the zigzag. Step 1 draws a normal small M; a later step carries its
sides on down to the bottom of the case. Every other part of the case is pink, so the case looks striped.
Version 1 (the whole case as a big M) is in claude/step-by-draw-letter-builders-24.md.

    python3 build_muffin.py
"""
import math
from r5kit import *

TOP, BERRY, CASE = FILL['lbrown'], FILL['blue'], FILL['pink']

W_ = 11.0                                     # each part of the case is 11 wide at the top, so the M is 11 wide
YT, DIP = 48.0, 5.5                           # the zigzag's top points, and how far its dips go down (half the M)
XS = [50 + (k - 2.5) * W_ for k in range(6)]  # the zigzag's six top points: 22.5 ... 77.5
TOPS = [P(x, YT) for x in XS]
DIPS = [P((a + b) / 2, YT + DIP) for a, b in zip(XS, XS[1:])]
TAPER = 0.78                                  # the case is narrower at the bottom
BOT = Seg(P(50 - 27.5 * TAPER, 80.0), (40, 82.4), (60, 82.4), P(50 + 27.5 * TAPER, 80.0))


def bottom_at(x):
    """the point on the bottom of the case at x"""
    t = seg_x(BOT, x)
    return P(*BOT.at(t))


FOLD_BOT = [bottom_at(50 + (x - 50) * TAPER) if k not in (0, 5) else (BOT.a if k == 0 else BOT.b) for k, x in enumerate(XS)]


def along(p, q, d):
    """the point d along the straight line from p towards q"""
    L = math.dist(p, q)
    return P(p[0] + (q[0] - p[0]) * d / L, p[1] + (q[1] - p[1]) * d / L)


# ---- 1: the M: the middle part of the case (two folds and one dip of the zigzag), a normal M 11 wide and 11 tall ----
ML_T, MR_T, M_V = TOPS[2], TOPS[3], DIPS[2]
ML_B, MR_B = along(ML_T, FOLD_BOT[2], 11.0), along(MR_T, FOLD_BOT[3], 11.0)
M_LINE = poly(ML_B, ML_T, M_V, MR_T, MR_B)

# ---- 2: the zigzag carries on out to each side ----
ZIG_L = poly(ML_T, DIPS[1], TOPS[1], DIPS[0], TOPS[0])
ZIG_R = poly(MR_T, DIPS[3], TOPS[4], DIPS[4], TOPS[5])

# ---- 3: the case: its two sides and the bottom ----
SIDE_L, SIDE_R = Seg(TOPS[0], BOT.a), Seg(TOPS[5], BOT.b)

# ---- 4: the M's sides carry on down to the bottom, and two more folds ----
M_MORE = [Seg(ML_B, FOLD_BOT[2]), Seg(MR_B, FOLD_BOT[3])]
FOLDS = [Seg(TOPS[1], FOLD_BOT[1]), Seg(TOPS[4], FOLD_BOT[4])]

# the bottom of the case, cut where the folds end on it
BOT_CH, BOT_PTS = cut_at_points([BOT], FOLD_BOT[1:5])
assert BOT_PTS == FOLD_BOT[1:5], (BOT_PTS, FOLD_BOT[1:5])

# ---- 5: the bumpy muffin top, from one end of the zigzag over to the other ----
left = curve(TOPS[0], (17.6, 47.4), (14.8, 39.6), (18.6, 34.2), (21.8, 29.6), (28.4, 26.6), (35.2, 27.4))
middle = curve(P(35.2, 27.4), (37.4, 19.4), (62.6, 19.4), P(64.8, 27.4))
right = rev(mirror(left))
TOP_LINE = left + middle + right
chain_ok(TOP_LINE)
assert TOP_LINE[-1].b == TOPS[5]

# ---- 6: blueberries ----
BERRIES = [circle(x, y, 2.4) for x, y in [(27.5, 40.5), (38.5, 33.5), (50, 29.5), (61.5, 33.5), (72.5, 40.5), (44.5, 41.5), (55.5, 41.5)]]

steps = [
    step('Start with an M', 'Draw a small capital M: two straight lines, joined at the top by a V that comes half-way down. This M is hiding in the muffin.',
         [line(*M_LINE)]),
    step('The zigzag', 'From each top of the M, draw a zigzag out to the side: down, up, down, up. This is the top of the paper case.',
         [line(*ZIG_L), line(*ZIG_R)]),
    step('The case', 'From the two ends of the zigzag, draw a line down each side, then a curved line across the bottom.',
         [line(SIDE_L, *BOT_CH, SIDE_R.rev())]),
    step('The folds', 'Make the two sides of the M longer, down to the bottom. Then draw a line down from each of the other two top points.',
         [line(s) for s in M_MORE + FOLDS]),
    step('The muffin top', 'From one end of the zigzag, draw a big bumpy muffin top, up and over to the other end.',
         [line(*TOP_LINE)]),
    step('Blueberries', 'Draw some little circles on the muffin for blueberries.',
         [ring(*b) for b in BERRIES]),
]

# ---- the colours ----
ZIG = rev(ZIG_L) + [Seg(ML_T, M_V), Seg(M_V, MR_T)] + ZIG_R          # the whole zigzag, left to right
muffin = fill(TOP, *(TOP_LINE + rev(ZIG)), cut=[d_fill(*b) for b in BERRIES])


def part(k):
    """part k of the case (0 to 4, left to right): down its left fold, along the bottom, up its right fold, back along the zigzag"""
    lt, rt, dip = TOPS[k], TOPS[k + 1], DIPS[k]
    lb, rb = FOLD_BOT[k], FOLD_BOT[k + 1]
    bot = piece(BOT_CH, lb, rb)
    return fill(CASE, Seg(lt, lb), *bot, Seg(rb, rt), Seg(rt, dip), Seg(dip, lt))


steps += [
    step('Colour light brown', 'Colour the muffin top light brown. Leave the blueberries.', [muffin], use='lbrown'),
    step('Colour blue', 'Colour the blueberries blue.', [fill(BERRY, *b) for b in BERRIES], use='blue'),
    step('Colour pink', 'Colour every other part of the paper case pink: the middle and both ends. Leave the rest white, for stripes.',
         [part(0), part(2), part(4)], use='pink'),
]

D = drawing('dx_muffin_m', 'M is for Muffin', 2, 12, 'things', ['Letters', 'Around the house'],
            'A blueberry muffin in a stripy paper case. The capital M is hiding in it: it is the middle part of the case, between the zigzags.',
            steps, ['lbrown', 'blue', 'pink'])
# The app's own colour check samples the paper on a 4-per-unit grid. The zigzag's 45 degree lines would run exactly
# through its sample points (and count twice, for the muffin and the case), so the whole drawing moves 0.1 to the right.
move(D, dx=0.1)
save('muffin', D, {'set': 'house-AZ', 'slot': 'M', 'kind': 'key', 'age_from': 4})
