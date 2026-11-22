"""fkit: helpers for drawings where shapes sit in front of each other (22 Nov 2026, the food drawings).

A Net holds named lines (chains of kit pieces). node() cuts every line where it meets another and makes both share
the very same point. hide() takes away the parts of a line that are behind a shape in front. face() walks round the
drawn lines that close in a point (like a paint bucket) and gives the pieces of that outline, so a colour's edge is
made of the very same pieces as the lines.
"""
import math
import numpy as np
from kit15 import *


# ---------- points along pieces ----------

def seg_arr(s, n=None):
    if n is None: n = 2 if len(s.p) == 2 else 40
    t = np.linspace(0, 1, n); p = np.array(s.p, float)
    if len(s.p) == 2:
        return np.outer(1 - t, p[0]) + np.outer(t, p[1])
    u = 1 - t
    return np.outer(u ** 3, p[0]) + np.outer(3 * u * u * t, p[1]) + np.outer(3 * u * t * t, p[2]) + np.outer(t ** 3, p[3])


def chain_arr(segs, n=None):
    out = [seg_arr(s, n)[:-1] for s in segs] + [np.array([segs[-1].b], float)]
    return np.vstack(out)


def seg_len(s):
    a = seg_arr(s, 2 if len(s.p) == 2 else 30)
    return float(np.hypot(*(a[1:] - a[:-1]).T).sum())


def bbox(s, pad=0.0):
    p = np.array(s.p, float)
    return p[:, 0].min() - pad, p[:, 1].min() - pad, p[:, 0].max() + pad, p[:, 1].max() + pad


def boxes_apart(a, b):
    return a[2] < b[0] or b[2] < a[0] or a[3] < b[1] or b[3] < a[1]


def set_a(s, pt):
    s.p = [P(*pt)] + s.p[1:]


def set_b(s, pt):
    s.p = s.p[:-1] + [P(*pt)]


def nearest_t(seg, pt, n=200):
    a = seg_arr(seg, n + 1); d = np.hypot(a[:, 0] - pt[0], a[:, 1] - pt[1]); k = int(d.argmin())
    lo, hi = max(0, k - 1) / n, min(n, k + 1) / n
    for _ in range(50):
        m1, m2 = lo + (hi - lo) / 3, hi - (hi - lo) / 3
        if math.dist(seg.at(m1), pt) < math.dist(seg.at(m2), pt): hi = m2
        else: lo = m1
    return (lo + hi) / 2


def seg_cross(sa, sb):
    """where two pieces cross: list of (ta, tb)"""
    A = seg_arr(sa, 2 if len(sa.p) == 2 else 49); B = seg_arr(sb, 2 if len(sb.p) == 2 else 49)
    p1, p2 = A[:-1][:, None, :], A[1:][:, None, :]; p3, p4 = B[:-1][None, :, :], B[1:][None, :, :]
    d1, d2 = p2 - p1, p4 - p3
    den = d1[..., 0] * d2[..., 1] - d1[..., 1] * d2[..., 0]
    w = p3 - p1
    with np.errstate(divide='ignore', invalid='ignore'):
        u = (w[..., 0] * d2[..., 1] - w[..., 1] * d2[..., 0]) / den
        v = (w[..., 0] * d1[..., 1] - w[..., 1] * d1[..., 0]) / den
    e = 1e-9
    hit = (np.abs(den) > 1e-14) & (u >= -e) & (u <= 1 + e) & (v >= -e) & (v <= 1 + e)
    out = []
    for i, j in zip(*np.nonzero(hit)):
        ta, tb = (i + u[i, j]) / (len(A) - 1), (j + v[i, j]) / (len(B) - 1)
        for _ in range(12):                                   # Newton, to land on both curves
            pa, pb = sa.at(ta), sb.at(tb); h = 1e-5
            fa = ((sa.at(min(1, ta + h))[0] - sa.at(max(0, ta - h))[0]), (sa.at(min(1, ta + h))[1] - sa.at(max(0, ta - h))[1]))
            fb = ((sb.at(min(1, tb + h))[0] - sb.at(max(0, tb - h))[0]), (sb.at(min(1, tb + h))[1] - sb.at(max(0, tb - h))[1]))
            ha = min(1, ta + h) - max(0, ta - h); hb = min(1, tb + h) - max(0, tb - h)
            ax, ay, bx, by = fa[0] / ha, fa[1] / ha, fb[0] / hb, fb[1] / hb
            det = -ax * by + bx * ay
            if abs(det) < 1e-12: break
            rx, ry = pb[0] - pa[0], pb[1] - pa[1]
            dta = (-rx * by + bx * ry) / det; dtb = (ax * ry - ay * rx) / det
            ta = min(1.0, max(0.0, ta + dta)); tb = min(1.0, max(0.0, tb + dtb))
            if abs(dta) + abs(dtb) < 1e-10: break
        if math.dist(sa.at(ta), sb.at(tb)) > 0.02: continue
        if all(abs(ta - x) > 1e-4 or abs(tb - y) > 1e-4 for x, y in out): out.append((ta, tb))
    return out


