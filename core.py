import pathlib

import pygame
from settings import *
from player_character import Player_Character
from object_character import Object_character
from support import import_folder, calculate_position, load_object_map, play_music
from pytmx.util_pygame import load_pygame
from tile import Tile

class Core:
    def __init__(self):
        self.level = DEFAULT_LEVEL
        self.player_obj_id = LEVEL_PLAYER_ID_MAP[self.level]

        #get display surface
        self.display_surface = pygame.display.get_surface()
        self.all_sprites = YSortGroup()
        self.obj_map = {}
        self.ground_map = {}
        # load music
        pygame.mixer.init() 
        self._reset(self.level)
        self.main_menu = True
        self.play_win = True

    def _reset(self, level):
        """
        :param player_obj_id: which object is movable py Player
        :param level: which level to load
        """
        self.obj_map = {}
        self.ground_map = {}
        self.level = level
        self.player_obj_id = LEVEL_PLAYER_ID_MAP[self.level]
        self.all_sprites.empty()
        self.load_level(level) 
        self.player_character.current_level = self.level
        self.player_character.combined_objects = 0
        self.player_character.winner = False 
         
         # add music to the level
        play_music(f"level{level}.mp3")

        self.all_sprites.scale(TILE_SIZE, TILE_SIZE)

    def next_level(self):
        max_level = len(LEVEL_PLAYER_ID_MAP) - 1
        #self.level = min(max_level - 1, self.level + 1)
        self.level += 1
        self.player_character.current_level = self.level
        if self.level == max_level:
            self.level = 0
        self._reset(self.level)

    def previous_level(self):
        self.level = max(0, self.level - 1)
        self._reset(self.level)

    def reset_level(self):
        self.player_character.combined_objects = 0
        self.player_character.winner = False
        self._reset(self.level)

    def run(self, dt, event):
        #title screen
        if self.main_menu == True:
            custom_font = pygame.font.Font(None, 66)
            font_rend = custom_font.render('But have you heard of ...?', True, (100, 100, 100))
            font_rect = font_rend.get_rect(topleft = (10, 10))
            pygame.draw.rect(self.display_surface, 'Black', font_rect)
            self.display_surface.blit(font_rend, font_rect)

            font_rend2 = self.player_character.font.render('a game by Martin, Chan and Filip', False, 'White')
            font_rect2 = font_rend2.get_rect(topleft = (10, 120))
            pygame.draw.rect(self.display_surface, 'Black', font_rect2)
            self.display_surface.blit(font_rend2, font_rect2)

            font_rend3 = self.player_character.font.render('Controls: arrow keys, space to continue, R to reset level', False, 'White')
            font_rect3 = font_rend3.get_rect(topleft = (10, 220))
            pygame.draw.rect(self.display_surface, 'Black', font_rect3)
            self.display_surface.blit(font_rend3, font_rect3)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.main_menu = False
            return
        
        if self.player_character.reset_level:
            self.reset_level()
            self.player_character.reset_level = False

        if not self.player_character.font_on_screen and not self.player_character.winner:
            self.display_surface.fill('#' + LEVEL_BACKGROUND[self.level])
            self.all_sprites.custom_draw(self.player_character)
            self.all_sprites.update(dt, event)
        elif self.player_character.font_on_screen and not self.player_character.winner and not self.player_character.is_combined:
            self.all_sprites.custom_draw(self.player_character)            
            font_rend = self.player_character.font.render(f'...{self.player_character.text_message}?', False, 'White')
            font_rect = font_rend.get_rect(center = self.player_character.draw_position)
            pygame.draw.rect(self.display_surface, 'Black', font_rect)
            self.display_surface.blit(font_rend, font_rect)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.player_character.font_on_screen = False
        elif self.player_character.font_on_screen and not self.player_character.winner and self.player_character.is_combined:
            self.all_sprites.custom_draw(self.player_character)
            font_rend = self.player_character.font.render(f'{self.player_character.text_message}', False, 'White')
            font_rect = font_rend.get_rect(center = self.player_character.draw_position)
            pygame.draw.rect(self.display_surface, 'Red', font_rect)
            self.display_surface.blit(font_rend, font_rect)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.player_character.font_on_screen = False
                self.reset_level()
        elif not self.player_character.font_on_screen and self.player_character.winner:
            if self.play_win:
                # play win music
                play_music('win.mp3')
                self.play_win = False
            self.player_character.combined_objects = 0
            self.all_sprites.custom_draw(self.player_character)
            font_rend = self.player_character.font.render(f'...? You tell me ;)', False, 'White')
            font_rect = font_rend.get_rect(center = self.player_character.draw_position)
            pygame.draw.rect(self.display_surface, 'Black', font_rect)
            self.display_surface.blit(font_rend, font_rect)
            keys = pygame.key.get_pressed()

            if keys[pygame.K_SPACE]:
                self.play_win = True
                self.next_level()

                        #check that all combinations are done
                        #resets
                
        #display level number
        font_level_status = self.player_character.font.render('Level: ' + str(self.level + 1) + ' ' + LEVEL_NAMES[self.level], False, 'White')
        font_level_status_rect = font_level_status.get_rect(topleft = (10, 10))
        pygame.draw.rect(self.display_surface, 'Black', font_level_status_rect)
        self.display_surface.blit(font_level_status, font_level_status_rect)

    def load_level(self, level):
        path_to_level = MAPS_FOLDER.joinpath(f"level{level}.tmx")
        path_to_objects = MAPS_FOLDER.joinpath(f"level{level}_Objects.csv")
        tmx_data = load_pygame(path_to_level)
        #tmx_data.objectgroups
        for x,y,surface in tmx_data.get_layer_by_name('Ground').tiles():
            Tile(self.all_sprites, surface, calculate_position(x,y), 'ground', y)
            self.ground_map[(x, y)] = True

        obj_xy_array = load_object_map(path_to_objects)
        for (x, y), id_str in obj_xy_array.items():
            obj_id = int(id_str)
            if obj_id == -1:
                continue
            elif obj_id == self.player_obj_id:
                self.player_character = Player_Character(self.all_sprites, (x, y), 'object', self.obj_map, self.ground_map, y, obj_id)
            else:
                self.obj_map[(x, y)] = Object_character(self.all_sprites, (x, y), obj_id, y, 'object')
    
class YSortGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.display_surface_height = self.display_surface.get_size()[1]
        self.display_surface_width = self.display_surface.get_size()[0]
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):    
        self.offset.x = player.rect.centerx - self.display_surface_width / 2
        self.offset.y = player.rect.centery - self.display_surface_height / 2

        for layer in LAYERS.values():
            for sprite in sorted(self.sprites(), key=lambda sprite: sprite.y_order):
                if sprite.z == layer:
                    self.display_surface.blit(sprite.image,sprite)

    def scale(self, width, height):
        for sprite in self.sprites():
            sprite.image = pygame.transform.scale2x(sprite.image)
            sprite.image = pygame.transform.smoothscale(sprite.image, (width, height))
            # sprite.image = pygame.transform.rotozoom(sprite.image, 0, 1.5)