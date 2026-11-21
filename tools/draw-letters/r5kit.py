"""Helpers for the round 5 drawings (21 Nov 2026): m is for monkey and n is for newt.

The drawings were sketched on a 200-wide page (Claude's round 5 sketches). T() moves sketch points onto the app's paper.
Smooth lines through sketch points become cubic pieces (Catmull-Rom), and lines that end on another line are trimmed
there and the other line is cut at the very same point, so colour edges stay exactly on their lines.
"""
import math
from kit15 import *


class Paper:
    def __init__(self, s, ox, oy):
        self.s, self.ox, self.oy = s, ox, oy

    def T(self, x, y):
        return P(x * self.s + self.ox, y * self.s + self.oy)

    def smooth(self, pts):
        """cubic pieces through sketch points (Catmull-Rom, end points doubled), on the paper"""
        q = [(x * self.s + self.ox, y * self.s + self.oy) for x, y in pts]
        Q = [q[0]] + q + [q[-1]]
        out = []
        for i in range(1, len(q)):
            p0, p1, p2, p3 = Q[i - 1], Q[i], Q[i + 1], Q[i + 2]
            c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
            c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
            a = out[-1].b if out else P(*p1)
            out.append(Seg(a, c1, c2, p2))
        return out

    def straight(self, pts):
        q = [self.T(*p) for p in pts]
        return [Seg(a, b) for a, b in zip(q, q[1:])]


def cr_dense(pts, n=24):
    Q = [pts[0]] + list(pts) + [pts[-1]]
    out = []
    for i in range(1, len(Q) - 2):
        p0, p1, p2, p3 = Q[i - 1], Q[i], Q[i + 1], Q[i + 2]
        for k in range(n):
            t = k / n; t2, t3 = t * t, t * t * t
            out.append(tuple(.5 * ((2 * p1[j]) + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t2
                                   + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t3) for j in (0, 1)))
    out.append(tuple(pts[-1]))
    return out


