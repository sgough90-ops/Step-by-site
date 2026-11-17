"""g is for grandad (dx_grandad_g), Around the house a to z, slot g. Grandad fishing in a pond.
The g is his float and fishing line: the round part is the float, bobbing in the water, and the stick is the line,
going down under the water and curling round at the bottom into the hook. Nothing crosses the g."""
from famkit import *

PEACH, GREEN, BROWN, RED, LBLUE = FILL['peach'], FILL['green'], FILL['brown'], FILL['red'], FILL['lblue']

# ---- 1: the g ----
GC, GR = (63.0, 62.0), 9.0
bowl = ring_ccw(GC, GR, -40)
SX = GC[0] + GR + 0.1          # just outside the round part, so the two lines touch without running together
gstick = [Seg((SX, 50.0), (SX, 86.0))] + arc(67.0, 86.0, 5.0, 5.0, 0, 180, start=P(SX, 86.0), end=P(62.0, 86.0))
WL, WR, WS = P(GC[0] - GR, GC[1]), P(GC[0] + GR, GC[1]), P(SX, GC[1])

# ---- 2: water, pond and ground ----
E = P(36.0, 62.0)
surfL = [Seg(E, (38.6, 60.0), (41.4, 60.0), (44.0, 62.0)), Seg((44.0, 62.0), (47.0, 64.2), (51.0, 64.2), WL)]
mid = Seg(WL, WR)
surfR = [Seg(WS, (74.6, 64.0), (77.4, 64.0), (80.0, 62.0)), Seg((80.0, 62.0), (82.6, 60.0), (85.4, 60.0), (88.0, 62.0)),
         Seg((88.0, 62.0), (90.0, 63.6), (92.2, 63.6), (94.0, 62.0))]
pond = [Seg((94.0, 62.0), (95.6, 80.0), (90.0, 95.0), (66.0, 95.0)), Seg((66.0, 95.0), (40.0, 95.0), (36.0, 90.0), E)]
ground = Seg((3.0, 62.0), E)

# ---- 3: a fish and bubbles ----
FC = (53.0, 83.0)
body = ring_from(FC, 6.5, 180, ry=4.0)
nose_tail = body[0].a
tail = poly(nose_tail, (nose_tail[0] - 4.6, 79.4), (nose_tail[0] - 4.6, 86.6), closed=True)
f_eye = dot(56.6, 82.0, w=2.2)
bubbles = [ring_from((60.6, 77.6), 1.1, -90), ring_from((58.6, 73.6), 1.4, -90)]

# ---- 4: head and face ----
HC, HR = (22.0, 27.0), 7.5
head = ring_from(HC, HR, -90)
eyes = [dot(19.3, 27.0, w=2.4), dot(24.7, 27.0, w=2.4)]
mo = [Seg((17.6, 32.0), (18.6, 29.6), (21.2, 28.9), (22.0, 29.9)), Seg((22.0, 29.9), (22.8, 28.9), (25.4, 29.6), (26.4, 32.0)),
      Seg((26.4, 32.0), (24.8, 31.3), (23.4, 31.9), (22.0, 31.2)), Seg((22.0, 31.2), (20.6, 31.9), (19.2, 31.3), (17.6, 32.0))]

# ---- 5: the cap ----
CL, CR = oc(HC, HR, 195), oc(HC, HR, -15)
cap = [Seg(CL, (13.8, 22.4), (15.4, 16.8), (22.4, 16.6)), Seg((22.4, 16.6), (28.2, 16.4), (31.4, 18.8), (32.4, 21.6)),
       Seg((32.4, 21.6), (32.9, 23.2), (31.6, 24.6), CR)]

# ---- 6: jumper and arms ----
JT, JB = 37.0, 50.0
nLt, nRt = oc(HC, HR, 105), oc(HC, HR, 75)
neckL, neckR = Seg(nLt, (nLt[0], JT)), Seg(nRt, (nRt[0], JT))
jumper = rrect(13.0, JT, 31.0, JB, 1.6)
RH = 2.8
d1 = unit(1.0, -0.32); c1 = (31.0 + d1[0] * 8.6, 41.3 + d1[1] * 8.6)
arm1a, arm1b, aa1, _ = limb(P(31.0, 39.2), P(31.0, 43.4), d1, c1, RH)
d2 = unit(-1.0, 0.55); c2 = (13.0 + d2[0] * 7.2, 41.3 + d2[1] * 7.2)
arm2a, arm2b, aa2, _ = limb(P(13.0, 39.2), P(13.0, 43.4), d2, c2, RH)
hand1, hand2 = ring_from(c1, RH, aa1), ring_from(c2, RH, aa2)

# ---- 7: trousers and boots ----
BT, GY = 58.6, 62.0
tr_l = Seg((14.8, JB), (14.8, BT)); tr_in = poly((19.0, BT), (22.0, 53.4), (25.0, BT)); tr_r = Seg((29.2, BT), (29.2, JB))
def boot(x0, x1):
    return [Seg((x0, GY), (x0, 59.8), (x0 + 0.8, BT), (x0 + 2.0, BT)), Seg((x0 + 2.0, BT), (x1 - 2.0, BT)),
            Seg((x1 - 2.0, BT), (x1 - 0.8, BT), (x1, 59.8), (x1, GY))]
