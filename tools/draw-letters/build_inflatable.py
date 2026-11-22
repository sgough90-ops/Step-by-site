"""I is for Inflatable boat (dx_inflatable_i), Vehicles A to Z, slot I (22 Nov 2026).
From his pick: round 2's "Paddle with two blades" boat with round 3's new paddle number 4, "Slim red paddle"
(claude/step-by-draw-vehicles-capitals-round3-paddle.py).

A yellow rubber boat seen from above and a little to the side, with a paddle lying across it. The I is real edges of
the paddle: the flat ends of its two blades and the left edge of its pole (the pole runs over the blades to their
ends). The far corner of each blade is rounder than the near one, so the I's bars sit centred on its long line.
Written in the sketch's numbers; the Pic moves it onto the paper.

    python3 build_inflatable.py
"""
from vkit import *

X0, X1, Y0, Y1, BAND = 5, 95, 38, 78, 8              # the boat
H = Y1 - Y0; R = H * 0.47
XC, TOP, BOT, BW, BL, SW, RL = 50, 21, 94, 7.4, 23, 3.6, 1.4   # the paddle
XL, XR = XC - SW / 2, XC + SW / 2
RR = RL + SW
FX0, FX1 = XC - BW + RL, XC + BW - RR                # the ends of the I's bars (centred on XL)
p = Pic(s=0.95, dx=2.5, dy=-4.6)

# ---- the boat, back to front ----
p.shape('base', rrect(X0, Y0 + BAND, X1, Y1 + BAND, R), step=5)
p.shape('tube', rrect(X0, Y0, X1, Y1, R), step=4)
ix, it = (X1 - X0) * 0.145, H * 0.27
p.shape('floor', rrect(X0 + ix, Y0 + it, X1 - ix, Y1 - it, H * 0.23), step=6)
HANDLES = []
for fx, side in ((0.27, 'L'), (0.73, 'R')):
    x = X0 + (X1 - X0) * fx
    for nm, (a, b) in (('hT' + side, (Y0 + H * 0.075, Y0 + H * 0.145)), ('hB' + side, (Y1 - H * 0.155, Y1 - H * 0.085))):
        p.shape(nm, rrect(x - 3.2, a, x + 3.2, b, 1.2), step=7); HANDLES.append(nm)


# ---- the paddle ----
def blade(y_tip, y_neck):
    s = 1 if y_neck > y_tip else -1
    L = abs(y_neck - y_tip); yb = y_tip + s * L * 0.5
    left = one(f"M{XL},{y_neck} C{XL - 0.4},{y_neck - s * L * 0.16} {XC - BW},{y_neck - s * L * 0.20} {XC - BW},{yb} "
               f"L{XC - BW},{y_tip + s * RL} Q{XC - BW},{y_tip} {FX0},{y_tip}")
    right = one(f"M{XR},{y_neck} C{XR + 0.4},{y_neck - s * L * 0.16} {XC + BW},{y_neck - s * L * 0.20} {XC + BW},{yb} "
                f"L{XC + BW},{y_tip + s * RR} Q{XC + BW},{y_tip} {FX1},{y_tip}")
    back = [Seg(*reversed(q.p)) for q in reversed(right)]
    return left, right, left + [Seg((FX0, y_tip), (FX1, y_tip))] + back + [Seg((XR, y_neck), (XL, y_neck))]


lt, rt, regt = blade(TOP, TOP + BL)
lb, rb, regb = blade(BOT, BOT - BL)
p.region('bladeT', regt)
p.region('bladeB', regb)
p.region('pole', box(XL, TOP, XR, BOT))
p.stroke('side_tl', lt, step=3); p.stroke('side_tr', rt, step=3)
p.stroke('side_bl', lb, step=3); p.stroke('side_br', rb, step=3)
p.stroke('pole_r', Seg((XR, TOP), (XR, BOT)), step=2)
p.stroke('I_top', Seg((FX0, TOP), (FX1, TOP)), step=1)
p.stroke('I_mid', Seg((XL, TOP), (XL, BOT)), step=1)
p.stroke('I_bot', Seg((FX0, BOT), (FX1, BOT)), step=1)
p.build()

HL = ['hTL', 'hBL']; HR = ['hTR', 'hBR']
steps = [
    step('Start with an I', 'Draw a tall capital I with a short line across the top and the bottom. This I is hiding in the paddle.', p.step(1)),
    step('The pole', "Draw a line down close beside the I's long line, from the top line to the bottom line.", p.step(2)),
    step('The blades', 'At each end, make a long blade: from the ends of the short line, go out and along, then curve in to the pole.', p.step(3)),
    step('The boat', 'Draw a long shape with round ends behind the paddle. Stop at the paddle and carry on the other side.', p.step(4)),
    step('The bottom', 'Draw a curve under the boat, a little lower, from one end round to the other. Stop at the paddle again.', p.step(5)),
    step('The floor', 'Inside the boat, draw a smaller long shape with round ends for the floor.', p.step(6)),
    step('Handles', 'Draw four small handles with round corners: two along the top of the boat and two along the bottom.', p.step(7)),
    step('Colour yellow', 'Colour the fat sides of the boat yellow. Leave the handles.',
         [p.face('yellow', (10, 58), holes=HL), p.face('yellow', (90, 58), holes=HR)], use='yellow'),
    step('Colour blue', 'Colour the bottom of the boat blue.', [p.face('blue', (20, 82)), p.face('blue', (80, 82))], use='blue'),
    step('Colour light blue', 'Colour the floor light blue.', [p.face('lblue', (30, 58)), p.face('lblue', (70, 58))], use='lblue'),
    step('Colour grey', 'Colour the pole and the four handles grey.', [p.face('grey', (XC, 58))] + [p.ring('grey', h) for h in HANDLES], use='grey'),
    step('Colour red', 'Colour the two blades red.',
         [p.face('red', (45.4, 30)), p.face('red', (54.6, 30)), p.face('red', (45.4, 85)), p.face('red', (54.6, 85))], use='red'),
]

D = drawing('dx_inflatable_i', 'I is for Inflatable boat', 2, 12, 'vehicles', ['Letters', 'Vehicles'],
            'A yellow rubber boat with a red paddle lying across it. The capital I is hiding in the paddle: the flat ends '
            'of its two blades and the edge of its pole.',
            steps, ['yellow', 'blue', 'lblue', 'grey', 'red'])
save('inflatable', D, {'set': 'vehicles-AZ', 'slot': 'I', 'kind': 'sail', 'age_from': 4})
save_white('inflatable', p.white)
if __name__ == '__main__':
    preview(D, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out', 'inflatable-look.png'))
