import pygame
from math import*
from collections import deque
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
bushes = []
waters = []
water_surr = []

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
        bushes.append(pygame.Rect(y*16, x*16, 16, 16))

for i in range(50):
    for j in range(50):
        if Map[i][j] == 1:
            waters.append(pygame.Rect(y*16, x*16, 16, 16))

for i in range(50):
    for j in range(50):
        if Map[i][j] == 0 or Map[i][j] == 3:
            grass_rect = pygame.Rect([j*16, i*16], [16, 16])
            range_rect = pygame.Rect(0, 0, 48, 48)
            range_rect.center = grass_rect.center
            if range_rect.collidelist(waters) != -1:
                water_surr.append(grass_rect)

class Good():
    def __init__(self, x, y, gender, color, speed, Range):
        self.rect = pygame.Rect(x*16, y*16, 16, 16)
        self.hunger = 100
        self.thirst = 100
        self.gender = gender
        self.speed = speed
        self.range = pygame.Rect([0, 0], ((Range**2)*16, (Range**2)*16))
        self.range.center = self.rect.center
        self.next_delay = 0
        self.find = 'water'
        self.finding = []
        if gender == 'M':
            self.color = color
        elif gender == 'F':
            self.color = 0

    def draw(self):
        if self.gender == 'M':
            pygame.draw.circle(screen, (self.color, self.color, self.color), self.rect.center, 8)
        elif self.gender == 'F':
            pygame.draw.circle(screen, (self.color, self.color, self.color), self.rect.center, 8, 3)

    def walk(self, trn_x, trn_y):
        self.rect.x += trn_x*16
        self.rect.y += trn_y*16
        self.range.center = self.rect.center

    def random_move(self):
        trn_x = 0
        trn_y = 0
        while True:
            trn_x = randint(-1, 1)
            trn_y = randint(-1, 1)
            pre_x = (self.rect.x//16)+trn_x
            pre_y = (self.rect.y//16)+trn_y
            try:
                if not(trn_y == 0 and trn_x == 0) and (Map[pre_y][pre_x] == 0 or Map[pre_y][pre_x] == 3) and pre_x == abs(pre_x) and pre_y == abs(pre_y):
                    break
            except:
                pass
        self.walk(trn_x, trn_y)
 
    def move(self, trn):
        try:
            pre_x = (self.rect.x//16)+trn[0]
            pre_y = (self.rect.y//16)+trn[1]
            if (Map[pre_y][pre_x] == 0 or Map[pre_y][pre_x] == 3) and pre_x == abs(pre_x) and pre_y == abs(pre_y):
                self.walk(trn[0], trn[1])
            else:
                self.random_move()
        except:
            self.random_move()

    def next_delay_calc(self):
        if pygame.time.get_ticks() >= self.next_delay:
            self.next_delay = pygame.time.get_ticks() + self.speed
            return True
        return False

    def path_find(self, goal):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        start = (self.rect.x // 16, self.rect.y // 16)
        goal = (goal[0]//16, goal[1]//16)
        queue = deque([(start, [])])
        visited = set([start])
        while queue:
            (x, y), path = queue.popleft()
            if (x, y) == goal:
                if path == []:
                    return [(0, 0)]
                return path
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < 50 and 0 <= ny < 50 and (Map[ny][nx] == 0 or Map[ny][nx] == 3) and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append(((nx, ny), path + [(dx, dy)]))
        return [(0, 0)]

    def find_near_bush(self):
        found_bush = []
        for i in bushes:
            if i.colliderect(self.range):
                found_bush.append(i)
        closest = None
        distance = 10000
        for i in found_bush:
            calc_dis = sqrt((i.centerx-self.rect.centerx)**2+(i.centery-self.rect.centery)**2)
            if calc_dis < distance:
                distance = calc_dis
                closest = [i.x, i.y]
        return closest

    def find_near_water(self):
        found_water = []
        for i in water_surr:
            if i.colliderect(self.range):
                water_surr.append(i)
        closest = None
        distance = 10000
        for i in found_water:
            calc_dis = sqrt((i.centerx-self.rect.centerx)**2+(i.centery-self.rect.centery)**2)
            if calc_dis < distance:
                distance = calc_dis
                closest = [i.x, i.y]
        return closest

max_good_count = 1
good_count = 0
good_pos = []
good_guys = []

while good_count < max_good_count:
    x, y = randint(0, 49), randint(0, 49)
    if Map[x][y] == 0 and not((y, x) in good_pos):
        good_count += 1
        good_pos.append((y, x))
        good_guys.append(Good(y, x, 'M', randint(10, 255), 1000, 2))

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
    for i in water_surr:
        pygame.draw.rect(screen, (255, 241, 0), i)

    for guy in good_guys:
        guy.draw()
        if guy.next_delay_calc():
            pass

    pygame.display.flip()
    clock.tick(60)
pygame.quit()
