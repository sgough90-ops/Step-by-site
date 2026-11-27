"""u is for urchin (dx_urchin_u), Animals a to z, slot u. From Claude's sketch 'Urchin (smiling)' (21 Nov 2026), which
he picked, with the u's stick taken off at his word ("you dont need the little vertical stem").
27 Nov 2026 (step 1 review, round 2, live): the body is narrower and taller, so the u has a normal shape (see below).

The small u is the bottom of the urchin's body: down its left side, round the bottom and up its right side.
The top of its body is a big curve from one end of the u to the other. Long pointed spikes stand all round it.
Sketch coordinates (200 x 200) are turned into the app's 100 x 100 paper by T().
"""
import math
from kit15 import *

OX, OY = 0.0, 1.0
def T(x, y):
    return P(x * 0.5 + OX, y * 0.5 + OY)

PURPLE, PINK = FILL['purple'], FILL['pink']

# ---- the u (sketch: sides at x 56 and 144, straight from y 78 to 104, then a round bottom down to y 148) ----
# 27 Nov 2026 (step 1 review, round 2): the u was 52 wide and 25 tall (twice as wide as it is tall), so step 1 looked
# like a shallow bowl. The body is now narrower and taller (straight sides, a lower dome on top), so the u is 44 wide and
# 35 tall. Was: sides at x 48 and 152, straight from y 98 to 110, round bottom to y 148, round top (radius 52).
CX = 100
R, CY, YS, RY, DRY = 44.0, 78.0, 104.0, 44.0, 30.0   # half-width, top of the sides, bottom of the sides, depth of the round bottom, height of the dome
uL = Seg(T(CX - R, CY), T(CX - R, YS))
bowl = arc(*T(CX, YS), R * 0.5, RY * 0.5, 180, 0, start=T(CX - R, YS), end=T(CX + R, YS))     # round the bottom, left to right
uR = Seg(T(CX + R, YS), T(CX + R, CY))
u_chain = [uL] + bowl + [uR]                         # from the top of the left side round to the top of the right side
chain_ok(u_chain)

# ---- the top of the body: from the right end of the u over the top to the left end ----
dome = arc(*T(CX, CY), R * 0.5, DRY * 0.5, 0, -180, start=T(CX + R, CY), end=T(CX - R, CY))
chain_ok(dome)
outline = u_chain + dome                             # the whole body, all the way round
assert outline[-1].b == outline[0].a


def length_table(ch, n=400):
    pts, cum = [], [0.0]
    for i, s in enumerate(ch):
        for k in range(n):
            t = k / n
            pts.append((i, t, s.at(t)))
    pts.append((len(ch) - 1, 1.0, ch[-1].b))
    for a, b in zip(pts, pts[1:]):
        cum.append(cum[-1] + math.dist(a[2], b[2]))
    return pts, cum


def at_len(tab, s):
    pts, cum = tab
    k = max(0, min(len(cum) - 2, next(j for j in range(len(cum)) if cum[j] >= s) - 1))
    i0, t0, p0 = pts[k]; i1, t1, p1 = pts[k + 1]
    f = (s - cum[k]) / max(1e-9, cum[k + 1] - cum[k])
    if i1 != i0:
        t1 = 1.0
    return i0, t0 + (t1 - t0) * f


def refine(ch, cuts):
    """Cut a chain at several (piece, t) places; returns the new chain and, for each cut name, the index of the piece that starts there."""
    by = {}
    for name, (i, t) in cuts.items():
        by.setdefault(i, []).append((t, name))
    new, node = [], {}
    for i, s in enumerate(ch):
        if i in by:
            lst = sorted(by[i]); pieces = split_many(s, [t for t, _ in lst])
            for k, (t, name) in enumerate(lst):
                new.append(pieces[k]); node[name] = len(new)
            new.append(pieces[-1])
        else:
            new.append(s)
    chain_ok(new)
    return new, node


# ---- spikes: nine along the u and nine along the top, spread evenly, half a gap from each end of the u ----
BASE, LONG = 6.0, 14.0           # app units: width of a spike where it meets the body, and how far it sticks out
def plan(ch, n):
    tab = length_table(ch)
    L = tab[1][-1]
    out = []
    for k in range(n):
        mid = L * (k + 0.5) / n
        out.append((at_len(tab, mid - BASE / 2), at_len(tab, mid), at_len(tab, mid + BASE / 2)))
    return out

