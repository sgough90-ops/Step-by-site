"""E is for Eclair (dx_eclair_e), Food and drink A to Z, slot E (23 Nov 2026).
From his pick (18:37): "E3" = "The end piece" on the E-eclair sheet
(claude/step-by-draw-redo-u-y-E-X-school-bus-sketches.py, s_eclair.py E3).
His plan for the letter (17:48): "each horizontal line on the E is part of the layer of the eclair".

A short piece cut off the end of an eclair, with a whole eclair lying behind it.
The E, 26 wide and 39 tall:
  the line down     the flat cut end of the piece
  the top line      the top of the piece (the chocolate icing runs along under it)
  the middle line   the bottom of the lid, where the cream starts (the cream hangs under it in bumps)
  the bottom line   the bottom of the piece
The cream stays white. Written in the sketch's numbers; the whole eclair sits 10 further right than in the sketch,
so that none of its lines stop on the letter.

    python3 build_eclair.py
"""
from bcommon import *

p = Pic(s=1.0, dx=0.0, dy=-4.0)
X0, X1, TOP, MID, CR, BOT = 12, 38, 40, 55, 62, 79          # the piece: lid TOP to MID, cream under MID, base CR to BOT
BX0, BX1, BT, BM, BC, BB = 46, 86, 24, 38, 44.5, 60          # the whole eclair behind


def bumps(x_from, x_to, y, k, ry):
    """k cream bumps hanging under the level y, going from x_from back to x_to (right to left)"""
    w = (x_from - x_to) / k
    out = []
    for i in range(k):
        a, b = x_from - i * w, x_from - (i + 1) * w
        out += arc((a + b) / 2, y, w / 2, ry, 0, 180, start=P(a, y), end=P(b, y))
    return out


def end(cx, y0, y1, right=True):
    """the round end of a layer between the heights y0 and y1 (a half circle)"""
    r = (y1 - y0) / 2
    if right:
        return arc(cx, y0 + r, r, r, -90, 90, start=P(cx, y0), end=P(cx, y1))
    return arc(cx, y0 + r, r, r, 90, 270, start=P(cx, y1), end=P(cx, y0))


def wavy_to(a, b, k, amp=1.25):
    pts = [a] + [(a[0] + (b[0] - a[0]) * i / k, (a[1] + b[1]) / 2 + (amp if i % 2 else -amp) - 0.3) for i in range(1, k)] + [b]
    return smooth(pts)


# ---- the plate ----
p.shape('plate', ell(50, 81, 47, 6.4), step=7)

# ---- the whole eclair behind: bottom, cream, lid, icing ----
BBASE = end(BX1, BC, BB) + [Seg((BX1, BB), (BX0, BB))] + end(BX0, BC, BB, right=False)
p.region('bbaseR', BBASE, Seg((BX0, BC), (BX1, BC)))
p.stroke('bbase', BBASE, step=6)
BCREAM = (arc(BX1, (BM + BC + 1) / 2, 4.4, (BC + 1 - BM) / 2, -90, 90, start=P(BX1, BM), end=P(BX1, BC + 1)) + bumps(BX1, BX0, BC + 1, 5, 3.6)
          + arc(BX0, (BM + BC + 1) / 2, 4.4, (BC + 1 - BM) / 2, 90, 270, start=P(BX0, BC + 1), end=P(BX0, BM)))
p.region('bcreamR', BCREAM, Seg((BX0, BM), (BX1, BM)))
p.stroke('bcream', BCREAM, step=6)
p.shape('blid', Seg((BX0, BT), (BX1, BT)), end(BX1, BT, BM), Seg((BX1, BM), (BX0, BM)), end(BX0, BT, BM, right=False), step=5)
r = (BM - BT) / 2
p.stroke('bicing', wavy_to((BX0 + r * math.cos(math.radians(190)), BT + r + r * math.sin(math.radians(190))),
                           (BX1 + r * math.cos(math.radians(-10)), BT + r + r * math.sin(math.radians(-10))), 9), step=5)

# ---- the piece in front: bottom, cream, lid, icing ----
BASE_END = end(X1, CR, BOT)
p.region('baseR', Seg((X0, CR), (X1, CR)), BASE_END, Seg((X1, BOT), (X0, BOT)), Seg((X0, BOT), (X0, CR)))
p.stroke('base_end', BASE_END, step=4)
CREAM = arc(X1, (MID + CR + 1) / 2, 4.6, (CR + 1 - MID) / 2, -90, 90, start=P(X1, MID), end=P(X1, CR + 1)) + bumps(X1, X0, CR + 1, 3, 3.9)
p.region('creamR', Seg((X0, MID), (X1, MID)), CREAM, Seg((X0, CR + 1), (X0, MID)))
p.stroke('cream', CREAM, step=3)
LID_END = end(X1, TOP, MID)
p.region('lidR', Seg((X0, TOP), (X1, TOP)), LID_END, Seg((X1, MID), (X0, MID)), Seg((X0, MID), (X0, TOP)))
p.stroke('lid_end', LID_END, step=2)
r = (MID - TOP) / 2
p.stroke('icing', wavy_to((X0, TOP + 5.6), (X1 + r * math.cos(math.radians(6)), TOP + r + r * math.sin(math.radians(6))), 6), step=2)

# ---- the E, in front of everything: across the top, down the cut end, across the bottom; then the middle line ----
p.stroke('e', poly((X1, TOP), (X0, TOP), (X0, BOT), (X1, BOT)), step=1)
p.stroke('e_mid', Seg((X0, MID), (X1, MID)), step=1)
p.build()

steps = [
    step('Start with an E', 'Draw a big letter E: a line across the top, a long line down, a line across the bottom, then a line across the middle.', p.step(1)),
    step('The top and its icing', 'Curve round from the end of the top line to the end of the middle line. Draw a wavy line across this part for the icing.', p.step(2)),
    step('Cream', 'Under the middle line draw the cream: a round blob at the end, then three bumps back to the long line.', p.step(3)),
    step('The bottom', 'From under the blob of cream, curve round and down to the end of the bottom line.', p.step(4)),
    step('A whole eclair', 'Behind it, a bit higher, draw a long shape with round ends. It is the top of a whole eclair. Draw a wavy line along it.', p.step(5)),
    step('More cream', 'Under the long shape draw a row of cream bumps with a blob at each end. Under them draw the round bottom of the eclair.', p.step(6)),
    step('The plate', 'Draw a long flat plate underneath.', p.step(7)),
    step('Colour brown', 'Colour the icing on the top of both eclairs brown, down to the wavy lines.',
         [p.face('brown', (25, 42.4)), p.face('brown', (66, 26.2))], use='brown'),
    step('Colour light brown', 'Colour the rest of each eclair light brown, above and below the cream. The cream stays white.',
         [p.face('lbrown', (25, 51)), p.face('lbrown', (25, 74)), p.face('lbrown', (66, 35)), p.face('lbrown', (70, 55))], use='lbrown'),
    step('Colour light blue', 'Colour the plate light blue.', [p.face('lblue', (60, 84))], use='lblue'),
]
D = drawing('dx_eclair_e', 'E is for Eclair', 3, 15, 'things', ['Letters', 'Around the house'],
            'A chocolate eclair with a piece cut off the end. The capital letter E is hiding in that piece: its flat cut end and its three layers.',
            steps, ['brown', 'lbrown', 'lblue'])
ok = finish('eclair', D, {'set': 'house-AZ', 'slot': 'E', 'kind': 'key', 'age_from': 5}, p)