def band_edges(pts, w0, w1, n=24, power=1.0, every=6):
    """the two edges of a band (arm, leg, tail) along a smooth line through sketch points, as sketch points
    (left of the direction of travel first, as seen on screen), thinned to every few samples"""
    c = cr_dense(pts, n)
    tot = sum(math.dist(c[i], c[i + 1]) for i in range(len(c) - 1)); acc = 0
    Lq, Rq = [], []
    for i, p in enumerate(c):
        if i: acc += math.dist(c[i - 1], p)
        a, b = c[max(i - 1, 0)], c[min(i + 1, len(c) - 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]; ln = math.hypot(dx, dy) or 1
        nx, ny = dy / ln, -dx / ln
        w = (w0 + (w1 - w0) * (acc / tot) ** power) / 2
        Lq.append((p[0] + nx * w, p[1] + ny * w)); Rq.append((p[0] - nx * w, p[1] - ny * w))
    pick = lambda q: q[::every] + ([q[-1]] if (len(q) - 1) % every else [])
    return pick(Lq), pick(Rq), c


def dense(ch, n=120):
    out = []
    for i, s in enumerate(ch):
        for k in range(n + (1 if i == len(ch) - 1 else 0)):
            out.append((i, k / n, s.at(k / n)))
    return out


def crossings(chA, chB, n=160):
    """all places where two chains cross: list of (iA, tA, iB, tB, point)"""
    A = dense(chA, n); B = dense(chB, n)
    res = []
    for k in range(len(A) - 1):
        (ia, ta, pa), (ia2, ta2, pa2) = A[k], A[k + 1]
        if ia2 != ia: ta2 = 1.0
        for m in range(len(B) - 1):
            (ib, tb, pb), (ib2, tb2, pb2) = B[m], B[m + 1]
            if ib2 != ib: tb2 = 1.0
            if max(pa[0], pa2[0]) < min(pb[0], pb2[0]) or max(pb[0], pb2[0]) < min(pa[0], pa2[0]): continue
            if max(pa[1], pa2[1]) < min(pb[1], pb2[1]) or max(pb[1], pb2[1]) < min(pa[1], pa2[1]): continue
            d = (pa2[0] - pa[0]) * (pb2[1] - pb[1]) - (pa2[1] - pa[1]) * (pb2[0] - pb[0])
            if abs(d) < 1e-12: continue
            u = ((pb[0] - pa[0]) * (pb2[1] - pb[1]) - (pb[1] - pa[1]) * (pb2[0] - pb[0])) / d
            v = ((pb[0] - pa[0]) * (pa2[1] - pa[1]) - (pb[1] - pa[1]) * (pa2[0] - pa[0])) / d
            if 0 <= u <= 1 and 0 <= v <= 1:
                q = (pa[0] + u * (pa2[0] - pa[0]), pa[1] + u * (pa2[1] - pa[1]))
                if all(math.dist(q, r[4]) > .2 for r in res):
                    res.append((ia, ta + u * (ta2 - ta), ib, tb + v * (tb2 - tb), q))
    return res


def nearest_t(seg, pt, n=400):
    best = min(range(n + 1), key=lambda k: math.dist(seg.at(k / n), pt))
    lo, hi = max(0, best - 1) / n, min(n, best + 1) / n
    for _ in range(60):
        a, b = lo + (hi - lo) / 3, hi - (hi - lo) / 3
        if math.dist(seg.at(a), pt) < math.dist(seg.at(b), pt): hi = b
        else: lo = a
    return (lo + hi) / 2


def cut_at_points(ch, pts):
    """cut a chain at the points nearest to pts; returns the new chain and the exact cut points (in the order given)"""
    places = []
    for p in pts:
        i = min(range(len(ch)), key=lambda k: min(math.dist(ch[k].at(j / 300), p) for j in range(301)))
        places.append((i, nearest_t(ch[i], p)))
    by = {}
    for i, t in places:
        by.setdefault(i, []).append(t)
    new = []
    for i, s in enumerate(ch):
        new += split_many(s, sorted(by[i])) if i in by else [s]
    chain_ok(new)
    exact = []
    for i, t in places:
        e = ch[i].at(t)
        exact.append(min((q.a for q in new[1:]), key=lambda q: math.dist(q, e)))
    return new, exact


def piece(ch, p, q):
    """the run of pieces of a chain from point p to point q (p before q along the chain)"""
    i = next(k for k, s in enumerate(ch) if s.a == p)
    j = next(k for k, s in enumerate(ch) if s.b == q and k >= i)
    return ch[i:j + 1]


def ring_piece(ch, p, q):
    """for a closed ring: the pieces from p round (in the ring's direction) to q, wrapping past the start if needed"""
    i = next(k for k, s in enumerate(ch) if s.a == p)
    out = []; k = i
    while True:
        out.append(ch[k])
        if ch[k].b == q: return out
        k = (k + 1) % len(ch)
        assert k != i, 'q not found on the ring'


def trim_to(edge, other, keep='start'):
    """trim a chain where it first (keep='start') or last (keep='end') crosses another chain.
    Returns (trimmed chain, the crossing point as a raw point)."""
    xs = crossings(edge, other)
    assert xs, 'no crossing found'
    xs.sort(key=lambda r: (r[0], r[1]))
    ia, ta, ib, tb, q = xs[0] if keep == 'start' else xs[-1]
    a, b = edge[ia].split(ta)
    if keep == 'start':
        return edge[:ia] + [a], q
    return [b] + edge[ia + 1:], q


def snap(ch, start=None, end=None):
    if start is not None: ch = snap_start(ch, start)
    if end is not None: ch = snap_end(ch, end)
    return ch


def q2c(p0, q, p2):
    """a quadratic curve as a cubic piece"""
    return Seg(p0, (p0[0] + 2 / 3 * (q[0] - p0[0]), p0[1] + 2 / 3 * (q[1] - p0[1])), (p2[0] + 2 / 3 * (q[0] - p2[0]), p2[1] + 2 / 3 * (q[1] - p2[1])), p2)
