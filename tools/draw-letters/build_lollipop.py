"""l is for Lollipop (dx_lollipop_l), Food and drink a to z, slot l (22 Nov 2026).
From his pick "l1 A giant swirl with a bow" (Claude's sketches, claude/step-by-draw-food-small-11-ideas-4-versions.md).

A big round swirly lollipop on a white stick, with a bow tied round the stick. The l is the left edge of the stick,
below the bow.

    python3 build_lollipop.py
"""
import math
from fkit import *

PINK, BLUE = FILL['pink'], FILL['blue']
CX, CY, R = 50.0, 31.0, 26.0
XL, XR, KT, KB, SB = 48.0, 52.0, 62.0, 68.0, 95.0     # stick edges, knot top and bottom, stick bottom

net = Net()
net.add('l', Seg((XL, KB), (XL, SB)))                                   # 1: the l
knot = rrect(46.5, KT, 53.5, KB, 1.2)
net.add('knot', knot)                                                   # 2: the bow
wing = [Seg((46.5, 63.3), (43, 59.8), (38.5, 58.6), (38.5, 65)), Seg((38.5, 65), (38.5, 71.4), (43, 70.2), (46.5, 66.7))]
net.add('wingL', wing)
net.add('wingR', rev(mirror(wing)))
circ = ell(CX, CY, R)                                                   # the sweet (from the top, clockwise)


def on_circle(x):
    s = circ[1] if x > CX else circ[2]                                  # the bottom right or bottom left piece
    t = seg_x(s, x); return P(*s.at(t))


net.add('stick', Seg((XR, KB), (XR, SB)), Seg((XR, SB), (XL, SB)))      # 3: the stick
net.add('topL', Seg(on_circle(XL), (XL, KT)))
net.add('topR', Seg(on_circle(XR), (XR, KT)))
net.add('sweet', circ)                                                  # 4: the sweet


T = 2.25 * 2 * math.pi
RF = 0.84 * R                                                           # the swirl grows to here, then turns out to the edge


def arm(phi0, n=40):
    T0 = T - math.radians(40); pts = []
    for i in range(n + 1):
        th = T0 * i / n; r = RF * th / T0; a = phi0 + th
        pts.append((CX + r * math.cos(a), CY + r * math.sin(a)))
    pts[0] = (CX, CY)
    a = phi0 + T - math.radians(16); pts.append((CX + 0.94 * R * math.cos(a), CY + 0.94 * R * math.sin(a)))
    end = P(CX + R * math.cos(phi0 + T), CY + R * math.sin(phi0 + T)); pts.append(end)
    return snap_end(smooth(pts), end)


net.add('arm1', arm(-math.pi / 2))                                      # 5: the swirl (ends on the right of the sweet)
net.add('arm2', arm(math.pi / 2))                                       # 6: the second swirl (ends on the left)
net.node()


def strip_seed():
    # a point between arm1 and the next turn of arm2, on a line going right from the middle
    T0 = T - math.radians(40)
    th = 2 * math.pi * 1.0 + math.pi / 2                                 # arm1 points right after one and a quarter turns
    r1 = RF * th / T0; r2 = RF * (th + math.pi) / T0
    return (CX + (r1 + r2) / 2, CY)


steps = [
    step('Start with an l', 'Draw a small letter l: one straight line down. This l is hiding in the lollipop.', net.lines('l')),
    step('The bow', 'At the top of the l, draw a little box for the knot. Add a loop on each side of it.', net.lines('knot', 'wingL', 'wingR')),
    step('The stick', 'Draw a second line down beside the l, and join them at the bottom. Draw the stick up above the knot too.',
         net.lines('stick', 'topL', 'topR')),
    step('The sweet', 'On top of the stick, draw a big circle.', net.lines('sweet')),
    step('The swirl', 'From the middle of the circle, draw a curly line that goes round and round, out to the edge.', net.lines('arm1')),
    step('The second swirl', 'From the middle again, draw another curly line in between the first one, out to the other side.', net.lines('arm2')),
    step('Colour pink', 'Colour every other stripe of the swirl pink, from the middle out to the edge.',
         [net.fill(PINK, strip_seed(), names=['sweet', 'arm1', 'arm2'])], use='pink'),
    step('Colour blue', 'Colour the bow blue.',
         [net.fill(BLUE, (50, (KT + KB) / 2), names=['knot']), net.fill(BLUE, (42, 65), names=['knot', 'wingL']),
          net.fill(BLUE, (58, 65), names=['knot', 'wingR'])], use='blue'),
]

D = drawing('dx_lollipop_l', 'l is for Lollipop', 2, 8, 'things', ['Letters', 'Around the house'],
            'A giant swirly lollipop with a bow. The small letter l is hiding in it: it is the edge of the stick, under the bow.',
            steps, ['pink', 'blue'])
save('lollipop', D, {'set': 'house-az', 'slot': 'l', 'kind': 'key', 'age_from': 4})
