"""B is for Brother (dx_brother_b), Around the house A to Z, slot B. A boy on a scooter, going to the left.
The B is his school bag on his back: its straight line is against his back and its two bumps are the bag.
Nothing crosses the B: his body, trousers and arm only touch its straight line."""
from famkit import *

PEACH, RED, ORANGE, BLUE, BLACK = FILL['peach'], FILL['red'], FILL['orange'], FILL['blue'], FILL['black']

# ---- 1: the B ----
BX, BT, BM, BB = 56.0, 40.0, 51.5, 64.0
stem_b = Seg((BX, BT), (BX, BB))
bowl1 = Seg((BX, BT), (66.0, BT), (66.0, BM), (BX, BM))
bowl2 = Seg((BX, BM), (68.4, BM), (68.4, BB), (BX, BB))

# ---- 2: head and face ----
HC, HR = (49.5, 31.0), 8.5
head = ring_from(HC, HR, -90)
eyes = [dot(46.4, 30.2, w=2.6), dot(52.6, 30.2, w=2.6)]
smile = Seg((46.2, 33.4), (47.4, 36.0), (51.6, 36.0), (52.8, 33.4))

# ---- 3: the hair ----
HL, HRt = oc(HC, HR, 200), oc(HC, HR, -20)
zig = poly((44.0, 18.6), (46.0, 15.4), (48.6, 18.2), (50.8, 14.8), (53.2, 18.2), (55.6, 15.6), (56.8, 19.6))
hair = [Seg(HL, (40.2, 24.6), (41.4, 20.4), (44.0, 18.6))] + zig + [Seg((56.8, 19.6), (58.8, 21.6), (59.2, 25.4), HRt)]

# ---- 4: neck and body ----
SH0, FR = P(BX, 43.5), P(45.0, 48.0)
shoulder = Seg(SH0, (51.0, 41.4), (45.5, 42.0), FR)
nLt, nRt = oc(HC, HR, 105), oc(HC, HR, 75)
sh = split_x(shoulder, [nRt[0], nLt[0]])
nRb, nLb = sh[0].b, sh[1].b
neckL, neckR = Seg(nLt, nLb), Seg(nRt, nRb)
HIP = 64.0
front = Seg(FR, (45.0, HIP)); waist = Seg((45.0, HIP), (BX, HIP))

# ---- 5: the arm, holding on ----
RH, CUFF = 3.0, 4.0
aA, aB = P(45.0, 49.2), P(45.0, 53.7)
d = unit(-1.0, -0.1)
hc = (45.0 + d[0] * 13.4, 51.45 + d[1] * 13.4)
ea, eb, aa, _ = limb(aA, aB, d, hc, RH)
a4, b4 = P(aA[0] + d[0] * CUFF, aA[1] + d[1] * CUFF), P(aB[0] + d[0] * CUFF, aB[1] + d[1] * CUFF)
hand = ring_from(hc, RH, aa)

# ---- 6: the trousers ----
DT = 82.5          # top of the scooter board
ST = 78.5          # top of the shoes
tr_front = Seg((45.0, HIP), (39.0, ST))
tr_inner = poly((43.5, ST), (48.0, 69.5), (53.0, ST))
tr_back = Seg((57.5, ST), (BX, HIP))

# ---- 7: the shoes, standing on the board ----
shoe1 = [Seg((33.5, DT), (33.5, 79.8), (35.0, ST), (38.0, ST)), Seg((38.0, ST), (44.0, ST)),
         Seg((44.0, ST), (45.4, ST), (46.0, 79.6), (46.0, 80.6)), Seg((46.0, 80.6), (46.0, DT))]
shoe2 = shift(shoe1, 14.5, 0.0)

# ---- 8: the scooter ----
bar_y = hc[1]
WF, WR_, RW = (21.5, 90.5), (58.5, 90.3), 4.0
stem_s = Seg(oc(WF, RW, -90), (25.0, bar_y))
handlebar = Seg((20.5, bar_y), P(hc[0] - RH, bar_y))
assert abs(oc(hc, RH, 180)[1] - P(0, bar_y)[1]) < 0.01
s_top, s_bot = at_y(stem_s, DT), at_y(stem_s, 86.0)
deck = [Seg(s_top, (62.0, DT))] + arc(62.0, 84.25, 1.75, 1.75, -90, 90, start=P(62.0, DT), end=P(62.0, 86.0)) + [Seg((62.0, 86.0), s_bot)]
wheelF, wheelR = ring_from(WF, RW, -90), ring_from(WR_, 3.8, -90)

