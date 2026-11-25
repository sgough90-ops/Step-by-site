"""5 is for Plum (dx_plum_5), Food and drink 1 to 9, slot 5 (23 Nov 2026).
From his pick "5: 4 Plum" (claude/step-by-draw-food-numbers-1-to-9-36-sketches.md).

A plum with a thin stalk and a leaf. The 5: its flat top is the middle line of the leaf, its line down is the
left edge of the stalk, and its round belly is the plum.

25 Nov 2026: he sent step 1 from the live app and said "Make this 5 more natural". The 5 had a short line down (22) and
a huge belly (71 across) that came back up almost to the flat top, so it read as a circle with a flag on it. Now the
line down is 28 (38 in every 100 of the 5's height), the plum is 52 across, and the stalk meets it higher up (50
degrees round from the left, was 35), so the belly only rises 6 above the end of the line. Written in the paper's own
numbers now (the sketch's numbers and the 1.36 scale have gone).

    python3 build_num_plum.py
"""
from ncommon import *

p = Pic(s=1.0, dx=0.0, dy=0.0)
XL, Y0, STEM, BAR, R, SW = 33.5, 16.5, 28.0, 34.0, 26.0, 4.0  # the 5: its corner, its line down, its flat top, the plum, and how wide the stalk is
TH = 50                                                       # how far round from the left the stalk meets the plum
XR, YM = XL + BAR, Y0 + STEM
CX, CY = XL + math.cos(math.radians(TH)) * R, YM + math.sin(math.radians(TH)) * R     # the middle of the plum
END = (CX - 0.766 * R, CY + 0.643 * R)                        # where the belly of the 5 stops
A0 = 180 + TH                                                 # the angle where the belly starts

# ---- the stalk's other edge (it carries on into the plum, which hides the end) ----
p.stroke('stalk_r', Seg((XL + SW, Y0), (XL + SW, YM + 4)), step=3)
p.region('plumR', circle(CX, CY, R))

# ---- the rest of the round plum, its shine, the leaf ----
p.stroke('gap', arc(CX, CY, R, R, 140, A0, start=P(*END), end=P(XL, YM)), step=2)
p.stroke('shine', arc(CX, CY, R - 6.5, R - 6.5, 292, 330), step=4, deco=True)
p.shape('leaf', leaf2((XL + SW, Y0), (XR, Y0), 13), step=4)

# ---- the 5, in front of everything: flat top, short line down, round belly ----
p.stroke('five', Seg((XR, Y0), (XL, Y0)), Seg((XL, Y0), (XL, YM)), arc(CX, CY, R, R, A0, 500, start=P(XL, YM), end=P(*END)), step=1)
p.build()

steps = [
    step('Start with a 5', 'Draw a number 5: a flat line across the top, a line down, then a round belly. This 5 is hiding in the plum.', p.step(1)),
    step('Make it round', 'From the end of the 5, curve back up to the line. Now the belly is a round plum.', p.step(2)),
    step('The stalk', 'Draw another line down from the top of the 5, just beside the first one. This is the stalk.', p.step(3)),
    step('The leaf', 'Draw a pointed leaf round the top line of the 5: a curve over it and a curve under it. Draw a little curved line on the plum for the shine.', p.step(4)),
    step('Colour purple', 'Colour the round plum purple.', [p.face('purple', (CX, CY))], use='purple'),
    step('Colour green', 'Colour the leaf green.', [p.ring('green', 'leaf')], use='green'),
    step('Colour brown', 'Colour the thin stalk brown.', [p.face('brown', (XL + SW / 2, Y0 + STEM / 2))], use='brown'),
]
D = drawing('dx_plum_5', '5 is for Plum', 1, 8, 'things', TAGS,
            'A round plum with a stalk and a leaf. The number 5 is hiding in it: the leaf, the stalk and the round plum.',
            steps, ['purple', 'green', 'brown'])
ok = finish('num5plum', D, {'set': SET, 'slot': '5', 'kind': 'key', 'age_from': 4}, p)
