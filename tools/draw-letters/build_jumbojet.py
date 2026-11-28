"""J is for Jumbo jet, new version (dx_jumbojet_j, the same key as the live one), Vehicles A to Z, slot J (28 Nov 2026).
From his pick on 28 Nov: number 4 on the sheet "J is for Jumbo jet" (the chubby jet with the purple tail fin, the orange
tummy and the grey engine), "but without the cloud and the star".
STATUS: LIVE since 28 Nov 2026, 17:31 (he said "add plane"). It replaced the old jumbo jet (11 steps, red fin),
which had no build script. Same key, put in with reapply.py.

A chubby jumbo jet facing left. The J is where it is in the live drawing: its straight line is the back edge of the
tail fin and the back of the jet; its hook is the round back corner and a short stretch of the underside, stopping where
the back of the wing joins. Everything else only touches the J. Written in the sketch's numbers; the Pic moves it onto
the paper.

Simpler than the sketch in one place, so a pencil can do it: the front of the engine is one oval (coloured black),
not an oval inside an oval.

    python3 build_jumbojet.py
"""
from bcommon import *

p = Pic(s=1.12, dx=-2.25, dy=-5.22)
JX, JT, JB, JR, JE = 82, 16, 68, 15, 58            # the J: down at JX from JT, round a corner of JR, along the bottom to JE
TOP = 45                                           # the top of the body behind the hump
TUM = 60                                           # the line along the side: orange below it
EX, EY, ER, EL = 32, 74.6, 3.8, 49                 # the engine: front oval at EX, tube back to EL (then a round end)

BODY = "M58,68 L36,68 C24,68 13,64.5 11.5,56 C10,47 17,36 30,36 L39,36 C47,36 48,45 56,45 L82,45"
J_BACK = [Seg((JX, TOP), (JX, JB - JR)), *arc(JX - JR, JB - JR, JR, JR, 0, 90), Seg((JX - JR, JB), (JE, JB))]
WING = "M38,68 L60,81.6 Q61.4,82.6 63.2,82.6 L66.6,82.6 Q68.8,82.6 67.8,80.6 L58,68"

# ---- under the jet: the engine (its back end is behind the wing), then the wing ----
p.shape('engine', Seg((EX, EY - ER), (EL, EY - ER)), arc(EL, EY, ER, ER, -90, 90), Seg((EL, EY + ER), (EX, EY + ER)),
        Seg((EX, EY + ER), (EX, EY - ER)), step=5)
p.shape('intake', circle(EX, EY, 2.4, ry=ER), step=5)
p.region('wingR', one(WING + " Z"))
p.stroke('wing', one(WING), step=4)

# ---- the jet: everything but its back end, which is the J ----
p.region('bodyR', one(BODY), J_BACK)
p.stroke('body', one(BODY), step=2)
p.stroke('fin', one("M62.6,45 L74.8,18.4 Q75.9,16 78.6,16 L82,16"), step=3)
p.shape('pilot', one("M15.6,50.4 C16.2,46.4 18.8,42.8 22.8,41.6 L26.8,41.6 L26.8,50.4 Z"), step=6)
for i, x in enumerate((33.5, 41, 48.5, 56, 63.5)):
    p.shape('win%d' % i, circle(x, 53.5, 2.2), step=6)
p.stroke('tummy', Seg((4, TUM), (92, TUM)), step=7)
p.shape('tailwing', one("M69,55.8 L77.2,50.6 L79.6,50.6 L75.8,55.8 Z"), step=7)

# ---- the J, in front of everything ----
p.stroke('J', Seg((JX, JT), (JX, JB - JR)), arc(JX - JR, JB - JR, JR, JR, 0, 90), Seg((JX - JR, JB), (JE, JB)), step=1)
p.build()
p.net.keep_in('tummy', 'bodyR')

steps = [
    step('Start with a J', 'Draw a capital J: a long straight line down, round the corner to the left, and a short line along.', p.step(1)),
    step('The body', 'From the end of the J go along and up round the big nose. Come back along the top, curve down a little, then go straight to the J.', p.step(2)),
    step('The tail fin', 'From the top of the body draw a slanting line up. Near the top, curve over and join the top of the J.', p.step(3)),
    step('The wing', 'Under the body draw a long line slanting down and back. Make a round tip, then go back up to the end of the J.', p.step(4)),
    step('The engine', 'In front of the wing draw a tall oval. Draw two lines from it back to the wing. The bottom one curls up at the end.', p.step(5)),
    step('Windows', "Draw the pilot's window at the front, with a round corner. Draw five little round windows in a row.", p.step(6)),
    step('Stripe and little wing', 'Draw a long line along the side, from the nose to the J. Above it, near the tail, draw a little slanting wing.', p.step(7)),
    step('Colour purple', 'Colour the tail fin purple. Colour the little wing near the tail purple too.',
         [p.face('purple', (74, 35)), p.ring('purple', 'tailwing')], use='purple'),
    step('Colour orange', 'Colour the tummy of the jet orange, under the long line.', [p.face('orange', (45, 64))], use='orange'),
    step('Colour light blue', "Colour the pilot's window and the five round windows light blue.",
         [p.ring('lblue', 'pilot')] + [p.ring('lblue', 'win%d' % i) for i in range(5)], use='lblue'),
    step('Colour grey', 'Colour the big wing and the engine grey.', [p.face('grey', (56, 74)), p.face('grey', (39, EY))], use='grey'),
    step('Colour black', 'Colour the oval at the front of the engine black.', [p.ring('black', 'intake')], use='black'),
]
D = drawing('dx_jumbojet_j', 'J is for Jumbo jet', 2, 15, 'vehicles', ['Letters', 'Vehicles'],
            'A chubby jumbo jet with a purple tail and an orange tummy. The capital J is hiding at the back: '
            'the back edge of the tail fin, the round back corner and a short line underneath.',
            steps, ['purple', 'orange', 'lblue', 'grey', 'black'])
ok = finish('jumbojet', D, {'set': 'vehicles-AZ', 'slot': 'J', 'kind': 'fly', 'age_from': 5}, p)

if __name__ == '__main__':
    pts = [q for st in D['steps'] for it in st['add'] for sub_, _ in CK.parse(it['d'], step=0.5) for q in sub_]
    xs = [q[0] for q in pts]; ys = [q[1] for q in pts]
    print('    on the paper: x %.2f to %.2f, y %.2f to %.2f (middle %.2f, %.2f)' % (min(xs), max(xs), min(ys), max(ys), (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2))
    print('    longest step text %d, bytes %d' % (max(len(st['text']) for st in D['steps']), len(json.dumps(D, separators=(',', ':')))))
