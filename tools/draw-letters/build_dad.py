"""D is for Dad (dx_dad_d), Around the house A to Z, slot D. Dad kicking a football, seen from the side.
The D is his T-shirt: its straight line is his back and its round side is his chest and tummy.
Nothing crosses the D: the neck, arms and shorts only touch it."""
from famkit import *

PEACH, GREEN, BLUE, RED, BLACK = FILL['peach'], FILL['green'], FILL['blue'], FILL['red'], FILL['black']

# ---- 1: the D ----
DX0, DT, DB, DC, DR = 36.0, 40.0, 68.0, (44.0, 54.0), 14.0
stick = Seg((DX0, DB), (DX0, DT))
d_top = Seg((DX0, DT), (44.0, DT))
d_arc = arc(DC[0], DC[1], DR, DR, -90, 90, start=P(44.0, DT), end=P(44.0, DB))
d_bot = Seg((44.0, DB), (DX0, DB))
def on_d(a): return oc(DC, DR, a)
def d_piece(a0, a1, p0=None, p1=None):
    return arc(DC[0], DC[1], DR, DR, a0, a1, start=p0 or on_d(a0), end=p1 or on_d(a1))

# ---- 2: head and neck ----
HC, HR = (45.0, 28.0), 9.0
head = ring_from(HC, HR, -90)
nLt, nRt = oc(HC, HR, 105), oc(HC, HR, 75)
nLb = P(nLt[0], DT)
aR = -math.degrees(math.acos((nRt[0] - DC[0]) / DR)); nRb = on_d(aR)
neckL, neckR = Seg(nLt, nLb), Seg(nRt, nRb)

# ---- 3: the face (looking at us) ----
eyes = [dot(41.6, 27.4, w=2.6), dot(48.4, 27.4, w=2.6)]
smile = Seg((41.4, 31.2), (42.6, 34.0), (47.4, 34.0), (48.6, 31.2))

# ---- 4: the hair ----
HL, HRt = oc(HC, HR, 200), oc(HC, HR, -20)
hair = [Seg(HL, (34.4, 21.0), (37.4, 16.2), (45.0, 16.2)), Seg((45.0, 16.2), (52.6, 16.2), (55.6, 21.0), HRt)]

# ---- 5: the arms, with the ends of the sleeves ----
RH, CUFF = 3.2, 4.0
fA, fB = on_d(-55), on_d(-38)
df = unit(0.8, -0.6); fc = ((fA[0] + fB[0]) / 2 + df[0] * 13.0, (fA[1] + fB[1]) / 2 + df[1] * 13.0)
fa, fb, faa, _ = limb(fA, fB, df, fc, RH)
bA, bB = P(DX0, 44.0), P(DX0, 50.0)
db = unit(-0.8, 0.6); bc = (DX0 + db[0] * 12.5, 47.0 + db[1] * 12.5)
ba, bb, baa, _ = limb(bA, bB, db, bc, RH)
def cuff_pts(a, b, d):
    return P(a.a[0] + d[0] * CUFF, a.a[1] + d[1] * CUFF), P(b.a[0] + d[0] * CUFF, b.a[1] + d[1] * CUFF)
fa4, fb4 = cuff_pts(fa, fb, df); ba4, bb4 = cuff_pts(ba, bb, db)
handF, handB = ring_from(fc, RH, faa), ring_from(bc, RH, baa)

# ---- 6: the shorts ----
SF = on_d(60)
back = Seg((DX0, DB), (34.5, 79.0))
# along the bottom, left to right, with a little notch between the legs so they read as shorts
bottom = poly((34.5, 79.0), (37.5, 78.8), (42.0, 78.6), (44.0, 75.6), (46.0, 78.3), (51.0, 77.9), (53.5, 77.7))
front = Seg((53.5, 77.7), SF)
lt = [bottom[0].b, bottom[1].b, bottom[3].b, bottom[4].b]       # leg tops: standing leg 0, 1; kicking leg 2, 3

# ---- 7: legs and trainers ----
SY = 89.0
stand = [Seg(lt[0], (lt[0][0], SY)), Seg(lt[1], (lt[1][0], SY))]
shoe1 = rrect(35.0, SY, 47.5, 94.0, 2.5)
U, Vd, O = (0.8, -0.6), (0.6, 0.8), lt[2]           # the kicking leg's own frame: V down the leg, U along the foot
def W_(u, v): return (O[0] + U[0] * u + Vd[0] * v, O[1] + U[1] * u + Vd[1] * v)
rel = (lt[3][0] - O[0], lt[3][1] - O[1]); u3 = rel[0] * U[0] + rel[1] * U[1]
L = 10.0
kb_end, kf_end = P(*W_(0, L)), P(*W_(u3, L))
kick = [Seg(lt[2], kb_end), Seg(lt[3], kf_end)]
shoe2 = xf(rrect(-2.0, L, 11.0, L + 4.5, 2.0), lambda x, y: W_(x, y))
# the shoe's top edge must pass through both leg ends: re-cut it there so the colour can follow it exactly
assert abs(u3 - 4.234) < 0.05, u3

