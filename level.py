import pygame
from pygame import rect
from player import *
from tiles import Tile
from settings import tile_size
import random 

class Level:
    def __init__(self, surface):

        # level setup
        self.display_surface = surface
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.reset()

    def setup_level(self):
        self.player.empty()
        self.tiles.empty()
        self.player.add(Player((250, 500)))
        self.tiles.add(Tile((250, 550), tile_size, 4))

    def reset(self):
        self.setup_level()

        self.world_shift = 2
        self.jump_percentage = 0.5
        self.jump_reach = 250
        self.score = 0
        self.score_clock = pygame.time.Clock()
        self.time_elapsed_since_last_increment = 0
        self.difficulty_bool = True
        self.tile_size_change = 4

        self.frame_iteration = 0
        self.player_on_rect = False

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    self.player_on_rect = True

    def spawn_tiles(self):
        last_tile = Tile((0,0), tile_size, 4)
        tile_count = 0
        for tile in self.tiles:
            if tile.rect.y > 800:
                tile.kill()

            last_tile = tile
            tile_count += 1

        if (tile_count < 8):
            self.tiles.add(Tile((random.randint(0, 372), last_tile.rect.y - self.jump_reach*self.jump_percentage), tile_size, self.tile_size_change))          
    
    def closest_tile(self):
        counter = 0

        for tile in self.tiles:
            if tile.rect.y < 800 and counter == 0:
                nearest_rect = tile
                counter += 1
            
        return nearest_rect.rect
    
    def check_death(self, pt=None):
        if pt is None:
            pt = self.player.sprite.rect
            if pt.y > 800:
                return True
            else:
                return False


    def score_increment(self):
        if self.check_death():           
            return False
        else:
            self.score += 10
            return True
            

    def increase_difficulty(self, score):
        if score == 200 and self.difficulty_bool:
            self.jump_percentage *= 1.4
            self.world_shift *= 1.3
            self.tile_size_change = 3
            self.difficulty_bool = False           
        if score == 400 and self.difficulty_bool:
            self.jump_percentage *= 1.4
            self.world_shift *= 1.2
            self.tile_size_change = 2
            self.difficulty_bool = False       
        if score == 600 and self.difficulty_bool:
            self.jump_percentage *= 1.4
            self.world_shift *= 1.2
            self.tile_size_change = 1
            self.difficulty_bool = False       


    def run(self, jump_bool, action):
        reward = 0
        game_over = False

        self.frame_iteration += 1
        clock1 = self.score_clock.tick()
        self.time_elapsed_since_last_increment += clock1       
        
        #longer time between increments
        if self.time_elapsed_since_last_increment > 600:
            self.score_increment()
            self.time_elapsed_since_last_increment = 0
            self.difficulty_bool = True

        self.spawn_tiles()          
        self.increase_difficulty(self.score)

        # level tiles
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        #self.scroll_y()

        # player
        player_jumped = self.player.update(jump_bool, action, self.player_on_rect)
        self.player_on_rect = False
        self.vertical_movement_collision()
        self.player.draw(self.display_surface)

        if self.check_death():
            reward = -10
            game_over = True
            return reward, game_over, self.score
        else:
            reward = 10
            return reward, game_over, self.score
            

             
            

