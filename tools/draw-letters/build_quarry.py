"""q is for quarry truck (Vehicles a to z, slot q). Side view, facing left.
The q: its round bowl is the top of the cab (the window goes inside it) and its stick is the back of the cab,
going down past the bowl to the bottom of the truck. The tipper hangs off the right of the stick.

25 Nov 2026: he sent step 1 from the live app and said "Make the front orange bit better". The front was a plain
box with round corners sticking out under the cab. Now it is a bonnet: its top slopes down to a round nose, it has a
grey bumper on the front corner, three slots along its side, and the round light sits near the nose. The q, the cab,
the tipper, the rocks and the wheels have not moved.
Later on 25 Nov: "try changing the orange underneath where the driver's head will be yellow like the rest of the vehicle".
The front is yellow now, like the cab and the tipper; the light on it is orange, so it still shows.
"""
import json, os
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out')

SX = 40.0; TOP = 26.0; BB = 46.0; BOT = 62.0

# ---- 1: the q ----
bowl = [Seg((SX, TOP), (31.0, TOP)),
        Seg((31.0, TOP), (23.0, TOP), (18.0, 31.5), (18.0, 37.0)),
        Seg((18.0, 37.0), (18.0, 42.5), (21.0, BB), (25.0, BB)),
        Seg((25.0, BB), (SX, BB))]
stick = Seg((SX, TOP), (SX, BOT))

# ---- 2: the window inside the bowl ----
win = [Seg((36.6, 29.4), (31.0, 29.4)),
       Seg((31.0, 29.4), (25.4, 29.4), (21.6, 33.0), (21.6, 37.0)),
       Seg((21.6, 37.0), (21.6, 39.6), (23.0, 41.0), (25.4, 41.0)),
       Seg((25.4, 41.0), (36.6, 41.0)),
       Seg((36.6, 41.0), (36.6, 29.4))]

# ---- 3: the bonnet: its top slopes down to a round nose; a bumper sits on its front corner ----
NX, BUY, BUX = 9.0, 56.6, 15.6                 # the nose, the top of the bumper, the back of the bumper
hood = [Seg((25.0, BB), (14.0, BB + 2.6)), Seg((14.0, BB + 2.6), (11.4, BB + 3.2), (NX, BB + 4.6), (NX, BB + 7.4)),
        Seg((NX, BB + 7.4), (NX, BUY))]
under = Seg((BUX, BOT), (SX, BOT))
bumper = [Seg((BUX, BUY), (7.6, BUY)), Seg((7.6, BUY), (6.4, BUY), (5.6, BUY + 0.8), (5.6, BUY + 2.0)),
          Seg((5.6, BUY + 2.0), (5.6, BOT - 0.4)), Seg((5.6, BOT - 0.4), (5.6, BOT + 0.8), (6.4, BOT + 1.6), (7.6, BOT + 1.6)),
          Seg((7.6, BOT + 1.6), (BUX, BOT + 1.6)), Seg((BUX, BOT + 1.6), (BUX, BOT)), Seg((BUX, BOT), (BUX, BUY))]
bonnet = hood + [Seg((NX, BUY), (BUX, BUY)), Seg((BUX, BUY), (BUX, BOT)), under]          # the edge of the orange part

# ---- 4: the tipper ----
TR = (88.0, 20.0); BR_ = (79.0, BOT)
tip = [Seg((SX, TOP), TR), Seg(TR, BR_), Seg(BR_, (SX, BOT))]

# ---- 5: a rim along the top, and three ribs ----
RY = 4.2
def on_top(x):
    return P(x, TOP + (TR[1] - TOP) * (x - SX) / (TR[0] - SX))
def on_right(y):
    t = (y - TR[1]) / (BR_[1] - TR[1]); return P(TR[0] + (BR_[0] - TR[0]) * t, y)
rimL = P(SX, TOP + RY)
rimR = on_right(TR[1] + RY + 0.2)
rimR = P(rimR[0], rimL[1] + (TR[1] - TOP) * (rimR[0] - SX) / (TR[0] - SX))
rimR = on_right(rimR[1])
rim = Seg(rimL, rimR)
def rim_at(x):
    t = (x - rim.a[0]) / (rim.b[0] - rim.a[0]); return P(x, rim.a[1] + (rim.b[1] - rim.a[1]) * t)
ribs = [Seg(rim_at(x), (x, BOT)) for x in (52.0, 62.0, 72.0)]

