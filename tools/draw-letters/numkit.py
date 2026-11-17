"""Helpers for the animal number drawings (17 Nov 2026): Meerkat 1, Swan 2, Butterfly 3, Stork 4, Pig 6, Shark 7,
Panda 8, Poodle 9 (Animals 1 to 9). Same kit as kit15 and famkit, plus ellipses (also turned ones),
where two shapes meet, and arcs whose ends sit exactly on those meeting points."""
import math
from famkit import *


class Ell:
    """An ellipse (or circle) round (cx, cy), radii rx and ry, turned rot degrees (clockwise on screen).
    Angles are the ellipse's own angles in degrees: 0 = its right end, 90 = its bottom (before turning)."""

    def __init__(self, cx, cy, rx, ry=None, rot=0.0):
        self.cx, self.cy, self.rx = cx, cy, rx
        self.ry = rx if ry is None else ry
        self.r = math.radians(rot)

    def pt(self, a):
        t = math.radians(a); c, s = math.cos(self.r), math.sin(self.r)
        x, y = self.rx * math.cos(t), self.ry * math.sin(t)
        return (self.cx + c * x - s * y, self.cy + s * x + c * y)

    def P(self, a):
        return P(*self.pt(a))

    def dv(self, a):
        t = math.radians(a); c, s = math.cos(self.r), math.sin(self.r)
        x, y = -self.rx * math.sin(t), self.ry * math.cos(t)
        return (c * x - s * y, s * x + c * y)

    def local(self, p):
        c, s = math.cos(self.r), math.sin(self.r)
        dx, dy = p[0] - self.cx, p[1] - self.cy
        return (c * dx + s * dy, -s * dx + c * dy)

    def F(self, p):
        x, y = self.local(p)
        return (x / self.rx) ** 2 + (y / self.ry) ** 2 - 1

    def ang(self, p):
        x, y = self.local(p)
        return math.degrees(math.atan2(y / self.ry, x / self.rx))

    def arc(self, a0, a1, start=None, end=None):
        """From angle a0 to a1 (a1 > a0 goes clockwise on screen), in pieces of 90 degrees or less."""
        n = max(1, int(math.ceil(abs(a1 - a0) / 90 - 1e-9)))
        out = []
        for i in range(n):
            t0 = a0 + (a1 - a0) * i / n; t1 = a0 + (a1 - a0) * (i + 1) / n
            k = 4 / 3 * math.tan(math.radians(t1 - t0) / 4)
            p0, p3 = self.pt(t0), self.pt(t1); d0, d1 = self.dv(t0), self.dv(t1)
            c1 = (p0[0] + k * d0[0], p0[1] + k * d0[1]); c2 = (p3[0] - k * d1[0], p3[1] - k * d1[1])
            if i == 0 and start is not None: p0 = start
            if i == n - 1 and end is not None: p3 = end
            if i > 0: p0 = out[-1].b
            out.append(Seg(p0, c1, c2, p3))
        return out

    def arc_pts(self, p0, p1, cw=True):
        """The arc from point p0 to point p1 (both on the ellipse), going clockwise (cw) or anticlockwise on screen."""
        a0, a1 = self.ang(p0), self.ang(p1)
        if cw:
            while a1 <= a0: a1 += 360
        else:
            while a1 >= a0: a1 -= 360
        return self.arc(a0, a1, start=P(*p0), end=P(*p1))

    def ring(self, a0=-90, cw=True):
        """The whole ellipse as a closed ring of four pieces, starting and ending exactly at angle a0."""
        s = self.P(a0)
        segs = self.arc(a0, a0 + (360 if cw else -360), start=s, end=s)
        return segs

    def ring_at(self, pts, cw=True):
        """The whole ellipse as pieces that start at pts[0] and pass exactly through every point in pts (in order)."""
        out = []
        for i in range(len(pts)):
            out += self.arc_pts(pts[i], pts[(i + 1) % len(pts)], cw)
        return out


def roots(f, lo, hi, n=3000):
    out = []
    xs = [lo + (hi - lo) * i / n for i in range(n + 1)]
    fs = [f(x) for x in xs]
    for i in range(n):
        if fs[i] == 0:
            out.append(xs[i]); continue
        if fs[i] * fs[i + 1] < 0:
            a, b, fa = xs[i], xs[i + 1], fs[i]
            for _ in range(90):
                m = (a + b) / 2; fm = f(m)
                if (fm > 0) == (fa > 0): a, fa = m, fm
                else: b = m
            out.append((a + b) / 2)
    return out


def meet_ee(A, B):
    """Points where ellipse A crosses ellipse B (rounded), in order of A's angle from -180."""
    return [A.P(a) for a in roots(lambda a: B.F(A.pt(a)), -180, 180)]


def meet_se(seg, E):
    """(t, point) where a piece crosses ellipse E."""
    return [(t, P(*seg.at(t))) for t in roots(lambda t: E.F(seg.at(t)), 0, 1)]


def seg_to(seg, t):
    """The piece from its start to t, ending exactly on the rounded point there."""
    a, _ = seg.split(t); return a


def seg_from(seg, t):
    _, b = seg.split(t); return b


def two(seg, t):
    """A piece cut in two at t, sharing the exact cut point."""
    return seg.split(t)


def at_t_x(seg, x):
    return seg_x(seg, x)


def at_t_y(seg, y):
    return seg_y(seg, y)


def qc(p0, q, p2):
    """A quadratic curve (p0, control q, p2) as a cubic piece."""
    return Seg(p0, (p0[0] + 2 / 3 * (q[0] - p0[0]), p0[1] + 2 / 3 * (q[1] - p0[1])),
               (p2[0] + 2 / 3 * (q[0] - p2[0]), p2[1] + 2 / 3 * (q[1] - p2[1])), p2)


def chain_split_at(segs, pt, tol=0.02):
    """Cut a chain at the place nearest to pt (pt must be on it); returns (before, after) sharing pt exactly."""
    best = None
    for i, s in enumerate(segs):
        for k in range(401):
            q = s.at(k / 400); d = math.dist(q, pt)
            if best is None or d < best[0]: best = (d, i, k / 400)
    d, i, t = best
    lo, hi = max(0, t - 1 / 400), min(1, t + 1 / 400)
    for _ in range(60):
        m1, m2 = lo + (hi - lo) / 3, hi - (hi - lo) / 3
        if math.dist(segs[i].at(m1), pt) < math.dist(segs[i].at(m2), pt): hi = m2
        else: lo = m1
    t = (lo + hi) / 2
    assert math.dist(segs[i].at(t), pt) < tol, ('point is not on the chain', pt, math.dist(segs[i].at(t), pt))
    a, b = segs[i].split(t)
    a = Seg(*(a.p[:-1] + [P(*pt)])) if len(a.p) == 4 else Seg(a.p[0], P(*pt))
    b = Seg(*([P(*pt)] + b.p[1:])) if len(b.p) == 4 else Seg(P(*pt), b.p[-1])
    return segs[:i] + [a], [b] + segs[i + 1:]


def piece_between(segs, p0, p1):
    """The part of a chain from point p0 to point p1 (p0 comes first along the chain)."""
    _, after = chain_split_at(segs, p0)
    before, _ = chain_split_at(after, p1)
    return before
