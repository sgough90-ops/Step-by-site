"""j is for jaguar (dx_jaguar_j), Animals a to z, slot j. Takes the Jack Russell's place, 25 Nov 2026.

He sent step 1 of "j is for Jack Russell" from the live app: "Give me four other variations instead of Jack Russell dog".
Of Claude's four he said "do it like you did for the Jaguar cub for the first one but do as a fully grown jaguar", and
then "yes, you can make live the ... Jaguar". Sketch: /home/claude/fix/r2.py jaguar().

A grown jaguar sitting up, side on, facing right. The j: its stick is the front of the chest, its curl is the front paw
on the ground, and its dot is the eye. Its spots are big and small round spots, coloured brown.
The Jack Russell (dx_jackrussell_j) stays in the page, out of the set, like other drawings that left a set.

    python3 build_jaguar.py
"""
from bcommon import *
import ncommon

p = Pic(s=1.0, dx=6.7, dy=3.1)
SX, TOPY, BOTY, HR = 66.0, 34.0, 82.0, 6.0
EYE = (66.0, 22.6)


def cr(pts, closed=False):
    """a smooth line through the points (Catmull-Rom as curves), as in the sketch"""
    q = list(pts); n = len(q)
    get = (lambda i: q[i % n]) if closed else (lambda i: q[max(0, min(n - 1, i))])
    out = []
    for i in range(n if closed else n - 1):
        a, b, c, d = get(i - 1), get(i), get(i + 1), get(i + 2)
        out.append(Seg(b, (b[0] + (c[0] - a[0]) / 6, b[1] + (c[1] - a[1]) / 6), (c[0] - (d[0] - b[0]) / 6, c[1] - (d[1] - b[1]) / 6), c))
    return out


# ---- the tail, behind everything: lying on the ground behind it and curling up at the end ----
p.shape('tail', cr([(31.5, 85.0), (20.0, 87.6), (9.6, 85.0), (5.0, 76.6), (6.0, 66.6), (10.6, 61.4), (15.0, 63.6), (14.4, 69.0),
                    (12.6, 75.0), (15.4, 80.6), (23.0, 82.6), (30.0, 81.0)], closed=True), step=6)

# ---- the body: its front edge is the j, so it hides what is behind it but draws only its other edges ----
jline = [Seg((SX, TOPY), (SX, BOTY))] + arc(SX - HR, BOTY, HR, HR, 0, 90, start=P(SX, BOTY), end=P(SX - HR, BOTY + HR)) + [Seg((SX - HR, BOTY + HR), (55.6, BOTY + HR))]
backline = [Seg((55.6, BOTY + HR), (33.0, BOTY + HR)), Seg((33.0, BOTY + HR), (23.0, BOTY + HR), (18.6, 80.0), (19.6, 70.0)),
            Seg((19.6, 70.0), (21.0, 58.0), (31.0, 47.0), (43.6, 38.0)), Seg((43.6, 38.0), (48.6, 34.4), (52.0, 30.0), (54.0, 24.0))]
p.region('body', jline + backline + [Seg((54.0, 24.0), (SX, TOPY))])
p.stroke('back', backline, step=4)
p.stroke('leg', Seg((57.4, 60.0), (57.4, BOTY + HR)), step=5, deco=True)                               # the back of its front leg
p.stroke('thigh', one("M45,88 C36,86 31.4,77.6 35,70 C38.6,63 49,61.6 57.4,66.6"), step=5, deco=True)   # its back leg
p.stroke('paw', one("M57.4,81.6 C52.6,80.2 47.6,82.4 46,88"), step=5, deco=True)                        # its back paw

# ---- ears behind the head, then the head (broad, with a strong muzzle) ----
def ear(pts):
    c = cr(pts)
    return c + [Seg(pts[-1], pts[0])]
p.shape('ear1', ear([(56.4, 13.6), (55.0, 8.0), (59.0, 5.4), (62.6, 9.6)]), step=2)
p.shape('ear2', ear([(66.0, 11.6), (67.0, 6.0), (71.6, 5.6), (73.0, 12.0)]), step=2)
p.shape('head', cr([(SX, TOPY), (72.6, 34.0), (78.6, 32.4), (81.6, 28.6), (81.6, 24.0), (78.6, 20.0), (74.6, 14.6), (68.0, 10.4), (60.0, 10.2),
                    (54.0, 14.4), (51.6, 21.6), (53.6, 29.0), (59.6, 33.4)], closed=True), step=2)
