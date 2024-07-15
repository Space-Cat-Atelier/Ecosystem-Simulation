import pygame
from random import randint

pygame.init()
clock = pygame.time.Clock()
run = True

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (71, 216, 100)
BLUE = (13, 123, 255)

size = (800, 800)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Ecosystem Simulation')
h = screen.get_height()
w = screen.get_width()

map_text = open('DATA\Map.txt')
map_text = map_text.readlines()
Map = []
for i in range(50):
    Map.append([])
    for j in range(50):
        if map_text[i][j] == '.':
            Map[-1].append(0)
        else:
            Map[-1].append(1)

sprites = pygame.transform.scale(pygame.image.load('DATA\SPRITES\Sprites.png'), [16, 64])
good = sprites.subsurface(pygame.Rect(0, 0, 16, 16))
bad = sprites.subsurface(pygame.Rect(0, 16, 16, 16))
tree = sprites.subsurface(pygame.Rect(0, 32, 16, 16))
bush = sprites.subsurface(pygame.Rect(0, 48, 16, 16))

max_bush_count = 50
max_tree_count = 50
bush_count = 0
tree_count = 0

while tree_count < max_tree_count:
    x, y = randint(0, 49), randint(0, 49)
    if Map[x][y] == 0:
        tree_count += 1
        Map[x][y] = 2

class Good():
    def __init__(self, x, y):
        self.rect = pygame.Rect(x*16, y*16, 16, 16)
        self.sprite = good
        self.hunger = 100
        self.thirst = 100
        self.gender = randint(0, 1)

    def draw(self):
        screen.blit(self.sprite, self.rect)

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    screen.fill(BLACK)
    for i in range(50):
        for j in range(50):
            if Map[i][j] == 0:
                pygame.draw.rect(screen, GREEN, pygame.Rect(j*16, i*16, 16, 16))
            elif Map[i][j] == 1:
                pygame.draw.rect(screen, BLUE, pygame.Rect(j*16, i*16, 16, 16))
            elif Map[i][j] == 2:
                pygame.draw.rect(screen, GREEN, pygame.Rect(j*16, i*16, 16, 16))
                screen.blit(tree, [j*16, i*16])
            elif Map[i][j] == 3:
                pygame.draw.rect(screen, GREEN, pygame.Rect(j*16, i*16, 16, 16))
                screen.blit(bush, [j*16, i*16])

    pygame.display.flip()
    clock.tick(60)
pygame.quit()
