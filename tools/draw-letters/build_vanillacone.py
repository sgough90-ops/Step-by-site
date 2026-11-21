"""V is for Vanilla cone (dx_vanillacone_v), Food and drink A to Z, slot V (21 Nov 2026).
From the 'Vanilla cone' card on the capital Food and drink catalogue page (seen online: an ice cream cone drawn from a V,
Nuu's Crafts). Drawn fresh in our style.

A crunchy waffle cone with one round scoop of vanilla ice cream on top. The V is the two straight sides of the cone,
meeting in a sharp point at the bottom. The bottom of the scoop sits across the top of the V, with a little drip
hanging down. The criss-cross lines on the cone go from side to side; they only touch the V, they never cross it.

    python3 build_vanillacone.py [straight|wavy]      (no argument: the picked one, written as out/vanillacone.json)
"""
import math, sys
from r5kit import *

VANILLA, CONE = '#fff0b3', FILL['lbrown']     # the same pale yellow as the yellow scoop in I is for Ice cream

# ---- 1: the V (44 wide, 52 tall: a normal capital V) ----
VL, VB, VR = P(28, 42), P(50, 94), P(72, 42)
V_LINE = poly(VL, VB, VR)
RIM_X = (36.8, 45.6, 54.4, 63.2)     # where the criss-cross lines meet the top of the cone (even steps across)
DRIP_X = 54.4                        # the drip hangs over one of them, so both lines there start under the drip


def hang(p, q, depth):
    """a round bump hanging down from p to q"""
    dx = q[0] - p[0]
    return Seg(p, (p[0] + dx * 0.02, p[1] + depth * 1.33), (q[0] - dx * 0.02, q[1] + depth * 1.33), q)


def drip(x0, x1, depth):
    """a drip: down from x0, round the bottom and back up to x1"""
    m = (x0 + x1) / 2; w = (x1 - x0) / 2
    return curve(P(x0, 42), (x0 - 0.2, 42 + depth * 0.55), (m - w * 0.62, 42 + depth), (m, 42 + depth),
                 (m + w * 0.62, 42 + depth), (x1 + 0.2, 42 + depth * 0.55), P(x1, 42))


def point_in(ring, pt, n=60):
    """is a point inside a closed chain of pieces (even-odd rule on a dense polygon)"""
    poly_ = [q for s in ring for q in s.samples(n)]
    x, y = pt; c = False
    for (x1, y1), (x2, y2) in zip(poly_, poly_[1:] + poly_[:1]):
        if (y1 > y) != (y2 > y):
            xi = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            if xi > x: c = not c
    return c


def make(style):
    # ---- 2: the scoop, from the top left of the V, up and over to the top right ----
    dome = curve(VL, (21.5, 29), (30, 9.5), (50, 9.5), (70, 9.5), (78.5, 29), VR)

    # ---- 3: the bottom of the scoop, across the top of the V, with a drip ----
    d0, d1 = DRIP_X - 3.2, DRIP_X + 3.2
    if style == 'straight':
        base = [Seg(VL, P(d0, 42))] + drip(d0, d1, 9.5) + [Seg(P(d1, 42), VR)]
    else:   # a wavy edge: little bumps between the criss-cross lines, and the drip
        xs = [28, 32.4, 41.2, 50.0, d0]
        base = [hang(P(a, 42), P(b, 42), 1.9) for a, b in zip(xs, xs[1:])]
        base += drip(d0, d1, 9.5)
        xs = [d1, 67.6, 72]
        base += [hang(P(a, 42), P(b, 42), 1.9) for a, b in zip(xs, xs[1:])]
    chain_ok(base)
    assert base[0].a == VL and base[-1].b == VR

    # ---- 4 and 5: the criss-cross lines on the cone ----
    cone_ring = V_LINE + rev(base)          # the cone's outline: down the V, then back along the bottom of the scoop

    def clip(x0, d):
        """the part of the straight line through (x0, 42), direction d, that is inside the cone; must be one piece"""
        far = [P(x0 - d[0] * 60, 42 - d[1] * 60), P(x0 + d[0] * 60, 42 + d[1] * 60)]
        hits = [q for s in cone_ring for t, q in line_hits_seg(far[0], far[1], s)]
        u = lambda q: (q[0] - far[0][0]) * d[0] + (q[1] - far[0][1]) * d[1]
        hits = sorted(set((round(q[0], 4), round(q[1], 4)) for q in hits), key=u)
        runs = [(a, b) for a, b in zip(hits, hits[1:]) if point_in(cone_ring, ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2))]
        assert len(runs) == 1, ('line is not one piece inside the cone', x0, runs)
        return Seg(P(*runs[0][0]), P(*runs[0][1]))

    dl = (VB[0] - VL[0], VB[1] - VL[1]); L = math.hypot(*dl); dl = (dl[0] / L, dl[1] / L)     # down the left side
    dr = (VB[0] - VR[0], VB[1] - VR[1]); L = math.hypot(*dr); dr = (dr[0] / L, dr[1] / L)     # down the right side
    one_way = [clip(x, dl) for x in RIM_X]
    other_way = [clip(x, dr) for x in RIM_X]

    # ---- 6: the shine on the scoop ----
    shine = [q2c(P(32.5, 28), P(34.2, 18.8), P(42.5, 15.2))]

    steps = [
        step('Start with a V', 'Draw a capital V: two straight lines that meet in a sharp point at the bottom. This V is hiding in the ice cream.',
             [line(*V_LINE)]),
        step('The scoop', 'From the top of one side of the V, draw a big round scoop of ice cream, up and over to the top of the other side.',
             [line(*dome)]),
        step('The drip', ('Draw a straight line across the top of the V, with a little drip hanging down.' if style == 'straight' else
                          'Draw a wavy line across the top of the V, with a little drip hanging down.'),
             [line(*base)]),
        step('Cone lines', 'Draw four lines across the cone, all leaning the same way, from side to side.',
             [line(s) for s in one_way]),
        step('Criss-cross', 'Now draw four lines leaning the other way, to make a criss-cross pattern on the cone.',
             [line(s) for s in other_way]),
        step('The shine', 'Draw a little curved line at the top of the scoop. It makes the ice cream look shiny.',
             [line(*shine)]),
        step('Colour yellow', 'Colour the ice cream and its drip pale yellow, like vanilla.',
             [fill(VANILLA, *(dome + rev(base)))], use='yellow'),
        step('Colour light brown', 'Colour the cone light brown.', [fill(CONE, *cone_ring)], use='lbrown'),
    ]
    return drawing('dx_vanillacone_v', 'V is for Vanilla cone', 2, 10, 'things', ['Letters', 'Around the house'],
                   'A crunchy cone with a scoop of vanilla ice cream. The capital V is hiding in it: it is the two sides of the cone.',
                   steps, ['yellow', 'lbrown'])


PICK = 'straight'

if __name__ == '__main__':
    v = sys.argv[1] if len(sys.argv) > 1 else PICK
    save('vanillacone' if len(sys.argv) == 1 else 'vanillacone_' + v, make(v),
         {'set': 'house-AZ', 'slot': 'V', 'kind': 'key', 'age_from': 4})
