"""vkit: a painter's layer over fkit, for the Vehicles capitals of 22 Nov 2026
(oil tanker, ketch, nuclear submarine, yacht, Viking boat).

A Pic is a picture made of parts that sit in front of each other, in the order they are added (back first):
  shape():  a closed part. It hides the lines of everything added before it.
  stroke(): a line (open or closed). It hides nothing. deco=True marks a line that is only decoration
            (a plank line, a window bar), which is left out when a colour's edge is walked.
  region(): hides like a shape but draws no line (for a part whose outline is made of other named lines).
build() then cuts every line where it meets another (fkit's node) and takes away what is behind a part in front.
A drawing is written in the numbers of the sketch it comes from; every point goes through the Pic's own
move-and-scale (fit) on its way in, so the picture can be placed on the app's paper in one place.
Colours: ring() colours a whole part that can be seen all round; face() colours the space round a point, closed
in by the drawn lines (fkit's paint bucket). Holes are the outlines of parts that sit inside the colour.
"""
import json, math, os, re
from fkit import *


def path(d):
    """chains of pieces from sketch path text (M L C Q Z, absolute numbers)"""
    t = re.findall(r'[MLCQZ]|-?\d*\.?\d+', d)
    i = 0; chains = []; segs = []; cur = start = None; cmd = None

    def num():
        nonlocal i
        v = float(t[i]); i += 1
        return v
    while i < len(t):
        if t[i] in 'MLCQZ':
            cmd = t[i]; i += 1
            if cmd == 'Z':
                if P(*cur) != P(*start): segs.append(Seg(cur, start))
                cur = start
                continue
        if cmd == 'M':
            if segs: chains.append(segs); segs = []
            cur = (num(), num()); start = cur; cmd = 'L'
        elif cmd == 'L':
            p = (num(), num())
            if P(*p) != P(*cur): segs.append(Seg(cur, p))
            cur = p
        elif cmd == 'C':
            c1 = (num(), num()); c2 = (num(), num()); p = (num(), num())
            segs.append(Seg(cur, c1, c2, p)); cur = p
        elif cmd == 'Q':
            q = (num(), num()); p = (num(), num())
            c1 = (cur[0] + 2 / 3 * (q[0] - cur[0]), cur[1] + 2 / 3 * (q[1] - cur[1]))
            c2 = (p[0] + 2 / 3 * (q[0] - p[0]), p[1] + 2 / 3 * (q[1] - p[1]))
            segs.append(Seg(cur, c1, c2, p)); cur = p
    if segs: chains.append(segs)
    return chains


def one(d):
    c = path(d)
    assert len(c) == 1, len(c)
    return c[0]


def box(x0, y0, x1, y1):
    return poly((x0, y0), (x1, y0), (x1, y1), (x0, y1), closed=True)