# ---- 9: speed lines ----
speed = [Seg((71.0, 58.0), (81.0, 58.0)), Seg((73.0, 64.0), (86.0, 64.0)), Seg((71.0, 70.0), (81.0, 70.0))]

# ---- colours ----
face = fill(PEACH, *head)
neck_f = fill(PEACH, neckL, sh[1].rev(), neckR.rev(), arc(HC[0], HC[1], HR, HR, 75, 105, start=nRt, end=nLt))
forearm = fill(PEACH, Seg(a4, ea.b), arc_via(hc, RH, ea.b, eb.b, ang(hc, aA)), Seg(eb.b, b4), Seg(b4, a4))
bag1 = fill(RED, bowl1, Seg((BX, BM), (BX, BT)))
bag2 = fill(RED, bowl2, Seg((BX, BB), (BX, BM)))
deck_f = fill(RED, deck, Seg(s_bot, s_top))
shirt = fill(ORANGE, sh, front, waist, Seg((BX, HIP), SH0))
sleeve = fill(ORANGE, Seg(aA, a4), Seg(a4, b4), Seg(b4, aB), Seg(aB, aA))
trousers = fill(BLUE, tr_front, Seg((39.0, ST), (43.5, ST)), tr_inner, Seg((53.0, ST), (57.5, ST)), tr_back, waist.rev())
hair_f = fill(BLACK, hair, arc(HC[0], HC[1], HR, HR, -20, -160, start=HRt, end=HL))
shoe_f = [fill(BLACK, s, Seg(s[-1].b, s[0].a)) for s in (shoe1, shoe2)]

steps = [
    step('Start with a B', 'Draw a big capital B: a straight line down, then two round bumps on its right side. This B is hiding in the picture.',
         [line(stem_b), line(bowl1, bowl2)]),
    step('Head and face', 'Draw a round head above the B, a little to the left. Give him two dots for eyes and a big smile.',
         [ring(*head)] + eyes + [line(smile)]),
    step('Spiky hair', 'Draw his hair round the top of his head, with spikes.', [line(*hair)]),
    step('Neck and body', 'Draw a short neck. Then draw his body: a curve for his shoulder, a line down his front and a line across to the B.',
         [line(neckL), line(neckR), line(shoulder, front, waist)]),
    step('The arm', 'Draw his arm reaching out in front, with a round hand. Draw a line across it for the end of his sleeve.',
         [line(ea), line(eb), ring(*hand), line(Seg(a4, b4))]),
    step('The trousers', 'Draw his trousers: one leg a bit in front and one a bit behind. The back of them comes down from the B.',
         [line(tr_front), line(*tr_inner), line(tr_back)]),
    step('The shoes', 'Draw a shoe at the bottom of each leg. The toes point to the left.', [line(*shoe1), line(*shoe2)]),
    step('The scooter', 'Draw a pole from his hand down to the ground, with a handlebar at the top. Draw a long board under his shoes, joined to the pole.',
         [line(stem_s), line(handlebar), line(*deck)]),
    step('Wheels and speed', 'Draw a wheel under each end of the board. Draw three lines behind him: he is going fast!',
         [ring(*wheelF), ring(*wheelR)] + [line(s) for s in speed]),
    step('Colour peach', 'Colour his face, neck, arm and hand peach, or the colour of your brother’s skin.',
         [face, neck_f, forearm, fill(PEACH, *hand)], use='peach'),
    step('Colour red', 'Colour his school bag red: both bumps of the B. Colour the scooter board red too.', [bag1, bag2, deck_f], use='red'),
    step('Colour orange', 'Colour his T-shirt and his sleeve orange.', [shirt, sleeve], use='orange'),
    step('Colour blue', 'Colour his trousers blue.', [trousers], use='blue'),
    step('Colour black', 'Colour his hair, his shoes and the two wheels black.',
         [hair_f] + shoe_f + [fill(BLACK, *wheelF), fill(BLACK, *wheelR)], use='black'),
]
D = drawing('dx_brother_b', 'B is for Brother', 3, 15, 'things', ['Letters', 'Around the house'],
            'A big brother whizzing along on his scooter. The capital B is hiding in it: it is the red school bag on his back.',
            steps, ['peach', 'red', 'orange', 'blue', 'black'])
save('brother', D, {'set': 'house-AZ', 'slot': 'B', 'kind': 'hop', 'age_from': 5})
