import sys
import pygame
from settings import *
from main import *
from agent import train

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
font = pygame.font.SysFont(None, 20)


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def main_menu():
    click = False
    while True:
        screen.fill('black')

        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(50, 100, 200, 50)
        button_2 = pygame.Rect(50, 200, 200, 50)

        if button_1.collidepoint((mx, my)):
            if click:
                game_human = GameHuman()
                game_human.runGame()
                
        if button_2.collidepoint((mx, my)):
            if click:
                train()

        pygame.draw.rect(screen, (255, 0, 0), button_1)
        pygame.draw.rect(screen, (255, 0, 0), button_2)
        draw_text("You play", font, (255, 255, 255), screen, button_1.x, button_1.y)
        draw_text("Machine learning play", font, (255, 255, 255), screen, button_2.x, button_2.y)

        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True    

        pygame.display.update()

main_menu()