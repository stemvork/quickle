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


class Tile(Sprite):
    def __init__(self, pos, colshape):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.rect  = self.image.get_rect()
        self.pos = pos
        self.colshape = colshape

        _col, _shp = colshape
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
        self.move(pos)

    def move(self, pos):
        self.pos = pos
        self.rect.topleft = pos[0]*50, pos[1]*50



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

bag = Bag()


class Rack(Group):
    def __init__(self):
        super().__init__()
        self.add(bag.take(6))
        self.pos = (3, 0)

    def draw(self, _screen):
        for index, sprite in enumerate(self.sprites()):
            sprite.move((self.pos[0] + index, self.pos[1]))
            _screen.blit(sprite.image, sprite.rect)


r = Rack()
s = Rack()
s.pos = (s.pos[0], 11)


class Board(Group):
    def __init__(self):
        super().__init__()


b = Board()


def proper_exit():
    pygame.quit()
    sys.exit()


def handle_keydown(args):
    key, _ = args
    if key == pygame.K_ESCAPE:
        proper_exit()
    elif key == pygame.K_SPACE:
        pos = random.randint(0, 6), random.randint(0, 6)
        tile = bag.take()
        tile.move(pos)
        print(tile.colshape)
        b.add(tile)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            proper_exit()
        elif event.type == pygame.KEYDOWN:
            args = event.key, None 
            handle_keydown(args)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            args = None
            handle_mousedown(args)

    screen.fill((80, 70, 90))
    b.draw(screen)
    r.draw(screen)
    s.draw(screen)

    bag_size_text = font.render(bag.size(), True, (150, 150, 150))
    bag_size_text_rect = bag_size_text.get_rect(center=(300, 300))
    screen.blit(bag_size_text, bag_size_text_rect)

    pygame.display.flip()
    clock.tick(60)
