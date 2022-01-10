import pygame, sys, time
from settings import *
from level import Level

pygame.init()

screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
level = Level(screen)

timer = False
delay = 0.05
jump_bool = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                x = time.time()
                timer = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                timer = False
                jump_bool = True
    
    if timer: 
        if time.time() - x >= delay:
            jump_bool = False
    
    screen.fill('black')
    if level.run(jump_bool) == False:
        break

    pygame.display.update()
    clock.tick(60)

