"""p is for police car (dx_policecar_p), Vehicles a to z, slot p (23 Nov 2026).
From his pick: round 3, number 4, "Fast car" (claude/step-by-draw-vehicles-small-seven-builds.md, "What is still open").

A low, fast police car facing left. The p is the front edge of the car (the stick) and its headlight (the bump).
The bonnet leaves the top of the stick at a slant, so it neither carries the stick on nor runs along the bump.
The blue stripe starts behind the front wheel, so no line runs into the p. Written in the sketch's numbers.

    python3 build_policecar.py
"""
from bcommon import *

p = Pic(s=1.02, dx=-2.2, dy=-3.2)
PX, PT, PM, PB, PW = 6, 54, 65.5, 77, 9.4          # the p: stick from PT down to PB, bump from PT to PM, PW wide
LX, LY = 57.6, 30.8                                # middle of the lights on the roof
OUT = "M6,54 L11.4,50.6 L34,48.4 C40,40 46,34.8 54,34.2 L63,34.2 C71,34.8 77,40 81,47.6 L90,48.8 Q95,49.6 95,54 L95,72 Q95,77 90,77 L6,77"

# ---- behind the car: the lights on the roof with their rays, the posts of the wing ----
for i, deg in enumerate((212, 248, 292, 328)):
    a = math.radians(deg)
    p.stroke('ray%d' % i, Seg((LX + 10.5 * math.cos(a), LY + 10.5 * math.sin(a)), (LX + 14.5 * math.cos(a), LY + 14.5 * math.sin(a))), step=6, deco=True)
p.stroke('lights', one("M50,38 L50,29.2 Q50,27.2 52,27.2 L63.2,27.2 Q65.2,27.2 65.2,29.2 L65.2,38"), step=6)
p.stroke('lightmid', Seg((LX, 27.2), (LX, 38)), step=6)
p.stroke('post0', Seg((86, 52), (86, 41.6)), step=6)
p.stroke('post1', Seg((92, 52), (92, 41.6)), step=6)

# ---- the car: everything but its front edge, which is the p ----
p.region('bodyR', one(OUT + " Z"))
p.stroke('body', one(OUT), step=3)
p.stroke('stripe', one("M26,66 L36,66 L42,58.6 L64,58.6 L70,66 L95,66"), step=4)
p.stroke('pillar', Seg((55.3, 34.2), (55.3, 58.6)), step=5)
p.shape('win0', one("M39,47.2 C43,41.6 47.4,38.2 53.6,37.6 L53.6,47.2 Z"), step=5)
p.shape('win1', one("M57,37.6 L62.6,37.6 C68.6,38.2 73,41.6 76.2,47.2 L57,47.2 Z"), step=5)
p.shape('star', star5(48.2, 53.2, 4.4, k=0.43), step=5)
p.shape('tail', rrect(92.2, 55, 95.8, 60.6, 1), step=3)
p.shape('wing', rrect(82, 39.6, 96.4, 43.8, 1.6), step=6)
for i, x in enumerate((26, 76)):
    p.shape('tyre%d' % i, circle(x, 76, 10.4), step=2)
    p.shape('hub%d' % i, circle(x, 76, 4.7), step=2)

# ---- the p, in front of everything: the stick, then the bump ----
p.stroke('p_stick', Seg((PX, PT), (PX, PB)), step=1)
p.stroke('p_bump', arc(PX, (PT + PM) / 2, PW, (PM - PT) / 2, -90, 90), step=1)
p.build()

steps = [
    step('Start with a p', 'Draw a small letter p: a straight line down, then a round bump on its right side, from the top to half-way down.', p.step(1)),
    step('Two wheels', 'Draw a big circle beside the bottom of the p, and another one further along. Draw a small circle inside each one.', p.step(2)),
    step('The car', 'From the top of the p go up a little and along. Curve up over the roof and down to the back. Go down, then along the bottom to the p. Add a back light.', p.step(3)),
    step('The stripe', 'From the front wheel draw a line along the side to the back of the car. In the middle it steps up and comes back down.', p.step(4)),
    step('Windows and a star', 'Draw two windows under the roof, with a straight line down between them to the stripe. Draw a star on the front door.', p.step(5)),
    step('Lights and wing', 'On the roof draw two little boxes for the lights, with four short lines shining out. At the back draw a flat wing on two short posts.', p.step(6)),
    step('Colour yellow', 'Colour the headlight in the p yellow. Colour the star yellow too.', [p.face('yellow', (10, 59.6)), p.ring('yellow', 'star')], use='yellow'),
    step('Colour blue', 'Colour the stripe blue, down to the bottom of the car. Colour the left light on the roof blue.',
         [p.face('blue', (51, 70)), p.face('blue', (90.6, 71)), p.face('blue', (53.8, 31))], use='blue'),
    step('Colour red', 'Colour the right light on the roof red. Colour the back light red.', [p.face('red', (61.4, 31)), p.ring('red', 'tail')], use='red'),
    step('Colour light blue', 'Colour the two windows light blue.', [p.ring('lblue', 'win0'), p.ring('lblue', 'win1')], use='lblue'),
    step('Colour black', 'Colour the two tyres black, round the small circles. Colour the wing black.',
         [p.ring('black', 'tyre0', holes=('hub0',)), p.ring('black', 'tyre1', holes=('hub1',)), p.ring('black', 'wing')], use='black'),
    step('Colour grey', 'Colour the middle of each wheel grey.', [p.ring('grey', 'hub0'), p.ring('grey', 'hub1')], use='grey'),
]
D = drawing('dx_policecar_p', 'p is for police car', 3, 18, 'vehicles', ['Letters', 'Vehicles'],
            'A fast police car with its lights flashing. The small letter p is hiding at the front: the front edge of the car and its headlight.',
            steps, ['yellow', 'blue', 'red', 'lblue', 'black', 'grey'])
ok = finish('policecar', D, {'set': 'vehicles-az', 'slot': 'p', 'kind': 'drive', 'age_from': 5}, p)
