"""W is for Water plane (dx_waterplane_w), Vehicles A to Z, slot W. Built from Claude's sketch "Water plane 1" (16 Nov 2026).
The W is the four thin bars that hold the float under the plane."""
from kit15 import *

YELLOW, RED, LBLUE, GREY = FILL['yellow'], FILL['red'], FILL['lblue'], FILL['grey']
TY, BY = 47, 66
wsegs = poly((35, TY), (42.5, BY), (50, TY), (57.5, BY), (65, TY))

NOSE = P(85, 36.5)
b_rb = Seg((65, TY), (75, 46.33), (81.67, 42.83), NOSE)
b_rt = Seg(NOSE, (81, 30.17), (74.67, 26.67), (66, 26))
top = Seg((66, 26), (30, 26))
b_lt = Seg((30, 26), (20.67, 26.67), (15.67, 30), (15, 36))
bl = split_many(b_lt, [0.3, 0.75])
b_lb = Seg((15, 36), (18.33, 42.67), (25, 46.33), (35, TY))
belly = [Seg((35, TY), (50, TY)), Seg((50, TY), (65, TY))]

f_mid = Seg((42.5, BY), (57.5, BY))
f_rest = [Seg((57.5, BY), (84, BY)), Seg((84, BY), (90.5, 67.6)), Seg((90.5, 67.6), (88.83, 72.2), (85.33, 74.5), (80, 74.5)),
          Seg((80, 74.5), (27, 74.5)), Seg((27, 74.5), (22.33, 73.83), (20.67, 71), (22, BY)), Seg((22, BY), (42.5, BY))]

WR_ = 2.4
wing = [Seg((33, 26), (33, 20 + WR_)), *arc(33 + WR_, 20 + WR_, WR_, WR_, 180, 270, start=P(33, 20 + WR_), end=P(33 + WR_, 20)),
        Seg((33 + WR_, 20), (64 - WR_, 20)), *arc(64 - WR_, 20 + WR_, WR_, WR_, 270, 360, start=P(64 - WR_, 20), end=P(64, 20 + WR_)),
        Seg((64, 20 + WR_), (64, 26))]
fin = poly(bl[0].b, (20.5, 21), (11.5, 18.6), bl[1].b)

win1, win2 = rrect(46, 30, 56, 37.5, 2), rrect(59, 30, 69.5, 37.5, 2)
hub = circle(87.2, 36.5, 2.2, start_deg=180)
blade_up, blade_dn = Seg((87.2, 34.3), (87.2, 24.5)), Seg((87.2, 38.7), (87.2, 48.5))

def waves(x0, x1, y, n, a):
    w = (x1 - x0) / n; out = []
    for i in range(n):
        s = -1 if i % 2 == 0 else 1; p = x0 + i * w
        out.append(Seg((p, y), (p + w / 3, y + s * a), (p + 2 * w / 3, y + s * a), (p + w, y)))
    return out
water = waves(4, 96, 80.5, 8, 2.7)

steps = [
    step('Start with a W', 'Draw a wide capital W with sharp points. Keep its three top points level.', [line(*wsegs)]),
    step('The body', 'From the right end of the W, draw a pointed nose, a long flat top and a round tail, back to the left end of the W.',
         [line(b_rb, b_rt, top, *bl, b_lb)]),
    step('The bottom', 'Join the three top points of the W with a straight line.', [line(b) for b in belly]),
    step('The float', 'Draw a long float under the W. Its top line joins the two bottom points of the W.', [line(f_mid), line(*f_rest)]),
    step('The wing', 'Draw a long wing with round ends on top of the plane.', [line(*wing)]),
    step('The tail fin', 'Draw a tall fin on the tail, leaning back.', [line(*fin)]),
    step('The windows', 'Draw two windows with round corners.', [ring(*win1), ring(*win2)]),
    step('The propeller', 'Draw a small circle on the nose, with a long thin line up and down from it.', [ring(*hub), line(blade_up), line(blade_dn)]),
    step('The water', 'Draw a wavy line under the float for the water.', [line(*water)]),
]
body_f = fill(YELLOW, b_rb, b_rt, top, *bl, b_lb, *belly, cut=[d_fill(*win1), d_fill(*win2)])
fin_f = fill(YELLOW, *fin, bl[1].rev())
steps += [
    step('Colour yellow', 'Colour the plane and its fin yellow.', [body_f, fin_f], use='yellow'),
    step('Colour red', 'Colour the wing and the float red.', [fill(RED, *wing, Seg((64, 26), (33, 26))), fill(RED, *f_rest, f_mid)], use='red'),
    step('Colour light blue', 'Colour the windows light blue.', [fill(LBLUE, *win1), fill(LBLUE, *win2)], use='lblue'),
    step('Colour grey', 'Colour the middle of the propeller grey.', [fill(GREY, *hub)], use='grey'),
]
P_ = drawing('dx_waterplane_w', 'W is for Water plane', 3, 15, 'vehicles', ['Letters', 'Vehicles'],
             'A yellow water plane on its red float, ready to land on the water. The capital W is hiding in it: '
             'it is the four thin bars that hold the float under the plane.',
             steps, ['yellow', 'red', 'lblue', 'grey'])
save('waterplane', P_, {'set': 'vehicles-AZ', 'slot': 'W', 'kind': 'fly', 'age_from': 5})
