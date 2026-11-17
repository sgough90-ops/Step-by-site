"""n is for nan (dx_nan_n), Around the house a to z, slot n. Nan in her armchair, knitting a scarf.
The n is the back of the armchair: its stick is the left side and its arch goes over the top and down the right side.
Nothing crosses the n: the chair arms, Nan and her hair are all inside it, and only touch it."""
from famkit import *

PEACH, PURPLE, GREY, PINK, GREEN = FILL['peach'], FILL['purple'], FILL['grey'], FILL['pink'], FILL['green']

# ---- 1: the n ----
NL, NR, NT, NB = 22.0, 76.0, 38.0, 78.0
stemL = Seg((NL, NT), (NL, NB))
archA = [Seg((NL, NT), (NL, 22.5), (33.5, 14.0), (49.0, 14.0)), Seg((49.0, 14.0), (64.5, 14.0), (NR, 22.5), (NR, NT))]
stemR = Seg((NR, NT), (NR, NB))

# ---- 2: head and face ----
HC, HR = (49.0, 39.0), 8.5
head = ring_from(HC, HR, -90)
lensL, lensR = ring_from((45.2, 39.2), 2.9, -90), ring_from((52.8, 39.2), 2.9, -90)
bridge = Seg((48.1, 39.2), (49.9, 39.2))
eyes = [dot(45.2, 39.4, w=2.2), dot(52.8, 39.4, w=2.2)]
smile = Seg((45.8, 43.0), (46.8, 45.1), (51.2, 45.1), (52.2, 43.0))

# ---- 3: curly hair with a bun ----
RO = 11.2
L_, R_ = oc(HC, HR, 195), oc(HC, HR, 345)
def scallop(a, b, bulge=1.6):
    return Seg(oc(HC, RO, a), oc(HC, RO + bulge, a + (b - a) * 0.15), oc(HC, RO + bulge, a + (b - a) * 0.85), oc(HC, RO, b))
s3, s4 = oc(HC, RO, 255), oc(HC, RO, 285)
hair = [Seg(L_, (L_[0] - 1.6, L_[1] - 0.2), oc(HC, RO, 203)[0:1] + (oc(HC, RO, 203)[1] + 0.8,), oc(HC, RO, 205)),
        scallop(205, 230), scallop(230, 255),
        Seg(s3, (42.6, 26.4), (43.2, 19.6), (49.0, 19.6)), Seg((49.0, 19.6), (54.8, 19.6), (55.4, 26.4), s4),
        scallop(285, 310), scallop(310, 335),
        Seg(oc(HC, RO, 335), (oc(HC, RO, 337)[0], oc(HC, RO, 337)[1] + 0.8), (R_[0] + 1.6, R_[1] - 0.2), R_)]

# ---- 4: neck and body ----
nLt, nRt = oc(HC, HR, 105), oc(HC, HR, 75)
CY = 49.6
nLb, nRb = P(nLt[0], CY), P(nRt[0], CY)
WY = 66.0
bodyL = [Seg(nLb, (41.5, 49.8), (37.2, 51.2), (35.8, 55.0)), Seg((35.8, 55.0), (34.6, 58.6), (32.6, 62.0), (31.6, WY))]
bodyR = mirror(bodyL, 49.0)          # from the neck down the right side
collar = Seg(nLb, nRb)

# ---- 5: the arms of the chair, and its feet ----
inL = split_many(Seg((31.6, 61.0), (31.6, NB)), [(WY - 61.0) / (NB - 61.0)])
armL = [Seg((NL, 58.0), (28.6, 58.0))] + arc(28.6, 61.0, 3.0, 3.0, -90, 0, start=P(28.6, 58.0), end=P(31.6, 61.0)) + inL + [Seg((31.6, NB), (NL, NB))]
armR = mirror(armL, 49.0)
footL = poly((24.0, NB), (24.0, 82.5), (29.6, 82.5), (29.6, NB)); footR = mirror(footL, 49.0)

