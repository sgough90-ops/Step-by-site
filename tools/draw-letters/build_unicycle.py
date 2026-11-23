"""u is for unicycle (dx_unicycle_u), Vehicles a to z, slot u (22 Nov 2026).
From his pick "u 1 Bag under the seat" (claude/step-by-draw-vehicles-small-12-ideas-4-versions.md).

The u is the little bag that hangs under the saddle and the post it hangs on: the bag's left side and round bottom
are the cup, the post is the stick. Written in the sketch's numbers.

    python3 build_unicycle.py
"""
from bcommon import *

p = Pic(s=1.0, dx=0.0, dy=1.5)
WX, WY, RO, RI, RH = 50, 70, 22, 16.7, 3.4          # the wheel: middle, tyre outside, tyre inside, hub
UX0, UX1, UT, UB, URY = 33, 50, 18, 40, 8.5         # the u


def on(r, deg):
    a = math.radians(deg)
    return (WX + r * math.cos(a), WY + r * math.sin(a))


# ---- the ground and the wheel ----
p.stroke('ground', Seg((8, 92.7), (92, 92.7)), step=6)
p.shape('tyre', circle(WX, WY, RO), step=5)
p.shape('rim', circle(WX, WY, RI), step=5)
for i, deg in enumerate((0, 90, 135, 180, 315)):
    p.stroke('spoke%d' % i, Seg((WX, WY), on(RI, deg)), step=6, w=1.3)
p.stroke('crank1', Seg((WX, WY), (59, 81)), step=4)
p.stroke('crank2', Seg((WX, WY), (41, 59)), step=4)

# ---- the fork (in front of the wheel), the hub, the pedals, the box at the top of the fork ----
p.region('forkR', box(48.2, 46, 51.8, WY))
p.stroke('fork_l', Seg((48.2, 44), (48.2, WY)), step=3)
p.stroke('fork_r', Seg((51.8, 44), (51.8, WY)), step=3)
p.shape('hub', circle(WX, WY, RH), step=3)
p.shape('pedal1', rrect(55.5, 80, 65.5, 83.6, 1.2), step=4)
p.shape('pedal2', rrect(34.5, 56.6, 44.5, 60.2, 1.2), step=4)
p.shape('crown', rrect(46.2, 40, 53.8, 47, 1.6), step=3)

# ---- the saddle (flat underneath from 33 to 62) and the buckle on the bag ----
p.shape('saddle', one("M30,14 C32,9 38,11 44,12 L58,12 C63,11 68,8 70,13 C71,17 66,18 62,18 L33,18 C30.5,18 29.4,16.5 30,14 Z"), step=2)
p.shape('buckle', rrect(38, 22, 45, 26.4, 1), step=2)

# ---- the u, in front of everything: the cup, then the stick ----
p.stroke('u_cup', Seg((UX0, UT), (UX0, UB - URY)), arc((UX0 + UX1) / 2, UB - URY, (UX1 - UX0) / 2, URY, 180, 0), step=1)
p.stroke('u_stick', Seg((UX1, UT), (UX1, UB)), step=1)
p.build()

steps = [
    step('Start with a u', 'Draw a small letter u: down, round the bottom and up to the right. Then a straight line down the right side.', p.step(1)),
    step('The saddle', 'Draw the saddle across the top of the u. It is flat underneath, with its ends curling up. Draw a little buckle on the bag.', p.step(2)),
    step('The fork', 'Under the u draw a small box with round corners. Draw two long lines down from it, ending in a small circle.', p.step(3)),
    step('Pedals', 'From the small circle draw a line down to the right and a line up to the left. Draw a little flat pedal on the end of each.', p.step(4)),
    step('The wheel', 'Draw a big circle round the small circle. Draw another circle just inside it. Stop at the fork and the pedals.', p.step(5)),
    step('Spokes', 'Draw five thin lines from the middle out to the wheel. Draw a long line under the wheel for the ground.', p.step(6)),
    step('Colour red', 'Colour the bag red, round the buckle.', [p.face('red', (41, 31), holes=('buckle',))], use='red'),
    step('Colour black', 'Colour the saddle, the tyre, the two pedals and the small box black.',
         [p.ring('black', 'saddle'), p.face('black', (69.4, 70)), p.ring('black', 'pedal1'), p.ring('black', 'pedal2'), p.ring('black', 'crown')], use='black'),
    step('Colour grey', 'Colour the fork, the small circle in the middle and the buckle grey.',
         [p.face('grey', (50, 58)), p.ring('grey', 'hub'), p.ring('grey', 'buckle')], use='grey'),
]
D = drawing('dx_unicycle_u', 'u is for unicycle', 3, 15, 'vehicles', ['Letters', 'Vehicles'],
            'A unicycle with a little red bag under the saddle. The small letter u is hiding there: the bag and the post it hangs on.',
            steps, ['red', 'black', 'grey'])
ok = finish('unicycle', D, {'set': 'vehicles-az', 'slot': 'u', 'kind': 'drive', 'age_from': 5}, p)
