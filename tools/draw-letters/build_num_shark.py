"""7 is for Shark (dx_shark_7), Animals 1 to 9, slot 7. Built from Claude's sketch "Shark 2" (picked 17 Nov 2026).
The 7 is the flat top of the shark's head and the slanting underside of its pointed nose."""
from numkit import *

GY, LB = FILL['grey'], FILL['lblue']

# the 7
S7, N7, E7 = P(30, 35), P(91, 35), P(55, 73)
top7, slant = Seg(S7, N7), Seg(N7, E7)

# tummy, tail and back: from the bottom of the 7 round to its start
belly = qc(E7, (33, 77), (15, 61))
TB = P(15, 61)
tail = [Seg(TB, (3, 73)), Seg((3, 73), (7, 52)), Seg((7, 52), (2.4, 32)), Seg((2.4, 32), (15, 48))]
back = [qc((15, 48), (18, 42), (20, 39)), Seg((20, 39), S7)]
FB0 = P(20, 39)

# where things meet the tummy line
def on_belly(x):
    return P(*belly.at(seg_x(belly, x)))
F2, F1, D0 = on_belly(46.4), on_belly(35.6), on_belly(24)
bp = chain_split_at([belly], F2); b_a = bp[0]                     # 7 .. F2
bq = chain_split_at(bp[1], F1); b_b, rest = bq                     # F2 .. F1, F1 ..
br = chain_split_at(rest, D0); b_c, b_d = br                       # F1 .. D0, D0 .. tail

# fins
dorsal = [Seg(FB0, (24.4, 15.6)), Seg((24.4, 15.6), S7)]
FT = P(29.6, 88.6)
bottom_fin = [Seg(F2, FT), Seg(FT, F1)]

# white tummy: from the tummy line up to the 7's slanting line
D1 = P(*slant.at(0.7))
divider = Seg(D0, (36, 62.4), (50, 61.2), D1)
sl_a, sl_b = chain_split_at([slant], D1)

gills = [qc((47, 46), (44.5, 52), (47, 58)), qc((53, 46), (50.5, 52), (53, 58))]
bub = [Ell(93.2, 17, 2.8), Ell(87.6, 8.6, 2)]

steps = [
    step('Start with a 7', 'Draw a big 7: a straight line across the top, then a long slanting line down to the left.', [line(top7, slant)]),
    step('The body', 'From the bottom of the 7, draw the tummy round to a big pointy tail, then the back up to the top of the 7.',
         [line(belly, *tail, *back)]),
    step('The fins', 'Draw a pointy fin on the shark’s back, and another one under its tummy.', [line(*dorsal), line(*bottom_fin)]),
    step('The white tummy', 'Draw a curved line from the bottom of the shark across to the slanting line of the 7.', [line(divider)]),
    step('The face', 'Draw a dot for the eye, two curved lines for the gills, and two bubbles.',
         [dot(75, 42, 3.6)] + [line(g) for g in gills] + [ring(*b.ring()) for b in bub]),
]
body_out = [top7] + sl_a + [divider.rev()] + b_d + tail + back
steps += [
    step('Colour grey', 'Colour the shark and its fins grey. Leave its tummy white.',
         [fill(GY, *body_out), fill(GY, *dorsal, back[1].rev()), fill(GY, *bottom_fin, *rev(b_b))], use='grey'),
    step('Colour light blue', 'Colour the bubbles light blue.', [fill(LB, *b.ring()) for b in bub], use='lblue'),
]
P_ = drawing('dx_shark_7', '7 is for Shark', 2, 10, 'animals', ['Numbers', 'Animals'],
             'A big shark with a white tummy, swimming along. The 7 is hiding in it: it is the flat top of the shark’s '
             'head and the slanting underside of its pointed nose.',
             steps, ['grey', 'lblue'])
P_ = move(P_, 1.4, 0)
save('num7shark', P_, {'set': 'animals-09', 'slot': '7', 'kind': 'swim', 'age_from': 5})
