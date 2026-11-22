"""Grapes that hide each other (21 Nov 2026, for G is for Grapes version 5).

Every grape is a circle, and the grapes are given front first. The first two are special: the next grape (FR), in front
of everything, and the G grape just behind it. Their circles cross at the two ends of the G: its top end (TT) and its
other end (CE). The G's round curve is the G grape's own edge, from TT the long way round to CE. The G's bar is the start
of the next grape's edge: from CE a little way along the bottom of the next grape, so the bar bends with that grape and
fits in. The rest of the next grape's edge goes on round from the end of the bar, through TT, and back down to CE.
Every grape after the first two is hidden by the ones before it.

For a grape behind, the part you can see is found by looking out from its middle in every direction (the middle must be
visible, and each look must go from seen to hidden only once). That gives the order of the edges round it: its own
circle and the circles of the grapes in front. The corners where those edges meet are worked out exactly, and every
piece is drawn from the same corners, so each colour edge sits exactly on a drawn line.

Version 4 had a straight bar going out from the G to the next grape (see claude/step-by-draw-letter-builders-24.md).
"""
import math
from r5kit import *


class Bunch:
    def __init__(self, circles, G0, RG, f_dir, f_dist, R, bar_len, settle=False):
        self.R, self.G0, self.RG = R, G0, RG
        a = math.radians(f_dir)
        self.F0 = P(G0[0] + f_dist * math.cos(a), G0[1] + f_dist * math.sin(a))
        self.C = [(self.F0[0], self.F0[1], R), (G0[0], G0[1], RG)] + [(x, y, R) for x, y in circles]
        self._pts = {}
        two = self.meet(0, 1)
        assert len(two) == 2, 'the next grape must overlap the G grape'
        rel = lambda p: (self.ang(1, p) - f_dir + 180) % 360 - 180
        self.TT, self.CE = sorted(two, key=rel)          # TT: the G's top end; CE: its other end, where the bar starts
        gT, gC = self.ang(1, self.TT), self.ang(1, self.CE)
        while gC >= gT: gC -= 360                        # the long way round, anticlockwise on screen (as a G is written)
        self.G_CURVE = arc(G0[0], G0[1], RG, RG, gT, gC, start=self.TT, end=self.CE)
        fx, fy = self.F0
        fC, fT = self.ang(0, self.CE), self.ang(0, self.TT)
        while fT <= fC: fT += 360                        # the next grape's edge inside the G grape: CE to TT, clockwise
        m = math.radians((fC + fT) / 2)
        assert self.in_disk(1, (fx + R * math.cos(m), fy + R * math.sin(m))), 'that edge should be inside the G grape'
        fB = fC - math.degrees(bar_len / R)              # the bar: from CE along the bottom of the next grape
        self.BE = P(fx + R * math.cos(math.radians(fB)), fy + R * math.sin(math.radians(fB)))
        self.G_BAR = arc(fx, fy, R, R, fC, fB, start=self.CE, end=self.BE)
        self.FR_OUT = arc(fx, fy, R, R, fB, fT - 360, start=self.BE, end=self.TT)        # on round, up to the top of the G
        self.FR_IN = arc(fx, fy, R, R, fT - 360, fC - 360, start=self.TT, end=self.CE)   # and down inside, to the bar's start
        self.FR_REST = self.FR_OUT + self.FR_IN
        self.FR_RING = self.G_BAR + self.FR_REST
        self.G_FILL = self.G_CURVE + rev(self.FR_IN)
        self.lines, self.fills = {}, {}
        self.moved = {}
        for i in range(2, len(self.C)):
            if settle:
                self.settle(i)
            else:
                self.lines[i], self.fills[i] = self.visible(i)

    # ---------- nudging a grape a little, so no tiny bits of it peek out between two grapes in front ----------
    def ok(self, i, lines):
        for l in lines:
            L = sum(math.dist(a, b) for s_ in l for a, b in zip(s_.samples(20), s_.samples(20)[1:]))
            if L < 3.0:
                return False
        for j in range(i):
            (x1, y1, r1), (x2, y2, r2) = self.C[i], self.C[j]
            ov = r1 + r2 - math.dist((x1, y1), (x2, y2))
            if ov > 3.3 or -1.2 < ov < 0.5:
                return False
        return True

    def settle(self, i):
        x0, y0, r = self.C[i]
        tries = [(0.0, 0.0)] + [(rr * math.cos(math.radians(a)), rr * math.sin(math.radians(a)))
                                for rr in (0.3, 0.6, 0.9, 1.2) for a in range(0, 360, 45)]
        for dx, dy in tries:
            self.C[i] = (round(x0 + dx, 2), round(y0 + dy, 2), r)
            for key in [k for k in self._pts if i in k]:
                del self._pts[key]
            try:
                lines, fill_ = self.visible(i)
            except AssertionError:
                continue
            if self.ok(i, lines):
                self.lines[i], self.fills[i] = lines, fill_
                if (dx, dy) != (0.0, 0.0): self.moved[i] = (round(dx, 2), round(dy, 2))
                return
        raise AssertionError('grape %d: no small nudge gets rid of its tiny bits' % i)

    # ---------- helpers ----------
    def meet(self, i, j):
        key = (min(i, j), max(i, j))
        if key not in self._pts:
            (x1, y1, r1), (x2, y2, r2) = self.C[key[0]], self.C[key[1]]
            d = math.hypot(x2 - x1, y2 - y1)
            if d >= r1 + r2 or d <= abs(r1 - r2):
                self._pts[key] = []
            else:
                a = (r1 * r1 - r2 * r2 + d * d) / (2 * d); h = math.sqrt(r1 * r1 - a * a)
                ux, uy = (x2 - x1) / d, (y2 - y1) / d; px, py = x1 + a * ux, y1 + a * uy
                self._pts[key] = [P(px - h * uy, py + h * ux), P(px + h * uy, py - h * ux)]
        return self._pts[key]

    def ang(self, k, p):
        x, y, r = self.C[k]
        return math.degrees(math.atan2(p[1] - y, p[0] - x)) % 360

    def carc(self, k, p, q, cw):
        x, y, r = self.C[k]
        a0, a1 = self.ang(k, p), self.ang(k, q)
        if cw:
            while a1 <= a0 + 1e-9: a1 += 360
        else:
            while a1 >= a0 - 1e-9: a1 -= 360
        return arc(x, y, r, r, a0, a1, start=p, end=q)

    def in_disk(self, k, p, eps=1e-9):
        x, y, r = self.C[k]
        return math.hypot(p[0] - x, p[1] - y) < r - eps

    def hidden(self, i, p):
        """is point p hidden by a grape in front of grape i"""
        return any(self.in_disk(j, p) for j in range(i))

    def dist_to(self, k, p):
        x, y, r = self.C[k]
        return abs(math.hypot(p[0] - x, p[1] - y) - r)

    def visible(self, i, step=0.25):
        x, y, r = self.C[i]
        assert not self.hidden(i, (x, y)), ('the middle of grape %d is hidden' % i)
        labels, pts = [], []
        n = int(round(360 / step))
        for k in range(n):
            a = math.radians(k * step); u = (math.cos(a), math.sin(a))
            hit = None; flips = 0; prev = False
            for m_ in range(1, 81):
                t = r * m_ / 80
                h = self.hidden(i, (x + u[0] * t, y + u[1] * t))
                if h != prev: flips += 1
                if h and hit is None:
                    lo, hi = (t - r / 80), t
                    for _ in range(40):
                        m = (lo + hi) / 2
                        if self.hidden(i, (x + u[0] * m, y + u[1] * m)): hi = m
                        else: lo = m
                    hit = hi
                prev = h
            assert flips <= 1, ('grape %d: a look out from its middle goes in and out of hiding' % i, k * step)
            if hit is None:
                labels.append(i); pts.append((x + u[0] * r, y + u[1] * r))
            else:
                p = (x + u[0] * hit, y + u[1] * hit)
                labels.append(min(range(i), key=lambda j: self.dist_to(j, p))); pts.append(p)
        if all(l == i for l in labels):
            return [circle(x, y, r)], circle(x, y, r)
        # runs of the same edge, going round clockwise on screen
        s0 = next(k for k in range(n) if labels[k] != labels[k - 1])
        runs = []
        k = s0
        while True:
            lab = labels[k]; start = k
            while labels[(k + 1) % n] == lab and (k + 1) % n != s0: k = (k + 1) % n
            runs.append((lab, start, k))
            k = (k + 1) % n
            if k == s0: break
        corners = []
        for (la, sa, ea), (lb, sb, eb) in zip(runs, runs[1:] + runs[:1]):
            near = ((pts[ea][0] + pts[sb][0]) / 2, (pts[ea][1] + pts[sb][1]) / 2)
            cands = self.meet(la, lb)
            assert cands, ('edges do not meet', i, la, lb)
            corners.append(min(cands, key=lambda q: math.dist(q, near)))
        segs, lines = [], []
        for idx, (lab, s, e) in enumerate(runs):
            p, q = corners[idx - 1], corners[idx]
            mid = pts[(s + ((e - s) % n) // 2) % n]
            if lab == i:
                piece_ = self.carc(i, p, q, True)
                lines.append(piece_)
            else:
                cw, ccw = self.carc(lab, p, q, True), self.carc(lab, p, q, False)
                md = lambda sg: min(math.dist(mid, z) for s_ in sg for z in s_.samples(30))
                piece_ = cw if md(cw) < md(ccw) else ccw
            segs += piece_
        chain_ok(segs)
        assert segs[-1].b == segs[0].a
        return lines, segs
