"""s is for snowmobile (dx_snowmobile_s), Vehicles a to z, slot s (23 Nov 2026).
From his pick, fourth go number 2 "On a silver arm" (Claude's sketches,
claude/step-by-draw-snowmobile-round4-dimsum-nuts-waffle-sketches.py). His own plan for the s (16:08, with a red s drawn
on a screenshot): it sits at the front of the track.

A red snowmobile with a white nose, facing right, held up above its track on two silver arms.
The s, from its start:
  the top line      the bottom edge of the body, just above the front of the track
  the top curve     the inside edge of the front arm, down from the body to the track
  the middle line   the top of the track, at its front
  the bottom curve  the round front end of the track
  the bottom line   the bottom of the track
It is 16 wide and 24 tall, made of level lines and two half circles, like his red one.
The seat sits on the body's top line (one shared line), so the body is whole when it is drawn in step 3.
Written in the sketch's numbers.

    python3 build_snowmobile.py
"""
from bcommon import *

p = Pic(s=1.0, dx=-2.0, dy=-2.5)
XA, XB, R1, R2, BOT = 46, 50, 5, 7, 91                         # the s: where its two curves start, how big they are, the snow
YT = BOT - 2 * R2                                              # the top of the track (the middle line of the s)
YTOP = YT - 2 * R1                                             # the bottom of the body (the top line of the s)
S0, S1 = XA + 8, XB - 7                                        # where the s starts (top right) and ends (bottom left)
DECK, REAR, XR = 35, 6, 18                                     # the top of the body, its back, the middle of the track's back end
RO = R1 + 2.6                                                  # the outside of the front arm
WH = [XR + (XB - XR) * i / 3 for i in range(4)]                # the four wheels in the track


def stick(a, b, w):
    dx, dy = b[0] - a[0], b[1] - a[1]; L = math.hypot(dx, dy); r = w / 2; th = math.degrees(math.atan2(dy, dx))
    nx, ny = -dy / L * r, dx / L * r
    p1, p2, p3, p4 = P(a[0] + nx, a[1] + ny), P(b[0] + nx, b[1] + ny), P(b[0] - nx, b[1] - ny), P(a[0] - nx, a[1] - ny)
    return [Seg(p1, p2)] + arc(b[0], b[1], r, r, th + 90, th - 90, start=p2, end=p3) + [Seg(p3, p4)] + arc(a[0], a[1], r, r, th - 90, th - 270, start=p4, end=p1)