# ---- 6: hands and needles ----
RH = 2.6
h1, h2 = (41.6, 58.6), (56.4, 58.6)
d1 = unit(1.0, -0.55); d2 = (-d1[0], d1[1])
p1 = P(h1[0] + d1[0] * RH, h1[1] + d1[1] * RH); tip1 = P(h1[0] + d1[0] * 13.0, h1[1] + d1[1] * 13.0)
p2 = P(h2[0] + d2[0] * RH, h2[1] + d2[1] * RH); tip2 = P(h2[0] + d2[0] * 13.0, h2[1] + d2[1] * 13.0)
needle1 = Seg(p1, tip1)
X = at_x(needle1, 49.0)
hand1, hand2 = ring_from(h1, RH, ang(h1, p1)), ring_from(h2, RH, ang(h2, p2))

# ---- 7: the knitting and a ball of wool ----
STOP = 56.0
kL, kR = at_y(needle1, STOP), None
kR = P(98.0 - kL[0], STOP)
assert abs(kR[0] - at_y(Seg(p2, tip2), STOP)[0]) < 0.02
needle2 = [Seg(p2, X), Seg(X, tip2)]
SB = 73.0
sideL = split_many(Seg(kL, (44.5, SB)), [(y - STOP) / (SB - STOP) for y in (62.5, WY, 67.5)])
sideR = split_many(Seg(kR, (53.5, SB)), [(y - STOP) / (SB - STOP) for y in (62.5, WY, 67.5)])
s_top, s_bot = Seg(kL, kR), Seg((53.5, SB), (44.5, SB))
stripes = [Seg(sideL[0].b, sideR[0].b), Seg(sideL[2].b, sideR[2].b)]
fringe = [Seg((x, SB), (x, 75.6)) for x in (45.6, 47.9, 50.1, 52.4)]
WB, WRd = (86.0, 90.0), 5.5
wool = ring_from(WB, WRd, -90)
wl = [Seg(oc(WB, WRd, 205), (83.0, 86.6), (88.0, 85.2), oc(WB, WRd, -40)), Seg(oc(WB, WRd, 150), (84.0, 92.4), (89.4, 92.0), oc(WB, WRd, 20))]
strand = Seg(oc(WB, WRd, 140), (79.6, 95.6), (76.4, 92.6), (73.2, 95.4))

# ---- 8: skirt, legs and slippers ----
waistL, waistR = Seg((31.6, WY), sideL[1].b), Seg(sideR[1].b, (66.4, WY))
hem = Seg((66.8, 86.0), (58.0, 87.6), (40.0, 87.6), (31.2, 86.0))
hp = split_x(hem, [58.0, 54.0, 44.0, 40.0])
tops = [p.b for p in hp[:-1]]
skirt = [Seg((66.4, NB), (66.8, 86.0))] + hp + [Seg((31.2, 86.0), (31.6, NB))]
SY = 92.0
legs = [Seg(t, (t[0], SY)) for t in tops]
slipR, slipL = rrect(52.0, SY, 60.5, 96.0, 2.0), rrect(37.5, SY, 46.0, 96.0, 2.0)

# ---- colours ----
neck_f = fill(PEACH, Seg(nLt, nLb), collar, Seg(nRb, nRt), arc(HC[0], HC[1], HR, HR, 75, 105, start=nRt, end=nLt))
legR = fill(PEACH, Seg(tops[1], (tops[1][0], SY)), Seg((tops[1][0], SY), (tops[0][0], SY)), Seg((tops[0][0], SY), tops[0]), hp[1])
legL = fill(PEACH, Seg(tops[3], (tops[3][0], SY)), Seg((tops[3][0], SY), (tops[2][0], SY)), Seg((tops[2][0], SY), tops[2]), hp[3])
body_f = fill(PURPLE, collar, bodyR, waistR.rev(), sideR[1].rev(), sideR[0].rev(), s_top.rev(), sideL[0], sideL[1], waistL.rev(), rev(bodyL),
              cut=[d_fill(*hand1), d_fill(*hand2)])
