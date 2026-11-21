"""u is for urchin (dx_urchin_u), Animals a to z, slot u. From Claude's sketch 'Urchin (smiling)' (21 Nov 2026), which
he picked, with the u's stick taken off at his word ("you dont need the little vertical stem").

The small u is the bottom half of the urchin's round body: down its left side, round the bottom and up its right side.
The top of its body is a big curve from one end of the u to the other. Long pointed spikes stand all round it.
Sketch coordinates (200 x 200) are turned into the app's 100 x 100 paper by T().
"""
import math
from kit15 import *

OX, OY = 0.0, 1.0
def T(x, y):
    return P(x * 0.5 + OX, y * 0.5 + OY)

PURPLE, PINK = FILL['purple'], FILL['pink']

# ---- the u (sketch: sides at x 48 and 152, straight from y 98 to 110, then a round bottom down to y 148) ----
CX, CY, R = 100, 98, 52
YS, RY = 110, 38
uL = Seg(T(48, CY), T(48, YS))
bowl = arc(*T(CX, YS), R * 0.5, RY * 0.5, 180, 0, start=T(48, YS), end=T(152, YS))     # round the bottom, left to right
uR = Seg(T(152, YS), T(152, CY))
u_chain = [uL] + bowl + [uR]                         # from the top of the left side round to the top of the right side
chain_ok(u_chain)

# ---- the top of the body: from the right end of the u over the top to the left end ----
dome = arc(*T(CX, CY), R * 0.5, R * 0.5, 0, -180, start=T(152, CY), end=T(48, CY))
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
BODY_C = T(CX, CY + 4)


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

eyeL = q2c((74, 96), (82, 86), (90, 96))
eyeR = q2c((110, 96), (118, 86), (126, 96))
smile = q2c((92, 108), (100, 116), (108, 108))
SPOTS = [(74, 66), (100, 58), (126, 66), (64, 120), (136, 118), (86, 134), (112, 136), (60, 86), (140, 86)]

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
             'A happy sea urchin covered in long pointy spikes. The small letter u is hiding in it: it is the bottom half of its round body.',
             steps, ['purple', 'pink'])
save('urchin', Pd, {'set': 'animals-az', 'slot': 'u', 'kind': 'swim', 'age_from': 4})