def blob(x0, x1, y, depth=8.5, amp=1.2, wl=12.5, end=2.2):
    """a puddle of sea like the ones in his pictures: wavy top, round ends, closed outline"""
    k = max(2, int(round((x1 - x0) / (wl / 2))))
    top = [(x0 + (x1 - x0) * i / k, y + (amp if i % 2 else -amp)) for i in range(k + 1)]
    kb = max(2, k // 2)
    bot = [(x1 - (x1 - x0) * i / kb, y + depth + (0.7 if i % 2 else -0.7)) for i in range(kb + 1)]
    return smooth(top + [(x1 + end, y + depth * 0.5)] + bot + [(x0 - end, y + depth * 0.5)], closed=True)


class Pic:
    def __init__(self, s=1.0, dx=0.0, dy=0.0):
        self.net = Net(); self.items = []; self.s, self.dx, self.dy = s, dx, dy
        self.white = []

    # ---- the move-and-scale ----
    def pt(self, x, y):
        return P(x * self.s + self.dx, y * self.s + self.dy)

    def T(self, *segs):
        out = []
        for s in flat(segs):
            m = Seg.__new__(Seg); m.p = [self.pt(x, y) for x, y in s.p]
            if m.p[0] != m.p[-1] or len(m.p) == 4: out.append(m)
        chain_ok(out)
        return out

    # ---- parts ----
    def _add(self, kind, name, segs, step, deco=False, w=W):
        segs = self.T(*segs)
        if kind == 'region':
            self.net.region(name, segs)
        else:
            self.net.add(name, segs, closed=(True if kind == 'shape' else None))
        self.items.append(dict(kind=kind, name=name, step=step, deco=deco, w=w))
        return self

    def shape(self, name, *segs, step, w=W):
        segs = flat(segs)
        assert P(*segs[-1].b) == P(*segs[0].a), (name, 'not closed')
        return self._add('shape', name, segs, step, w=w)

    def stroke(self, name, *segs, step, deco=False, w=W):
        return self._add('stroke', name, segs, step, deco, w)

    def region(self, name, *segs):
        return self._add('region', name, flat(segs), None)

    def build(self, keep=()):
        """keep: pairs (name, front) where the part must NOT be hidden by that front"""
        n = self.net
        n.node()
        for i, it in enumerate(self.items):
            if it['kind'] == 'region': continue
            fronts = [jt['name'] for jt in self.items[i + 1:] if jt['kind'] in ('shape', 'region') and (it['name'], jt['name']) not in keep]
            if fronts: n.hide(it['name'], *fronts)
        return self

    # ---- lines ----
    def lines(self, *names):
        out = []
        for nm in names:
            w = next(it['w'] for it in self.items if it['name'] == nm)
            out += self.net.lines(nm, w=w)
        return out

    def step(self, k):
        return self.lines(*[it['name'] for it in self.items if it['step'] == k])

    # ---- colours ----
    def _cut(self, holes):
        return [d_fill(*self.net.all(h)) for h in holes] or None

    def ring(self, pencil, name, holes=()):
        segs = self.net.all(name)
        assert segs[0].a == segs[-1].b, (name, 'cannot be seen all round, use face()')
        return fill(FILL[pencil], *segs, cut=self._cut(holes))

    def face(self, pencil, seed, holes=(), names=None, skip=()):
        skip = tuple(skip) + tuple(it['name'] for it in self.items if it['deco'])
        names = names or [it['name'] for it in self.items if it['kind'] != 'region']
        return self.net.fill(FILL[pencil], self.pt(*seed), names=names, skip=skip, cut=self._cut(holes))

    def stay_white(self, *names):
        self.white += [d_fill(*self.net.all(h)) for h in names]


def save_white(name, white):
    here = os.path.dirname(os.path.abspath(__file__))
    f = os.path.join(here, 'out', name + '.white.json')
    if white: json.dump(white, open(f, 'w'))
    elif os.path.exists(f): os.remove(f)


def preview(D, out, px=900, red_steps=1):
    """a quick look: finished colours on the left, lines only with the letter in red on the right (rsvg, no browser)"""
    import subprocess, html
    def svg(colour):
        parts = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="%d" height="%d">' % (px, px), '<rect width="100" height="100" fill="#fff"/>']
        fills, lines = [], []
        for si, st in enumerate(D['steps']):
            for it in st['add']:
                if 'fill' in it:
                    if colour:
                        d = it['d'] + ''.join(' ' + c for c in it.get('cut', []))
                        fills.append('<path d="%s" fill="%s" fill-rule="evenodd"/>' % (html.escape(d), it['fill']))
                else:
                    col = '#e03131' if (si < red_steps and not colour) else '#343a40'
                    lines.append('<path d="%s" fill="none" stroke="%s" stroke-width="%.3f" stroke-linecap="round" stroke-linejoin="round"/>' % (html.escape(it['d']), col, it.get('w', 1.8) * 0.6))
        return ''.join(parts + fills + lines + ['</svg>'])
    from PIL import Image
    ims = []
    for colour in (True, False):
        f = out[:-4] + ('-c' if colour else '-l') + '.svg'
        open(f, 'w').write(svg(colour))
        subprocess.run(['rsvg-convert', f, '-o', f[:-4] + '.png'], check=True)
        ims.append(Image.open(f[:-4] + '.png').convert('RGB')); os.remove(f); os.remove(f[:-4] + '.png')
    im = Image.new('RGB', (px * 2 + 30, px + 20), '#dee2e6')
    im.paste(ims[0], (10, 10)); im.paste(ims[1], (px + 20, 10))
    im.save(out)
    return out
