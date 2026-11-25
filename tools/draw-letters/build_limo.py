"""l is for limousine (dx_limo_l), Vehicles a to z, slot l. A front you can tell from the back, 25 Nov 2026.

The limousine was made on 12 Nov from his ChatGPT sheet and had no build script (the page held the only copy). On
25 Nov he said "Make the back of the limo more natural"; Claude gave it a boot as long as the bonnet (limoback.py, on
the natural-fixes branch), and he answered that he could not tell which end was the front and which the back. So this
is a proper build, and the two ends are now different:

  front: a long bonnet that slopes down to a low nose, a long round yellow light, a raked windscreen, and the driver
         (a head with a flat cap whose peak points forward) in the front window;
  back:  a steep back window, a flat boot that stays high, a square tail, a tall red light, and an aerial that leans back.

The l, the wheels, the front door and the row of five windows are where they were: the l is still the tall straight edge of
the front door. The lights are now notches in the edge of the grey, not holes in it, so the old "hole touches its
edge" failure has gone. The driver's face is yellow, like the front light: left white it was a gap in the grey, which the
app's own checker counts as a fail, and yellow needs no extra pencil.

Later on 25 Nov he said "I do like it. I just want you to take out the lines now on the back door", so the back door has
gone: its two lines, and its handle with them (a handle with no door looked like a stray dot). The front door stays.

    python3 build_limo.py
"""
from bcommon import *
import ncommon

p = Pic()
SX, ROOF, BOT, WT, WB = 40.0, 33.0, 57.5, 36.0, 43.3      # the l, the roof, the bottom of the car, the top and bottom of the windows

# ---- the car: top edge (front to back) and the bottom; the wheels sit in front of the bottom ----
top = one("M5,57.5 L5,50.2 C5,49 5.9,48.4 7.4,48.2 L23.5,44.5 L31,34.4 C31.67,33.47 32.73,33 34.2,33 "
          "L73.4,33 C75,33 76,33.8 76.4,35 L79.4,43.6 L91.6,44 C93.8,44.2 95,45.4 95,47.6 L95,57.5")
p.stroke('top', top, step=4)
p.stroke('under', Seg((5.0, BOT), (95.0, BOT)), step=5)

# ---- the driver, behind the door: a round head, a flat cap, its peak pointing forward ----
p.shape('head', circle(35.8, 41.6, 2.4), step=10)
p.shape('cap', one("M33.2,40.5 C33.4,37.6 38.2,37.6 38.4,40.5 Z"), step=10)
p.stroke('peak', Seg((33.2, 40.5), (31.5, 40.9)), step=10, deco=True)
p.region('sill', box(32.0, WB, 39.6, 46.5))               # the door hides the driver below the window

# ---- five windows: the first two share the l as an edge ----
p.stroke('win1', poly((SX, WT), (33.2, WT), (27.8, WB), (SX, WB)), step=6)
p.stroke('win2', poly((SX, WT), (47.2, WT), (47.2, WB), (SX, WB)), step=6)
p.stroke('win3', box(49.4, WT, 55.6, WB), step=7)
p.stroke('win4', box(57.8, WT, 66.4, WB), step=7)
p.stroke('win5', poly((68.6, WT), (73.2, WT), (75.8, WB), (68.6, WB), closed=True), step=7)

# ---- doors, handles, lights, aerial, road ----
p.stroke('door1', Seg((27.8, WB), (27.8, BOT)), step=8)        # the front door: this line, and the l is its other edge
p.stroke('light1', one("M5,50.6 L9.6,50.6 C11,50.6 11.8,51.6 11.8,52.7 C11.8,53.8 11,54.8 9.6,54.8 L5,54.8"), step=9)
p.stroke('light2', poly((95.0, 48.2), (91.0, 48.2), (91.0, 54.6), (95.0, 54.6)), step=9)
p.stroke('h1', circle(36.4, 48.8, 1.0), step=8, deco=True)
AX = 86.4
p.stroke('aerial', Seg((AX, 43.6 + (AX - 79.4) / (91.6 - 79.4) * 0.4), (90.4, 36.6)), step=11, deco=True)
p.stroke('road', Seg((3.0, 67.2), (97.0, 67.2)), step=11)

