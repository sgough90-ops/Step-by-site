"""M is for Mum (dx_mum_m), Around the house A to Z, slot M. Mum in a red dress, flying a kite.
The M is the top of her dress: its two sides are the sides of the dress and its V is the V-neck.
Nothing crosses the M: the shoulders, arms and skirt only touch its corners and sides."""
from famkit import *

PEACH, RED, BROWN, YELLOW = FILL['peach'], FILL['red'], FILL['brown'], FILL['yellow']

# ---- 1: the M ----
ML, MR, MT, MB = 26.0, 52.0, 44.0, 70.0
pkL, pkR, botL, botR, V = P(ML, MT), P(MR, MT), P(ML, MB), P(MR, MB), P(39.0, 57.5)
M_ = poly(botL, pkL, V, pkR, botR)

# ---- 2: the head ----
HC, HR = (39.0, 28.5), 8.5
head = ring_from(HC, HR, -90)

# ---- 3: neck and shoulders ----
nLt, nRt = oc(HC, HR, 110), oc(HC, HR, 70)
NB = 41.0
nLb, nRb = P(nLt[0], NB), P(nRt[0], NB)
hL = at_x(Seg(pkL, nLb), 31.0); hR = at_x(Seg(nRb, pkR), 47.0)
shL1, shL2, neckL = Seg(pkL, hL), Seg(hL, nLb), Seg(nLb, nLt)
neckR, shR1, shR2 = Seg(nRt, nRb), Seg(nRb, hR), Seg(hR, pkR)

# ---- 4: the hair ----
TOP = P(39.0, 16.0)
hairL = [Seg(hL, (29.6, 39.4), (27.2, 35.5), (27.2, 31.5)), Seg((27.2, 31.5), (27.2, 22.5), (32.4, 16.0), TOP)]
hair = hairL + rev(mirror(hairL, 39.0))
assert hair[-1].b == hR, (hair[-1].b, hR)

# ---- 5: the face ----
eyes = [dot(35.6, 28.0, w=2.6), dot(42.4, 28.0, w=2.6)]
smile = Seg((35.6, 31.6), (36.8, 34.4), (41.2, 34.4), (42.4, 31.6))

# ---- 6: the arms: one out to the side, one up holding the kite string ----
RH = 3.4
c1 = (26.0 - 0.8 * 15.5, 47.0 + 0.6 * 15.5)
a1, b1, aa1, _ = limb(pkL, P(26.0, 50.0), (-0.8, 0.6), c1, RH)
c2 = (52.0 + 0.8 * 15.5, 47.0 - 0.6 * 15.5)
a2, b2, aa2, _ = limb(pkR, P(52.0, 50.0), (0.8, -0.6), c2, RH)
hand1, hand2 = ring_from(c1, RH, aa1), ring_from(c2, RH, aa2)

# ---- 7: the skirt ----
hem = Seg((59.0, 86.0), (48.0, 88.6), (30.0, 88.6), (19.0, 86.0))
hp = split_x(hem, [46.6, 42.6, 35.4, 31.4])           # right to left
tops = [p.b for p in hp[:-1]]
skirt = [Seg(botL, botR), Seg(botR, (59.0, 86.0))] + hp + [Seg((19.0, 86.0), botL)]

# ---- 8: legs and shoes ----
SY = 92.0
legs = [Seg(t, (t[0], SY)) for t in tops]
shoeR, shoeL = rrect(40.4, SY, 49.8, 96.6, 2.2), rrect(29.2, SY, 38.6, 96.6, 2.2)

# ---- 9: the kite ----
KT, KR, KB, KL, KX = P(82.0, 5.0), P(92.0, 14.0), P(82.0, 31.0), P(72.0, 14.0), P(82.0, 14.0)
kite = poly(KT, KR, KB, KL, closed=True)
spars = [Seg(KL, KR), Seg(KT, KX), Seg(KX, KB)]

# ---- 10: string and tail ----
hs = oc(c2, RH, -38)
string = Seg(hs, (71.0, 35.8), (77.0, 34.6), KB)
tail = [Seg(KB, (80.5, 35.5), (84.0, 37.0), (84.0, 41.5)), Seg((84.0, 41.5), (84.0, 46.0), (86.5, 47.5), (86.5, 52.0))]
T1, T2 = tail[0].b, tail[1].b
bows = [bow(T1, -1, 3.8, 2.2), bow(T1, 1, 3.8, 2.2), bow(T2, -1, 3.8, 2.2), bow(T2, 1, 3.8, 2.2)]

