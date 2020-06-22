import pygame
import random
import sys
import math
from pygame.sprite import Sprite, Group


pygame.init()
font = pygame.font.SysFont("Arial", 30)


clock = pygame.time.Clock()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption('Quickle')


COLORS = [pygame.Color(c) for c in 
            ["#ff0000", "#00ff00", '#0000ff',
             '#cccc00', '#00cccc', '#cc00cc']]


def agree(t1, t2):
    if t1.colshape[0] == t2.colshape[0]:
        return True
    elif t1.colshape[1] == t2.colshape[1]:
        return True
    return False

class Tile(Sprite):
    def __init__(self, pos, colshape):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.rect  = self.image.get_rect()
        self.pos = pos
        self.colshape = colshape
        self.draw_shape()
        self.move(pos)

    def move(self, pos):
        self.pos = pos
        self.rect.topleft = pos[0]*50, pos[1]*50
    
    def draw_shape(self):
        _col, _shp = self.colshape
        color = COLORS[_col]
        center = (25, 25)
        cx     = 25
        radius = 18
        offset = cx - 18
        self.image.fill((0, 0, 0))
        if _shp == 0:
            pygame.draw.circle(self.image, color, center, radius)
        elif _shp == 1:
            _offset = offset + 2
            _radius = radius - 2
            pygame.draw.rect(self.image, color, (_offset, _offset, 2*_radius, 2*_radius))
        elif _shp == 2:
            _offset = offset-2
            _pts = [(cx, _offset), (_offset, cx), (cx, 50-_offset), (50-_offset, cx)]
            pygame.draw.polygon(self.image, color, _pts)
        elif _shp == 3:
            _cx = 50 // 4 + 1
            _r  = 8
            _pts = [(cx, _cx), (_cx, cx), (cx, 50-_cx), (50-_cx, cx)]
            for pt in _pts:
                pygame.draw.circle(self.image, color, pt, _r)
            pygame.draw.circle(self.image, color, center, _r)
        elif _shp == 4:
            _pts = [(offset, offset), (cx+offset//2, cx-offset//2), (50-offset, 50-offset), (cx-offset//2, cx+offset//2)]
            pygame.draw.polygon(self.image, color, _pts)
            _pts = [(offset, 50-offset), (cx+offset//2, cx+offset//2), (50-offset, offset), (cx-offset//2, cx-offset//2)]
            pygame.draw.polygon(self.image, color, _pts)
        elif _shp == 5:
            _a = 8
            _r = radius
            _pts = []
            for a in range(_a):
                _pts.append((cx + _r * math.cos(a * 3 * 45 * math.pi / 180),
                    cx + _r * math.sin(a * 3 * 45 * math.pi / 180)))
            pygame.draw.polygon(self.image, color, _pts)
            pygame.draw.circle(self.image, color, center, radius//2+2)
    def has_neighbor_in(self, board):
        if len(board.sprites()) == 0:
            return True
        elif len(self.get_neighs(board))>0:
            return True
        return False
    def get_neighs(self, board):
        neighs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        tiles  = []
        for sprite in board.sprites():
            sx, sy = self.pos
            ox, oy = sprite.pos
            delta = ox-sx, oy-sy
            if delta in neighs:
                tiles.append(sprite)
        return tiles
    def attach_legal(self, board):
        neighs = self.get_neighs(board)
        if len(neighs) == 0:
            return True
        for n in neighs:
            return agree(self, n)


class Bag:
    def __init__(self):
        self.tiles = []
        for i in range(6):
            for j in range(6):
                for k in range(3):
                    tile = Tile((0, 0), (i, j))
                    self.tiles.append(tile)
        random.shuffle(self.tiles)
    
    def take(self, n=1):
        if len(self.tiles) > 0:
            if n > 1:
                tiles = []
                for i in range(n):
                    tiles.append(self.tiles.pop())
                return tiles
            else:
                return self.tiles.pop()

    def size(self):
        return str(len(self.tiles))


class Rack(Group):
    def __init__(self, bag, ypos=None):
        super().__init__()
        self.add(bag.take(6))
        if ypos:
            self.pos = (3, ypos)
        else:
            self.pos = (3, 0)

    def draw(self, _screen):
        for index, sprite in enumerate(self.sprites()):
            sprite.move((self.pos[0] + index, self.pos[1]))
            _screen.blit(sprite.image, sprite.rect)
            
    def take(self, pos):
        kpos = pos * 50 + 5 + self.pos[0] * 50, 5 + self.pos[1] * 50
        for sprite in self.sprites():
            if sprite.rect.collidepoint(kpos):
                tile = sprite
                self.remove(sprite)
                return tile


class Board(Group):
    def __init__(self):
        super().__init__()


class Game:
    def __init__(self):
        self.board = Board()
        self.bag = Bag()
        self.racks = []
        self.racks.append(Rack(self.bag))
        self.racks.append(Rack(self.bag, 11))
        self.selected = None
        self.player = 0
    
    def next(self):
        self.player = self.player + 1 if self.player < len(self.racks)-1 else 0


g = Game()


def proper_exit():
    pygame.quit()
    sys.exit()

def handle_keydown(args):
    key, g = args
    if key == pygame.K_ESCAPE:
        proper_exit()
    elif key == pygame.K_SPACE:
        pos = random.randint(0, 6), random.randint(0, 6)
        tile = g.bag.take()
        tile.move(pos)
        g.board.add(tile)
    elif key in range(pygame.K_1, pygame.K_1+6):
        g.selected = g.racks[g.player].take(key - pygame.K_1)
    elif key == pygame.K_RETURN:
        g.next()
    return g

def handle_mousedown(args):
    g = args
    if g.selected is not None:
        # if g.selected.has_neighbor_in(g.board):
        if g.selected.attach_legal(g.board):
            g.board.add(g.selected)
            print(len(g.board.sprites()))
            g.selected = None
    return g

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            proper_exit()
        elif event.type == pygame.KEYDOWN:
            args = event.key, g
            g = handle_keydown(args)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            args = g
            g = handle_mousedown(args)

    screen.fill((80, 70, 90))
    g.board.draw(screen)
    for r in g.racks:
        r.draw(screen)

    if g.selected:
        mousepos = pygame.mouse.get_pos()
        mx, my   = mousepos[0] // 50, mousepos[1] // 50
        g.selected.move((mx, my))
        screen.blit(g.selected.image, g.selected.rect)

    bag_size_text = font.render(g.bag.size(), True, (150, 150, 150))
    bag_size_text_rect = bag_size_text.get_rect(center=(300, 300))
    screen.blit(bag_size_text, bag_size_text_rect)

    pygame.display.flip()
    clock.tick(60)
