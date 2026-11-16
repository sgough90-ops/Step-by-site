"""S is for Submarine (dx_submarine_s), Vehicles A to Z, slot S. Rebuilt from his ChatGPT sheet (15 Nov 2026).
The S is the propeller: its two curves are the round edges of the two blades."""
from kit15 import *

ORANGE, LBLUE, GREY = FILL['orange'], FILL['lblue'], FILL['grey']

SC, TS, BS = P(80, 50), P(87, 39), P(73, 61)
s1 = Seg(TS, (85.6, 36.4), (83, 35), (80, 35))
s2 = Seg((80, 35), (75.6, 35), (72.4, 38.6), (72.4, 42.6))
s3 = Seg((72.4, 42.6), (72.4, 45.8), (76, 47.4), SC)
s4 = Seg(SC, (84, 52.6), (87.6, 54.2), (87.6, 57.4))
s5 = Seg((87.6, 57.4), (87.6, 61.4), (84.4, 65), (80, 65))
s6 = Seg((80, 65), (77, 65), (74.4, 63.6), BS)
bl1, bl2 = Seg(TS, SC), Seg(SC, BS)

# the hull: a long capsule
R = 13
rarc1 = arc(53, 50, R, R, 0, -90, start=P(66, 50), end=P(53, 37))
htop = Seg((53, 37), (23, 37))
nosearc = arc(23, 50, R, R, -90, -270, start=P(23, 37), end=P(23, 63))
hbot = Seg((23, 63), (53, 63))
rarc2 = arc(53, 50, R, R, 90, 0, start=P(53, 63), end=P(66, 50))
hull = [*rarc1, htop, *nosearc, hbot, *rarc2]
shaft = Seg((66, 50), SC)
noseline = Seg((28, 37), (31.2, 44), (31.2, 56), (28, 63))
ports = [circle(x, 50, 3.4) for x in (39.5, 49.5, 59.5)]

tower = [Seg((36, 37), (36, 30.6)), *arc(38.6, 30.6, 2.6, 2.6, 180, 270, start=P(36, 30.6), end=P(38.6, 28)), Seg((38.6, 28), (49.4, 28)),
         *arc(49.4, 30.6, 2.6, 2.6, 270, 360, start=P(49.4, 28), end=P(52, 30.6)), Seg((52, 30.6), (52, 37))]
scope = [Seg((43.5, 28), (43.5, 18)), Seg((43.5, 18), (36.5, 18)), Seg((36.5, 18), (36.5, 15)), Seg((36.5, 15), (43.3, 15)),
         *arc(43.3, 18.2, 3.2, 3.2, 270, 360, start=P(43.3, 15), end=P(46.5, 18.2)), Seg((46.5, 18.2), (46.5, 28))]
bubbles = [circle(86.4, 30.2, 1.4), circle(90.2, 23.6, 1.8), circle(85.6, 17.6, 1.3)]

steps = [
    step('Start with an S', 'Draw a capital S on the right of your paper.', [line(s1, s2, s3, s4, s5, s6)]),
    step('The propeller', 'Draw a straight line from the top end of the S to its middle, and another from the middle to the bottom end.',
         [line(bl1), line(bl2)]),
    step('The submarine', 'Draw a long round shape on the left, like a big sausage.', [ring(hull)]),
    step('The shaft', 'Join the back of the submarine to the middle of the S with a short line.', [line(shaft)]),
    step('The front', 'Draw a curved line near the front of the submarine.', [line(noseline)]),
    step('Portholes', 'Draw three round windows in a row.', [ring(p) for p in ports]),
    step('The tower', 'Draw a box with round corners on top of the submarine.', [line(*tower)]),
    step('The periscope', 'Draw a pipe going up from the tower and bending forward, so the crew can look out.', [line(*scope)]),
    step('Bubbles', 'Draw three bubbles floating up from the propeller.', [ring(b) for b in bubbles]),
]
main = fill(ORANGE, *rarc1, Seg((53, 37), (28, 37)), noseline, Seg((28, 63), (53, 63)), *rarc2, cut=[d_fill(*p) for p in ports])
cap = fill(LBLUE, Seg((28, 37), (23, 37)), *nosearc, Seg((23, 63), (28, 63)), noseline.rev())
tow = fill(ORANGE, *tower, Seg((52, 37), (36, 37)))
sco = fill(GREY, *scope, Seg((46.5, 28), (43.5, 28)))
blade1 = fill(GREY, s1, s2, s3, bl1.rev())
blade2 = fill(GREY, s4, s5, s6, bl2.rev())
steps += [
    step('Colour orange', 'Colour the submarine and the tower orange. Leave the windows and the front for now.', [main, tow], use='orange'),
    step('Colour light blue', 'Colour the front and the round windows light blue.', [cap] + [fill(LBLUE, *p) for p in ports], use='lblue'),
    step('Colour grey', 'Colour the propeller and the periscope grey.', [blade1, blade2, sco], use='grey'),
]
P_ = drawing('dx_submarine_s', 'S is for Submarine', 3, 15, 'vehicles', ['Letters', 'Vehicles'],
             'An orange submarine with round windows, a periscope and a spinning propeller. The capital S is hiding in it: '
             'its two curves are the round edges of the two propeller blades.',
             steps, ['orange', 'lblue', 'grey'])
scale(P_, 1.12, 49, 40)
move(P_, 0, 8)
save('submarine', P_, {'set': 'vehicles-AZ', 'slot': 'S', 'kind': 'swim', 'age_from': 5})
