import pygame, sys, time
from settings import *
from level import Level, LevelHuman

class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()
        self.level = Level(self.screen)

        self.timer = False
        self.delay = 0.05
        self.jump_bool = True

    def runGame(self, action): 
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
                        #self.jump_bool = True
            
            if self.timer: 
                if time.time() - x >= self.delay:
                    pass
                    #self.jump_bool = False
            
            self.screen.fill('black')
            reward, game_over, score = self.level.run(self.jump_bool, action)                

            pygame.display.update()
            self.clock.tick(60)

            return reward, game_over, score

class GameHuman:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()
        self.level = LevelHuman(self.screen)

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
                        #jump_bool = True
            
            if self.timer: 
                if time.time() - x >= self.delay:
                    pass
                    #jump_bool = False
            
            self.screen.fill('black')
            if self.level.run(self.jump_bool) == False:
                break

            pygame.display.update()
            self.clock.tick(60)