# ---- wheels in front, then the l in front of everything ----
for nm, x in (('w1', 18.0), ('w2', 82.0)):
    p.shape(nm, circle(x, 59.0, 6.8), step=2)
    p.shape('hub' + nm[1], circle(x, 59.0, 2.8), step=3)
p.stroke('l', Seg((SX, ROOF), (SX, BOT)), step=1)
p.build()

ALL = [it['name'] for it in p.items if it['kind'] != 'region']
DECO = tuple(it['name'] for it in p.items if it['deco'])
glass = [p.face('lblue', (30.6, 42.0)), p.face('lblue', (43.6, 39.6)), p.ring('lblue', 'win3'), p.ring('lblue', 'win4'), p.ring('lblue', 'win5')]
cap = p.ring('black', 'cap')
face = p.net.fill(FILL['yellow'], p.pt(35.8, 42.2), names=ALL, skip=DECO)   # the driver's face (yellow, like the front light: no extra pencil)
INSIDE = ('l', 'door1', 'win1', 'win2', 'win3', 'win4', 'win5', 'head', 'cap', 'road', 'hub1', 'hub2')
body = p.net.fill(FILL['grey'], p.pt(50.0, 50.0), names=ALL, skip=INSIDE + DECO, cut=[g['d'] for g in glass] + [cap['d'], face['d']])

steps = [
    step('Start with an l', 'Draw a small letter l: one straight stick, and nothing else. Put it a little to the left of the middle. This l is hiding in the limousine.', p.step(1)),
    step('Two wheels', 'Draw two wheels, low down and very far apart: one to the left of the stick and one a long way to the right.', p.step(2)),
    step('Wheel middles', 'Draw a smaller circle in the middle of each wheel.', p.step(3)),
    step('The long car', 'Start low at the front. Go up, along the sloping bonnet, up the windscreen and along the roof. Come down steeply, along the flat boot and down the back.', p.step(4)),
    step('Underneath', 'Draw the bottom of the car in three pieces: front to wheel, wheel to wheel, wheel to back. The middle piece touches the bottom of the stick.', p.step(5)),
    step('Two windows', 'Draw a window on each side of the stick. The stick is one edge of each window. The front one slopes like the windscreen.', p.step(6)),
    step('More windows', 'Draw three more windows in a row along the car. The last one slopes a little at the back.', p.step(7)),
    step('The front door', 'Draw a line down from the front corner of the first window. With the stick, it makes the front door. Draw a dot on the door for a handle.', p.step(8)),
    step('Two lights', 'Draw a long round light on the front of the car. Draw a tall light on the back.', p.step(9)),
    step('The driver', 'Draw the driver in the front window: a round head with a flat cap on top. The peak of the cap points to the front.', p.step(10)),
    step('Aerial and road', 'Draw an aerial sticking up from the boot, leaning back. Then draw a long line under the wheels for the road.', p.step(11)),
    step('Colour the car', 'Colour the car grey. Go round the windows and the lights. Colour the middles of the wheels grey too.',
         [body, p.ring('grey', 'hub1'), p.ring('grey', 'hub2')], use='grey'),
    step('Colour the windows', 'Colour the five windows light blue. Go round the driver.', glass, use='lblue'),
    step('Colour yellow', "Colour the front light yellow. Colour the driver's face yellow too.", [p.face('yellow', (8.0, 52.7)), face], use='yellow'),
    step('The back light', 'Colour the back light red.', [p.face('red', (93.0, 51.4))], use='red'),
    step('Colour black', "Colour the two tyres black, round the grey middles. Colour the driver's cap black too.",
         [p.ring('black', 'w1', holes=['hub1']), p.ring('black', 'w2', holes=['hub2']), cap], use='black'),
]

D = drawing('dx_limo_l', 'l is for limousine', 2, 14, 'vehicles', ['Letters', 'Vehicles'],
            'A long grey limousine with five windows and a driver. The small letter l is hiding in it: it is the tall straight '
            'edge of the front door.',
            steps, ['grey', 'lblue', 'yellow', 'red', 'black'])
ok = finish('limo', D, {'set': 'vehicles-az', 'slot': 'l', 'kind': 'drive', 'age_from': 4}, p)
print('    on the paper: x %.1f to %.1f, y %.1f to %.1f' % tuple(ncommon.extent(D)[i] for i in (0, 2, 1, 3)))