def in_poly(pt, poly):
    x, y = pt; a = poly; b = np.roll(poly, -1, axis=0)
    c = ((a[:, 1] > y) != (b[:, 1] > y))
    with np.errstate(divide='ignore', invalid='ignore'):
        xs = a[:, 0] + (y - a[:, 1]) * (b[:, 0] - a[:, 0]) / (b[:, 1] - a[:, 1])
    return bool((c & (xs > x)).sum() % 2)


def poly_area(poly):
    x, y = poly[:, 0], poly[:, 1]
    return 0.5 * float(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1)))


# ---------- shapes ----------

def ell(cx, cy, rx, ry=None, start=-90):
    return circle(cx, cy, rx, start, ry)


def smooth(pts, closed=False, k=1.0):
    """cubic pieces through the points (Catmull-Rom); closed=True gives a ring"""
    m = len(pts)
    g = (lambda i: pts[i % m]) if closed else (lambda i: pts[max(0, min(m - 1, i))])
    out = []
    for i in range(m if closed else m - 1):
        p0, p1, p2, p3 = g(i - 1), g(i), g(i + 1), g(i + 2)
        c1 = (p1[0] + (p2[0] - p0[0]) / 6 * k, p1[1] + (p2[1] - p0[1]) / 6 * k)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6 * k, p2[1] - (p3[1] - p1[1]) / 6 * k)
        a = out[-1].b if out else P(*p1)
        out.append(Seg(a, c1, c2, p2))
    if closed: set_b(out[-1], out[0].a)
    return out


def leaf2(base, tip, w, skew=0.0):
    """a pointed leaf from base to tip, as two curved pieces: base -> tip along one side, tip -> base along the other"""
    (bx, by), (tx, ty) = base, tip
    dx, dy = tx - bx, ty - by; L = math.hypot(dx, dy); nx, ny = -dy / L, dx / L
    at = lambda t, s: (bx + dx * t + nx * s, by + dy * t + ny * s)
    h = w * 0.67
    return [Seg(base, at(0.18, h + skew), at(0.68, h + skew), tip), Seg(tip, at(0.68, -h + skew), at(0.18, -h + skew), base)]


def half_leaf(x, top, mid, bw, sg):
    """half of a round leaf against an upright line at x, from (x, top) round to (x, mid); sg=1 right, -1 left.
    With sg=1 it is the bowl of a P or an R."""
    h = mid - top
    return [Seg((x, top), (x + sg * bw * 0.55, top + h * 0.02), (x + sg * bw, top + h * 0.2), (x + sg * bw, top + h * 0.5)),
            Seg((x + sg * bw, top + h * 0.5), (x + sg * bw, top + h * 0.8), (x + sg * bw * 0.45, mid - h * 0.02), (x, mid))]


def sub(seg, t0, t1):
    """the part of a piece between t0 and t1"""
    a, b = seg.split(t1) if t1 < 1 else (seg, None)
    if t0 > 0: a = a.split(t0 / t1)[1]
    return a


# ---------- the net ----------

