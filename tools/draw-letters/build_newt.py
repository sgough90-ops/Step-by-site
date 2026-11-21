"""n is for newt (dx_newt_n), Animals a to z, slot n. From Claude's round 5 sketch 'Newt (walking)' (21 Nov 2026), drawn from
the lizard picture he sent (a lizard drawn from a capital N in its two front legs; capital N is already the narwhal, and a lizard
doesn't start with n, so it is a newt), with its feet and pointed toes all facing forward, as he asked.

The small n is the gap under its chest between its two front legs: the n's first line is the back edge of its front leg,
its arch is the underside of its chest, and its last line is the front edge of its other front leg. The newt's outline runs
from the bottom of the n's last line all the way round to the bottom of its first line, so the n closes it.
Sketch coordinates (200 x 200) go onto the app's 100 x 100 paper by T().
"""
import os, json
from r5kit import *

pp = Paper(0.48, 1.0, 1.0)
T, S = pp.T, pp.s
GREEN = FILL['green']

X0, X1, NT, NB, NRY = 68, 100, 140, 162, 11
BACK = [(42, 78), (60, 84), (84, 82), (110, 80), (138, 83)]
HEAD = [(26, 84), (13, 95), (9, 107), (13, 118), (26, 126), (42, 130), (54, 131)]
TAIL = [(160, 106), (176, 98), (184, 78), (180, 54), (164, 38), (142, 34), (124, 42), (118, 56)]


