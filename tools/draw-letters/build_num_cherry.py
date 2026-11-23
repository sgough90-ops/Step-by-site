"""6 is for Cherry (dx_cherry_6), Food and drink 1 to 9, slot 6 (23 Nov 2026).
From his pick "6: 1 Cherry" (claude/step-by-draw-food-numbers-1-to-9-36-sketches.md).

A cherry on a long curved stalk with a leaf. The 6: its long curve is the outside edge of the stalk and its loop is
the cherry. Written in the sketch's numbers.

    python3 build_num_cherry.py
"""
from ncommon import *

p = Pic(s=1.09, dx=-12.4, dy=-2.9)
CX, CY, R, SW = 46, 66, 22, 3
S0, C1, C2, E = (70, 20), (50, 6), (24, 22), (CX - R, CY)       # the long curve of the 6, ending on the left of the loop
stem = Seg(S0, C1, C2, E)


def inside_pt(t, off):
    """a point just inside the curve of the 6 (on the traveller's left going down it)"""
    u = 1 - t
    x, y = stem.at(t)
    dx = 3 * u * u * (C1[0] - S0[0]) + 6 * u * t * (C2[0] - C1[0]) + 3 * t * t * (E[0] - C2[0])
    dy = 3 * u * u * (C1[1] - S0[1]) + 6 * u * t * (C2[1] - C1[1]) + 3 * t * t * (E[1] - C2[1])
    L = math.hypot(dx, dy)
    return (x + dy / L * off, y - dx / L * off)


# ---- the stalk's inside edge (it carries on into the cherry, which hides the end) ----
inner = smooth([inside_pt(i / 10, SW) for i in range(11)])
p.stroke('stalk_in', Seg(S0, inner[0].a), inner, step=2)
p.region('cherryR', circle(CX, CY, R))

# ---- the shine and the leaf ----
p.stroke('shine', arc(CX, CY, R - 6.5, R - 6.5, 200, 240), step=3, deco=True)
p.shape('leaf', leaf2(S0, (90, 12), 13), step=3)

# ---- the 6, in front of everything: the long curve down, then the loop ----
p.stroke('six', stem, arc(CX, CY, R, R, 180, -180, start=P(*E), end=P(*E)), step=1)
p.build()

steps = [
    step('Start with a 6', 'Draw a number 6: a long curved line coming down, then a round loop at the bottom. This 6 is hiding in the cherry.', p.step(1)),
    step('The stalk', 'Draw a second line just inside the curve of the 6, from the top down to the loop. Join the two lines at the top with a tiny line.', p.step(2)),
    step('The leaf', 'Draw a pointed leaf at the top of the stalk. Draw a little curved line inside the loop for the shine.', p.step(3)),
    step('Colour red', 'Colour the round cherry red.', [p.face('red', (CX, CY))], use='red'),
    step('Colour green', 'Colour the thin stalk and the leaf green.', [p.face('green', inside_pt(0.4, SW / 2)), p.ring('green', 'leaf')], use='green'),
]
D = drawing('dx_cherry_6', '6 is for Cherry', 1, 6, 'things', TAGS,
            'A shiny cherry on a long stalk with a leaf. The number 6 is hiding in it: the curved stalk and the round cherry.',
            steps, ['red', 'green'])
ok = finish('num6cherry', D, {'set': SET, 'slot': '6', 'kind': 'key', 'age_from': 4}, p)
