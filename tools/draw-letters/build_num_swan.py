"""2 is for Swan (dx_swan_2), Animals 1 to 9, slot 2. Built from Claude's sketch "Goose 3" (picked 17 Nov 2026; he asked
for it to be called Swan). The 2 is the curve under the swan's head, the front of its neck and chest, and the waterline."""
from numkit import *

GY, OR, BK = FILL['grey'], FILL['orange'], FILL['black']

# the 2
C2 = Ell(39, 30, 11)
s2 = C2.P(180); bk = C2.P(220); e2 = C2.P(400 - 360)
arc_beak = C2.arc(180, 220, start=s2, end=bk)            # the bottom of the 2's curve: the beak sits on it
arc_rest = C2.arc(220, 400, start=bk, end=e2)
BL, BR = P(20, 75), P(85, 75)
slant, base = Seg(e2, BL), Seg(BL, BR)

# head and neck: from the top of the beak, over the head, down the back of the neck
N = P(62, 49)
head = [Seg(bk, (30.2, 15.4), (32.6, 11.2), (39, 11)), Seg((39, 11), (47.6, 10.6), (56.4, 12.6), (58.6, 22.4)),
        Seg((58.6, 22.4), (60.4, 30.4), (61.6, 40), N)]
# back and tail, down to the end of the 2
TT = P(96, 49)
back = qc(N, (75, 42), TT)
tail = [Seg(TT, (93, 56)), qc((93, 56), (94, 70), BR)]

# beak, with the black knob at its base
TIP = P(14, 28.5)
b_up, b_lo = Seg(bk, TIP), Seg(TIP, s2)
K1 = P(*b_up.at(0.34)); K2 = P(*b_lo.at(0.68))
up_a, up_b = chain_split_at([b_up], K1)
lo_a, lo_b = chain_split_at([b_lo], K2)
knob = qc(K1, (23.6, 26.8), K2)

# wings: the front wing grows out of the back, the back wing out of the front wing's front edge
A = P(*back.at(seg_x(back, 64.6)))
B = P(*back.at(seg_x(back, 87.2)))
T1 = P(95.6, 21)
fw_lead = qc(A, (73.4, 27.6), T1)
fw_trail = [qc(T1, (89.8, 28.6), (95, 33)), qc((95, 33), (86.6, 36.6), (91.4, 42)), qc((91.4, 42), (85.4, 43), B)]
Cc = P(*fw_lead.at(seg_x(fw_lead, 66.8)))
Dd = P(*fw_lead.at(seg_x(fw_lead, 82.2)))
T2 = P(83.6, 8.2)
bw_lead = qc(Cc, (65.6, 21), T2)
bw_trail = [qc(T2, (81.6, 16.4), (86.4, 19.6)), qc((86.4, 19.6), (79.6, 21.4), Dd)]

waves = [Seg((3, 83), (5.67, 81.33), (8.33, 81.33), (11, 83)), Seg((11, 83), (13.67, 84.67), (16.33, 84.67), (19, 83)),
         Seg((75, 85.2), (77.67, 83.53), (80.33, 83.53), (83, 85.2)), Seg((83, 85.2), (85.67, 86.87), (88.33, 86.87), (91, 85.2))]
splash = [Seg((14, 69.6), (9.2, 66.8)), Seg((12.4, 74.2), (6.4, 73.2))]

steps = [
    step('Start with a 2', 'Draw a big 2: round over the top, a long straight line down to the left, then a straight line along the bottom.',
         [line(*arc_beak, *arc_rest, slant, base)]),
    step('The head and neck', 'From the curve of the 2, draw the top of the head and the back of the neck, curving down.', [line(*head)]),
    step('The back and tail', 'Draw the back along to a pointy tail, then down to the end of the 2.', [line(back, *tail)]),
    step('The beak', 'Draw a pointy beak at the front, with a short line across it near the head.', [line(b_up, b_lo), line(knob)]),
    step('The front wing', 'Draw a big wing stretching up from the back, with a wavy edge.', [line(fw_lead, *fw_trail)]),
    step('The back wing', 'Draw the other wing peeping out behind it.', [line(bw_lead, *bw_trail)]),
    step('The eye and water', 'Draw a dot for the eye, little waves on the water and two splash lines.',
         [dot(36, 16, 3.4)] + [line(waves[0], waves[1]), line(waves[2], waves[3])] + [line(s) for s in splash]),
]
fw_piece = piece_between([fw_lead], Cc, Dd)
steps += [
    step('Colour grey', 'Colour the back wing grey. Leave the swan white.', [fill(GY, bw_lead, *bw_trail, *rev(fw_piece))], use='grey'),
    step('Colour orange', 'Colour the front of the beak orange.', [fill(OR, *up_b, *lo_a, knob.rev())], use='orange'),
    step('Colour black', 'Colour the end of the beak by the head black.', [fill(BK, *up_a, knob, *lo_b, *arc_beak)], use='black'),
]
P_ = drawing('dx_swan_2', '2 is for Swan', 2, 10, 'animals', ['Numbers', 'Animals'],
             'A swan on the water, stretching up its wings for a big flap. The 2 is hiding in it: it is the curve under '
             'the swan’s head, the front of its neck and the waterline.',
             steps, ['grey', 'orange', 'black'])
save('num2swan', P_, {'set': 'animals-09', 'slot': '2', 'kind': 'swim', 'age_from': 5})
