import pygame
from pygame.key import name
from enum import Enum

class Direction(Enum):
    Left = pygame.math.Vector2(-1, 0)
    Right = pygame.math.Vector2(1, 0)
    Jump = pygame.math.Vector2(0, -8)
    Nothing = pygame.math.Vector2(0, 0)


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
        
    def get_input(self, jump_bool, action):
        keys = pygame.key.get_pressed() 

        if keys[pygame.K_d]:
            self.direction = Direction.Right
        elif keys[pygame.K_a]:
            self.direction = Direction.Left
        else: 
            self.direction = Direction.Nothing

        if keys[pygame.K_SPACE] and jump_bool:
            self.direction = Direction.Jump

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed

    def update(self, jump_bool, action):
        self.get_input(jump_bool, action)
        self.rect.x += self.direction.x * self.speed
        self.apply_gravity()
        