def tail_edges(pts, w0, w1, n=16):
    c = cr_dense(pts, n)
    tot = sum(math.dist(c[i], c[i + 1]) for i in range(len(c) - 1)); acc = 0; Lq, Rq = [], []
    for i, p in enumerate(c):
        if i: acc += math.dist(c[i - 1], p)
        a, b = c[max(i - 1, 0)], c[min(i + 1, len(c) - 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]; ln = math.hypot(dx, dy) or 1
        nx, ny = -dy / ln, dx / ln
        w = (w0 + (w1 - w0) * ((acc / tot) ** .8)) / 2
        Lq.append((p[0] + nx * w, p[1] + ny * w)); Rq.append((p[0] - nx * w, p[1] - ny * w))
    return c, Lq, Rq


def thin(q, every=8):
    return q[::every] + ([q[-1]] if (len(q) - 1) % every else [])


def foot_parts(x, y, hw, low=False):
    """a foot pointing forward (left) with three straight-sided pointed toes, at the bottom of a leg whose middle is x
    and whose bottom is y. Returns (heel curve points, corner points), going from the leg's back edge bottom (x + hw, y)
    round the heel and the toes to its front edge bottom (x - hw, y). low: toes fanned lower (the foot under the n)."""
    angles = (138, 162, 186) if low else (146, 176, 206)
    L, w = (15, 17.5, 15), 5.4
    pc = (-hw + 1.5, 4.6)
    us = [(math.cos(math.radians(a)), math.sin(math.radians(a))) for a in angles]
    heel = [(hw, 0), (hw - .6, 5.2), (hw - 5, 8.6)]
    pts = []
    for i, (u, ln) in enumerate(zip(us, L)):
        v = (-u[1], u[0])
        b = (pc[0] + u[0] * 2.4, pc[1] + u[1] * 2.4)
        lo = (b[0] - v[0] * w, b[1] - v[1] * w); hi = (b[0] + v[0] * w, b[1] + v[1] * w)
        tip = (b[0] + u[0] * ln, b[1] + u[1] * ln)
        if i == 0: pts.append(lo)
        pts.append(tip)
        if i < 2:
            u2 = us[i + 1]; m = (u[0] + u2[0], u[1] + u2[1]); ml = math.hypot(*m)
            pts.append((pc[0] + m[0] / ml * 6.8, pc[1] + m[1] / ml * 6.8))
        else:
            pts.append(hi)
    pts.append((-hw, 0))
    mv = lambda q: [(x + a, y + b) for a, b in q]
    return mv(heel), mv(pts)


def foot_chain(x, y, hw, low=False, start=None):
    """the foot as pieces, from the leg's front edge bottom round the toes and the heel to its back edge bottom"""
    heel, pts = foot_parts(x, y, hw, low)
    corners = pp.straight(pts[::-1])
    if start is not None: corners = snap(corners, start=start)
    h = snap(pp.smooth(heel[::-1]), start=corners[-1].b)
    return corners + h


def chainup(*groups):
    """join pieces made separately: each one starts exactly where the one before ends"""
    out = []
    for g in groups:
        g = list(g)
        if out: g = snap(g, start=out[-1].b)
        out += g
    chain_ok(out)
    return out

# ---------- the n ----------
N0, N1, N2, N3 = T(X0, NB), T(X0, NT), T(X1, NT), T(X1, NB)
arch = arc((X0 + X1) / 2 * S + 1, NT * S + 1, (X1 - X0) / 2 * S, NRY * S, 180, 360, start=N1, end=N2)
n_line = [Seg(N0, N1)] + arch + [Seg(N2, N3)]

# ---------- the outline, in order from the bottom of the n's last line round to the bottom of its first line ----------
c, Lq, Rq = tail_edges(TAIL, 32, 3)
hipB, hipT = Lq[0], Rq[0]
bx1 = hipB[0]; bx0 = bx1 - 17
tip = c[-1]; wt = 1.5
a0 = math.degrees(math.atan2(Lq[-1][1] - tip[1], Lq[-1][0] - tip[0]))
cap = [(tip[0] + wt * math.cos(math.radians(a0 - 180 * k / 6)), tip[1] + wt * math.sin(math.radians(a0 - 180 * k / 6))) for k in range(1, 6)]

rfoot = foot_chain(X1 + 7, NB, 7, low=True, start=N3)                          # other front leg's foot, toes forward
rleg = pp.smooth([(114, 162), (113, 148), (116, 132)])
belly = pp.smooth([(116, 132), (130, 135), (bx0, 133)])
bleg1 = pp.smooth([(bx0, 133), (bx0 - 1.5, 148), (bx0 - 1, 160)])
bfoot = foot_chain((bx0 + bx1) / 2, 160, (bx1 - bx0 + 2) / 2)
bleg2 = pp.smooth([(bx1 + 1, 160), (bx1 + 2, 146), hipB])
tail = pp.smooth(thin(Lq) + cap + thin(Rq[::-1]))
back = pp.smooth([hipT] + BACK[::-1])
head = pp.smooth([BACK[0]] + HEAD)
fleg = pp.smooth([(54, 131), (54, 147), (56, 161)])
ffoot = foot_chain((56 + X0) / 2, NB, (X0 - 56) / 2)
ffoot = snap(ffoot, end=N0)

parts = [rfoot, rleg, belly, bleg1, bfoot, bleg2, tail, back, head, fleg, ffoot]
joined = []
for g in parts:
    g = list(g)
    if joined: g = snap(g, start=joined[-1][-1].b)
    joined.append(g)
joined[-1] = snap(joined[-1], end=N0)
rfoot, rleg, belly, bleg1, bfoot, bleg2, tail, back, head, fleg, ffoot = joined
chain_ok([s for g in joined for s in g])
assert rfoot[0].a == N3 and ffoot[-1].b == N0

# ---------- the far back leg: a sliver of leg and its heel behind the near one, from under the tail to the near leg ----------
far_raw = pp.smooth([(bx1 + 6, 112), (bx1 + 7.5, 132), (bx1 + 8.5, 150), (bx1 + 6.5, 157), (bx1 - 2, 156)])
xs_t = crossings(far_raw, tail); xs_b = crossings(far_raw, bleg2)
assert len(xs_t) == 1 and len(xs_b) == 1, (len(xs_t), len(xs_b))
tail, (JT,) = cut_at_points(tail, [xs_t[0][4]])
bleg2, (JB,) = cut_at_points(bleg2, [xs_b[0][4]])
ia, ta = xs_t[0][0], xs_t[0][1]; far = [far_raw[ia].split(ta)[1]] + far_raw[ia + 1:]
xs_b = crossings(far, bleg2); ib, tb = xs_b[0][0], xs_b[0][1]; far = far[:ib] + [far[ib].split(tb)[0]]
far = snap(far, start=JT, end=JB)

# ---------- face and spots ----------
EYE, NOST = T(32, 97), T(14, 100)
smile_raw = pp.smooth([(7, 109.6), (12, 112.8), (22, 116.6), (32, 116.8), (41, 113)])
xs = crossings(smile_raw, head); assert len(xs) == 1, len(xs)
head, (JS,) = cut_at_points(head, [xs[0][4]])
smile = [smile_raw[xs[0][0]].split(xs[0][1])[1]] + smile_raw[xs[0][0] + 1:]
smile = snap(smile, start=JS)
SPOTS = [(56, 94), (74, 92), (96, 90), (118, 93), (140, 96), (64, 110), (88, 106), (112, 110), (170, 86), (174, 64), (160, 46)]

steps = [
    step('Start with an n', 'Draw a small letter n: a short straight line, then a hump that comes straight down.', [line(*n_line)]),
    step('A front leg', 'From the bottom of the first line, draw a foot with three pointed toes, then the front of the leg up to its neck.',
         [line(*(rev(ffoot) + rev(fleg)))]),
    step('The head', 'Draw its big round head, from its neck round its chin and nose to the top of its head.', [line(*rev(head))]),
    step('Back and tail', 'Draw its back, then a long tail curling up over it and back down to its tummy.', [line(*(rev(back) + rev(tail)))]),
    step('The other front leg', 'From the bottom of the last line, draw a foot with pointed toes, the back of the leg and its tummy.',
         [line(*(rfoot + rleg + belly))]),
    step('The back legs', 'Draw a back leg with a pointed foot up to the tail, and a bit of the other back leg behind it.',
         [line(*(bleg1 + bfoot + bleg2)), line(*far)]),
    step('Eye, mouth and spots', 'Draw a dot for its eye, a long smile, a little nose dot and spots on its back and tail.',
         [dot(*EYE, w=4.6), dot(*NOST, w=1.8), line(*smile)] + [dot(*T(*p), w=2.4) for p in SPOTS]),
]
outline = [s for g in (rfoot, rleg, belly, bleg1, bfoot, bleg2, tail, back, head, fleg, ffoot) for s in g]
body = fill(GREEN, *(outline + [Seg(N0, N1)] + arch + [Seg(N2, N3)]))
far_fill = fill(GREEN, *(far + piece(bleg2, JB, bleg2[-1].b) + piece(tail, tail[0].a, JT)))
steps.append(step('Colour green', 'Colour the newt green.', [body, far_fill], use='green'))

Pd = drawing('dx_newt_n', 'n is for newt', 2, 10, 'animals', ['Letters', 'Animals'],
             'A newt walking along. The small n is the gap between its two front legs: their inside edges and the underside of its chest.',
             steps, ['green'])
save('newt', Pd, {'set': 'animals-az', 'slot': 'n', 'kind': 'hop', 'age_from': 4})
