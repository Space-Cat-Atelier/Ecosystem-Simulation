import pygame

pygame.init()
clock = pygame.time.Clock()
run = True

BLACK = (20, 20, 20)
WHITE = (240, 240, 240)
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

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    screen.fill(BLACK)
    for i in range(50):
        for j in range(50):
            if Map[i][j]:
                pygame.draw.rect(screen, BLUE, pygame.Rect(j*16, i*16, 16, 16))
            else:
                pygame.draw.rect(screen, GREEN, pygame.Rect(j*16, i*16, 16, 16))

    pygame.display.flip()
    clock.tick(60)
pygame.quit()
