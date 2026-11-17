"""4 is for Stork (dx_stork_4), Animals 1 to 9, slot 4. Built from Claude's sketch "Stork 4" (picked 17 Nov 2026).
The 4 is the stork's legs: the bent leg goes down and then across, and the leg it stands on crosses it."""
from numkit import *

BK, GY, RD = FILL['black'], FILL['grey'], FILL['red']

body = Ell(46, 31, 22, 14)
def under(x):
    return P(x, body.cy + body.ry * math.sqrt(1 - ((x - body.cx) / body.rx) ** 2))
def over(x):
    return P(x, body.cy - body.ry * math.sqrt(1 - ((x - body.cx) / body.rx) ** 2))

# the 4: the legs
LA, LB = under(40), under(52)
KNEE, HEEL, FOOT = P(40, 66), P(66, 66), P(52, 92)
four = [line(Seg(LA, KNEE), Seg(KNEE, HEEL)), line(Seg(LB, FOOT))]

# body, with a gap at the top right for the neck
NB, NF = over(57), over(66.6)                     # back and front of the neck, where they meet the body
TU, TL = body.P(195), body.P(150)                 # tail roots
body_pts = [NF, LB, LA, TL, TU, NB]
body_line = []
for a, b in zip(body_pts, body_pts[1:]):
    body_line += body.arc_pts(a, b, cw=True)

# neck and head
head = Ell(69, 6.4, 5)
nb_full = qc(NB, (63.2, 15), (64.6, 4))           # back of the neck, cut where it reaches the head
tb, H_back = meet_se(nb_full, head)[0]
neck_b = Seg(*(seg_to(nb_full, tb).p[:-1] + [H_back]))
nf_full = qc((72, 4.6), (72.6, 19), NF)            # front of the neck, from where it leaves the head
tf, H_front = meet_se(nf_full, head)[-1]
neck_f = Seg(*([H_front] + seg_from(nf_full, tf).p[1:]))
BU0, BU1, BL0, BL1 = head.P(-58), head.P(-6), head.P(14), head.P(52)
beak_u = [Seg(BU0, (92, 2)), Seg((92, 2), BU1)]
beak_l = [Seg(BL0, (90.6, 14.6)), Seg((90.6, 14.6), BL1)]
head_ring = head.ring_at([H_back, BU0, BU1, BL0, BL1, H_front], cw=True)
clatter = [Seg((90.4, 20.4), (94.2, 22.4)), Seg((88.4, 24.4), (91.2, 28.4))]

# tail and wing
TIP = P(13.6, 33.6)
tail = [Seg(TU, TIP), Seg(TIP, TL)]
wing = [qc((28, 29), (43, 21), (61, 31)), qc((61, 31), (44, 42), (28, 29))]

# feet and ground
toes_up = [Seg(HEEL, (70.5, 63.5)), Seg(HEEL, (71, 67.6))]
toes_dn = [Seg(FOOT, (46.8, 95)), Seg(FOOT, (57.2, 95))]
ground = Seg((35, 95), (75, 95))

steps = [
    step('Start with a 4', 'Draw a big 4: a line down and then across to the right. Then a long line straight down that crosses it.', four),
    step('The body', 'Draw a big oval body on top of the 4. Leave a gap at the top right for the neck.', [line(*body_line)]),
    step('The neck', 'Draw two curved lines up from the gap for the neck.', [line(neck_b), line(neck_f)]),
    step('The head', 'Draw a circle for the head on top of the neck, with a dot for the eye.', [ring(*head_ring), dot(69.6, 4.8, 2.4)]),
    step('The beak', 'Draw a long open beak: two pointy triangles. Add two little lines to show it clattering.',
         [line(*beak_u), line(*beak_l)] + [line(c) for c in clatter]),
    step('The tail and wing', 'Draw a pointy tail at the back, and a wing shape inside the body.', [line(*tail), ring(*wing)]),
    step('The feet', 'Draw two little toes at the end of each leg, and a line for the ground.',
         [line(t) for t in toes_up] + [line(t) for t in toes_dn] + [line(ground)]),
]
tail_arc = body.arc_pts(TL, TU, cw=True)
up_root = head.arc_pts(BU1, BU0, cw=False)
lo_root = head.arc_pts(BL1, BL0, cw=False)
steps += [
    step('Colour black', 'Colour the tail black.', [fill(BK, *tail, *tail_arc)], use='black'),
    step('Colour grey', 'Colour the wing grey. Leave the stork white.', [fill(GY, *wing)], use='grey'),
    step('Colour red', 'Colour the beak red.', [fill(RD, *beak_u, *up_root), fill(RD, *beak_l, *lo_root)], use='red'),
]
P_ = drawing('dx_stork_4', '4 is for Stork', 2, 10, 'animals', ['Numbers', 'Animals'],
             'A stork standing on one leg with its head held high, clattering its long beak. The 4 is hiding in it: '
             'the bent leg goes down and then across, and the leg it stands on crosses it.',
             steps, ['black', 'grey', 'red'])
P_ = move(scale(P_, 0.9, 50, 50), 0, 3)           # a little smaller, so the beak fits on the paper
save('num4stork', P_, {'set': 'animals-09', 'slot': '4', 'kind': 'fly', 'age_from': 5})
