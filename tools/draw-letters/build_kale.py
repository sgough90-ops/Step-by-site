"""k is for Kale (dx_kale_k), Food and drink a to z, slot k (23 Nov 2026).
From sketch "k3 One curly leaf" (Claude's sketches, claude/step-by-draw-food-small-12-ideas-4-versions.md).
He asked why the k was black when the other leaf lines were light green, and whether it could be a different colour.
In the app every line is pencil, so here ALL the leaf lines are pencil: the k and the other lines match.

One big curly kale leaf with a pale stalk. The k is the right edge of the stalk (its tall line) and two of the
lines that branch from it (its arm and leg). Step 1 draws the tall line down to the bottom of the leaf, so the k has
a normal shape; step 3 carries it on down as the stalk. Written in the sketch's numbers.

    python3 build_kale.py
"""
import qcheck                                    # the quicker crossing test (the same 9 checks)
from bcommon import *

p = Pic(s=0.97, dx=5.4, dy=4.2)
X, TOP, BASE, BOT = 48.0, 10.0, 85.0, 94.0       # the k's line: its top, where the leaf ends, the bottom of the stalk
XL = 43.0                                        # the stalk's other edge
J, ARM, LEG = (X, 62.0), (70.0, 40.0), (69.0, 83.0)
CEN = (46.0, 46.0)                               # the middle of the leaf (bumps bulge away from it)
EDGE = [(X, BASE), (56, 86), (65, 90), (77, 88), (83, 75), (79, 61), (81, 46), (76, 29), (67, 15), (57, 6), (46, 2),
        (35, 6), (25, 15), (16, 29), (11, 46), (13, 61), (9, 75), (15, 88), (27, 90), (36, 86), (XL, BASE)]


def curly(pts, per=7.6):
    """little round bumps along the smooth curve through pts, from its first point to its last"""
    base = smooth(pts)
    dense = [q for s in base for q in [s.at(i / 14) for i in range(14)]] + [base[-1].b]
    cum = [0.0]
    for a, b in zip(dense, dense[1:]): cum.append(cum[-1] + math.dist(a, b))
    k = int(round(cum[-1] / per)); anchors = []; j = 0
    for i in range(k + 1):
        s = cum[-1] * i / k
        while j < len(cum) - 2 and cum[j + 1] < s: j += 1
        a, b = dense[j], dense[j + 1]; t = (s - cum[j]) / max(1e-9, cum[j + 1] - cum[j])
        anchors.append(P(a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t))
    anchors[0], anchors[-1] = P(*pts[0]), P(*pts[-1])
    out = []
    for i, (a, b) in enumerate(zip(anchors, anchors[1:])):
        dx, dy = b[0] - a[0], b[1] - a[1]; L = math.hypot(dx, dy); ux, uy = dx / L, dy / L
        nx, ny = uy, -ux
        m = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
        if nx * (m[0] - CEN[0]) + ny * (m[1] - CEN[1]) < 0: nx, ny = -nx, -ny
        h = 0.66 * L
        c1 = (a[0] + nx * h, a[1] + ny * h); c2 = (b[0] + nx * h, b[1] + ny * h)
        if i == 0: c1 = (a[0] + 0.3 * L * ux, a[1] + ny * h)               # the first and last bumps lean away from the stalk
        if i == len(anchors) - 2: c2 = (b[0] - 0.3 * L * ux, b[1] + ny * h)
        out.append(Seg(a, c1, c2, b))
    return out


rib = Seg((X, TOP), (46.2, 22), (44.2, 50), (XL, BASE))            # the stalk's left edge, inside the leaf


def on_rib(y):
    """the point of the stalk's left edge at height y (in the sketch's numbers)"""
    lo, hi = 0.0, 1.0
    for _ in range(60):
        m = (lo + hi) / 2
        if rib.at(m)[1] < y: lo = m
        else: hi = m
    return rib.at((lo + hi) / 2)


# ---- the leaf's curly edge, the stalk, the thin leaf lines ----
p.stroke('leaf', curly(EDGE), step=2)
p.stroke('stalk', rib, Seg((XL, BASE), (XL, BOT)), Seg((XL, BOT), (X, BOT)), Seg((X, BOT), (X, BASE)), step=3)
VEINS = [(on_rib(62), (23, 40)), (on_rib(62), (24, 83)), (on_rib(45), (27, 25)), (on_rib(29), (34.5, 14)),
         ((50.6, 45), (66, 26.5)), ((50.6, 29), (59.5, 14.5))]
for i, (a, b) in enumerate(VEINS):
    p.stroke('vein%d' % i, Seg(a, b), step=4, deco=True, w=1.2)

# ---- the k, in front of everything ----
p.stroke('k_stick', Seg((X, TOP), (X, BASE)), step=1)
p.stroke('k_arm', Seg(J, ARM), step=1)
p.stroke('k_leg', Seg(J, LEG), step=1)
p.build()

steps = [
    step('Start with a k', 'Draw a small letter k: a tall line down, then two slanting lines on its right. They meet low down on the tall line.', p.step(1)),
    step('The curly leaf', 'Start at the bottom of the k. Draw little round bumps all the way round the k: up one side, over the top and down the other side.', p.step(2)),
    step('The stalk', 'From the top of the k, draw a long line down its left side. Carry it on below the leaf, go across, and come back up to the k.', p.step(3)),
    step('Leaf lines', 'Draw thin lines on the leaf, slanting out from the middle like the arm and leg of the k.', p.step(4)),
    step('Colour the leaf', 'Colour the leaf green, on both sides of the stalk. Leave the stalk white.', [p.face('green', (62, 60))], use='green'),
]
D = drawing('dx_kale_k', 'k is for Kale', 2, 10, 'things', ['Letters', 'Around the house'],
            'A big curly leaf of kale. The small letter k is hiding in it: the edge of the stalk and two of the lines on the leaf.',
            steps, ['green'])
ok = finish('kale', D, {'set': 'house-az', 'slot': 'k', 'kind': 'key', 'age_from': 4}, p)
