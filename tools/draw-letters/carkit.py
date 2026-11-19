"""Helpers for the race car numbers (19 Nov 2026).

The cars were sketched on a 200-wide page (y about 30 to 186). They are put on the app's 100 x 100 paper with
x' = 0.46 x + 4 and y' = 0.46 y + 5.4, so every car is the same size and all the wheels sit on the same road.
"""
import math
from kit import *

S = 0.46


def tx(x): return x * S + 4


def ty(y): return y * S + 5.4


def T(x, y):
    """A sketch point on the app's paper (rounded)."""
    return P(tx(x), ty(y))


def C(*pts):
    """A cubic piece from sketch points."""
    return Seg(*[T(*q) for q in pts])


def Lp(*pts):
    """Straight pieces through sketch points."""
    return poly(*[T(*q) for q in pts])


def q2c(p0, c, p1):
    """A quadratic curve (sketch points) as one cubic piece."""
    a, cc, b = T(*p0), (tx(c[0]), ty(c[1])), T(*p1)
    c1 = (a[0] + 2 / 3 * (cc[0] - a[0]), a[1] + 2 / 3 * (cc[1] - a[1]))
    c2 = (b[0] + 2 / 3 * (cc[0] - b[0]), b[1] + 2 / 3 * (cc[1] - b[1]))
    return Seg(a, c1, c2, b)


def ang(cx, cy, p):
    return math.degrees(math.atan2(p[1] - cy, p[0] - cx))


def on_circle(cx, cy, r, deg):
    return P(cx + r * math.cos(math.radians(deg)), cy + r * math.sin(math.radians(deg)))


def circle_at_y(cx, cy, r, y):
    """Where a level line at height y meets a circle: (left point, right point)."""
    dx = math.sqrt(r * r - (y - cy) ** 2)
    return P(cx - dx, y), P(cx + dx, y)


def arc_between(cx, cy, r, pa, pb, cw=True):
    """The arc of a circle from point pa to point pb, clockwise on screen (cw) or anticlockwise, ending exactly on them."""
    a0, a1 = ang(cx, cy, pa), ang(cx, cy, pb)
    if cw:
        while a1 <= a0: a1 += 360
    else:
        while a1 >= a0: a1 -= 360
    return arc(cx, cy, r, r, a0, a1, start=pa, end=pb)


class Wheel:
    """A wheel from sketch centre and radius: the tyre and its middle (0.4 of the size, as in the sketches)."""
    def __init__(self, x, y, r, hub=0.4):
        self.c = T(x, y); self.r = r2(r * S); self.hr = r2(r * hub * S)
        self.tyre = circle(self.c[0], self.c[1], self.r)
        self.hub = circle(self.c[0], self.c[1], self.hr)

    def at_y(self, y_sketch):
        return circle_at_y(self.c[0], self.c[1], self.r, ty(y_sketch))

    def over_top(self, pa, pb):
        """The top of the tyre from pa to pb, going over the top (pa on the right, pb on the left)."""
        return arc_between(self.c[0], self.c[1], self.r, pa, pb, cw=False)

    def lines(self):
        return [ring(*self.tyre), ring(*self.hub)]

    def black(self):
        return fill(FILL['black'], *self.tyre, cut=[d_fill(*self.hub)])

    def grey(self):
        return fill(FILL['grey'], *self.hub)


def visor(hx, hy, r, left=False, k=1.0):
    """The visor from the sketches' helmet, as a closed shape (sketch centre and radius). left: the helmet faces left.
    k < 1 makes it a little smaller, so it keeps clear of the helmet's edge."""
    s = -1 if left else 1
    a = (hx - s * .15 * r * k, hy - .5 * r * k); b = (hx + s * .72 * r * k, hy - .5 * r * k)
    qc = (hx + s * .98 * r * k, hy - .2 * r * k); c_ = (hx + s * .9 * r * k, hy + .22 * r * k); d = (hx - s * .15 * r * k, hy + .22 * r * k)
    return [Seg(T(*a), T(*b)), q2c(b, qc, c_), Seg(T(*c_), T(*d)), Seg(T(*d), T(*a))]


class Dome:
    """A helmet peeping out of the cockpit: the part of a circle above a level rim line (sketch centre, radius, rim y)."""
    def __init__(self, x, y, r, rim_y):
        self.cx, self.cy = tx(x), ty(y); self.r = r * S; self.rim = ty(rim_y)
        self.pL, self.pR = circle_at_y(self.cx, self.cy, self.r, self.rim)
        self.arc = arc_between(self.cx, self.cy, self.r, self.pL, self.pR, cw=True)   # over the top, left to right
        self.vis = visor(x, y, r)

    def lines(self):
        return [line(*self.arc), ring(*self.vis)]

    def yellow(self):
        return fill(FILL['yellow'], *(self.arc + [Seg(self.pR, self.pL)]), cut=[d_fill(*self.vis)])

    def blue(self):
        return fill(FILL['lblue'], *self.vis)


def road():
    return line(Seg(T(4, 181.8), T(196, 181.8)))


def pts_line(*pts):
    """Straight pieces through app points (already rounded)."""
    return poly(*pts)