class Net:
    def __init__(self):
        self.runs, self.closed, self.poly, self.order = {}, {}, {}, []

    def add(self, name, *segs, closed=None):
        segs = [Seg(*s.p) for s in flat(segs)]; chain_ok(segs)
        if closed is None: closed = segs[-1].b == segs[0].a
        assert name not in self.runs, name
        self.runs[name] = [segs]; self.closed[name] = closed; self.order.append(name)
        if closed: self.poly[name] = chain_arr(segs)
        return self

    def region(self, name, *segs):
        """a shape used only to hide things behind it (its lines are added under other names)"""
        segs = flat(segs); chain_ok(segs); assert segs[-1].b == segs[0].a, 'region not closed'
        self.poly[name] = chain_arr(segs)
        return self

    def inside(self, pt, name):
        return in_poly(pt, self.poly[name])

    def items(self, names=None):
        for nm in (names or self.order):
            for ri, run in enumerate(self.runs[nm]):
                for pi, s in enumerate(run):
                    yield nm, ri, pi, s

    def node(self, tol=0.03):
        """cut every line where it crosses or meets another, sharing the exact point"""
        its = list(self.items()); bx = [bbox(s, 0.05) for *_, s in its]
        cuts = {}
        near_end = lambda s, t: (s.a if math.dist(s.at(t), s.a) < 0.02 else (s.b if math.dist(s.at(t), s.b) < 0.02 else None))
        for x in range(len(its)):
            for y in range(x + 1, len(its)):
                if boxes_apart(bx[x], bx[y]): continue
                (na, ra, ia, sa), (nb, rb, ib, sb) = its[x], its[y]
                for ta, tb in seg_cross(sa, sb):
                    ea, eb = near_end(sa, ta), near_end(sb, tb)
                    if ea is not None and eb is not None: continue
                    pt = ea if ea is not None else (eb if eb is not None else P(*sa.at(ta)))
                    if ea is None: cuts.setdefault((na, ra, ia), []).append((ta, pt))
                    if eb is None: cuts.setdefault((nb, rb, ib), []).append((tb, pt))
        # the ends of open lines that sit on another line
        for nm in self.order:
            for ri, run in enumerate(self.runs[nm]):
                if run[0].a == run[-1].b: continue
                for e in (run[0].a, run[-1].b):
                    for y, (nb, rb, ib, sb) in enumerate(its):
                        if (nb, rb) == (nm, ri): continue
                        if e == sb.a or e == sb.b: continue
                        b = bx[y]
                        if not (b[0] - tol <= e[0] <= b[2] + tol and b[1] - tol <= e[1] <= b[3] + tol): continue
                        t = nearest_t(sb, e)
                        if math.dist(sb.at(t), e) < tol and math.dist(e, sb.a) > 0.05 and math.dist(e, sb.b) > 0.05:
                            if all(q != e for _, q in cuts.get((nb, rb, ib), [])):
                                cuts.setdefault((nb, rb, ib), []).append((t, e))
        for nm in self.order:
            new_runs = []
            for ri, run in enumerate(self.runs[nm]):
                new = []
                for pi, s in enumerate(run):
                    c = sorted(cuts.get((nm, ri, pi), []))
                    c2 = []
                    for t, pt in c:
                        if c2 and (pt == c2[-1][1] or t - c2[-1][0] < 1e-5): continue
                        if pt == s.a or pt == s.b: continue
                        c2.append((t, pt))
                    if not c2: new.append(s); continue
                    parts = split_many(s, [t for t, _ in c2])
                    for k, (t, pt) in enumerate(c2):
                        set_b(parts[k], pt); set_a(parts[k + 1], pt)
                    new += parts
                chain_ok(new); new_runs.append(new)
            self.runs[nm] = new_runs
        return self

    def drop(self, name, test):
        """take away the pieces of a line for which test(piece) is true"""
        out = []
        for run in self.runs[name]:
            was_ring = run[0].a == run[-1].b
            keep = [not test(s) for s in run]
            cur, groups = [], []
            for s, k in zip(run, keep):
                if k: cur.append(s)
                elif cur: groups.append(cur); cur = []
            if cur: groups.append(cur)
            if was_ring and len(groups) > 1 and keep[0] and keep[-1]:
                groups[0] = groups.pop() + groups[0]
            out += groups
        self.runs[name] = out
        return self

    def hide(self, name, *fronts):
        """take away the parts of a line that are behind any of the front shapes"""
        return self.drop(name, lambda s: any(self.inside(s.at(0.5), f) for f in fronts))

    def keep_in(self, name, *shapes):
        """keep only the parts of a line that are inside one of the shapes"""
        return self.drop(name, lambda s: not any(self.inside(s.at(0.5), f) for f in shapes))

    def all(self, name):
        return [s for run in self.runs[name] for s in run]

    def lines(self, *names, w=W):
        out = []
        for nm in names:
            for run in self.runs[nm]:
                out.append(ring(*run, w=w) if run[0].a == run[-1].b else line(*run, w=w))
        return out

    # ---------- colouring ----------
    def _graph(self, names):
        segs = [s for nm in names for run in self.runs[nm] for s in run]
        nodes = {}
        for pid, s in enumerate(segs):
            L = max(seg_len(s), 1e-6); t = min(0.3, 0.25 / L)
            qa, qb = s.at(t), s.at(1 - t)
            nodes.setdefault(s.a, []).append((math.atan2(qa[1] - s.a[1], qa[0] - s.a[0]), pid, 1))
            nodes.setdefault(s.b, []).append((math.atan2(qb[1] - s.b[1], qb[0] - s.b[0]), pid, -1))
        for v in nodes.values(): v.sort()
        return segs, nodes

    def face(self, seed, names=None, skip=()):
        """the outline (pieces, in order) of the space round the seed point, closed in by the drawn lines"""
        names = [n for n in (names or self.order) if n not in skip]
        segs, nodes = self._graph(names)
        arrs = [seg_arr(s, 2 if len(s.p) == 2 else 25) for s in segs]

        def walk(pid, d):
            loop = []; cur = (pid, d)
            for _ in range(4000):
                loop.append(cur)
                s = segs[cur[0]]; v = s.b if cur[1] > 0 else s.a
                out = nodes[v]; back = (cur[0], -cur[1])
                k = next(i for i, (_, p, dd) in enumerate(out) if (p, dd) == back)
                _, p, dd = out[(k + 1) % len(out)]
                cur = (p, dd)
                if cur == (pid, d): return loop
            raise AssertionError('walk did not close')

        best = None
        for ang in (0, 90, 180, 270, 45, 135, 225, 315):
            ux, uy = math.cos(math.radians(ang)), math.sin(math.radians(ang))
            hit = None
            for pid, a in enumerate(arrs):
                p1, p2 = a[:-1], a[1:]; dx, dy = p2[:, 0] - p1[:, 0], p2[:, 1] - p1[:, 1]
                den = ux * dy - uy * dx
                with np.errstate(divide='ignore', invalid='ignore'):
                    r = ((p1[:, 0] - seed[0]) * dy - (p1[:, 1] - seed[1]) * dx) / den
                    v = ((p1[:, 0] - seed[0]) * uy - (p1[:, 1] - seed[1]) * ux) / den
                ok = (np.abs(den) > 1e-12) & (r > 1e-9) & (v >= 0) & (v <= 1)
                if ok.any():
                    rr = float(r[ok].min())
                    if hit is None or rr < hit[0]: hit = (rr, pid)
            if hit is None: continue
            for d in (1, -1):
                loop = walk(hit[1], d)
                changed = True
                while changed:                                  # take out there-and-back spurs
                    changed = False
                    for k in range(len(loop)):
                        a, b = loop[k], loop[(k + 1) % len(loop)]
                        if a[0] == b[0] and a[1] == -b[1] and len(loop) > 2:
                            for idx in sorted([k, (k + 1) % len(loop)], reverse=True): loop.pop(idx)
                            changed = True; break
                chain = [segs[p] if dd > 0 else segs[p].rev() for p, dd in loop]
                poly = chain_arr(chain)
                if in_poly(seed, poly):
                    ar = abs(poly_area(poly))
                    if best is None or ar < best[0] - 1e-6: best = (ar, chain)
        assert best is not None, ('no closed outline found round', seed)
        return best[1]

    def visible_fills(self, colour, name, fronts, names=None, skip=(), min_area=1.0, grid=0.4):
        """colour every part of a shape that can be seen (the parts not behind any of the front shapes)"""
        from scipy.spatial import cKDTree
        poly = self.poly[name]
        x0, y0, x1, y1 = poly[:, 0].min(), poly[:, 1].min(), poly[:, 0].max(), poly[:, 1].max()
        cand = [(x, y) for x in np.arange(x0 + grid / 2, x1, grid) for y in np.arange(y0 + grid / 2, y1, grid)]
        cand = [c for c in cand if in_poly(c, poly) and not any(in_poly(c, self.poly[f]) for f in fronts)]
        tree = cKDTree(np.vstack([poly] + [self.poly[f] for f in fronts]))
        out = []
        while len(cand) * grid * grid >= min_area:
            d, _ = tree.query(np.array(cand)); k = int(d.argmax())
            if d[k] < 0.3: break
            chain = self.face(cand[k], names, skip)
            fp = chain_arr(chain)
            left = [c for c in cand if not in_poly(c, fp)]
            if len(left) == len(cand): break
            out.append(fill(colour, *chain)); cand = left
        return out

    def fill(self, colour, seed, names=None, skip=(), cut=None):
        return fill(colour, *self.face(seed, names, skip), cut=cut)
