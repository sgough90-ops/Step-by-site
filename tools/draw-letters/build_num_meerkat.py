"""1 is for Meerkat (dx_meerkat_1), Animals 1 to 9, slot 1. Built from Claude's sketch "Meerkat 1" (picked 17 Nov 2026).
The 1 is the meerkat's straight back, and the top of its head sloping down to its nose is the flick."""
from numkit import *

LB, BR, GY = FILL['lbrown'], FILL['brown'], FILL['grey']

# the rock (drawn later, but the 1 and the tummy end on it)
R1 = Seg((25, 96), (25, 81), (39, 73), (56, 73))
R2 = Seg((56, 73), (73, 73), (85, 81), (85, 96))
S = P(*R2.at(seg_x(R2, 62)))                      # bottom of the 1
E = P(*R1.at(seg_x(R1, 52.6)))                    # bottom of the tummy
F2 = P(*R1.at(seg_x(R1, 45.6)))                   # front of the foot
TT = P(*R2.at(seg_x(R2, 76.5)))                   # tip of the tail

# the 1
F0, TOP = P(51, 23), P(62, 15)
flick, stick = Seg(F0, TOP), Seg(TOP, S)

# face: nose and chin
nose = qc(F0, (47, 25), (48, 28.5))
chin = qc(nose.b, (51, 31.5), (56, 30.5))

# the front: chest, two paws, tummy
A1, B1, A2, B2 = P(52.3, 40), P(51.3, 46), P(50.9, 50.6), P(50.8, 56.4)
chest = Seg(chin.b, (54, 31.6), (52.8, 36), A1)
paw1 = [Seg(A1, (49.2, 40.4), (45.6, 43.2), (46.2, 46.2)), Seg((46.2, 46.2), (46.7, 48.4), (50, 48.3), B1)]
mid = Seg(B1, (51.1, 47.8), (50.9, 49.2), A2)
paw2 = [Seg(A2, (48.4, 51), (46.6, 53.6), (47.3, 55.7)), Seg((47.3, 55.7), (47.9, 57.6), (50, 57.6), B2)]
belly = Seg(B2, (49.6, 62), (49.9, 69.5), E)
F1 = P(*belly.at(0.72))
belly_a, belly_b = chain_split_at([belly], F1)
front = [chest] + paw1 + [mid] + paw2 + belly_a + belly_b

# arms: the top edge of each arm, from the shoulder to its paw
arm1 = Seg((56.2, 36.6), (55.2, 37.6), (53.8, 38.9), A1)
arm2 = Seg((56.6, 45.2), (55, 46.4), (52.8, 48.4), A2)

# face details
patch = Ell(55.5, 23.6, 3.2, 2.5)
ear = Ell(59.7, 20.4, 1.35)

# foot and tail
foot = Seg(F1, (48.6, 69.6), (45.4, 71.2), F2)
TU0, TL0 = P(62, 59.5), P(62, 64.5)
tail_up = Seg(TU0, (70, 60.2), (75.2, 66), TT)
tail_lo = Seg(TL0, (67.6, 65.4), (72.4, 69.6), TT)

# rock pieces for the colours
r1a, r1b = chain_split_at([R1], F2)               # ground .. F2 .. top
r1b1, r1b2 = chain_split_at(r1b, E)               # F2 .. E, E .. top
r2a, r2b = chain_split_at([R2], S)                # top .. S, S .. ground
r2b1, r2b2 = chain_split_at(r2b, TT)              # S .. tail tip, tail tip .. ground
G0, G1 = P(4, 96), P(96, 96)
ground = Seg(G0, G1)
rock_base = Seg((85, 96), (25, 96))

grass = [qc((8, 96), (9.5, 92), (7.5, 89)), qc((11.6, 96), (12.1, 91.5), (14.6, 88.5)), qc((15, 96), (14, 93), (16, 90.6))]
rocklines = [qc((35, 86.5), (39.5, 83.6), (44, 85.4)), qc((69.5, 84.8), (73.8, 83.8), (77, 86.6))]

steps = [
    step('Start with a 1', 'Draw a big 1: a short line up to the right, then a long straight line down. Make it tall.', [line(flick, stick)]),
    step('The nose', 'From the start of the 1, draw a pointy nose and a little chin.', [line(nose, chin)]),
    step('The front', 'From the chin, draw the front of the meerkat down to the bottom, with two little paws sticking out.', [line(*front)]),
    step('The arms', 'Draw a short curved line down to the top of each paw.', [line(arm1), line(arm2)]),
    step('The eye and ear', 'Draw an oval with a dot in it for the eye, a dot on the nose and a small circle for the ear.',
         [ring(*patch.ring()), dot(55.5, 23.6, 2.4), dot(49.2, 26.4, 2.4), ring(*ear.ring())]),
    step('The rock', 'Draw a big round rock under the meerkat. Its top touches the bottom of the 1 and the bottom of the tummy.', [line(R1, R2)]),
    step('The foot and tail', 'Draw a foot at the front, and a long tail from the back down onto the rock.', [line(foot), line(tail_up), line(tail_lo)]),
    step('The ground', 'Draw a line along the ground, a little tuft of grass and two lines on the rock.',
         [line(ground)] + [line(g) for g in grass] + [line(r) for r in rocklines]),
]
body_out = [nose, chin] + front + [r1b2[0]] + r2a + [Seg(S, TOP), Seg(TOP, F0)]
cuts = [d_fill(*patch.ring()), d_fill(*ear.ring())]
steps += [
    step('Colour light brown', 'Colour the meerkat, its foot and its tail light brown.',
         [fill(LB, *body_out, cut=cuts), fill(LB, foot, *r1b1, *rev(belly_b)), fill(LB, tail_up, tail_lo.rev(), Seg(TL0, TU0))], use='lbrown'),
    step('Colour brown', 'Colour the eye patch and the ear brown.', [fill(BR, *patch.ring()), fill(BR, *ear.ring())], use='brown'),
    step('Colour grey', 'Colour the rock grey.', [fill(GY, R1, R2, rock_base)], use='grey'),
]
P_ = drawing('dx_meerkat_1', '1 is for Meerkat', 2, 10, 'animals', ['Numbers', 'Animals'],
             'A meerkat on the lookout from the top of a rock, with its paws held up. The 1 is hiding in it: '
             'it is the meerkat’s straight back, and the top of its head is the flick.',
             steps, ['lbrown', 'brown', 'grey'])
save('num1meerkat', P_, {'set': 'animals-09', 'slot': '1', 'kind': 'hop', 'age_from': 5})
