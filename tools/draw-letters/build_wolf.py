"""w is for wolf (dx_wolf_w), Animals a to z, slot w. Rebuilt from his ChatGPT sheet (15 Nov 2026).
The w is the zigzag edge of the wolf's white chest fur."""
from kit15 import *

GREY, PINK, YELLOW, BLACK = FILL['grey'], FILL['pink'], FILL['yellow'], FILL['black']
CX = 47.0

# ---- the w ----
W1, W2 = (34, 52), (60, 52)
wpts = [W1, (40.5, 61), (CX, 55.5), (53.5, 61), W2]
wsegs = poly(*wpts)

# ---- body ----
lside = Seg(W1, (27.5, 59), (24.6, 72), (25.4, 83))
lcorn = Seg((25.4, 83), (25.7, 86.4), (27.6, 88), (31, 88))
bottom = Seg((31, 88), (63, 88))
rcorn = Seg((63, 88), (66.4, 88), (68.3, 86.4), (68.6, 83))
rside = Seg((68.6, 83), (69.4, 72), (66.5, 59), W2)
t = seg_y(rside, 68)
ra, rb = rside.split(t)
P1 = ra.b

legL = Seg((40.5, 70), (40.5, 88))
legR = Seg((53.5, 70), (53.5, 88))
pawL = Seg((31.8, 88), (31.8, 83.6), (38, 83.6), (38, 88))
pawR = Seg((56, 88), (56, 83.6), (62.2, 88 - 4.4), (62.2, 88))

tail_up = Seg(P1, (75, 64.5), (80.4, 58.6), (86.4, 52.4))
tail_dn = Seg((86.4, 52.4), (88, 62.5), (82.4, 76.4), (68.6, 83))

# ---- head (left half, then mirrored) ----
hl = [Seg(W1, (26.5, 49.5)), Seg((26.5, 49.5), (31, 46.5)), Seg((31, 46.5), (24.5, 41.5)), Seg((24.5, 41.5), (30.8, 38.6)),
      Seg((30.8, 38.6), (29.9, 35.4), (30.2, 32.2), (31.8, 29.5)), Seg((31.8, 29.5), (32.2, 16.8)), Seg((32.2, 16.8), (41.2, 25.6))]
htop = Seg((41.2, 25.6), (44.6, 24.2), (49.4, 24.2), (52.8, 25.6))
hr = rev(mirror(hl, CX))
head = hl + [htop] + hr
assert head[-1].b == W2
chin = Seg(W1, W2)

earL = poly((33.4, 20.6), (38.4, 25.3), (33.4, 27.4), closed=True)
earR = rev(mirror(earL, CX))
eyeL, eyeR = circle(40.2, 35.6, 2.5), circle(53.8, 35.6, 2.5)

# muzzle: a dome sitting on the chin
mz = [Seg((39.4, 52), (39.6, 46.6), (43.2, 43.4), (CX, 43.4)), Seg((CX, 43.4), (50.8, 43.4), (54.4, 46.6), (54.6, 52))]
nose = [Seg((44.4, 45.5), (44.9, 44.7), (49.1, 44.7), (49.6, 45.5)), Seg((49.6, 45.5), (49.6, 46.4), (47.9, 48.1), (CX, 48.1)),
        Seg((CX, 48.1), (46.1, 48.1), (44.4, 46.4), (44.4, 45.5))]
m0 = Seg((CX, 48.1), (CX, 49.6))
mL = Seg((CX, 49.6), (46.1, 50.6), (44.5, 50.5), (43.7, 49.5))
mR = mirror([mL], CX)[0]

steps = [
    step('Start with a w', 'Draw a small letter w. Make the middle point a little lower than the two ends.', [line(*wsegs)]),
    step('The body', 'From the left end of the w, curve out and down to the bottom, go along, then curve up to the right end of the w.',
         [line(lside, lcorn, bottom, rcorn, rside)]),
    step('The front legs', 'Draw two straight lines from the middle of the body down to the bottom.', [line(legL), line(legR)]),
    step('The back paws', 'Draw a little bump on the bottom line in each corner.', [line(pawL), line(pawR)]),
    step('The tail', 'From the right side of the body, draw a big fluffy tail that goes up to a point and curves back to the bottom.',
         [line(tail_up, tail_dn)]),
    step('The head', 'From the left end of the w, draw two fluffy cheeks, a pointy ear, the top of the head, the other ear and two more cheeks to the right end.',
         [line(*head)]),
    step('The chin', 'Draw a straight line from one end of the w to the other. Now the wolf has a white chest.', [line(chin)]),
    step('Inside the ears', 'Draw a small triangle inside each ear.', [ring(earL), ring(earR)]),
    step('The eyes', 'Draw two circles for the eyes, with a dot in each one.', [ring(eyeL), ring(eyeR), dot(40.2, 35.6, 2.4), dot(53.8, 35.6, 2.4)]),
    step('The muzzle', 'Draw a round bump sitting on the chin, in the middle.', [line(*mz)]),
    step('Nose and mouth', 'Draw the nose at the top of the bump. Draw a little line down from it and a smile on each side.',
         [ring(nose), line(m0), line(mL), line(mR)]),
]
head_fill = fill(GREY, *head, Seg(W2, (54.6, 52)), rev(mz), Seg((39.4, 52), W1), cut=[d_fill(*earL), d_fill(*earR), d_fill(*eyeL), d_fill(*eyeR)])
body_fill = fill(GREY, lside, lcorn, bottom, rcorn, rside, rev(wsegs))
tail_fill = fill(GREY, tail_up, tail_dn, ra)
steps += [
    step('Colour grey', 'Colour the head, the body and the tail grey. Leave the chest and the muzzle white.', [head_fill, body_fill, tail_fill], use='grey'),
    step('Colour pink', 'Colour inside the ears pink.', [fill(PINK, *earL), fill(PINK, *earR)], use='pink'),
    step('Colour yellow', 'Colour the eyes yellow, round the dots.', [fill(YELLOW, *eyeL), fill(YELLOW, *eyeR)], use='yellow'),
    step('Colour black', 'Colour the nose black.', [fill(BLACK, *nose)], use='black'),
]
P = drawing('dx_wolf_w', 'w is for wolf', 3, 15, 'animals', ['Letters', 'Animals'],
            'A grey wolf sitting down, with a fluffy tail, pointy ears and a white chest. The small letter w is hiding in it: '
            'it is the zigzag edge of the white fur on its chest.',
            steps, ['grey', 'pink', 'yellow', 'black'])
move(P, -4, 0)
save('wolf', P, {'set': 'animals-az', 'slot': 'w', 'kind': 'walk', 'age_from': 5})