# ---- 8: the football ----
BC, BR = (71.0, 77.0), 6.6
ball = ring_from(BC, BR, -90)
pent = [oc(BC, 2.7, -90 + 72 * i) for i in range(5)]
pentagon = poly(*pent, closed=True)
spokes = [Seg(p, oc(BC, BR, -90 + 72 * i)) for i, p in enumerate(pent)]

# ---- colours ----
face = fill(PEACH, *head)
neck_f = fill(PEACH, neckL, Seg(nLb, (44.0, DT)), d_piece(-90, aR, P(44.0, DT), nRb), neckR.rev(),
              arc(HC[0], HC[1], HR, HR, 75, 105, start=nRt, end=nLt))
def forearm(a, b, a4, b4, c):
    return fill(PEACH, Seg(a4, a.b), arc_via(c, RH, a.b, b.b, ang(c, a.a)), Seg(b.b, b4), Seg(b4, a4))
legS = fill(PEACH, Seg(lt[0], (lt[0][0], SY)), Seg((lt[0][0], SY), (lt[1][0], SY)), Seg((lt[1][0], SY), lt[1]), bottom[1].rev())
legK = fill(PEACH, Seg(lt[2], kb_end), Seg(kb_end, kf_end), Seg(kf_end, lt[3]), bottom[4].rev())
shirt = fill(GREEN, stick, d_top, d_arc, d_bot)
sleeveF = fill(GREEN, Seg(fA, fa4), Seg(fa4, fb4), Seg(fb4, fB), d_piece(-38, -55, fB, fA))
sleeveB = fill(GREEN, Seg(bA, ba4), Seg(ba4, bb4), Seg(bb4, bB), Seg(bB, bA))
shorts = fill(BLUE, Seg((DX0, DB), (44.0, DB)), d_piece(90, 60, P(44.0, DB), SF), front.rev(), rev(bottom), back.rev())
hair_f = fill(BLACK, hair, arc(HC[0], HC[1], HR, HR, -20, -160, start=HRt, end=HL))

steps = [
    step('Start with a D', 'Draw a big capital D: a straight line down, then a big round curve from the top to the bottom. This D is hiding in Dad.',
         [line(stick.rev()), line(d_top, *d_arc, d_bot)]),
    step('Head and neck', 'Draw a round head above the D. Join it to the D with a short neck.',
         [ring(*head), line(neckL), line(neckR)]),
    step('The face', 'Give him two dots for eyes and a big smile.', eyes + [line(smile)]),
    step('The hair', 'Draw his short hair over the top of his head.', [line(*hair)]),
    step('The arms', 'Draw an arm out in front and one out behind, each with a round hand. Draw a line across each arm for the sleeve.',
         [line(fa), line(fb), ring(*handF), line(Seg(fa4, fb4)), line(ba), line(bb), ring(*handB), line(Seg(ba4, bb4))]),
    step('The shorts', 'Draw his shorts under the D.', [line(back, *bottom, front)]),
    step('Legs and trainers', 'Draw one leg standing straight down and one leg kicking forward. Give each one a trainer.',
         [line(s) for s in stand] + [ring(*shoe1)] + [line(k) for k in kick] + [ring(*shoe2)]),
    step('The football', 'Draw a football in front of his foot. Draw a little shape with five sides in the middle, and five lines out to the edge.',
         [ring(*ball), ring(*pentagon)] + [line(s) for s in spokes]),
    step('Colour peach', 'Colour his face, neck, hands, arms and legs peach, or the colour of your dad’s skin.',
         [face, neck_f, forearm(fa, fb, fa4, fb4, fc), forearm(ba, bb, ba4, bb4, bc), fill(PEACH, *handF), fill(PEACH, *handB), legS, legK],
         use='peach'),
    step('Colour green', 'Colour his T-shirt green, with the two sleeves.', [shirt, sleeveF, sleeveB], use='green'),
    step('Colour blue', 'Colour his shorts blue.', [shorts], use='blue'),
    step('Colour red', 'Colour his trainers red.', [fill(RED, *shoe1), fill(RED, *shoe2)], use='red'),
    step('Colour black', 'Colour his hair black, or the same colour as your dad’s hair. Colour the middle of the football black.',
         [hair_f, fill(BLACK, *pentagon)], use='black'),
]
D = drawing('dx_dad_d', 'D is for Dad', 3, 15, 'things', ['Letters', 'Around the house'],
            'Dad in a green T-shirt, kicking a football. The capital D is hiding in him: it is his T-shirt. The straight line is his back and the round side is his tummy.',
            steps, ['peach', 'green', 'blue', 'red', 'black'])
save('dad', D, {'set': 'house-AZ', 'slot': 'D', 'kind': 'hop', 'age_from': 5})