bootL, bootR = boot(12.6, 21.2), boot(22.8, 31.4)

# ---- 8: the fishing rod ----
TIP = P(79.0, 19.0)
rd = unit(TIP[0] - c1[0], TIP[1] - c1[1]); r0 = P(c1[0] + rd[0] * RH, c1[1] + rd[1] * RH)
rod = Seg(r0, TIP)
fline = Seg(TIP, (SX, 50.0))

# ---- colours ----
def arm_fill(a, b, c):
    return fill(GREEN, a, arc_via(c, RH, a.b, b.b, ang(c, a.a)), b.rev(), Seg(b.a, a.a))
neck_f = fill(PEACH, neckL, Seg((nLt[0], JT), (nRt[0], JT)), neckR.rev(), arc(HC[0], HC[1], HR, HR, 75, 105, start=nRt, end=nLt))
cap_f = fill(BROWN, cap, arc(HC[0], HC[1], HR, HR, -15, -165, start=CR, end=CL))
trousers = fill(BROWN, Seg((29.2, JB), (14.8, JB)), tr_l, Seg((14.8, BT), (19.0, BT)), tr_in, Seg((25.0, BT), (29.2, BT)), tr_r)
boots = [fill(BROWN, b, Seg(b[-1].b, b[0].a)) for b in (bootL, bootR)]
float_top = fill(RED, arc(GC[0], GC[1], GR, GR, 180, 360, start=WL, end=WR), mid.rev())
water = fill(LBLUE, surfL, arc(GC[0], GC[1], GR, GR, 180, 0, start=WL, end=WR), Seg(WR, WS), surfR, pond, cut=[d_fill(*body), d_fill(*tail)])

steps = [
    step('Start with a g', 'Draw a small letter g: a round shape, then a stick down its right side that curls round to the left at the bottom.',
         [ring(*bowl), line(*gstick)]),
    step('The pond', 'Draw a wavy line on each side of the round part, and a line across it. Draw the bottom of the pond, and the ground on the left.',
         [line(*surfL), line(mid), line(*surfR), line(*pond), line(ground)]),
    step('A fish', 'Draw a fish swimming up to the hook, with a tail, an eye and two bubbles.',
         [ring(*body), ring(*tail), f_eye] + [ring(*b) for b in bubbles]),
    step('Head and face', 'Draw Grandad’s round head on the left. Give him two dots for eyes and a big bushy moustache.',
         [ring(*head)] + eyes + [ring(*mo)]),
    step('The cap', 'Draw a flat cap on top of his head. It sticks out a bit at the front.', [line(*cap)]),
    step('Jumper and arms', 'Draw a short neck and a jumper: a box with round corners. Draw an arm on each side with a round hand.',
         [line(neckL), line(neckR), ring(*jumper), line(arm1a), line(arm1b), ring(*hand1), line(arm2a), line(arm2b), ring(*hand2)]),
    step('Trousers and boots', 'Draw his trousers under the jumper, and a boot at the bottom of each leg, standing on the ground.',
         [line(tr_l), line(*tr_in), line(tr_r), line(*bootL), line(*bootR)]),
    step('The fishing rod', 'Draw a long fishing rod from his hand up over the water. Draw the fishing line from the end of it down to the top of the g.',
         [line(rod), line(fline)]),
    step('Colour peach', 'Colour his face, neck and hands peach, or the colour of your grandad’s skin. Leave his moustache white.',
         [fill(PEACH, *head, cut=[d_fill(*mo)]), neck_f, fill(PEACH, *hand1), fill(PEACH, *hand2)], use='peach'),
    step('Colour green', 'Colour his jumper and his arms green.', [fill(GREEN, *jumper), arm_fill(arm1a, arm1b, c1), arm_fill(arm2a, arm2b, c2)], use='green'),
    step('Colour brown', 'Colour his cap, trousers and boots brown.', [cap_f, trousers] + boots, use='brown'),
    step('Colour red', 'Colour the top of the float red. Colour the fish red too.', [float_top, fill(RED, *body), fill(RED, *tail)], use='red'),
    step('Colour the water', 'Colour the water light blue. Go round the fish.', [water], use='lblue'),
]
D = drawing('dx_grandad_g', 'g is for grandad', 3, 15, 'things', ['Letters', 'Around the house'],
            'Grandad in his flat cap, fishing in a pond. The small letter g is hiding in it: the round part is the float and the stick is the line and the hook.',
            steps, ['peach', 'green', 'brown', 'red', 'lblue'])
import json as _j, os as _o
_j.dump([d_fill(*mo)], open(_o.path.join(_o.path.dirname(_o.path.abspath(__file__)), 'out', 'grandad.white.json'), 'w'))
save('grandad', D, {'set': 'house-az', 'slot': 'g', 'kind': 'key', 'age_from': 5})
