"""M is for Moth (Animals A to Z, slot M). Seen from above, wings open.
The M: the tall lines are the outside edges of the two top wings, the V is their front edges.
The head sits in the point of the V; the body hangs under it."""
import json, os
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out')

XL, XR = 17.0, 83.0
YT, YB = 23.0, 62.0
V = (50.0, 48.0)

M_ = poly((XL, YB), (XL, YT), V, (XR, YT), (XR, YB))

h1 = Seg(V, (48.7, 45.6), (45.8, 44.2), (45.8, 41.6))
h2 = Seg((45.8, 41.6), (45.8, 39.3), (47.7, 37.6), (50, 37.6))
headL = [h1, h2]
head = headL + rev(mirror(headL))
b1 = Seg(V, (47.8, 50.5), (46.3, 54.5), (46.3, 58.5))
b2 = Seg((46.3, 58.5), (46.3, 67), (48.3, 78), (50, 86))
bodyL = [b1, b2]
body = bodyL + rev(mirror(bodyL))
J = b1.b

backL = [Seg((XL, YB), (26, 68.5), (38, 65), J)]
backR = mirror(backL)

tK = 0.60
b2a, b2b = b2.split(tK)
K_ = b2a.b
lowL = [Seg((XL, YB), (13.6, 68.5), (16.3, 78.2), (24.0, 78.9)),
        Seg((24.0, 78.9), (27.8, 79.2), (30.4, 77.3), (31.6, 74.2)),
        Seg((31.6, 74.2), (32.2, 80.2), (36.6, 85.2), (41.2, 84.2)),
        Seg((41.2, 84.2), (45.0, 83.3), (47.3, 79.6), K_)]
lowR = mirror(lowL)

h2a, h2b = h2.split(0.5)
A1 = h2a.b
feelL = Seg(A1, (45.6, 33.5), (41.5, 23.5), (34.0, 20.5))
def hairs(f, ts=(0.42, 0.63, 0.84), d=(-3.3, 1.4)):
    out = []
    for t in ts:
        p = P(*f.at(t)); out.append(Seg(p, (p[0] + d[0], p[1] + d[1])))
    return out
hairL = hairs(feelL)
feelR = mirror([feelL])[0]; hairR = mirror(hairL)

SC = (32.0, 51.4)
spotL = circle(SC[0], SC[1], 5.7); pupL = circle(SC[0], SC[1], 2.5)
spotR = mirror(spotL); pupR = mirror(pupL)

def stripe(y):
    t = seg_line_cross_y(b2, y); p = P(*b2.at(t))
    return Seg(p, (100 - p[0], p[1]))
stripes = [stripe(y) for y in (62.5, 67.0, 71.5)]

wingL = [Seg((XL, YB), (XL, YT)), Seg((XL, YT), V), b1] + rev(backL)
wingR = [Seg((XR, YB), (XR, YT)), Seg((XR, YT), V)] + mirror([b1]) + rev(backR)
lowerL = lowL + [b2a.rev()] + rev(backL)
lowerR = lowR + mirror([b2a.rev()]) + rev(backR)

steps = [
    step('Start with an M', 'Draw a big, wide capital M: two tall straight lines, with a V between their tops. This M is hiding in the moth.',
         [line(*M_)]),
    step('Head and body', 'Draw a small round head sitting in the point of the V. Then draw a long thin body under it, with a pointed end.',
         [ring(*head), ring(*body)]),
    step('The top wings', 'From the bottom of each tall line, draw a curved line in to the body. Now the M has made two big wings.',
         [line(*backL), line(*backR)]),
    step('The bottom wings', 'Draw a smaller wing under each big one. Start at the bottom of the tall line, make two round bumps and finish at the body.',
         [line(*lowL), line(*lowR)]),
    step('The feelers', 'Draw two long curved feelers on top of the head. Add three little hairs to each one.',
         [line(feelL), line(feelR)] + [line(s) for s in hairL + hairR]),
    step('Eye spots', 'Draw a big circle on each top wing. Then draw a smaller circle inside each one.',
         [ring(*spotL), ring(*spotR), ring(*pupL), ring(*pupR)]),
    step('Stripes', 'Draw three short lines across the body.',
         [line(s) for s in stripes]),
    step('Colour brown', 'Colour the two top wings brown, round the big circles. Colour the head and the body brown too.',
         [fill(FILL['brown'], *wingL, cut=[d_fill(*spotL)]), fill(FILL['brown'], *wingR, cut=[d_fill(*spotR)]),
          fill(FILL['brown'], *head), fill(FILL['brown'], *body)], use='brown'),
    step('Colour light brown', 'Colour the two bottom wings light brown.',
         [fill(FILL['lbrown'], *lowerL), fill(FILL['lbrown'], *lowerR)], use='lbrown'),
    step('Colour the spots', 'Colour the two small circles black. Leave the rings round them white. Now they look like big eyes!',
         [fill(FILL['black'], *pupL), fill(FILL['black'], *pupR)], use='black'),
]

D = drawing('dx_moth_m', 'M is for Moth', 2, 12, 'animals', ['Letters', 'Animals'],
            'A moth with its wings open and a big eye spot on each one. The capital M is hiding in it: its two tall lines are the outside edges of the top wings and its V is their front edges.',
            steps, ['brown', 'lbrown', 'black'])
json.dump(D, open(os.path.join(OUT, 'moth.json'), 'w'))
json.dump([d_fill(*spotL), d_fill(*spotR)], open(os.path.join(OUT, 'moth.white.json'), 'w'))
json.dump({'set': 'animals-AZ', 'slot': 'M', 'kind': 'fly', 'age_from': 5}, open(os.path.join(OUT, 'moth.place.json'), 'w'))
print('moth: %d steps' % len(steps))
