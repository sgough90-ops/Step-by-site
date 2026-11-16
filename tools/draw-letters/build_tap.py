"""T is for Tap (dx_tap_t), Around the house A to Z, slot T. Rebuilt from his ChatGPT sheet (15 Nov 2026).
The T is the water pipe: the top line runs along the wall and the stick comes down into the tap."""
from kit15 import *

LBROWN, GREY, LBLUE, RED = FILL['lbrown'], FILL['grey'], FILL['lblue'], FILL['red']

bar = Seg((30, 16), (70, 16))
stem = Seg((50, 16), (50, 35))

body = rrect(41, 40.5, 59, 55, 3)
nut = [Seg((46, 40.5), (46, 36.2)), *arc(47.2, 36.2, 1.2, 1.2, 180, 270, start=P(46, 36.2), end=P(47.2, 35)), Seg((47.2, 35), (52.8, 35)),
       *arc(52.8, 36.2, 1.2, 1.2, 270, 360, start=P(52.8, 35), end=P(54, 36.2)), Seg((54, 36.2), (54, 40.5))]
sp_up = [Seg((41, 44), (33, 44)), Seg((33, 44), (29.1, 44), (26, 47.1), (26, 51)), Seg((26, 51), (26, 57.5))]
sp_lo = [Seg((41, 50.5), (34.5, 50.5)), Seg((34.5, 50.5), (33.1, 50.5), (32, 51.6), (32, 53)), Seg((32, 53), (32, 57.5))]
mouth = Seg((26, 57.5), (32, 57.5))
arm_up, arm_lo = Seg((59, 45), (71, 45)), Seg((59, 50), (71, 50))
handle = rrect(71, 38, 75.6, 57, 2.2)

drop = [Seg((29, 60.6), (29.6, 62), (31.6, 63.6), (31.6, 65.4)), *arc(29, 65.4, 2.6, 2.6, 0, 180, start=P(31.6, 65.4), end=P(26.4, 65.4)),
        Seg((26.4, 65.4), (26.4, 63.6), (28.4, 62), (29, 60.6))]

TL, TR, BRt, BLt = P(16, 72), P(42, 72), P(38, 85), P(20, 85)
def on_side(a, b, y):
    t = (y - a[1]) / (b[1] - a[1]); return P(a[0] + (b[0] - a[0]) * t, y)
WY = 76
WL, WR = on_side(TL, BLt, WY), on_side(TR, BRt, WY)
bowl = poly(TL, TR, BRt, BLt, closed=True)
water = [Seg(WL, (22.4, 74.4), (25.4, 77.6), (29, 76)), Seg((29, 76), (32.6, 74.4), (35.6, 77.6), WR)]

steps = [
    step('Start with a T', 'Draw a big capital T near the top. It is the water pipe.', [line(bar), line(stem)]),
    step('The tap', 'Draw a box with round corners a little way under the T.', [ring(body)]),
    step('The nut', 'Join the bottom of the T to the box with a little cap.', [line(*nut)]),
    step('The spout', 'From the left of the box, draw a fat pipe that goes out and bends down. Close the end.', [line(*sp_up), line(*sp_lo), line(mouth)]),
    step('The handle', 'From the right of the box, draw two lines out. Finish them with a tall round handle.', [line(arm_up), line(arm_lo), ring(handle)]),
    step('A drip', 'Draw a drop of water falling from the spout.', [ring(drop)]),
    step('The bowl', 'Draw a bowl under the drip: a long line, two slanted sides and a short line across the bottom.', [ring(bowl)]),
    step('The water', 'Draw a wavy line across the bowl. The bowl is filling up!', [line(*water)]),
]
nut_fill = fill(GREY, *nut, Seg((54, 40.5), (46, 40.5)))
sp_fill = fill(LBROWN, *sp_up, mouth, rev(sp_lo), Seg((41, 50.5), (41, 44)))
arm_fill = fill(LBROWN, arm_up, Seg((71, 45), (71, 50)), arm_lo.rev(), Seg((59, 50), (59, 45)))
water_fill = fill(LBLUE, *water, Seg(WR, BRt), Seg(BRt, BLt), Seg(BLt, WL))
bowl_fill = fill(RED, Seg(TL, TR), Seg(TR, WR), rev(water), Seg(WL, TL))
steps += [
    step('Colour light brown', 'Colour the tap, the spout and the lever light brown, like shiny brass.', [fill(LBROWN, *body), sp_fill, arm_fill], use='lbrown'),
    step('Colour grey', 'Colour the nut and the handle grey.', [nut_fill, fill(GREY, *handle)], use='grey'),
    step('Colour light blue', 'Colour the drip and the water light blue.', [fill(LBLUE, *drop), water_fill], use='lblue'),
    step('Colour red', 'Colour the top of the bowl red, above the water.', [bowl_fill], use='red'),
]
P_ = drawing('dx_tap_t', 'T is for Tap', 2, 10, 'things', ['Letters', 'Around the house'],
             'A shiny tap dripping into a bowl of water. The capital T is hiding in it: it is the water pipe that comes down into the tap.',
             steps, ['lbrown', 'grey', 'lblue', 'red'])
scale(P_, 1.12, 46, 50)
move(P_, 3, 0)
save('tap', P_, {'set': 'house-AZ', 'slot': 'T', 'kind': 'key', 'age_from': 5})