skirt_f = fill(PURPLE, waistL, sideL[2], sideL[3], s_bot.rev(), sideR[3].rev(), sideR[2].rev(), waistR, mirror(inL, 49.0)[1], skirt, inL[1].rev())
hair_f = fill(GREY, hair, arc(HC[0], HC[1], HR, HR, 345, 195, start=R_, end=L_))
knit1 = fill(PINK, s_top, sideR[0], stripes[0].rev(), sideL[0].rev())
knit2 = fill(PINK, stripes[1], sideR[3], s_bot, sideL[3].rev())
armL_f = fill(GREEN, armL, Seg((NL, NB), (NL, 58.0)))
armR_f = fill(GREEN, armR, Seg((NR, NB), (NR, 58.0)))
feet_f = [fill(GREEN, footL, Seg((29.6, NB), (24.0, NB))), fill(GREEN, footR, Seg(footR[-1].b, footR[0].a))]
armR_top = armR[:2]                      # along the top of the right arm, from the n to the corner
back_f = fill(GREEN, Seg((NL, 58.0), (NL, NT)), archA, Seg((NR, NT), (NR, 58.0)), armR[0], armR[1], mirror(inL, 49.0)[0],
              rev(bodyR), Seg(nRb, nRt), arc(HC[0], HC[1], HR, HR, 75, -15, start=nRt, end=R_), rev(hair),
              arc(HC[0], HC[1], HR, HR, 195, 105, start=L_, end=nLt), Seg(nLt, nLb), bodyL, inL[0].rev(), rev(armL[1:2]), armL[0].rev())

steps = [
    step('Start with an n', 'Draw a small letter n: a straight line down, then an arch from its top, over and down. This n is hiding in the armchair.',
         [line(stemL), line(*archA, stemR)]),
    step('Head and face', 'Draw Nan’s round head in the middle of the n. Give her round glasses, two dots for eyes and a smile.',
         [ring(*head), ring(*lensL), ring(*lensR), line(bridge)] + eyes + [line(smile)]),
    step('Hair and a bun', 'Draw her curly hair round the top of her head, with a round bun on top.', [line(*hair)]),
    step('Neck and body', 'Draw a short neck with a line across the bottom. Then draw her shoulders and her sides, getting wider as they go down.',
         [line(Seg(nLt, nLb)), line(Seg(nRt, nRb)), line(collar), line(*bodyL), line(*bodyR)]),
    step('The chair', 'Draw the arms of the armchair inside the bottom of the n, one on each side. Draw a little foot under each one.',
         [line(*armL), line(*armR), line(*footL), line(*footR)]),
    step('Hands and needles', 'Draw two round hands. Draw a knitting needle from each hand. The needles cross in the middle.',
         [ring(*hand1), ring(*hand2), line(needle1), line(needle2[0]), line(needle2[1])]),
    step('The knitting', 'Draw a scarf hanging from the needles, with two stripes and a fringe. Draw a ball of wool on the floor.',
         [line(sideL), line(s_top), line(sideR), line(s_bot)] + [line(s) for s in stripes] + [line(f) for f in fringe] +
         [ring(*wool)] + [line(w) for w in wl] + [line(strand)]),
    step('Skirt and slippers', 'Draw a line across her middle on each side of the scarf. Draw her skirt, two legs and a pair of slippers.',
         [line(waistL), line(waistR), line(*skirt)] + [line(l) for l in legs] + [ring(*slipR), ring(*slipL)]),
    step('Colour peach', 'Colour her face, neck, hands and legs peach, or the colour of your nan’s skin.',
         [fill(PEACH, *head), neck_f, fill(PEACH, *hand1), fill(PEACH, *hand2), legR, legL], use='peach'),
    step('Colour purple', 'Colour her cardigan and her skirt purple.', [body_f, skirt_f], use='purple'),
    step('Colour the hair', 'Colour her hair grey, or the same colour as your nan’s hair.', [hair_f], use='grey'),
    step('Colour pink', 'Colour the scarf pink, leaving the middle stripe white. Colour the ball of wool and her slippers pink too.',
         [knit1, knit2, fill(PINK, *wool), fill(PINK, *slipR), fill(PINK, *slipL)], use='pink'),
    step('Colour the chair', 'Colour the armchair green: the back, the two arms and the feet.', [back_f, armL_f, armR_f] + feet_f, use='green'),
]
D = drawing('dx_nan_n', 'n is for nan', 3, 15, 'things', ['Letters', 'Around the house'],
            'Nan in her big green armchair, knitting a pink scarf. The small letter n is hiding in it: it is the back of the armchair.',
            steps, ['peach', 'purple', 'grey', 'pink', 'green'])
save('nan', D, {'set': 'house-az', 'slot': 'n', 'kind': 'key', 'age_from': 5})
