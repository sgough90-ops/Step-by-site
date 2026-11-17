"""Helpers for the family drawings (16 Nov 2026): Mum, Dad, Brother (Around the house A to Z),
nan, grandad and sister (Around the house a to z). Same kit as kit15, plus a peach pencil (as the gnome uses)
and a few circle helpers."""
import math
import kit15
from kit15 import *

kit15.MATS['peach'] = ('pencil', 'Peach pencil', '1', '#ffc9a3')
FILL['peach'] = '#ffd8b5'
kit15.MATS['white'] = ('pencil', 'White pencil', '1', '#f1f3f5')
FILL['white'] = '#f8f9fa'


def oc(c, r, a, ry=None):
    """The point at angle a (degrees, 0 = right, 90 = down) on a circle (or oval with ry) round c."""
    return P(c[0] + r * math.cos(math.radians(a)), c[1] + (r if ry is None else ry) * math.sin(math.radians(a)))


def carc(c, r, a0, a1, ry=None):
    """Arc of a circle from angle a0 to a1, with its ends snapped exactly onto oc(c, r, a0) and oc(c, r, a1)."""
    return arc(c[0], c[1], r, r if ry is None else ry, a0, a1, start=oc(c, r, a0, ry), end=oc(c, r, a1, ry))


def ring_from(c, r, a0, ry=None):
    """A whole circle starting (and ending) exactly at angle a0, going clockwise on screen."""
    segs = carc(c, r, a0, a0 + 360, ry)
    last = segs[-1]; segs[-1] = Seg(last.p[0], last.p[1], last.p[2], segs[0].a)
    return segs


def hit_circle(p, d, c, r):
    """Where the line p + s*d meets the circle: the two values of s, smaller first."""
    fx, fy = p[0] - c[0], p[1] - c[1]
    A = d[0] * d[0] + d[1] * d[1]; B = 2 * (fx * d[0] + fy * d[1]); C = fx * fx + fy * fy - r * r
    disc = B * B - 4 * A * C
    assert disc >= 0, ('misses the circle', p, d, c, r)
    q = math.sqrt(disc)
    return (-B - q) / (2 * A), (-B + q) / (2 * A)


def ang(c, p):
    return math.degrees(math.atan2(p[1] - c[1], p[0] - c[0]))


def unit(dx, dy):
    L = math.hypot(dx, dy); return (dx / L, dy / L)


def limb(a, b, d, c, r):
    """A straight arm or leg: two edges starting at a and b, going in direction d, each ending on the hand circle (c, r).
    Returns (edge from a, edge from b, angle where edge a meets the hand, angle where edge b meets the hand)."""
    d = unit(*d)
    sa = hit_circle(a, d, c, r)[0]; sb = hit_circle(b, d, c, r)[0]
    ea = P(a[0] + d[0] * sa, a[1] + d[1] * sa); eb = P(b[0] + d[0] * sb, b[1] + d[1] * sb)
    return Seg(a, ea), Seg(b, eb), ang(c, ea), ang(c, eb)


def at_x(seg, x):
    return P(*seg.at(seg_x(seg, x)))


def at_y(seg, y):
    return P(*seg.at(seg_y(seg, y)))


def split_x(seg, xs):
    """Cut one piece where it reaches each x in xs (in order along the piece)."""
    ts = [seg_x(seg, x) for x in xs]
    return split_many(seg, ts)


def bow(T, side, w=3.2, h=1.7):
    """Half a bow on a kite tail: a little triangle with its tip at T, pointing out to side (-1 left, 1 right). Starts at T."""
    return poly(T, (T[0] + side * w, T[1] - h), (T[0] + side * w, T[1] + h), closed=True)


def fsave(name, P_, place):
    save(name, P_, place)


def arc_via(c, r, p0, p1, via):
    """The arc of the circle from point p0 to point p1 (both on it) that passes the angle via (degrees)."""
    a0, a1 = ang(c, p0) % 360, ang(c, p1) % 360; v = via % 360
    cw = (a1 - a0) % 360            # going clockwise on screen (angle growing)
    if (v - a0) % 360 <= cw:
        return arc(c[0], c[1], r, r, a0, a0 + cw, start=P(*p0), end=P(*p1))
    return arc(c[0], c[1], r, r, a0, a0 - (360 - cw), start=P(*p0), end=P(*p1))


def xf(segs, f):
    """The same pieces with every point moved by f(x, y) -> (x, y)."""
    out = []
    for s in segs:
        m = Seg.__new__(Seg); m.p = [P(*f(x, y)) for x, y in s.p]; out.append(m)
    return out


def shift(segs, dx, dy):
    return xf(segs, lambda x, y: (x + dx, y + dy))


def _rn(a, b):
    """Right-hand normal (on screen, y down) of the direction a -> b."""
    dx, dy = b[0] - a[0], b[1] - a[1]; L = math.hypot(dx, dy)
    return (-dy / L, dx / L)


def _meet(p, d1, q, d2):
    den = d1[0] * d2[1] - d1[1] * d2[0]
    if abs(den) < 1e-9: return None
    t = ((q[0] - p[0]) * d2[1] - (q[1] - p[1]) * d2[0]) / den
    return (p[0] + d1[0] * t, p[1] + d1[1] * t)


def offset_chain(segs, d):
    """A copy of a smooth chain moved d to its right-hand side (Tiller-Hanson, good when d is small next to the bends).
    Joints are kept shared, so the result is still a chain."""
    out = []
    for s in segs:
        if len(s.p) == 2:
            n = _rn(s.p[0], s.p[1])
            q = [(x + d * n[0], y + d * n[1]) for x, y in s.p]
        else:
            p0, p1, p2, p3 = s.p
            n1, n2, n3 = _rn(p0, p1), _rn(p1, p2), _rn(p2, p3)
            a0 = (p0[0] + d * n1[0], p0[1] + d * n1[1]); a3 = (p3[0] + d * n3[0], p3[1] + d * n3[1])
            l1 = (p1[0] - p0[0], p1[1] - p0[1]); l2 = (p2[0] - p1[0], p2[1] - p1[1]); l3 = (p3[0] - p2[0], p3[1] - p2[1])
            b1 = (p1[0] + d * n2[0], p1[1] + d * n2[1])
            m1 = _meet(a0, l1, b1, l2) or (p1[0] + d * n1[0], p1[1] + d * n1[1])
            b2 = (p2[0] + d * n2[0], p2[1] + d * n2[1])
            m2 = _meet(b2, l2, a3, l3) or (p2[0] + d * n3[0], p2[1] + d * n3[1])
            q = [a0, m1, m2, a3]
        if out: q[0] = out[-1].b
        out.append(Seg(*q))
    return out


def ring_ccw(c, r, a0):
    """A whole circle starting (and ending) exactly at angle a0, going anticlockwise on screen (the way a written o or g goes)."""
    segs = arc(c[0], c[1], r, r, a0, a0 - 360, start=oc(c, r, a0), end=oc(c, r, a0))
    return segs
