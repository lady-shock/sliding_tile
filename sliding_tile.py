import pygame
from pygame.locals import *
import pygwidgets
import random
from settings import *

pygame.init()
screen = pygame.display.set_mode((450, 600))
pygame.display.set_caption("Sliding Tile")
clock = pygame.Clock()
full_surf = pygame.Surface((300, 400))
full_surf.fill('#303030')
full_image = pygame.image.load("../assets/electricity.png").convert()
rows = 4
cols = 3
BORDER = 'black'
SPEED = 10

class Tile(pygame.Surface):
    def __init__(self, ID, img, crop, dim=(100, 100)):
        super().__init__(dim)
        self.ID = ID
        self.cell = ID
        self.rect = self.get_rect()
        self.sliding = False
        self.slide_count = 0
        self.slide_vector = ((0,0))
        self.blit(img, (0,0), (*crop, *dim))
        pygame.draw.line(self, BORDER, (0,0), (99,0), width = 1)
        pygame.draw.line(self, BORDER, (99, 0), (99, 99), width=1)
        pygame.draw.line(self, BORDER, (99,99), (0,99), width=1)
        pygame.draw.line(self, BORDER, (0, 99), (0, 0), width=1)

    def update(self):
        if self.sliding:
            self.rect.x += (self.slide_vector[0]) * SPEED
            self.rect.y += (self.slide_vector[1]) * SPEED
            self.slide_count += 1
            if self.slide_count >= 100/SPEED:
                self.slide_count = 0
                self.sliding = False
    def slide(self):
        for cell in neighbors[self.cell]:
            if cells[cell].tile == None:
                target_cell = cell
                self.sliding = True
                cells[self.cell].tile = None
                cells[target_cell].tile = self
                match (self.cell - target_cell):
                    case 3:
                        direction = 'up'
                    case -3:
                        direction = 'down'
                    case 1:
                        direction = 'left'
                    case -1:
                        direction = 'right'
                self.slide_vector = directions[direction]
                self.cell = target_cell
                return 1

class Cell():
    def __init__(self, pos, tile=None):
        self.pos = pos
        self.tile = tile

tiles = []
cells = []
for n in range(rows * cols):
    tiles.append(Tile(n, full_image, (100*(n%3), 100*(n//3))))
    cells.append(Cell((100*(n%cols), 100*(n//cols))))
tiles.pop(0)
random.shuffle(tiles)
for index, tile in enumerate(tiles):
    tile.rect.x, tile.rect.y = cells[index].pos
    cells[index].tile = tile
    tile.cell = index

running = True
while running:
    screen.fill('black')
    full_surf.fill('#303030')

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            pos= pygame.mouse.get_pos()
            for tile in tiles:
                rel_to_window = tile.rect.move((75, 75))
                if rel_to_window.collidepoint(pos):
                    tile.slide()

    for tile in tiles:
        full_surf.blit(tile, tile.rect)
        tile.update()
    screen.blit(full_surf, (75, 75))
    pygame.display.flip()
    clock.tick(30)