# ---- colours ----
def arm_fill(a, b, c):
    return fill(PEACH, a, arc_via(c, RH, a.b, b.b, ang(c, a.a)), b.rev(), Seg(b.a, a.a))

chest = fill(PEACH, shL1, shL2, neckL, arc(HC[0], HC[1], HR, HR, 110, 70, start=nLt, end=nRt), neckR, shR1, shR2, Seg(pkR, V), Seg(V, pkL))
hair_f = fill(BROWN, hair, shR1.rev(), neckR.rev(), arc(HC[0], HC[1], HR, HR, 70, -250, start=nRt, end=nLt), neckL.rev(), shL2.rev())
bodice = fill(RED, Seg(botL, pkL), Seg(pkL, V), Seg(V, pkR), Seg(pkR, botR), Seg(botR, botL))
legR = fill(PEACH, Seg(tops[1], (tops[1][0], SY)), Seg((tops[1][0], SY), (tops[0][0], SY)), Seg((tops[0][0], SY), tops[0]), hp[1])
legL = fill(PEACH, Seg(tops[3], (tops[3][0], SY)), Seg((tops[3][0], SY), (tops[2][0], SY)), Seg((tops[2][0], SY), tops[2]), hp[3])
kite_f = [fill(YELLOW, Seg(KT, KX), Seg(KX, KL), Seg(KL, KT)), fill(YELLOW, Seg(KT, KR), Seg(KR, KX), Seg(KX, KT)),
          fill(YELLOW, Seg(KX, KR), Seg(KR, KB), Seg(KB, KX)), fill(YELLOW, Seg(KX, KB), Seg(KB, KL), Seg(KL, KX))]

steps = [
    step('Start with an M', 'Draw a big capital M in the middle of your paper: up, down to a point, up, and down again. This M is hiding in Mum.',
         [line(*M_)]),
    step('The head', 'Draw a round head above the middle of the M.', [ring(*head)]),
    step('Neck and shoulders', 'From the bottom of the head, draw a short neck. Then draw a sloping line out to each top corner of the M.',
         [line(neckL.rev(), shL2.rev(), shL1.rev()), line(neckR, shR1, shR2)]),
    step('The hair', 'Draw her hair round the top of her head. It comes down each side and stops on her shoulders.', [line(*hair)]),
    step('The face', 'Give her two dots for eyes and a big smile.', eyes + [line(smile)]),
    step('The arms', 'Draw an arm coming out of each side of the dress, with a round hand. One arm points down, one points up.',
         [line(a1), line(b1), ring(*hand1), line(a2), line(b2), ring(*hand2)]),
    step('The skirt', 'Draw a line across the bottom of the M. Then draw a skirt under it that gets wider at the bottom.', [ring(*skirt)]),
    step('Legs and shoes', 'Draw two legs under the skirt, and a shoe on each one.',
         [line(l) for l in legs] + [ring(*shoeR), ring(*shoeL)]),
    step('The kite', 'Draw a kite up in the sky: a diamond, taller at the bottom. Draw a cross inside it.',
         [ring(*kite)] + [line(s) for s in spars]),
    step('String and tail', 'Draw a string from her hand to the kite. Give the kite a wiggly tail with two bows on it.',
         [line(string), line(*tail)] + [ring(*b) for b in bows]),
    step('Colour peach', 'Colour her face, neck, arms, hands and legs peach, or the colour of your mum’s skin.',
         [fill(PEACH, *head), chest, arm_fill(a1, b1, c1), arm_fill(a2, b2, c2), fill(PEACH, *hand1), fill(PEACH, *hand2), legR, legL], use='peach'),
    step('Colour red', 'Colour the dress red: the top and the skirt. Colour her shoes and the bows on the kite red too.',
         [bodice, fill(RED, *skirt), fill(RED, *shoeR), fill(RED, *shoeL)] + [fill(RED, *b) for b in bows], use='red'),
    step('Colour the hair', 'Colour her hair brown, or the same colour as your mum’s hair.', [hair_f], use='brown'),
    step('Colour the kite', 'Colour the kite yellow.', kite_f, use='yellow'),
]
D = drawing('dx_mum_m', 'M is for Mum', 3, 15, 'things', ['Letters', 'Around the house'],
            'Mum in a red dress, flying a kite. The capital M is hiding in her: it is the top of her dress, and the V in the middle is the V-neck.',
            steps, ['peach', 'red', 'brown', 'yellow'])
save('mum', D, {'set': 'house-AZ', 'slot': 'M', 'kind': 'hop', 'age_from': 5})
