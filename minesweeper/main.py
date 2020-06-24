import pygame
import random
import sys
import math
from pygame.sprite import Sprite, Group

WIDTH  = 600
HEIGHT = 600
ROWS = 10
COLS = 10
SIZE = 600 // max(ROWS, COLS)
TOTALBEES = 11

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


class Cell(Sprite):
    def __init__(self, i, j, _GRID):
        super().__init__()
        #self.bee = random.choice([True, False])
        self.bee = False
        self.revealed = DEBUG
        self.marked = False
        self.i = i;
        self.j = j;
        self.x = i * SIZE
        self.y = j * SIZE
        self.w = SIZE
        self.h = SIZE
        self.center = self.w//2, self.h//2
        self.n = 0
        self.n_text = None
        self.grid = _GRID

        self.image = pygame.Surface((self.w, self.h))
        coord = self.x, self.y
        self.rect  = self.image.get_rect(topleft = coord)

        self.update()

    def update(self):
        if self.revealed:
            if self.marked:
                self.draw_empty(clicked=True)
                if self.bee:
                    self.draw_mark(bee=True)
                else:
                    self.draw_mark()
            elif self.bee:
                self.draw_empty()
                self.draw_bee()
            else:
                self.draw_empty(clicked=True)
                if self.n_text is not None:
                    self.image.blit(self.n_text, self.n_text_rect)

        elif self.marked:
            self.draw_empty(clicked=True)
            self.draw_mark()

        else:
            self.draw_empty()

    def draw_empty(self, clicked=False):
        color = (200, 200, 200) if clicked else (255, 255, 255)
        self.image.fill(color)
        pygame.draw.rect(self.image, (0, 0, 0), (0, 0, self.w, self.h), 2)

    def draw_bee(self):
        pygame.draw.circle(self.image, (0, 0, 0), (self.w//2, self.h//2), 18)

    def draw_mark(self, bee=False):
        color = (0, 255, 0) if bee else (255, 0, 0)
        pygame.draw.circle(self.image, color, (self.w//2, self.h//2), 18)

    def contains(self, x, y):
        return self.rect.collidepoint(x, y)

    def mark(self):
        self.marked = True
        self.update()

    def unmark(self):
        self.marked = False
        self.update()

    def reveal(self):
        self.revealed = True
        if self.n == 0:
            self.floodfill()
        self.update()

    def floodfill(self):
        for j in [-1, 0, 1]:
            for i in [-1, 0, 1]:
                _r = self.j + j
                _c = self.i + i
                if _r > -1 and _r < ROWS and _c > -1 and _c < COLS:
                    neighbor = self.grid.grid[_r][_c]
                    if not neighbor.revealed and not neighbor.bee:
                        neighbor.reveal()

    def count_bees(self):
        if self.bee:
            self.n = -1
            return
        total = 0
        for j in [-1, 0, 1]:
            for i in [-1, 0, 1]:
                _r = self.j + j
                _c = self.i + i
                if _r > -1 and _r < ROWS and _c > -1 and _c < COLS:
                    try:
                        if self.grid.grid[_r][_c].bee:
                            total += 1
                    except IndexError:
                        print("Index out of bounds")
        self.n = total
        if self.n > 0:
            self.n_text = font.render(str(self.n), True, (0, 0, 0))
            self.n_text_rect = self.n_text.get_rect(center=self.center)
            self.update()

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
                cell = Cell(c, r, self)
                self.grid[r][c] = cell
                self.add(cell)
        self.create_bees()
        for r in range(len(self.grid)):
            for c in range(len(self.grid[r])):
                self.grid[r][c].count_bees()

    def create_bees(self):
        options = []
        for j in range(ROWS):
            for i in range(COLS):
                options.append([i, j])

        for n in range(TOTALBEES):
            index = random.randint(0, len(options)-1)
            _i, _j = options.pop(index)
            self.grid[_j][_i].bee = True
            self.grid[_j][_i].update()
    
    def count_neutral(self):
        total = 0
        for j in range(len(self.grid)):
            for i in range(len(self.grid[j])):
                if self.grid[j][i].revealed or self.grid[j][i].marked:
                    total +=  1
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
            for cell in GRID.sprites():
                if cell.contains(x, y):
                    if cell.marked:
                        return
                    cell.reveal()
                    if cell.bee:
                        GRID.game_over()
        elif pygame.mouse.get_pressed()[2]:
            for cell in GRID.sprites():
                if cell.contains(x, y):
                    if not cell.marked:
                        cell.mark()
                    else:
                        cell.unmark()
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
