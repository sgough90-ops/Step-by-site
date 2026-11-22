"""O is for Orange (dx_orange_o), Food and drink A to Z, slot O (22 Nov 2026).
From his pick "O1 Whole orange with a leaf" (Claude's sketches, claude/step-by-draw-food-11-ideas-4-versions.md).

The O is the round outline of the orange. On top is a tiny green stalk with one leaf.

    python3 build_orange.py
"""
import math
from fkit import *

ORANGE, GREEN = FILL['orange'], FILL['green']
CX, CY, RX, RY = 50, 61, 33, 34

net = Net()
net.add('O', ell(CX, CY, RX, RY))                                   # 1: the O, from the top, clockwise
net.add('nub', poly((48.3, 29), (48.5, 21.6), (51.7, 21.6), (51.9, 29)))   # the tiny stalk (its feet go into the O, then are trimmed)
leaf = leaf2((51.7, 21.6), (79, 11.5), 13)
net.add('leaf', leaf)
net.node()
net.hide('nub', 'O')

# the middle line of the leaf, the shine and the dots are only lines (no colour edge uses them)
rib = Seg((57.5, 19.4), (62, 17.2), (67.5, 15.5), (73, 13.7))
shine = arc(CX, CY, RX - 6.5, RY - 6.5, 200, 238)
dots = [dot(x, y, w=2.6) for x, y in [(41, 52), (57, 47), (66, 62), (46, 71), (60, 78), (34, 66)]]

steps = [
    step('Start with an O', 'Draw a big round capital O. This O is hiding in the orange.', net.lines('O')),
    step('The stalk', 'Draw a tiny stalk on top of the O: two short lines going up, and a line across the top.', net.lines('nub')),
    step('The leaf', 'Draw a pointed leaf from the top of the stalk. Draw a line along its middle.', net.lines('leaf') + [line(rib)]),
    step('Shine and dots', 'Inside the O, draw a curved line near the top left for the shine. Add a few little dots for the peel.',
         [line(*shine)] + dots),
    step('Colour orange', 'Colour the orange orange, all the way to the edge of the O.', [net.fill(ORANGE, (50, 62), names=['O'])], use='orange'),
    step('Colour green', 'Colour the tiny stalk and the leaf green.',
         [net.fill(GREEN, (50.1, 24.5), names=['O', 'nub']), net.fill(GREEN, (66, 16.5), names=['leaf'])], use='green'),
]

D = drawing('dx_orange_o', 'O is for Orange', 1, 6, 'things', ['Letters', 'Around the house'],
            'A big juicy orange with a leaf. The capital O is hiding in it: it is the round outline of the orange.',
            steps, ['orange', 'green'])
save('orange', D, {'set': 'house-AZ', 'slot': 'O', 'kind': 'key', 'age_from': 4})
