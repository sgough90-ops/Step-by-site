"""Q is for Quail (Animals A to Z, slot Q). Side view, facing left.
The Q: its circle is the round body and its tail is the bottom edge of the quail's tail feathers.
The head, the tail's top edge and the legs all start on the circle: nothing crosses the Q."""
import json, math, os
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out')

BC = (54.0, 58.0); BR = 21.0
HC = (34.0, 35.0); HR = 11.0

def at(c, r, a):
    return P(c[0] + r * math.cos(math.radians(a)), c[1] + r * math.sin(math.radians(a)))
def ang(c, p):
    return math.degrees(math.atan2(p[1] - c[1], p[0] - c[0]))

# ---- 1: the Q ----
Qc = circle(BC[0], BC[1], BR)
TA = 40.0
cross_pt = at(BC, BR, TA)
tail = Seg(at(BC, 12.0, TA), at(BC, 32.0, TA))

# ---- 2: the head, touching the body ----
d = math.dist(BC, HC); a_ = (HR * HR - BR * BR + d * d) / (2 * d); h = math.sqrt(HR * HR - a_ * a_)
ux, uy = (BC[0] - HC[0]) / d, (BC[1] - HC[1]) / d
px, py = HC[0] + a_ * ux, HC[1] + a_ * uy
I1 = P(px - h * uy, py + h * ux); I2 = P(px + h * uy, py - h * ux)
# head arc goes the long way round (outside the body); I1 is the lower-left one
if I1[0] > I2[0]: I1, I2 = I2, I1
h1, h2 = ang(HC, I1), ang(HC, I2)
while h2 < h1: h2 += 360
head = arc(HC[0], HC[1], HR, HR, h2, h1 + 360, start=I2, end=I1) if (h1 + 360 - h2) > 180 else arc(HC[0], HC[1], HR, HR, h1, h2, start=I1, end=I2)
# the bit of the body between the two points (for colouring the head)
b1, b2 = ang(BC, head[-1].b), ang(BC, head[0].a)
while b2 < b1: b2 += 360
if b2 - b1 > 180: b1 += 360; b1, b2 = b2, b1
neck = arc(BC[0], BC[1], BR, BR, ang(BC, head[-1].b), ang(BC, head[-1].b) + ((ang(BC, head[0].a) - ang(BC, head[-1].b) + 540) % 360 - 180), start=head[-1].b, end=head[0].a)

# ---- 3: the beak ----
bk1, bk2 = at(HC, HR, 165), at(HC, HR, 195)
beak = [Seg(bk1, (17.0, HC[1])), Seg((17.0, HC[1]), bk2)]
beak_arc = arc(HC[0], HC[1], HR, HR, 195, 165, start=bk2, end=bk1)

# ---- 4: the plume on top of the head, curling forward ----
pa, pb = at(HC, HR, 254), at(HC, HR, 286)
plume = [Seg(pb, (39.6, 18.0), (34.4, 11.2), (27.0, 12.4)),
         Seg((27.0, 12.4), (24.0, 12.9), (23.8, 16.8), (26.8, 17.0)),
         Seg((26.8, 17.0), (30.0, 17.2), (31.0, 20.0), pa)]
plume_arc = arc(HC[0], HC[1], HR, HR, 254, 286, start=pa, end=pb)

# ---- 5: the eye ----
eye = circle(29.6, 33.0, 1.9)
shine = circle(30.2, 32.3, 0.8)

# ---- 6: the top of the tail ----
ts = at(BC, BR, 8.0)
tip = tail.b
ttop = Seg(ts, (80.0, 64.0), (84.0, 74.0), tip)
tail_arc = arc(BC[0], BC[1], BR, BR, 8.0, TA, start=ts, end=cross_pt)
tail_in = Seg(cross_pt, tip)

# ---- 7: the wing ----
wing = [Seg((42.0, 59.0), (48.0, 50.0), (62.0, 48.0), (71.0, 55.5)),
        Seg((71.0, 55.5), (62.0, 63.5), (49.0, 64.5), (42.0, 59.0))]

# ---- 8: the legs ----
lg1, lg2 = at(BC, BR, 112), at(BC, BR, 72)
legL = poly(lg1, (43.0, 88.0), (37.0, 88.0))
toeL = Seg((43.0, 88.0), (40.6, 91.0))
legR = poly(lg2, (62.6, 88.0), (68.4, 88.0))
toeR = Seg((62.6, 88.0), (60.4, 91.0))

# ---- 9: spots on the chest ----
spots = [dot(40.0, 66.0), dot(44.6, 71.4), dot(50.0, 74.4)]

steps = [
    step('Start with a Q', 'Draw a big capital Q: a round circle with a tail sticking out at the bottom. This Q is hiding in the quail.',
         [ring(*Qc), line(tail)]),
    step('The head', 'Draw a small round head at the top left of the Q. It sits on the body.',
         [line(*head)]),
    step('The beak', 'Draw a little pointed beak on the front of the head.',
         [line(*beak)]),
    step('A curly feather', 'Draw a feather on top of the head that curls forward, with a little round end.',
         [line(*plume)]),
    step('The eye', 'Draw a small round eye on the head.',
         [ring(*eye)]),
    step('The tail', 'Start on the body, above the tail of the Q. Draw a curved line out to the end of the tail. Now the quail has a pointed tail.',
         [line(ttop)]),
    step('The wing', 'Draw a wing on the body: a long leaf shape.',
         [ring(*wing)]),
    step('Legs and spots', 'Draw two thin legs with feet under the body. Draw three little dots on the front.',
         [line(*legL), line(toeL), line(*legR), line(toeR)] + spots),
    step('Colour light brown', 'Colour the body and the head light brown. Go round the wing and the eye.',
         [fill(FILL['lbrown'], *Qc, cut=[d_fill(*wing)]), fill(FILL['lbrown'], *(head + neck), cut=[d_fill(*eye)])], use='lbrown'),
    step('Colour brown', 'Colour the wing, the curly feather and the tail brown.',
         [fill(FILL['brown'], *wing), fill(FILL['brown'], *(plume + plume_arc)), fill(FILL['brown'], *([ttop] + [tail_in.rev()] + rev(tail_arc)))], use='brown'),
    step('Colour the beak', 'Colour the beak orange.',
         [fill(FILL['orange'], *(beak + beak_arc))], use='orange'),
    step('Colour the eye', 'Colour the eye black.',
         [fill(FILL['black'], *eye)], use='black'),
]

D = drawing('dx_quail_q', 'Q is for Quail', 2, 12, 'animals', ['Letters', 'Animals'],
            'A round little quail with a curly feather on its head. The capital Q is hiding in it: the circle is its body and the tail of the Q is the bottom of its tail feathers.',
            steps, ['lbrown', 'brown', 'orange', 'black'])
json.dump(D, open(os.path.join(OUT, 'quail.json'), 'w'))
json.dump({'set': 'animals-AZ', 'slot': 'Q', 'kind': 'hop', 'age_from': 4}, open(os.path.join(OUT, 'quail.place.json'), 'w'))
print('quail: %d steps' % len(steps))
