"""Small kit for writing Step by Draw drawings as code (stepby/1 format, 100 x 100 paper).

Every shape is made of Seg pieces (straight lines and cubic curves) whose points are rounded once,
when the piece is made. Lines and colour outlines are then written from the very same pieces,
so a colour edge is always exactly on its line.
"""
import math, json

W = 1.8          # normal line width in the app's data
K = 0.5522847498 # quarter-circle Bezier constant


def r2(v):
    v = round(v + 0.0, 2)
    if v == 0: v = 0.0
    return v


def fmt(v):
    s = ('%.2f' % r2(v)).rstrip('0').rstrip('.')
    return '0' if s in ('-0', '') else s


def P(x, y):
    return (r2(x), r2(y))


class Seg:
    """A straight line (2 points) or a cubic curve (4 points)."""
    def __init__(self, *pts):
        self.p = [P(*q) for q in pts]
        assert len(self.p) in (2, 4)

    @property
    def a(self): return self.p[0]

    @property
    def b(self): return self.p[-1]

    def rev(self):
        s = Seg.__new__(Seg); s.p = self.p[::-1]; return s

    def cmd(self):
        if len(self.p) == 2:
            return 'L %s %s' % (fmt(self.p[1][0]), fmt(self.p[1][1]))
        return 'C %s' % ' '.join('%s %s' % (fmt(x), fmt(y)) for x, y in self.p[1:])

    def at(self, t):
        if len(self.p) == 2:
            (x0, y0), (x1, y1) = self.p
            return (x0 + (x1 - x0) * t, y0 + (y1 - y0) * t)
        (x0, y0), (x1, y1), (x2, y2), (x3, y3) = self.p
        u = 1 - t
        return (u*u*u*x0 + 3*u*u*t*x1 + 3*u*t*t*x2 + t*t*t*x3,
                u*u*u*y0 + 3*u*u*t*y1 + 3*u*t*t*y2 + t*t*t*y3)

    def split(self, t):
        """Two pieces, cut at t (exact de Casteljau, then rounded)."""
        if len(self.p) == 2:
            m = self.at(t)
            return Seg(self.p[0], m), Seg(m, self.p[1])
        p0, p1, p2, p3 = self.p
        L = lambda a, b: (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
        q0, q1, q2 = L(p0, p1), L(p1, p2), L(p2, p3)
        r0, r1 = L(q0, q1), L(q1, q2)
        m = L(r0, r1)
        return Seg(p0, q0, r0, m), Seg(m, r1, q2, p3)

    def samples(self, n=None):
        if n is None:
            n = 2 if len(self.p) == 2 else 60
        return [self.at(i / (n - 1)) for i in range(n)]


def chain_ok(segs):
    for s1, s2 in zip(segs, segs[1:]):
        assert s1.b == s2.a, ('pieces do not join', s1.b, s2.a)


def d_line(*segs):
    """Path text for a line made of pieces that follow on from each other."""
    segs = [s for s in segs]
    chain_ok(segs)
    return 'M %s %s ' % (fmt(segs[0].a[0]), fmt(segs[0].a[1])) + ' '.join(s.cmd() for s in segs)


def d_fill(*segs):
    """Path text for a closed colour outline made of pieces."""
    segs = list(segs)
    chain_ok(segs)
    assert segs[-1].b == segs[0].a, ('outline is not closed', segs[-1].b, segs[0].a)
    return d_line(*segs) + ' Z'


def line(*segs, w=W):
    return {"d": d_line(*segs), "w": w}


def fill(colour, *segs, cut=None):
    o = {"d": d_fill(*segs), "fill": colour}
    if cut: o["cut"] = cut
    return o


def ring(*segs, w=W):
    """A closed line shape (a circle, a box): the pencil ends where it began."""
    return {"d": d_fill(*segs), "w": w}


def dot(x, y, w=3.0, upright=True):
    """A dot: a very short line drawn with a round pen (as the app's other drawings do)."""
    if upright:
        return {"d": 'M %s %s L %s %s' % (fmt(x), fmt(y - 0.1), fmt(x), fmt(y + 0.1)), "w": w}
    return {"d": 'M %s %s L %s %s' % (fmt(x - 0.1), fmt(y), fmt(x + 0.1), fmt(y)), "w": w}


# ---------- shape helpers ----------

def poly(*pts, closed=False):
    pts = [P(*q) for q in pts]
    segs = [Seg(a, b) for a, b in zip(pts, pts[1:])]
    if closed: segs.append(Seg(pts[-1], pts[0]))
    return segs


def arc(cx, cy, rx, ry, a0, a1, start=None, end=None):
    """Elliptical arc from angle a0 to a1 (degrees, 0 = right, 90 = down, as on screen), as cubic pieces of 90 degrees or less.
    start/end: give exact (already rounded) end points to snap onto."""
    n = max(1, int(math.ceil(abs(a1 - a0) / 90 - 1e-9)))
    out = []
    for i in range(n):
        t0 = math.radians(a0 + (a1 - a0) * i / n); t1 = math.radians(a0 + (a1 - a0) * (i + 1) / n)
        k = 4 / 3 * math.tan((t1 - t0) / 4)
        p0 = (cx + rx * math.cos(t0), cy + ry * math.sin(t0)); p3 = (cx + rx * math.cos(t1), cy + ry * math.sin(t1))
        c1 = (p0[0] - k * rx * math.sin(t0), p0[1] + k * ry * math.cos(t0))
        c2 = (p3[0] + k * rx * math.sin(t1), p3[1] - k * ry * math.cos(t1))
        if i == 0 and start is not None: p0 = start
        if i == n - 1 and end is not None: p3 = end
        if i > 0: p0 = out[-1].b
        out.append(Seg(p0, c1, c2, p3))
    return out


def circle(cx, cy, r, start_deg=-90, ry=None):
    """A whole circle (or ellipse with ry) as four pieces, starting at start_deg and going round clockwise on screen."""
    segs = arc(cx, cy, r, r if ry is None else ry, start_deg, start_deg + 360)
    last = segs[-1]; segs[-1] = Seg(last.p[0], last.p[1], last.p[2], segs[0].a)
    return segs


def rev(segs):
    return [s.rev() for s in reversed(segs)]


def join(*groups):
    out = []
    for g in groups:
        if isinstance(g, Seg): out.append(g)
        else: out.extend(g)
    return out


def seg_line_cross_y(seg, y, lo=0.0, hi=1.0):
    """t where a piece crosses height y (one crossing between lo and hi)."""
    f = lambda t: seg.at(t)[1] - y
    a, b = lo, hi
    fa = f(a)
    for _ in range(80):
        m = (a + b) / 2
        if (f(m) > 0) == (fa > 0): a, fa = m, f(m)
        else: b = m
    return (a + b) / 2


def seg_line_cross_x(seg, x, lo=0.0, hi=1.0):
    f = lambda t: seg.at(t)[0] - x
    a, b = lo, hi
    fa = f(a)
    for _ in range(80):
        m = (a + b) / 2
        if (f(m) > 0) == (fa > 0): a, fa = m, f(m)
        else: b = m
    return (a + b) / 2


# ---------- extra helpers (14 Nov 2026) ----------

def rrect(x0, y0, x1, y1, r, start='top'):
    """A closed box with round corners, as pieces, going clockwise on screen from the top-left end of the top edge."""
    r = min(r, (x1 - x0) / 2, (y1 - y0) / 2)
    segs = []
    segs.append(Seg((x0 + r, y0), (x1 - r, y0)))
    segs += arc(x1 - r, y0 + r, r, r, -90, 0, start=P(x1 - r, y0), end=P(x1, y0 + r))
    segs.append(Seg((x1, y0 + r), (x1, y1 - r)))
    segs += arc(x1 - r, y1 - r, r, r, 0, 90, start=P(x1, y1 - r), end=P(x1 - r, y1))
    segs.append(Seg((x1 - r, y1), (x0 + r, y1)))
    segs += arc(x0 + r, y1 - r, r, r, 90, 180, start=P(x0 + r, y1), end=P(x0, y1 - r))
    segs.append(Seg((x0, y1 - r), (x0, y0 + r)))
    segs += arc(x0 + r, y0 + r, r, r, 180, 270, start=P(x0, y0 + r), end=P(x0 + r, y0))
    segs = [s for s in segs if s.a != s.b]
    chain_ok(segs)
    return segs


def mirror(segs, cx=50.0):
    """The same pieces flipped left to right about x = cx (order and direction kept, so a chain stays a chain)."""
    out = []
    for s in segs:
        m = Seg.__new__(Seg); m.p = [P(2 * cx - x, y) for x, y in s.p]; out.append(m)
    return out


def curve(*pts):
    """A smooth curve through points given as (point, control, control, point, control, control, point ...)."""
    assert (len(pts) - 1) % 3 == 0
    return [Seg(pts[i], pts[i + 1], pts[i + 2], pts[i + 3]) for i in range(0, len(pts) - 1, 3)]


def cut_at(segs, i, t):
    """Split piece i of a chain at t; returns (pieces before the cut, pieces after), sharing the exact cut point."""
    a, b = segs[i].split(t)
    return segs[:i] + [a], [b] + segs[i + 1:]


def close(segs):
    """The chain plus a straight line back to its start (for colour outlines of open lines)."""
    return list(segs) + ([Seg(segs[-1].b, segs[0].a)] if segs[-1].b != segs[0].a else [])


# ---------- the drawing ----------

MATS = {
    'paper': ('paper', 'Paper', '1 sheet', '#fbf8ef'),
    'pencil': ('pencil', 'Pencil', '1', '#f2c14e'),
    'red': ('pencil', 'Red pencil', '1', '#fa5252'),
    'yellow': ('pencil', 'Yellow pencil', '1', '#ffd43b'),
    'blue': ('pencil', 'Blue pencil', '1', '#4dabf7'),
    'lblue': ('pencil', 'Light blue pencil', '1', '#74c0fc'),
    'green': ('pencil', 'Green pencil', '1', '#40c057'),
    'grey': ('pencil', 'Grey pencil', '1', '#adb5bd'),
    'black': ('pencil', 'Black pencil', '1', '#343a40'),
    'orange': ('pencil', 'Orange pencil', '1', '#ff922b'),
    'pink': ('pencil', 'Pink pencil', '1', '#f783ac'),
    'brown': ('pencil', 'Brown pencil', '1', '#a9713b'),
    'lbrown': ('pencil', 'Light brown pencil', '1', '#d9a066'),
    'lgreen': ('pencil', 'Light green pencil', '1', '#a9e34b'),
}
FILL = {'red': '#ff6b6b', 'yellow': '#ffd43b', 'blue': '#4dabf7', 'lblue': '#a5d8ff', 'green': '#8ad35a',
        'grey': '#c9ced6', 'black': '#4b5058', 'orange': '#ffa94d', 'pink': '#ffa8c8', 'brown': '#c08a5c',
        'lbrown': '#f2c078', 'lgreen': '#d8f08a'}


def drawing(key, title, level, minutes, theme, tags, description, steps, pencils):
    mats = [{"id": i, "kind": MATS[i][0], "name": MATS[i][1], "qty": MATS[i][2], "color": MATS[i][3]} for i in ['paper', 'pencil'] + pencils]
    return {"format": "stepby/1", "category": "draw", "id": key, "title": title, "level": level, "difficulty": "Easy",
            "time": "%d min" % minutes, "tags": tags, "theme": theme, "description": description,
            "canvas": {"w": 100, "h": 100, "grid": 10}, "materials": mats, "steps": steps}


def step(title, text, items, use='pencil'):
    assert len(text) <= 160, (title, len(text))
    return {"title": title, "text": text, "use": [use], "add": items}
