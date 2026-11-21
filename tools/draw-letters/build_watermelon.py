"""W is for Watermelon (dx_watermelon_w), Food and drink A to Z, slot W (21 Nov 2026).
From the 'Watermelon' card on the capital Food and drink catalogue page (also found online: Jasim Drawing and others).

Two slices of watermelon side by side, both with their points at the bottom. The W is the straight cut sides of the
two slices: down, up, down, up. The middle top of the W is where the two slices touch. Over the top of each V is the
curved skin of the slice, with a green band, and the red inside has little black seeds.

    python3 build_watermelon.py
"""
import math
from kit15 import *

RED, GREEN = FILL['red'], FILL['green']

# ---- 1: the W (70 wide, 54 tall: a normal capital W, its middle top as high as its sides) ----
TL, B1, M, B2, TR = P(15, 28), P(32.5, 82), P(50, 28), P(67.5, 82), P(85, 28)
W_LINE = poly(TL, B1, M, B2, TR)

BULGE = 6.5        # how far the skin curves up above the tops of the W
BAND = 4.2         # how thick the green skin is at the top
PALE = 3.6         # how thick the pale band under the skin is (left white)


def ang_of(cx, cy, rx, ry, p):
    return math.degrees(math.atan2((p[1] - cy) / ry, (p[0] - cx) / rx)) % 360


def arc_to(cx, cy, rx, ry, p0, p1, clockwise=True):
    """the arc of an oval from point p0 to point p1 (both on it), clockwise on screen or the other way (as in kit.py)"""
    a0 = ang_of(cx, cy, rx, ry, p0); a1 = ang_of(cx, cy, rx, ry, p1)
    if clockwise:
        while a1 <= a0 + 1e-9: a1 += 360
    else:
        while a1 >= a0 - 1e-9: a1 -= 360
    return arc(cx, cy, rx, ry, a0, a1, start=P(*p0), end=P(*p1))


def dome(a, b, h):
    """centre and radius of the circle through a, b and the point h above their middle"""
    half = math.dist(a, b) / 2
    r = (half * half + h * h) / (2 * h)
    mx = (a[0] + b[0]) / 2
    return (mx, a[1] - h + r), r


def circle_line(c, r, p, q):
    """the first point (from p) where the circle (c, r) meets the straight piece p->q"""
    dx, dy = q[0] - p[0], q[1] - p[1]
    fx, fy = p[0] - c[0], p[1] - c[1]
    A = dx * dx + dy * dy; B = 2 * (fx * dx + fy * dy); C = fx * fx + fy * fy - r * r
    disc = math.sqrt(B * B - 4 * A * C)
    ts = sorted(t for t in ((-B - disc) / (2 * A), (-B + disc) / (2 * A)) if 0 <= t <= 1)
    assert ts, 'the circle misses the line'
    return P(p[0] + dx * ts[0], p[1] + dy * ts[0])     # the one nearest p (the top of the side)


def slice_parts(a, apex, b):
    """outer skin line a->b, the line under the green skin and the line under the pale band (both end on the sides)"""
    c, r = dome(a, b, BULGE)
    outer = arc_to(c[0], c[1], r, r, a, b, clockwise=True)
    out = [outer]
    for ri in (r - BAND, r - BAND - PALE):
        pa = circle_line(c, ri, a, apex)          # on the left side of this V
        pb = circle_line(c, ri, b, apex)          # on the right side of this V
        out += [arc_to(c[0], c[1], ri, ri, pa, pb, clockwise=True), pa, pb]
    return out


OUT_L, IN_L, LA, LB, PALE_L, LA2, LB2 = slice_parts(TL, B1, M)
OUT_R, IN_R, RA, RB, PALE_R, RA2, RB2 = slice_parts(M, B2, TR)


def seeds(apex, top_mid):
    """little seeds in a slice, each one leaning towards the point of the slice"""
    out = []
    ax, ay = apex
    for fx, fy in [(-0.27, 0.22), (0.27, 0.22), (0.0, 0.38), (-0.15, 0.55), (0.15, 0.55), (0.0, 0.72)]:
        # fy: how far down from the top (0) to the point (1); fx: how far across, as a share of the width there
        y = top_mid[1] + (ay - top_mid[1]) * fy
        half = 17.5 * (ay - y) / (ay - top_mid[1])
        x = ax + fx * 2 * half
        L = math.hypot(ax - x, ay - y); ux, uy = (ax - x) / L, (ay - y) / L
        p, q = P(x - ux * 0.55, y - uy * 0.55), P(x + ux * 0.55, y + uy * 0.55)
        out.append({"d": 'M %s %s L %s %s' % (fmt(p[0]), fmt(p[1]), fmt(q[0]), fmt(q[1])), "w": 2.6})
    return out


SEEDS_L = seeds(B1, (32.5, 34))
SEEDS_R = seeds(B2, (67.5, 34))

steps = [
    step('Start with a W', 'Draw a capital W: four straight lines, down, up, down, up. This W is hiding in the watermelon.',
         [line(*W_LINE)]),
    step('The tops', 'Draw a curved line over the top of each V, from one top to the other. Now you have two slices.',
         [line(*OUT_L), line(*OUT_R)]),
    step('The skin', 'Inside each slice, draw another curved line from side to side, just under the top. This is the skin.',
         [line(*IN_L), line(*IN_R)]),
    step('The rind', 'Draw one more curved line under each skin, a little lower down.',
         [line(*PALE_L), line(*PALE_R)]),
    step('The seeds', 'Draw some little seeds in each slice.', SEEDS_L + SEEDS_R),
]

# ---- the colours ----
skin_l = fill(GREEN, *(OUT_L + [Seg(M, LB)] + rev(IN_L) + [Seg(LA, TL)]))
skin_r = fill(GREEN, *(OUT_R + [Seg(TR, RB)] + rev(IN_R) + [Seg(RA, M)]))
red_l = fill(RED, *(PALE_L + [Seg(LB2, B1), Seg(B1, LA2)]))
red_r = fill(RED, *(PALE_R + [Seg(RB2, B2), Seg(B2, RA2)]))
steps += [
    step('Colour green', 'Colour the skin at the top of each slice green.', [skin_l, skin_r], use='green'),
    step('Colour red', 'Colour the inside of each slice red, all the way down to the points. Leave the thin band under the skin white.', [red_l, red_r], use='red'),
]

D = drawing('dx_watermelon_w', 'W is for Watermelon', 1, 8, 'things', ['Letters', 'Around the house'],
            'Two juicy slices of watermelon. The capital W is hiding in them: it is the straight sides of the two slices.',
            steps, ['green', 'red'])
save('watermelon', D, {'set': 'house-AZ', 'slot': 'W', 'kind': 'key', 'age_from': 4})
