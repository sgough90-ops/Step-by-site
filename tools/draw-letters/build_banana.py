"""Y is for Yellow banana (dx_banana_y), Food and drink A to Z, slot Y (21 Nov 2026).
From his screenshot of MK Fine art's banana drawn from a Y (OmRNTcL9VsQ), drawn fresh in our style.

A banana with its top peeled. The two arms of the capital Y are the top edges of the two floppy pieces of peel,
where they fold away from the soft banana inside, and the line down the Y is the seam down the peel underneath.
Step 1 is a normal Y (the arms meet half-way down); step 6 carries the line on down to the bottom of the banana.
The banana inside stays white (the paper), the peel is yellow and the little stalk brown.
"""
from kit15 import *

YELLOW, BROWN = FILL['yellow'], FILL['brown']

# ---- 1: the Y (a normal capital Y: 24 wide, 30 tall, arms meeting half-way down) ----
AL, AR, J, S1 = P(38, 33.5), P(62, 33.5), P(50, 48.5), P(50, 63.5)
arm_l, arm_r, stem = Seg(AL, J), Seg(AR, J), Seg(J, S1)

# ---- 2: the soft banana inside, from the top of one arm, round the top, to the top of the other ----
inside = [Seg(AL, (37.6, 26), (37.9, 18), (39.6, 12)),
          Seg((39.6, 12), (41.6, 5.6), (46, 3.5), (50, 3.5)),
          Seg((50, 3.5), (54, 3.5), (58.4, 5.6), (60.4, 12)),
          Seg((60.4, 12), (62.1, 18), (62.4, 26), AR)]

# ---- 3: the left piece of peel: out from the top of the arm, down to its tip, back in to the middle of the Y ----
TIP = P(24, 70.4)
flap_top = [Seg(AL, (33.4, 31), (25.4, 31.4), (21, 36.4)),
            Seg((21, 36.4), (16.6, 41.4), (15.8, 52), (17, 61)),
            Seg((17, 61), (17.9, 67), (20.6, 70.6), TIP)]
d = (-math.cos(math.radians(24)), math.sin(math.radians(24)))          # how the lower edge leaves the middle of the Y
under = Seg(TIP, (29, 65), (J[0] + 11 * d[0], J[1] + 11 * d[1]), J)  # lower edge, from the tip back to the middle
BX = 38.6                                                              # the bottom of the banana starts under the peel here
t_b = seg_x(under, BX)
under_out, under_in = under.split(t_b)                                 # tip -> BL0, BL0 -> middle of the Y
BL0 = under_out.b
flap_l = flap_top + [under_out, under_in]
flap_r = mirror(flap_l)                                                # the right piece: AR ... -> J
BR0 = flap_r[-1].a

# ---- 5: the bottom of the banana, still in its peel ----
SL, SR = P(47.2, 92), P(52.8, 92)
side_l = [Seg(BL0, (38.3, 66), (38.8, 79.5), (41.4, 86.4)),
          Seg((41.4, 86.4), (43, 90.2), (45, 91.7), SL)]
base = Seg(SL, SR)
side_r = rev(mirror(side_l))                                           # SR -> BR0
bottom = side_l + [base] + side_r
assert bottom[-1].b == BR0

# ---- 6: the line down the Y carries on to the bottom ----
SB = P(50, 92)
seam = Seg(S1, SB)

# ---- 7: the little stalk under the bottom ----
stalk = [Seg(SL, (47.4, 93.6), (47.5, 95.2), (47.7, 96)),
         Seg((47.7, 96), (49.2, 96.6), (50.8, 96.6), (52.3, 96)),
         Seg((52.3, 96), (52.5, 95.2), (52.6, 93.6), SR)]

# ---- 8: a curved line on each piece of peel, from the arm of the Y out towards the tip ----
RIB0 = point_on_line(AL, J, 0.36)
rib_l = Seg(RIB0, (35.4, 40), (27, 46), (23.2, 60.5))
rib_r = mirror([rib_l])[0]

# ---- the colours ----
peel_l = fill(YELLOW, *(flap_l + [Seg(J, AL)]))
peel_r = fill(YELLOW, *(flap_r + [Seg(J, AR)]))
lower = fill(YELLOW, *([under_in.rev()] + bottom + [flap_r[-1]]))
stalk_fill = fill(BROWN, *(stalk + [base.rev()]))

steps = [
    step('Start with a Y', 'Draw a capital Y: two short slanting lines that meet in the middle, then a straight line down. This Y is hiding in the banana.',
         [line(arm_l), line(arm_r), line(stem)]),
    step('The banana', 'From the top of the left arm, draw up, round the top and down to the top of the right arm. This is the soft banana inside.',
         [line(*inside)]),
    step('Left peel', 'From the top of the left arm, draw a big floppy piece of peel out and down to a tip, then back in to the middle of the Y.',
         [line(*flap_l)]),
    step('Right peel', 'Do the same on the right: a floppy piece of peel out and down to a tip, then back in to the middle of the Y.',
         [line(*flap_r)]),
    step('The bottom', 'From under the left peel, draw down the side, across the bottom and back up to under the right peel.',
         [line(*bottom)]),
    step('A longer line', 'Make the straight line of the Y longer, all the way down to the bottom of the banana.',
         [line(seam)]),
    step('The stalk', 'Draw a little stalk at the very bottom.',
         [line(*stalk)]),
    step('Peel lines', 'Draw a curved line on each piece of peel, from the arm of the Y out towards its tip.',
         [line(rib_l), line(rib_r)]),
    step('Colour yellow', 'Colour all the peel yellow. Leave the soft banana at the top white.',
         [peel_l, peel_r, lower], use='yellow'),
    step('Colour brown', 'Colour the stalk brown.',
         [stalk_fill], use='brown'),
]

D = drawing('dx_banana_y', 'Y is for Yellow banana', 2, 10, 'things', ['Letters', 'Around the house'],
            'A yellow banana with its top peeled. The capital Y is hiding in it: the tops of the two pieces of peel are its arms, and the line down the peel is its tail.',
            steps, ['yellow', 'brown'])
save('banana', D, {'set': 'house-AZ', 'slot': 'Y', 'kind': 'key', 'age_from': 4})
