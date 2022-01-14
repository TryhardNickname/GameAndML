import pygame
from pygame.key import name
from enum import Enum
import numpy as np

class Direction(Enum):
    Left = pygame.math.Vector2(-1, 0)
    Right = pygame.math.Vector2(1, 0)
    Jump = pygame.math.Vector2(0, -8)

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((32, 32))
        self.image.fill('red')
        self.rect = self.image.get_rect(topleft = pos)  
        self.speed = 8
        self.gravity = 0.2
        self.jump_speed = -8
        self.jump_clock = pygame.time.Clock()
        self.direction = pygame.math.Vector2(0, 0)
        
    def get_input(self, jump_bool, action, player_on_rect):
        keys = pygame.key.get_pressed() 
        if action != None:
            if np.array_equal(action, [1,0,0]):
                self.direction.x = 1
            elif np.array_equal(action, [0,1,0]):
                self.direction.x = -1
            elif np.array_equal(action, [0,0,1]) and jump_bool and player_on_rect:
                self.direction.y = self.jump_speed
                return True

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed

    def update(self, jump_bool, action, player_on_rect):
        jump_or_not = self.get_input(jump_bool, action, player_on_rect)
        self.rect.x += self.direction.x * self.speed
        self.apply_gravity()
        return jump_or_not
    
class PlayerHuman(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((32, 32))
        self.image.fill('red')
        self.rect = self.image.get_rect(topleft = pos)

        self.direction = pygame.math.Vector2(0,0)
        self.speed = 8
        self.gravity = 0.2
        self.jump_speed = -8
        self.jump_clock = pygame.time.Clock()

    def get_input(self, jump_bool, player_on_rect):
        keys = pygame.key.get_pressed() 

        if keys[pygame.K_d]:
            self.direction.x = 1
        elif keys[pygame.K_a]:
            self.direction.x = -1
        else: 
            self.direction.x = 0

        if keys[pygame.K_SPACE] and jump_bool and player_on_rect:
            self.jump()
            return True



    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed

    def update(self, jump_bool, player_on_rect):
        jump_or_not = self.get_input(jump_bool, player_on_rect)
        self.rect.x += self.direction.x * self.speed
        self.apply_gravity()
        return jump_or_not
        