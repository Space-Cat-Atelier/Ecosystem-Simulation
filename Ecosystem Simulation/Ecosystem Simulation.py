import pygame
from random import randint, choice

pygame.init()
clock = pygame.time.Clock()
run = True

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (71, 216, 100)
DGREEN = (0, 125, 0)
BLUE = (13, 123, 255)
BROWN = (185, 122, 87)

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

max_bush_count = 50 
max_tree_count = 75
bush_count = 0
tree_count = 0

while tree_count < max_tree_count:
    x, y = randint(0, 49), randint(0, 49)
    if Map[x][y] == 0:
        tree_count += 1
        Map[x][y] = 2

while bush_count < max_bush_count:
    x, y = randint(0, 49), randint(0, 49)
    if Map[x][y] == 0:
        bush_count += 1
        Map[x][y] = 3

class Good():
    def __init__(self, x, y, gender, color, speed):
        self.rect = pygame.Rect(x*16, y*16, 16, 16)
        self.hunger = 100
        self.thirst = 100
        self.gender = gender
        self.speed = speed
        if gender == 'M':
            self.color = color
        elif gender == 'F':
            self.color = 0

    def draw(self):
        if self.gender == 'M':
            pygame.draw.circle(screen, (self.color, self.color, self.color), self.rect.center, 8)
        elif self.gender == 'F':
            pygame.draw.circle(screen, (self.color, self.color, self.color), self.rect.center, 8, 3)

    def move(self, trn_x, trn_y):
        self.rect.x += trn_x*16
        self.rect.y += trn_y*16

    def move_random(self):
        trn_x = 0
        trn_y = 0
        while trn_x == trn_y == 0:
            trn_x = randint(-1, 1)
            trn_y = randint(-1, 1)
        self.rect.x += trn_x*16
        self.rect.y += trn_y*16

max_good_count = 1
good_count = 0

good_guys = []

while good_count < max_good_count:
    x, y = randint(0, 49), randint(0, 49)
    if Map[x][y] == 0:
        good_count += 1
        good_guys.append(Good(y, x, 'M', randint(10, 255), 1))

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
                pygame.draw.polygon(screen, DGREEN, [(j*16, i*16+16), (j*16+8, i*16), (j*16+16, i*16+16)])
            elif Map[i][j] == 3:
                pygame.draw.rect(screen, GREEN, pygame.Rect(j*16, i*16, 16, 16))
                pygame.draw.line(screen, DGREEN, [j*16+8, i*16+16], [j*16+8, i*16], 2)
                pygame.draw.line(screen, DGREEN, [j*16+8, i*16+16], [j*16, i*16], 2)
                pygame.draw.line(screen, DGREEN, [j*16+8, i*16+16], [j*16+16, i*16], 2)

    for guy in good_guys:
        guy.draw()

    pygame.display.flip()
    clock.tick(60)
pygame.quit()
