import pygame
class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size, multiply):
        super().__init__()
        self.image = pygame.Surface((size*multiply, size))
        self.image.fill('grey')
        self.rect = self.image.get_rect(topleft = pos)

    def update(self, y_shift):
        self.rect.y += y_shift