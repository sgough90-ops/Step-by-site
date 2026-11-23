"""e is for excavator (dx_excavator_e), Vehicles a to z, slot e (22 Nov 2026).
From his pick "e 3 Round engine at the back" (claude/step-by-draw-vehicles-small-12-ideas-4-versions.md).

An excavator facing right. The e is the round engine cover at the back: its line across is where the yellow cover
meets the grey weight below, and its curve is the round edge of the cover. The grey body starts at the right end of
the line across and comes back to the tail of the e, so the gap of the e stays open (the round weight and the body
are one grey shape). Written in the sketch's numbers.

    python3 build_excavator.py
"""
from bcommon import *

p = Pic(s=1.0, dx=-5.2, dy=-4.3)
CX, CY, R, GAP = 30, 52, 15, 42
E_END = (CX + R * math.cos(math.radians(GAP)), CY + R * math.sin(math.radians(GAP)))     # the tail of the e


def band(a, b, w):
    """the two long edges of a straight arm from a to b, w wide"""
    (x1, y1), (x2, y2) = a, b
    L = math.hypot(x2 - x1, y2 - y1); nx, ny = -(y2 - y1) / L * w / 2, (x2 - x1) / L * w / 2
    return Seg((x1 + nx, y1 + ny), (x2 + nx, y2 + ny)), Seg((x1 - nx, y1 - ny), (x2 - nx, y2 - ny))


# ---- the tracks and the block the body sits on ----
p.shape('tracks', rrect(12, 78, 72, 94, 8), step=4)
for i in range(4):
    p.shape('wheel%d' % i, circle(20 + 44 * i / 3, 86, 4.3), step=4)
p.stroke('ped_l', Seg((46, 71), (46, 78)), step=4)
p.stroke('ped_r', Seg((60, 71), (60, 78)), step=4)

# ---- the arm: first part (behind), second part (in front), the round joint, the bucket ----
ELBOW, BASE, TIP = (85, 19), (62, 54), (91, 46.5)
a1, a2 = band(BASE, ELBOW, 7.5)
p.stroke('arm1_a', a1, step=5); p.stroke('arm1_b', a2, step=5)
b1, b2 = band(ELBOW, TIP, 6)
p.region('arm2R', b1, Seg(b1.b, b2.b), b2.rev(), Seg(b2.a, b1.a))
p.stroke('arm2_a', b1, step=5); p.stroke('arm2_b', b2, step=5)
p.shape('joint', circle(ELBOW[0], ELBOW[1], 4.4), step=5)
p.shape('bucket', one("M85,45 L97,45 C99,51 98,58 92,61 L84,57 L88,52 Z"), step=6)

# ---- the cab (hides the bottom of the arm) and its window ----
p.region('cabR', rrect(49.5, 29, 68.5, 57.2, 4))
p.stroke('cab', one("M49.5,57 L49.5,33 Q49.5,29 53.5,29 L64.5,29 Q68.5,29 68.5,33 L68.5,57"), step=3)
p.shape('window', rrect(53, 33, 64.5, 45, 2), step=3)

# ---- the grey body: from the right end of the e's middle line round to the tail of the e ----
p.stroke('body', one("M45,52 L48,57 L69,57 Q72,57 72,60 L72,68 Q72,71 69,71 L42,71 L%s,%s" % E_END), step=2)

# ---- three little slots on the engine cover (decoration only) ----
for i, x in enumerate((24, 30, 36)):
    p.stroke('slot%d' % i, Seg((x, 42.5), (x, 47.5)), step=3, deco=True)

# ---- the e, in front of everything: the line across, then the curve up and all the way round ----
p.stroke('e', Seg((CX - R, CY), (CX + R, CY)),
         arc(CX, CY, R, R, 360, 180, end=P(CX - R, CY)), arc(CX, CY, R, R, 180, GAP, start=P(CX - R, CY), end=P(*E_END)), step=1)
p.build()

steps = [
    step('Start with an e', 'Draw a big letter e: a line across, then from its right end curve up and all the way round. Stop before you get back.', p.step(1)),
    step('The body', 'From the right end of the line across, slant down a little. Then draw a long box: along, down, back along the bottom and up to the tail of the e.', p.step(2)),
    step('The cab', 'On top of the box draw the cab with round corners and a window. Draw three little lines in the top of the e.', p.step(3)),
    step('The tracks', 'Draw two short lines down from the box. Under them draw a long shape with round ends, with four little wheels inside.', p.step(4)),
    step('The arm', 'Draw a long arm from the cab up to the right, with a round joint at the top. From the joint draw a second arm coming down.', p.step(5)),
    step('The bucket', 'On the end of the arm draw the bucket: flat on top, a round back and a pointed scoop.', p.step(6)),
    step('Colour yellow', 'Colour the top of the e, the cab and the two parts of the arm yellow.',
         [p.face('yellow', (30, 45)), p.face('yellow', (59, 51), holes=('window',)), p.face('yellow', (76.5, 32.5)), p.face('yellow', (88, 32))], use='yellow'),
    step('Colour grey', 'Colour the bottom of the e and the long box grey. Colour the four wheels and the round joint grey too.',
         [p.face('grey', (30, 58))] + [p.ring('grey', 'wheel%d' % i) for i in range(4)] + [p.ring('grey', 'joint')], use='grey'),
    step('Colour black', 'Colour the tracks black, round the wheels. Colour the block above them and the bucket black.',
         [p.ring('black', 'tracks', holes=tuple('wheel%d' % i for i in range(4))), p.face('black', (53, 74.5)), p.ring('black', 'bucket')], use='black'),
    step('Colour light blue', 'Colour the cab window light blue.', [p.ring('lblue', 'window')], use='lblue'),
]
D = drawing('dx_excavator_e', 'e is for excavator', 3, 18, 'vehicles', ['Letters', 'Vehicles'],
            'An excavator with a round engine cover at the back. The small letter e is hiding there: the round cover and the line across it.',
            steps, ['yellow', 'grey', 'black', 'lblue'])
ok = finish('excavator', D, {'set': 'vehicles-az', 'slot': 'e', 'kind': 'drive', 'age_from': 5}, p)
