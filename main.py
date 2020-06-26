import pygame
import random
import sys
import math
from pygame.sprite import Sprite, Group

WIDTH  = 595
HEIGHT = WIDTH
ROWS = 7
COLS = 7
SIZE = WIDTH // max(ROWS, COLS)

DEBUG = False

pygame.init()
font = pygame.font.SysFont("Arial", 30)


clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Marksweeper')


COLORS = [pygame.Color(c) for c in 
            ["#ff0000", "#00ff00", '#0000ff',
             '#cccc00', '#00cccc', '#cc00cc']]


def make_grid(cols, rows):
    arr = []
    for r in range(rows):
        row = [None] * cols
        arr.append(row)
    return arr


class Tile(Sprite):
    def __init__(self, i, j, _GRID):
        super().__init__()
        self.i = i
        self.j = j
        self.revealed = False
        self.x = i * SIZE
        self.y = j * SIZE
        self.w = SIZE
        self.h = SIZE
        self.center = self.w//2, self.h//2
        self.color = (255, 255, 255)
        self.grid = _GRID

        self.image = pygame.Surface((self.w, self.h))

        self.update()

    def move(self, pos):
        self.i = pos[0]
        self.j = pos[1]
        self.update()

    def update(self):
        coord = self.x, self.y
        self.color = (255, 255, 255) if self.revealed else (180, 180, 180)
        self.rect  = self.image.get_rect(topleft = coord)
        self.draw_empty()

    def draw_empty(self):
        self.image.fill(self.color)
        pygame.draw.rect(self.image, (0, 0, 0), (0, 0, self.w, self.h), 2)

    def contains(self, x, y):
        return self.rect.collidepoint(x, y)

class BGTile(Tile):
    def __init__(self, i, j, _GRID, color):
        super().__init__(i, j, _GRID)
        self.color = color
        self.update()

    def move(self, pos):
        pass
    
    def update(self):
        coord = self.x, self.y
        self.rect  = self.image.get_rect(topleft = coord)
        self.draw_empty()

class Grid(Group):
    def __init__(self):
        super().__init__()
        self.cols = COLS
        self.rows = ROWS
        self.grid = make_grid(self.cols, self.rows)
        self.revealed = 0
        self.ended = False

        for r in range(len(self.grid)):
            for c in range(len(self.grid[r])):
                tile = Tile(c, r, self)
                self.grid[r][c] = tile
                self.add(tile)
        center_old = self.grid[ROWS//2][COLS//2]
        self.remove(center_old)
        center_tile = BGTile(ROWS//2, COLS//2, self, (255, 0, 0))
        self.add(center_tile)
        self.grid[ROWS//2][COLS//2] = center_tile

    def at(self, x, y):
        for cell in self.sprites():
            if cell.contains(x, y):
                return cell

    def count_neutral(self):
        total = 0
        for j in range(len(self.grid)):
            for i in range(len(self.grid[j])):
                pass
        self.revealed = total
        return ROWS * COLS - total
    
    def game_over(self):
        for j in range(len(self.grid)):
            for i in range(len(self.grid[j])):
                self.grid[j][i].reveal()
        self.ended = True

GRID = Grid()
    
def proper_exit():
    pygame.quit()
    sys.exit()

def handle_keydown(args):
    key, GRID = args
    if key == pygame.K_ESCAPE:
        proper_exit()
    elif key == pygame.K_SPACE:
        pass
    elif key == pygame.K_RETURN:
        pass
    elif key == pygame.K_r:
        if GRID.ended:
            GRID = Grid()
    return GRID

def handle_mousedown(args):
    args = GRID
    if not GRID.ended:
        x, y = pygame.mouse.get_pos()

        if pygame.mouse.get_pressed()[0]:
            print(GRID.at(ROWS//2, COLS//2).color)
            for cell in GRID.sprites():
                if cell.contains(x, y):
                    cell.revealed = True
                    cell.update()

        elif pygame.mouse.get_pressed()[2]:
            pass

        if GRID.count_neutral() == 0:
            GRID.game_over()

    return GRID


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            proper_exit()
        elif event.type == pygame.KEYDOWN:
            args = event.key, GRID
            GRID = handle_keydown(args)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            args = GRID
            GRID = handle_mousedown(args)

    screen.fill((80, 70, 90))
    GRID.draw(screen)
    
    pygame.display.flip()
    clock.tick(60)
