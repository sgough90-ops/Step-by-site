"""E is for Electric train (dx_electrictrain_e), Vehicles A to Z, slot E. Built from Claude's sketch "Electric train 4" (16 Nov 2026).
The E is the flat back end of the train (the line down), with the roof, the stripe and the floor as its three arms."""
from kit15 import *
import math

RED, LBLUE, BLACK, GREY, YELLOW = FILL['red'], FILL['lblue'], FILL['black'], FILL['grey'], FILL['yellow']

X0, TY, MY, BY = 14, 31, 51, 71
TOPX, MIDX, BOTX = 62, 59, 62
e_top = Seg((TOPX, TY), (X0, TY)); e_down = Seg((X0, TY), (X0, BY)); e_bot = Seg((X0, BY), (BOTX, BY))
e_mid = Seg((X0, MY), (MIDX, MY))

FX, FS = 90, 63          # the front of the train, and where the stripe meets it
nose = Seg((TOPX, TY), (76.67, 31.67), (86, 41), (FX, 59))
front_a, front_b = Seg((FX, 59), (FX, FS)), Seg((FX, FS), (FX, BY))
floor_x = Seg((FX, BY), (BOTX, BY))
stripe = Seg((MIDX, MY), (70.33, 51.67), (80.67, 55.67), (FX, FS))

wins = [rrect(19, 35, 30, 46, 2.2), rrect(33, 35, 44, 46, 2.2), rrect(47, 35, 58, 46, 2.2)]
ws = [Seg((63, 35), (72.33, 36.33), (79, 41), (83, 49)), Seg((83, 49), (63, 49)), Seg((63, 49), (63, 35))]
light = circle(85, 66, 1.8)

WCY, WR = 75.8, 5.2
def wheel(cx):
    dx = math.sqrt(WR * WR - (WCY - BY) ** 2)
    a0 = math.degrees(math.atan2(BY - WCY, -dx)); a1 = math.degrees(math.atan2(BY - WCY, dx))
    return arc(cx, WCY, WR, WR, a0 % 360, a1, start=P(cx - dx, BY), end=P(cx + dx, BY)), circle(cx, WCY, 1.7)
wheels = [wheel(x) for x in (25, 38, 67, 80)]

wire = Seg((4, 18), (96, 18))
panto = poly((36, TY), (43, 25), (37, 18))
track = Seg((4, 81.4), (96, 81.4))

steps = [
    step('Start with an E', 'Draw a big capital E, long and low. Make the top and bottom arms long, and the middle arm a little shorter.',
         [line(e_top, e_down, e_bot), line(e_mid)]),
    step('The front', 'From the end of the top arm, curve down for the nose, then go straight down and back along to the bottom arm.',
         [line(nose, front_a, front_b, floor_x)]),
    step('The stripe', 'Draw a curved line from the end of the middle arm to the front.', [line(stripe)]),
    step('The windows', 'Draw three square windows and a curved window at the front.', [ring(*w) for w in wins] + [ring(*ws)]),
    step('The light', 'Draw a small circle at the front for the light.', [ring(*light)]),
    step('The wheels', 'Draw four wheels under the train, two at each end, with a small circle in each one.',
         [line(*a) for a, _ in wheels] + [ring(*h) for _, h in wheels]),
    step('The wire', 'Draw a long line across the top for the electric wire.', [line(wire)]),
    step('The arm', 'Draw a zigzag arm from the roof up to the wire.', [line(*panto)]),
    step('The track', 'Draw a long line under the wheels for the track.', [line(track)]),
]
red_body = fill(RED, e_mid, stripe, front_b, floor_x, e_bot.rev(), Seg((X0, BY), (X0, MY)), cut=[d_fill(*light)])
wheel_fills = [fill(BLACK, *a, Seg(a[-1].b, a[0].a), cut=[d_fill(*h)]) for a, h in wheels]
steps += [
    step('Colour red', 'Colour the bottom half of the train red. Leave the top white.', [red_body], use='red'),
    step('Colour light blue', 'Colour all the windows light blue.', [fill(LBLUE, *w) for w in wins] + [fill(LBLUE, *ws)], use='lblue'),
    step('Colour black', 'Colour the wheels black.', wheel_fills, use='black'),
    step('Colour grey', 'Colour the middles of the wheels grey.', [fill(GREY, *h) for _, h in wheels], use='grey'),
    step('Colour yellow', 'Colour the light yellow.', [fill(YELLOW, *light)], use='yellow'),
]
P_ = drawing('dx_electrictrain_e', 'E is for Electric train', 3, 15, 'vehicles', ['Letters', 'Vehicles'],
             'A red and white electric train on its track, with an arm up to the wire. The capital E is hiding in it: '
             'the flat back end is the line down, and the roof, the stripe and the floor are the three arms.',
             steps, ['red', 'lblue', 'black', 'grey', 'yellow'])
save('electrictrain', P_, {'set': 'vehicles-AZ', 'slot': 'E', 'kind': 'drive', 'age_from': 5})