# ---- 6: rocks piled on top ----
rx = [44.0, 53.5, 63.0, 72.5, 82.0]
pts = [on_top(x) for x in rx]
rocks = [Seg(pts[0], (pts[0][0] - 1.0, pts[0][1] - 6.0), (pts[1][0] - 1.0, pts[1][1] - 7.0), pts[1]),
         Seg(pts[1], (pts[1][0] - 1.0, pts[1][1] - 10.5), (pts[2][0] + 1.5, pts[2][1] - 10.0), pts[2]),
         Seg(pts[2], (pts[2][0] + 0.0, pts[2][1] - 7.0), (pts[3][0] + 0.5, pts[3][1] - 8.0), pts[3]),
         Seg(pts[3], (pts[3][0] + 1.0, pts[3][1] - 6.0), (pts[4][0] + 1.5, pts[4][1] - 5.0), pts[4])]

# ---- 7: the wheels ----
WY = 73.5; WR = 9.0
wheels = [circle(24.0, WY, WR), circle(68.0, WY, WR)]
hubs = [circle(24.0, WY, 3.6), circle(68.0, WY, 3.6)]

# ---- 8: the frame between the wheels, and a headlight ----
frame = rrect(36.0, 66.0, 56.0, 69.6, 1.6)
lamp = circle(14.4, 52.6, 2.2)
slots = [Seg((x, 51.4), (x, 57.6)) for x in (22.0, 26.0, 30.0)]

steps = [
    step('Start with a q', 'Draw a small letter q: a round bowl, then a straight line going down past the bottom of it. This q is hiding in the truck.',
         [line(*bowl), line(stick)]),
    step('The window', 'Draw a window inside the bowl of the q, the same shape but smaller.',
         [ring(*win)]),
    step('The front', 'From the bottom of the bowl, draw a line sloping down to the left, round the nose and down. Draw a bumper on the corner, then a line back to the q.',
         [line(*hood), ring(*bumper), line(under)]),
    step('The tipper', 'From the top of the q, draw a long line sloping up to the right. Go down a slanting side and back along the bottom to the q.',
         [line(*tip)]),
    step('Rim and ribs', 'Draw a line along the top of the tipper. Then draw three straight lines down from it to the bottom.',
         [line(rim)] + [line(r) for r in ribs]),
    step('Rocks', 'Draw a pile of big round rocks on top of the tipper.',
         [line(*rocks)]),
    step('The wheels', 'Draw two big wheels under the truck. Draw a small circle in the middle of each one.',
         [ring(*w) for w in wheels] + [ring(*h) for h in hubs]),
    step('Frame, light and slots', 'Draw a long thin box between the wheels. Draw a round light on the front of the truck, and three short lines on its side.',
         [ring(*frame), ring(*lamp)] + [line(s) for s in slots]),
    step('Colour yellow', 'Colour the cab yellow, round the window. Colour the front of the truck yellow too, round the light, and the tipper under the rim.',
         [fill(FILL['yellow'], *(bowl + [Seg((SX, BB), (SX, TOP))]), cut=[d_fill(*win)]),
          fill(FILL['yellow'], *(bonnet + [Seg((SX, BOT), (SX, BB)), Seg((SX, BB), (25.0, BB))]), cut=[d_fill(*lamp)]),
          fill(FILL['yellow'], *poly(rimL, rimR, BR_, (SX, BOT), closed=True))], use='yellow'),
    step('Colour orange', 'Colour the light orange. Colour the rim on the tipper orange too.',
         [fill(FILL['orange'], *lamp),
          fill(FILL['orange'], *poly((SX, TOP), TR, rimR, rimL, closed=True))], use='orange'),
    step('Colour the window', 'Colour the window light blue.',
         [fill(FILL['lblue'], *win)], use='lblue'),
    step('Colour grey', 'Colour the rocks grey. Colour the middles of the wheels and the bumper grey too.',
         [fill(FILL['grey'], *(rocks + [Seg(pts[4], pts[0])])), fill(FILL['grey'], *hubs[0]), fill(FILL['grey'], *hubs[1]), fill(FILL['grey'], *bumper)], use='grey'),
    step('Colour black', 'Colour the two tyres black, round the grey middles. Colour the frame black too.',
         [fill(FILL['black'], *wheels[0], cut=[d_fill(*hubs[0])]), fill(FILL['black'], *wheels[1], cut=[d_fill(*hubs[1])]),
          fill(FILL['black'], *frame)], use='black'),
]

D = drawing('dx_quarrytruck_q', 'q is for quarry truck', 3, 15, 'vehicles', ['Letters', 'Vehicles'],
            'A big yellow quarry truck carrying a pile of rocks. The small letter q is hiding in it: its bowl is the top of the cab and its stick is the back of the cab.',
            steps, ['yellow', 'orange', 'lblue', 'grey', 'black'])
json.dump(D, open(os.path.join(OUT, 'quarry.json'), 'w'))
json.dump({'set': 'vehicles-az', 'slot': 'q', 'kind': 'drive', 'age_from': 5}, open(os.path.join(OUT, 'quarry.place.json'), 'w'))
print('quarry: %d steps' % len(steps))
