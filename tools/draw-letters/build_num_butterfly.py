"""3 is for Butterfly (dx_butterfly_3), Animals 1 to 9, slot 3. Built from Claude's sketch "Butterfly 2" (picked 17 Nov 2026).
The 3 is the round outer edges of the butterfly's top wing and bottom wing."""
from numkit import *

PU, BL, BK, BR, GR = FILL['purple'], FILL['blue'], FILL['black'], FILL['brown'], FILL['green']

# the 3
T0, MID, B0 = P(48, 17), P(52, 50), P(48, 83)
top3 = Seg(T0, (96, 17), (96, 50), MID)
bot3 = Seg(MID, (88, 50), (88, 83), B0)

# head and body
head = Ell(34, 34, 5)
body = Ell(35, 52, 5, 14)
H1, H2 = meet_ee(head, body)                     # (right, left) where the head and body cross
W1 = meet_se(Seg(T0, (37, 47)), body)[0][1]       # top wing's front edge meets the body
W2 = meet_se(Seg(B0, (37, 54)), body)[0][1]       # bottom wing's front edge meets the body
M = P(39.95, 50)                                  # middle line meets the body
# stripes: across the body
def across(y):
    dx = body.rx * math.sqrt(1 - ((y - body.cy) / body.ry) ** 2)
    return P(body.cx - dx, y), P(body.cx + dx, y)
S1L, S1R = across(46.3)
S2L, S2R = across(55)
LG1, LG2 = body.P(105), body.P(75)                # where the legs start
# the body line: from where it leaves the head on the right, down the right side, round the bottom and up the left side
bpts = [H1, W1, S1R, M, S2R, W2, LG2, LG1, S2L, S1L, H2]
body_line = []
for a, b in zip(bpts, bpts[1:]):
    body_line += body.arc_pts(a, b, cw=True)
head_ring = head.ring_at([H2, H1], cw=True)       # from the left crossing, over the top, to the right crossing, then back under
head_top = head_ring[:len(head.arc_pts(H2, H1, cw=True))]

# wings
lead1, lead2, midline = Seg(W1, T0), Seg(B0, W2), Seg(M, MID)

# feelers and eye
feel_l = [Seg(head.P(-122), (30.1, 25.8), (27.4, 22.6), (24, 21.8)), Seg((24, 21.8), (21.4, 21.3), (20.6, 23.8), (22.6, 24.8))]
feel_r = [Seg(head.P(-62), (37.3, 25.4), (38.9, 22.4), (41.6, 20.8)), Seg((41.6, 20.8), (44, 19.4), (45.4, 22), (43.2, 23.2))]

# spots
spots_top = [Ell(60, 29, 3), Ell(72, 35, 3), Ell(59, 41, 2.4)]
spots_bot = [Ell(58, 61.5, 2.4), Ell(68, 67.5, 2.4)]

# twig, legs and leaf
twig = rrect(3, 68.5, 40.5, 73, 2.25)
legs = [Seg(LG1, (31.6, 68.5)), Seg(LG2, (37.8, 68.5))]
LB_ = P(9, 68.5); LT = P(16.6, 61.6)
leaf = [Seg(LB_, (10.4, 64.6), (13, 62), LT), Seg(LT, (16.2, 64.6), (13.2, 67.6), LB_)]

steps = [
    step('Start with a 3', 'Draw a big 3: a round bump out to the right, then another round bump under it.', [line(top3, bot3)]),
    step('The head and body', 'Draw a small circle for the head, and a long oval body under it, a little way from the 3.',
         [ring(*head_ring), line(*body_line)]),
    step('The wings', 'Draw three lines from the body: one to the top of the 3, one to its middle and one to its bottom.',
         [line(lead1), line(midline), line(lead2)]),
    step('The feelers', 'Draw two curly feelers on top of the head, and a dot for the eye.', [line(*feel_l), line(*feel_r), dot(32.4, 33.6, 2.6)]),
    step('Stripes and spots', 'Draw two stripes across the body, and round spots on the wings.',
         [line(Seg(S1L, S1R)), line(Seg(S2L, S2R))] + [ring(*s.ring()) for s in spots_top + spots_bot]),
    step('The twig', 'Draw a twig under the butterfly, two little legs down onto it, and a leaf.',
         [ring(*twig), line(legs[0]), line(legs[1]), ring(*leaf)]),
]
# colour outlines
up = body.arc_pts(M, W1, cw=False)                # body edge from the middle line up to the top wing's edge
dn = body.arc_pts(W2, M, cw=False)                # body edge from the bottom wing's edge up to the middle line
holes_t = [d_fill(*s.ring()) for s in spots_top]
holes_b = [d_fill(*s.ring()) for s in spots_bot]
steps += [
    step('Colour purple', 'Colour the top wing purple. Leave the spots for later.', [fill(PU, lead1, top3, midline.rev(), *up, cut=holes_t)], use='purple'),
    step('Colour blue', 'Colour the bottom wing blue.', [fill(BL, midline, bot3, lead2, *dn, cut=holes_b)], use='blue'),
    step('Colour black', 'Colour the spots black.', [fill(BK, *s.ring()) for s in spots_top + spots_bot], use='black'),
    step('Colour brown', 'Colour the head, the body and the twig brown.', [fill(BR, *body_line, *head_top), fill(BR, *twig)], use='brown'),
    step('Colour green', 'Colour the leaf green.', [fill(GR, *leaf)], use='green'),
]
P_ = drawing('dx_butterfly_3', '3 is for Butterfly', 2, 10, 'animals', ['Numbers', 'Animals'],
             'A chubby butterfly with spotty wings and curly feelers, sitting on a twig. The 3 is hiding in it: '
             'it is the round outer edges of the top wing and the bottom wing.',
             steps, ['purple', 'blue', 'black', 'brown', 'green'])
P_ = move(P_, 10, 0)                              # centre it on the paper
save('num3butterfly', P_, {'set': 'animals-09', 'slot': '3', 'kind': 'fly', 'age_from': 5})
