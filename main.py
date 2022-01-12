import pygame, sys, time
from settings import *
from level import Level

class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()
        self.level = Level(self.screen)

        self.timer = False
        self.delay = 0.05
        self.jump_bool = True

    def runGame(self): 
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        x = time.time()
                        self.timer = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        self.timer = False
                        self.jump_bool = True
            
            if self.timer: 
                if time.time() - x >= self.delay:
                    self.jump_bool = False
            
            self.screen.fill('black')
            self.level.run(self.jump_bool)                

            pygame.display.update()
            self.clock.tick(60)


game = Game()
game.runGame()