def tilt(segs, deg, cx, cy):
    c, s = math.cos(math.radians(deg)), math.sin(math.radians(deg)); out = []
    for g in segs:
        m = Seg.__new__(Seg); m.p = [P(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in g.p]; out.append(m)
    return out


# ---- the s ----
S = ([Seg((S0, YTOP), (XA, YTOP))] + arc(XA, YTOP + R1, R1, R1, 270, 90, start=P(XA, YTOP), end=P(XA, YT)) + [Seg((XA, YT), (XB, YT))] +
     arc(XB, YT + R2, R2, R2, -90, 90, start=P(XB, YT), end=P(XB, BOT)) + [Seg((XB, BOT), (S1, BOT))])
# ---- the body: everything but the piece of its bottom edge that is the top of the s ----
BODY = one("M%s,%s L%s,%s L%s,%s Q%s,%s %s,%s L55,%s L61,%s C62,%s 63,%s 66,%s C78,%s 88,%s 93,%s C95,%s 91,%s 86,%s L%s,%s L%s,%s L%s,%s" % (
    XA, YTOP, REAR, YTOP, REAR, DECK + 6, REAR, DECK, REAR + 6, DECK, DECK, DECK - 2, DECK - 3.6, DECK - 4, DECK - 4,
    DECK - 2, DECK + 10, DECK + 22, YT - 7, YT - 2.5, YT - 2.5, XB + R2 + 6.5, YT - 2.5, XB + R2 + 3, YTOP, S0, YTOP))
# ---- the track: everything but its front end, which is the bottom of the s ----
TRACK = [Seg((XA, YT), (XR, YT))] + arc(XR, YT + R2, R2, R2, 270, 90, start=P(XR, YT), end=P(XR, BOT)) + [Seg((XR, BOT), (S1, BOT))]
TRACK_ALL = ([Seg((XR, YT), (XB, YT))] + arc(XB, YT + R2, R2, R2, -90, 90, start=P(XB, YT), end=P(XB, BOT)) + [Seg((XB, BOT), (XR, BOT))] +
             arc(XR, YT + R2, R2, R2, 90, 270, start=P(XR, BOT), end=P(XR, YT)))

p.shape('wind', one("M63,%s C63,%s 67,%s 73,%s C76,%s 78,%s 79,%s Z" % (DECK - 3.5, DECK - 13, DECK - 20, DECK - 23, DECK - 17, DECK - 10, DECK - 0.5)), step=6)
p.stroke('post', Seg((59.6, DECK + 0.6), (55, DECK - 12.4)), step=6)
p.shape('leg', box(71.5, YT - 5, 74.5, BOT - 1), step=5)
p.shape('armB', box(21.4, YTOP - 3, 24.6, YT + 3), step=4)
p.stroke('armF', arc(XA, YTOP + R1, RO, RO, 232, 128), step=4)
p.region('bodyR', BODY, Seg((S0, YTOP), (XA, YTOP)))
p.stroke('body', BODY, step=3)
p.stroke('divide', Seg((58, DECK - 1), (58, YTOP)), step=3)
p.stroke('seat', [Seg((12.5, DECK), (12.5, DECK - 3.4))] + arc(15.7, DECK - 3.4, 3.2, 3.2, 180, 270, start=P(12.5, DECK - 3.4), end=P(15.7, DECK - 6.6)) +
         [Seg((15.7, DECK - 6.6), (47.8, DECK - 6.6))] + arc(47.8, DECK - 3.4, 3.2, 3.2, 270, 360, start=P(47.8, DECK - 6.6), end=P(51, DECK - 3.4)) +
         [Seg((51, DECK - 3.4), (51, DECK))], step=6)
p.shape('grip', stick((50.6, DECK - 12), (57.6, DECK - 13.2), 3.2), step=6)
p.region('trackR', TRACK_ALL)
p.stroke('track', TRACK, step=2)
for i, x in enumerate(WH):
    p.shape('wheel%d' % i, circle(x, YT + R2, R2 * 0.5), step=2)
p.shape('ski', one("M61,88 L88,88 C93,88 95,85 96,81.5 L98,82 C97.5,87 95,91 89,91 L61,91 Z"), step=5)
p.shape('lamp', tilt(ell(86.4, DECK + 18, 3, 2.1), 38, 86.4, DECK + 18), step=7)
for i, (a, b) in enumerate(((5, 24), (30, 56), (66, 97))):
    p.stroke('snow%d' % i, one("M%s,96.5 Q%s,93.3 %s,96.5" % (a, (a + b) / 2, b)), step=7, deco=True)
p.stroke('s', S, step=1)
p.build()

steps = [
    step('Start with an s', 'Draw a small letter s with flat ends: along the top, round to the left, a short line, a bigger curve round to the right, then back along the bottom.', p.step(1)),
    step('The track', 'The bottom of the s is the front of the track. From the middle of the s draw a long line back, round the end and along the bottom. Draw four wheels inside.', p.step(2)),
    step('The body', 'From the top of the s go back, up and along the top. Go over the big round nose, back under it and up a short slope to the s. Add a line down the middle.', p.step(3)),
    step('Two arms', 'The body sits on two arms. Draw a curved line round the top of the s, from the body down to the track. Further back, draw two lines close together.', p.step(4)),
    step('The ski', 'In front of the track draw a long thin ski that curls up at its tip. Join it to the nose with two lines close together.', p.step(5)),
    step('Seat, handlebar, windscreen', 'Draw a long seat on top. Draw a slanting line up from the body with a little sausage on top. Draw a tall pointed windscreen on the nose.', p.step(6)),
    step('Headlight and snow', 'Draw a small oval on the nose for the headlight. Draw three low bumps of snow underneath.', p.step(7)),
    step('Colour orange', 'Colour the back of the body orange, as far as the line down the middle. Leave the nose white.', [p.face('orange', (30, 52))], use='orange'),
    step('Colour light blue', 'Colour the windscreen light blue.', [p.face('lblue', (71, 22))], use='lblue'),
    step('Colour black', 'Colour the track black, round the four wheels. Colour the seat and the handlebar black too.',
         [p.face('black', (23, YT + 1.6), holes=['wheel%d' % i for i in range(4)]), p.face('black', (30, DECK - 3)), p.ring('black', 'grip')], use='black'),
    step('Colour grey', 'Colour the four wheels grey. Colour the two arms, the ski and its leg grey too.',
         [p.ring('grey', 'wheel%d' % i) for i in range(4)] + [p.face('grey', (23, YTOP + 5)), p.face('grey', (XA - R1 - 1.3, YTOP + 5)), p.ring('grey', 'ski'), p.face('grey', (73, 81))], use='grey'),
    step('Colour yellow', 'Colour the headlight yellow.', [p.ring('yellow', 'lamp')], use='yellow'),
]
D = drawing('dx_snowmobile_s', 's is for snowmobile', 3, 15, 'vehicles', ['Letters', 'Vehicles'],
            'An orange snowmobile on the snow. The small letter s is hiding at the front of its track: under the body, down the arm, and round the end of the track.',
            steps, ['orange', 'lblue', 'black', 'grey', 'yellow'])
ok = finish('snowmobile', D, {'set': 'vehicles-az', 'slot': 's', 'kind': 'drive', 'age_from': 5}, p)
