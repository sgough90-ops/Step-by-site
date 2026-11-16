"""t is for toucan (dx_toucan_t), Animals a to z, slot t. From Claude's sketch 'toucan 3' (new designs S to Z).
The t: the stick is the back edge of the tail, the curl is the tail's round tip, the bar is the twig."""
from kit15 import *

BLACK, ORANGE, LBLUE, GREEN, BROWN = FILL['black'], FILL['orange'], FILL['lblue'], FILL['green'], FILL['brown']

# ---- the t ----
STX, TOP, BOT = 30, 44, 82
stick = Seg((STX, TOP), (STX, 74.8))
curl = Seg((STX, 74.8), (STX, 80.56), (31.89, BOT), (34.41, BOT))
tailend = Seg((34.41, BOT), (36.3, BOT))
BY, BL, BR = 53, 21.9, 46.2
bar = Seg((BL, BY), (BR, BY))

# ---- body: from the top of the stick, up the back, over the head, down the face and chest to the end of the bar ----
back = Seg((STX, TOP), (30.6, 34), (37.8, 23.5), (45, 19))
head = Seg((45, 19), (47.2, 9.6), (59.2, 8.2), (63.9, 13.6))
B1, B2 = (63.9, 13.6), (63.9, 29.6)
face = Seg(B1, B2)
chest = Seg(B2, (66.2, 41), (52.5, 46.5), (BR, BY))
chest_a, chest_b = chest.split(0.6)
Q = chest_a.b
bib = Seg(B2, (55.2, 31), (49.6, 38.6), Q)

# ---- beak ----
btop = Seg(B1, (73.5, 6.2), (88.6, 12.2), (92.4, 25.6))
hook = Seg((92.4, 25.6), (93, 28.6), (90.8, 31), (87.6, 30.4))
bbot = Seg((87.6, 30.4), (80, 31.6), (70.5, 31.4), B2)
hk_a, hk_b = hook.split(0.45)
mouth = Seg((63.9, 22.2), (72.5, 22.2), (82, 24), hk_a.b)

# ---- eye ----
eye = circle(56.6, 18.2, 3.2)

# ---- tail front edge ----
TF = (38.5, BY)
tailfront = Seg(TF, (38.3, 63), (37.2, 74), (36.3, BOT))

# ---- toes (little loops hooked under the twig) ----
def toe(x0, x1, dep=2.4):
    return Seg((x0, BY), (x0, BY + dep * 1.33), (x1, BY + dep * 1.33), (x1, BY))
toe1, toe2 = toe(40.6, 42.4), toe(43.2, 45.0)

# ---- leaf on the left end of the twig ----
leaf = [Seg((BL, BY), (18.6, 49.9), (13.4, 51.6), (10.8, 56.6)), Seg((10.8, 56.6), (14.4, 58.6), (19.6, 57.6), (BL, BY))]

# ---- branch: from the right end of the twig down to the corner ----
bup = Seg((BR, BY), (60, 57.6), (76, 64.6), (90.5, 72.4))
blo = Seg((BR, BY), (58, 61.4), (72, 70.6), (86.4, 79.6))
bend = Seg((90.5, 72.4), (86.4, 79.6))

steps = [
    step('Start with a t', 'Draw a small letter t: a tall stick that curls round to the right at the bottom, and a long bar across it, near the top.',
         [line(stick, curl, tailend), line(bar)]),
    step('The body and head', 'Start at the top of the t. Go up the back, round the head, straight down the face, then round the tummy to the end of the bar.',
         [line(back, head, face, chest)]),
    step('The big beak', 'From the top of the face, draw a huge beak that curves to a hooked tip, then comes back along the bottom to the face.',
         [line(btop, hook, bbot)]),
    step('The mouth', 'Draw a curved line along the beak, from the face to the tip.', [line(mouth)]),
    step('The eye', 'Draw a circle on the head with a dot in the middle.', [ring(eye), dot(57.1, 18.2, 2.6)]),
    step('The white chest', 'From the bottom of the beak, draw a curve down to the tummy. This is the toucan\'s white chest.', [line(bib)]),
    step('The tail', 'The stick of the t is the back of the tail. Draw the front of the tail: a line from the bar down to the end of the curl.', [line(tailfront)]),
    step('The toes', 'Draw two little loops under the bar. They are the toes holding on to the twig.', [line(toe1), line(toe2)]),
    step('A leaf', 'Draw a leaf on the left end of the bar.', [ring(leaf)]),
    step('The branch', 'From the right end of the bar, draw two lines down to the corner, getting further apart. Join them at the end.',
         [line(bup), line(blo), line(bend)]),
]
body_fill = fill(BLACK, back, head, face, bib, chest_b, Seg((BR, BY), (STX, BY)), Seg((STX, BY), (STX, TOP)), cut=[d_fill(*eye)])
tail_fill = fill(BLACK, Seg((STX, BY), TF), tailfront, tailend.rev(), curl.rev(), Seg((STX, 74.8), (STX, BY)))
steps += [
    step('Colour black', 'Colour the body, the head and the tail black. Leave the chest and the eye white for now.', [body_fill, tail_fill], use='black'),
    step('Colour orange', 'Colour the big beak orange.', [fill(ORANGE, btop, hook, bbot, face.rev())], use='orange'),
    step('Colour light blue', 'Colour the eye and the toes light blue.',
         [fill(LBLUE, *eye), fill(LBLUE, toe1, Seg((40.6 + 1.8, BY), (40.6, BY))), fill(LBLUE, toe2, Seg((45.0, BY), (43.2, BY)))], use='lblue'),
    step('Colour green', 'Colour the leaf green.', [fill(GREEN, *leaf)], use='green'),
    step('Colour brown', 'Colour the branch brown.', [fill(BROWN, bup, bend, blo.rev())], use='brown'),
]
P = drawing('dx_toucan_t', 't is for toucan', 3, 15, 'animals', ['Letters', 'Animals'],
            'A toucan with a huge orange beak, sitting on the end of a twig. The small letter t is hiding in it: '
            'the back of the tail is the stick, the round tip of the tail is the curl and the twig is the bar.',
            steps, ['black', 'orange', 'lblue', 'green', 'brown'])
move(P, 0, 4)
save('toucan', P, {'set': 'animals-az', 'slot': 't', 'kind': 'fly', 'age_from': 5})
