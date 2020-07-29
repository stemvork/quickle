import pygame
import random
import sys
import math
from pygame.sprite import Sprite
# Some constants
WIDTH  = 595
HEIGHT = WIDTH
ROWS = 7
COLS = 7
SIZE = WIDTH // max(ROWS, COLS)
DEBUG = False
CARDCOUNTS = {
    "bears": 2,
    "foxes": 6,
    "foresters": 2,
    "hunters": 8,
    "ducks": 7,
    "pheasants": 8,
    "trees": 15
}
MOVABLE = {
    "bears": 1,
    "foxes": 1,
    "foresters": 2,
    "hunters": 2,
    "ducks": 0,
    "pheasants": 0,
    "trees": 0
}
COLORMAP = {
    "bears": 2,
    "foxes": 2,
    "foresters": 3,
    "hunters": 3,
    "ducks": 4,
    "pheasants": 4,
    "trees": 4,
    "empty": 6
}
print("There are", len(CARDCOUNTS.keys()), "categories. They make up",
      sum(CARDCOUNTS.values()), "cards",'\n') if DEBUG else None
CARDS = [item[0] for item in CARDCOUNTS.items() for i in range(item[1])]
random.shuffle(CARDS)
print(CARDS,'\n') if DEBUG else None
POSITIONS = [(i, j) for i in range(7) for j in range(7) if (i, j) != (3, 3)]
# random.shuffle(POSITIONS)
print(POSITIONS,'\n') if DEBUG else None
CARDS = [(b, a, 0) for a, b in zip(CARDS, POSITIONS)]
CARDS.insert(24, ((3, 3), "empty", 1))
print(CARDS,'\n') if DEBUG else None

# Initialise pygame
pygame.init()
font = pygame.font.SysFont("Arial", 30)

# Basic components
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Beer is Los')
COLORS = [pygame.Color(c) for c in
            ["#ff0000", "#00ff00", '#0000ff',
             '#cccc00', '#00cccc', '#cc00cc',
             '#037918',]]

# Some handler functions
def proper_exit():
    pygame.quit()
    sys.exit()

def revealCard(idx):
    card = CARDS[idx]
    if card[2] == 0:
        CARDS[idx] = (card[0], card[1], 1)
        return True
    else:
        return False

def getMovable(idx):
    return MOVABLE[CARDS[idx][1]]

PLAYER = 0
# Game loop
while True:
    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            proper_exit()
        elif event.type == pygame.KEYDOWN:
            pass
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            mi, mj = mx // SIZE, my // SIZE
            idx = mi*7+mj
            revealed = revealCard(idx)
            if not revealed and getMovable(idx) > 0 and getMovable(idx)+1 == PLAYER:
                print("Get movin'!")
                PLAYER = not PLAYER
            elif revealed:
                print("Player", PLAYER, "found", CARDS[idx], '\n') if DEBUG else None
                PLAYER = not PLAYER
            else:
                pass

    # Draw loop
    screen.fill(COLORS[-1])
    for card in CARDS:
        cardColor = COLORS[COLORMAP[card[1]]]
        if card[2] > 0:
            pygame.draw.rect(screen, cardColor,
                         (card[0][0] * SIZE, card[0][1] * SIZE, SIZE, SIZE))

    # Finish the draw loop
    pygame.display.flip()
    clock.tick(60)
