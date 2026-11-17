"""s is for sister (dx_sister_s), Around the house a to z, slot s. A girl dancing with a long ribbon on a stick.
The s is the ribbon: it is one edge of the ribbon, and a second line beside it makes it wide.
Nothing crosses the s: the stick only touches its end."""
from famkit import *

PEACH, YELLOW, ORANGE, PINK, RED = FILL['peach'], FILL['yellow'], FILL['orange'], FILL['pink'], FILL['red']

# ---- 1: the s ----
CX, CY, SW, SH = 40.0, 45.0, 13.5, 27.0
def S_(u, v): return P(CX + u * SW, CY + v * SH)
S0, T, Lf, M_, Rt, Bt, E = S_(0.95, -0.55), S_(0, -1), S_(-0.95, -0.5), S_(0, 0), S_(0.95, 0.5), S_(0, 1), S_(-0.95, 0.6)
md = unit(1.0, 0.72)
s_ = [Seg(S0, (S0[0], 23.0), (47.6, T[1]), T), Seg(T, (32.4, T[1]), (Lf[0], 24.2), Lf),
      Seg(Lf, (Lf[0], 37.2), (M_[0] - md[0] * 7.6, M_[1] - md[1] * 7.6), M_),
      Seg(M_, (M_[0] + md[0] * 7.6, M_[1] + md[1] * 7.6), (Rt[0], 52.6), Rt),
      Seg(Rt, (Rt[0], 65.6), (47.6, Bt[1]), Bt), Seg(Bt, (33.4, Bt[1]), (E[0] + 3.2, E[1] + 4.6), E)]

# ---- 2: the other edge of the ribbon ----
RW = 3.8
s2 = offset_chain(s_, RW)
S0b, Eb = s2[0].a, s2[-1].b
r_start, r_end = Seg(S0b, S0), Seg(E, Eb)

# ---- 3: head and face ----
HC, HR = (77.0, 30.0), 8.5
head = ring_from(HC, HR, -90)
eyes = [dot(73.6, 29.6, w=2.6), dot(80.4, 29.6, w=2.6)]
smile = Seg((73.4, 32.8), (74.6, 35.4), (79.4, 35.4), (80.6, 32.8))

# ---- 4: hair with two bunches ----
HL, HRt = oc(HC, HR, 200), oc(HC, HR, -20)
capL = Seg(HL, (66.6, 23.4), (68.6, 18.6), (77.0, 18.6))
capR = Seg((77.0, 18.6), (85.4, 18.6), (87.4, 23.4), HRt)
cl = split_many(capL, [0.06, 0.4]); cr = rev(mirror(cl, HC[0]))
a1, a2 = cl[0].b, cl[1].b            # the left bunch is tied on between these
tip = (a1[0] - 8.6, a1[1] + 3.4)
bunL = [Seg(a1, (a1[0] - 2.2, a1[1] + 3.6), (tip[0] + 3.0, tip[1] + 3.0), tip),
        Seg(tip, (tip[0] - 2.4, tip[1] - 3.4), (a2[0] - 5.2, a2[1] - 2.0), a2)]
bunR = rev(mirror(bunL, HC[0]))
assert bunR[0].a == cr[0].b and bunR[-1].b == cr[1].b and cr[-1].b == HRt, (bunR[0].a, cr[0].b, bunR[-1].b, cr[1].b, cr[-1].b, HRt)

# ---- 5: neck and dress ----
nLt, nRt = oc(HC, HR, 105), oc(HC, HR, 75)
DT = 41.0
nLb, nRb = P(nLt[0], DT), P(nRt[0], DT)
DL, DR = P(71.0, DT), P(83.0, DT)
hem = Seg((90.0, 72.0), (82.0, 74.0), (72.0, 74.0), (64.0, 72.0))
LEG = [83.5, 80.0, 74.0, 70.5]
hp = split_x(hem, LEG)
tops = [p.b for p in hp[:-1]]
dress = [Seg(DL, nLb), Seg(nLb, nRb), Seg(nRb, DR), Seg(DR, (90.0, 72.0))] + hp + [Seg((64.0, 72.0), DL)]
sideL, sideR = Seg((64.0, 72.0), DL), Seg(DR, (90.0, 72.0))