u_plan, d_plan = plan(u_chain, 9), plan(dome, 9)
u_cuts = {('u', k, j): v for k, trip in enumerate(u_plan) for j, v in ((0, trip[0]), (1, trip[2]))}
d_cuts = {('d', k, j): v for k, trip in enumerate(d_plan) for j, v in ((0, trip[0]), (1, trip[2]))}
u_mid = [u_chain[i].at(t) for _, (i, t), _ in u_plan]
d_mid = [dome[i].at(t) for _, (i, t), _ in d_plan]
u_chain, u_node = refine(u_chain, u_cuts)
dome, d_node = refine(dome, d_cuts)
BODY_C = T(CX, (CY - DRY + YS + RY) / 2)


def spikes(ch, node, tag, mids):
    lines, fills = [], []
    for k, m in enumerate(mids):
        i0, i1 = node[(tag, k, 0)], node[(tag, k, 1)]
        A, B = ch[i0].a, ch[i1].a
        nx, ny = m[0] - BODY_C[0], m[1] - BODY_C[1]
        # point straight out from the outline: use the outline's own direction there
        tx, ty = B[0] - A[0], B[1] - A[1]; tl = math.hypot(tx, ty)
        ox, oy = ty / tl, -tx / tl
        if ox * nx + oy * ny < 0:
            ox, oy = -ox, -oy
        tip = P(m[0] + ox * LONG, m[1] + oy * LONG)
        sp = [Seg(A, tip), Seg(tip, B)]
        lines.append(line(*sp))
        fills.append(fill(PINK, *(sp + rev(ch[i0:i1]))))
    return lines, fills

u_lines, u_fills = spikes(u_chain, u_node, 'u', u_mid)
d_lines, d_fills = spikes(dome, d_node, 'd', d_mid)

# ---- face and spots (from the sketch) ----
def q2c(p0, q, p1):
    """a quadratic curve (sketch units) as one cubic piece (app units)"""
    c1 = (p0[0] + 2 / 3 * (q[0] - p0[0]), p0[1] + 2 / 3 * (q[1] - p0[1]))
    c2 = (p1[0] + 2 / 3 * (q[0] - p1[0]), p1[1] + 2 / 3 * (q[1] - p1[1]))
    return Seg(T(*p0), T(*c1), T(*c2), T(*p1))

MID = (CY - DRY + YS + RY) / 2                       # the middle of the body, top to bottom
EY = MID - 2
eyeL = q2c((CX - 22, EY), (CX - 14, EY - 10), (CX - 6, EY))
eyeR = q2c((CX + 6, EY), (CX + 14, EY - 10), (CX + 22, EY))
smile = q2c((CX - 8, EY + 12), (CX, EY + 20), (CX + 8, EY + 12))
def inside(x, y, m=9):
    if y <= CY:
        return ((x - CX) / (R - m)) ** 2 + ((y - CY) / (DRY - m)) ** 2 < 1
    if y <= YS:
        return abs(x - CX) < R - m
    return ((x - CX) / (R - m)) ** 2 + ((y - YS) / (RY - m)) ** 2 < 1
SPOTS = [(CX - 24, CY - DRY * 0.45), (CX, CY - DRY * 0.7), (CX + 24, CY - DRY * 0.45),
         (CX - R + 11, MID + 4), (CX + R - 11, MID + 4), (CX - 16, YS + RY * 0.55), (CX + 16, YS + RY * 0.55)]
for x, y in SPOTS:
    assert inside(x, y, 6), (x, y)
steps = [
    step('Start with a u', 'Draw a small letter u: straight down, round the bottom and straight back up.', [line(*u_chain)]),
    step('The top', 'Join the two ends of the u with a big round curve over the top. Now it is a round body.', [line(*dome)]),
    step('Spikes on top', 'Draw long pointy spikes all over the top of the body.', d_lines),
    step('Spikes underneath', 'Draw more pointy spikes all round the bottom, on the u.', u_lines),
    step('Happy face', 'Draw two curved lines for its happy shut eyes, and a smile.', [line(eyeL), line(eyeR), line(smile)]),
    step('Spots', 'Draw little dots all over its body.', [dot(*T(x, y), w=2.4) for x, y in SPOTS]),
    step('Colour purple', "Colour the urchin's body purple.", [fill(PURPLE, *(u_chain + dome))], use='purple'),
    step('Colour pink', 'Colour all the spikes pink.', d_fills + u_fills, use='pink'),
]
Pd = drawing('dx_urchin_u', 'u is for urchin', 2, 10, 'animals', ['Letters', 'Animals'],
             'A happy sea urchin covered in long pointy spikes. The small letter u is hiding in it: it is the bottom of its body.',
             steps, ['purple', 'pink'])
save('urchin', Pd, {'set': 'animals-az', 'slot': 'u', 'kind': 'swim', 'age_from': 4})