p.shape('nose', circle(80.8, 23.4, 2.0, ry=1.7), step=3)
p.stroke('mouth', one("M81,26.2 C79.6,29.4 76,30 73.4,28.4"), step=3, deco=True)

# ---- spots: big and small round spots (rings with a dot in looked like buttons in the app's thick pencil line) ----
ROS = [(40.0, 44.0), (48.0, 38.6), (30.6, 56.0), (39.6, 54.6), (49.0, 49.0), (26.0, 68.0), (58.0, 44.0), (58.6, 54.0), (26.6, 80.0), (48.0, 59.0)]
BODY_DOTS = [(61.6, 66.0), (61.6, 76.0), (41.0, 73.0), (45.0, 80.4)]
TAIL_DOTS = [(9.6, 78.0), (9.6, 67.6), (16.4, 84.6)]
FACE_DOTS = [(56.6, 18.4), (60.6, 14.6), (56.0, 25.6), (61.6, 27.0)]
for k, (x, y) in enumerate(ROS): p.shape('ros%d' % k, circle(x, y, 1.7), step=7)
for nm, pts, r in (('bd', BODY_DOTS, 1.2), ('td', TAIL_DOTS, 1.2), ('fd', FACE_DOTS, 1.0)):
    for k, (x, y) in enumerate(pts): p.shape('%s%d' % (nm, k), circle(x, y, r), step=8)     # the app allows 14 new lines a step

# ---- the j, in front of everything ----
p.shape('jdot', circle(EYE[0], EYE[1], 1.5), step=1)
p.stroke('j', jline, step=1)
p.build()

N = lambda nm, pts: ['%s%d' % (nm, k) for k in range(len(pts))]
yellow = [p.face('yellow', (52.0, 72.0), holes=N('ros', ROS) + N('bd', BODY_DOTS)),
          p.face('yellow', (7.6, 75.0), holes=N('td', TAIL_DOTS)),
          p.face('yellow', (72.0, 20.0), holes=['jdot'] + N('fd', FACE_DOTS)),
          p.face('yellow', (58.8, 8.2)), p.face('yellow', (69.6, 8.6))]
brown = [p.ring('brown', n) for n in N('ros', ROS) + N('bd', BODY_DOTS) + N('td', TAIL_DOTS) + N('fd', FACE_DOTS)]

steps = [
    step('Start with a j', 'Draw a small letter j: a long stick that curls round to the left at the bottom, with a dot above it. This j is hiding in the jaguar.', p.step(1)),
    step('Head and ears', 'Draw a big head on top of the stick, round the dot. The dot is its eye. Draw two small round ears on top.', p.step(2)),
    step('Nose and mouth', 'Draw a nose at the front of its face, and a mouth under it.', p.step(3)),
    step('Its body', 'From the curl of the j, draw a line along the ground, round its bottom and up its back to its head.', p.step(4)),
    step('Its legs', 'Draw a line up from the ground for the back of its front leg. Draw a big curve for its back leg, and a line for its back paw.', p.step(5)),
    step('Its tail', 'Draw a long tail lying on the ground behind it, curling up at the end.', p.step(6)),
    step('Big spots', 'Draw ten round spots on its back, its side and its back leg.', p.step(7)),
    step('Small spots', 'Draw smaller spots on its front leg, its back leg and its tail. Draw four on its head too.', p.step(8)),
    step('Colour yellow', 'Colour the jaguar yellow all over. Go round the spots.', yellow, use='yellow'),
    step('Colour the spots', 'Colour all the spots brown.', brown, use='brown'),
    step('Colour black', 'Colour its nose and its eye black.', [p.ring('black', 'nose'), p.ring('black', 'jdot')], use='black'),
]
D = drawing('dx_jaguar_j', 'j is for jaguar', 3, 15, 'animals', ['Letters', 'Animals'],
            'A big spotty jaguar sitting up. The small letter j is hiding in it: its stick is the front of its chest, its curl is its '
            'front paw and its dot is its eye.',
            steps, ['yellow', 'brown', 'black'])
ok = finish('jaguar', D, {'set': 'animals-az', 'slot': 'j', 'kind': 'hop', 'age_from': 5}, p)