# ---- 6: arms, hands and the stick ----
RHd = 3.0
pA, pB = at_y(sideL, 43.0), at_y(sideL, 48.0)
d1 = unit(-1.0, -0.62); c1 = ((pA[0] + pB[0]) / 2 + d1[0] * 9.5, (pA[1] + pB[1]) / 2 + d1[1] * 9.5)
armA1, armB1, aa1, _ = limb(pA, pB, d1, c1, RHd)
qA, qB = at_y(sideR, 43.0), at_y(sideR, 49.0)
d2 = unit(1.0, 0.75); c2 = ((qA[0] + qB[0]) / 2 + d2[0] * 9.0, (qA[1] + qB[1]) / 2 + d2[1] * 9.0)
armA2, armB2, aa2, _ = limb(qA, qB, d2, c2, RHd)
hand1, hand2 = ring_from(c1, RHd, aa1), ring_from(c2, RHd, aa2)
wd = unit(S0[0] - c1[0], S0[1] - c1[1]); wp = P(c1[0] + wd[0] * RHd, c1[1] + wd[1] * RHd)
wand = Seg(wp, S0)

# ---- 7: legs and shoes ----
SY = 84.0
legs = [Seg(t, (t[0], SY)) for t in tops]
shoeR, shoeL = rrect(78.2, SY, 85.3, 88.4, 1.8), rrect(68.7, SY, 75.8, 88.4, 1.8)

# ---- colours ----
def arm_fill(a, b, c):
    return fill(PEACH, a, arc_via(c, RHd, a.b, b.b, ang(c, a.a)), b.rev(), Seg(b.a, a.a))
neck_f = fill(PEACH, Seg(nLt, nLb), Seg(nLb, nRb), Seg(nRb, nRt), arc(HC[0], HC[1], HR, HR, 75, 105, start=nRt, end=nLt))
legR = fill(PEACH, Seg(tops[1], (tops[1][0], SY)), Seg((tops[1][0], SY), (tops[0][0], SY)), Seg((tops[0][0], SY), tops[0]), hp[1])
legL = fill(PEACH, Seg(tops[3], (tops[3][0], SY)), Seg((tops[3][0], SY), (tops[2][0], SY)), Seg((tops[2][0], SY), tops[2]), hp[3])
dress_f = fill(YELLOW, *dress)
hair_f = fill(ORANGE, cl, cr, arc(HC[0], HC[1], HR, HR, -20, -160, start=HRt, end=HL))
bunL_f = fill(ORANGE, bunL, cl[1].rev())
bunR_f = fill(ORANGE, bunR, cr[1].rev())
ribbon = fill(PINK, s_, r_end, rev(s2), r_start)

steps = [
    step('Start with an s', 'Draw a small letter s: start at the top on the right, curve round to the left, across, round to the right and back.',
         [line(*s_)]),
    step('The ribbon', 'Draw a second line beside the s, the same shape, just outside its top curve. Join the ends. It is a long ribbon!',
         [line(*s2), line(r_start), line(r_end)]),
    step('Head and face', 'Draw a round head on the right. Give her two dots for eyes and a big smile.', [ring(*head)] + eyes + [line(smile)]),
    step('Hair and bunches', 'Draw her hair round the top of her head. Give her two bunches, one sticking out on each side.',
         [line(*cl, *cr), line(*bunL), line(*bunR)]),
    step('Neck and dress', 'Draw a short neck. Then draw her dress: a line across, sides that get wider, and a curved line at the bottom.',
         [line(Seg(nLt, nLb)), line(Seg(nRt, nRb)), ring(*dress)]),
    step('Arms and the stick', 'Draw her arms with round hands: one up, holding a short stick, and one down. The stick holds the end of the ribbon.',
         [line(armA1), line(armB1), ring(*hand1), line(wand), line(armA2), line(armB2), ring(*hand2)]),
    step('Legs and shoes', 'Draw two legs under the dress, and a shoe on each one.', [line(l) for l in legs] + [ring(*shoeR), ring(*shoeL)]),
    step('Colour peach', 'Colour her face, neck, arms, hands and legs peach, or the colour of your sister’s skin.',
         [fill(PEACH, *head), neck_f, arm_fill(armA1, armB1, c1), arm_fill(armA2, armB2, c2), fill(PEACH, *hand1), fill(PEACH, *hand2), legR, legL],
         use='peach'),
    step('Colour yellow', 'Colour her dress yellow.', [dress_f], use='yellow'),
    step('Colour the hair', 'Colour her hair and her bunches orange, or the same colour as your sister’s hair.', [hair_f, bunL_f, bunR_f], use='orange'),
    step('Colour pink', 'Colour the long ribbon pink.', [ribbon], use='pink'),
    step('Colour red', 'Colour her shoes red.', [fill(RED, *shoeR), fill(RED, *shoeL)], use='red'),
]
D = drawing('dx_sister_s', 's is for sister', 2, 12, 'things', ['Letters', 'Around the house'],
            'A sister dancing with a long pink ribbon on a stick. The small letter s is hiding in it: it is the ribbon, swirling through the air.',
            steps, ['peach', 'yellow', 'orange', 'pink', 'red'])
save('sister', D, {'set': 'house-az', 'slot': 's', 'kind': 'hop', 'age_from': 5})
