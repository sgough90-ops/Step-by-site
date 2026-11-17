"""U is for Unicorn (dx_unicorn_u), Animals A to Z, slot U. Built from Claude's sketch "Unicorn 1" (16 Nov 2026).
The U is the two sides of the unicorn's long face and its round nose."""
from kit15 import *

PURPLE, PINK, YELLOW = FILL['purple'], FILL['pink'], FILL['yellow']
XL, XR, YT, YB, CX, R = 33, 67, 31, 72, 50, 17
u_l = Seg((XL, YT), (XL, YB))
u_arc = arc(CX, YB, R, R, 180, 0, start=P(XL, YB), end=P(XR, YB))
u_r = Seg((XR, YB), (XR, YT))

c1, c2 = P(44.3, 32.6), P(55.7, 32.6)
fringe = [bump(P(XL, YT), c1, 0.36), bump(c1, c2, 0.36), bump(c2, P(XR, YT), 0.36)]

m_left = Seg((XL, YT), (26.5, 29.5), (29, 14.4), (50, 14.4))
m_right = Seg((50, 14.4), (69, 14.4), (72.5, 24), (72.6, 31))
mL = split_many(m_left, [0.3, 0.6, 0.95])
mR = split_many(m_right, [0.05, 0.4, 0.7])
LOCK_Y = 44.5
lock_out = Seg((72.6, 31), (72.8, 42), (77.6, 54), (74.6, 67))
lock_in = Seg((74.6, 67), (73.2, 57), (71.6, 48.4), (XR, LOCK_Y))

ear_l = [Seg(mL[0].b, (24.5, 12.5)), Seg((24.5, 12.5), mL[1].b)]
ear_r = [Seg(mR[1].b, (75.5, 12.5)), Seg((75.5, 12.5), mR[2].b)]

TIP = P(50, 3.5)
hb1, hb2 = mL[2].b, mR[0].b
horn = [Seg(hb1, TIP), Seg(TIP, hb2)]
st1 = Seg(point_on_line(hb1, TIP, 0.22), point_on_line(TIP, hb2, 0.62))
st2 = Seg(point_on_line(hb1, TIP, 0.55), point_on_line(TIP, hb2, 0.30))

eye_l, eye_r = circle(42, 51, 2.6), circle(58, 51, 2.6)
NY = 68
nose = Seg((XL, NY), (44.33, 64.67), (55.67, 64.67), (XR, NY))

steps = [
    step('Start with a U', 'Draw a big capital U: straight down, round the bottom and straight back up. Make it tall.', [line(u_l, *u_arc, u_r)]),
    step('The fringe', 'Join the two tops of the U with a wavy line of three bumps.', [line(*fringe)]),
    step('The mane', 'From the top left of the U, draw the hair up over the head and down the right side into a long lock that ends on the U.',
         [line(*mL, *mR, lock_out, lock_in)]),
    step('The ears', 'Draw a pointy ear on each side of the mane.', [line(*ear_l), line(*ear_r)]),
    step('The horn', 'Draw a tall pointy horn on top of the head, with two stripes across it.', [line(*horn), line(st1), line(st2)]),
    step('The eyes', 'Draw two circles for the eyes, with a dot in each one.', [ring(*eye_l), ring(*eye_r), dot(42, 51, 2.4), dot(58, 51, 2.4)]),
    step('The nose', 'Draw a curved line across the bottom of the U, and two dots for the nostrils.', [line(nose), dot(44, 79, 2.4), dot(56, 79, 2.4)]),
]
mane = fill(PURPLE, *mL, *mR, lock_out, lock_in, Seg((XR, LOCK_Y), (XR, YT)), *rev(fringe))
nose_f = fill(PINK, nose, Seg((XR, NY), (XR, YB)), *rev(u_arc), Seg((XL, YB), (XL, NY)))
horn_f = fill(YELLOW, *horn, mR[0].rev(), mL[3].rev())
steps += [
    step('Colour purple', 'Colour the mane and the eyes purple. Leave the face and the ears white.', [mane, fill(PURPLE, *eye_l), fill(PURPLE, *eye_r)], use='purple'),
    step('Colour pink', 'Colour the nose pink.', [nose_f], use='pink'),
    step('Colour yellow', 'Colour the horn yellow.', [horn_f], use='yellow'),
]
P_ = drawing('dx_unicorn_u', 'U is for Unicorn', 2, 10, 'animals', ['Letters', 'Animals'],
             "A unicorn's face with a purple mane and a golden horn. The capital U is hiding in it: "
             'it is the two sides of the long face and the round nose.',
             steps, ['purple', 'pink', 'yellow'])
save('unicorn', P_, {'set': 'animals-AZ', 'slot': 'U', 'kind': 'hop', 'age_from': 5})
