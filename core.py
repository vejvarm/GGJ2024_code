import pathlib

import pygame
from settings import *
from player_character import Player_Character
from object_character import Object_character
from support import import_folder, calculate_position, load_object_map, play_music
from pytmx.util_pygame import load_pygame
from tile import Tile
from sys import exit
import time


class Core:
    def __init__(self):
        self.level = DEFAULT_LEVEL
        self.max_level = len(LEVEL_PLAYER_ID_MAP) - 1
        self.player_obj_id = LEVEL_PLAYER_ID_MAP[self.level]

        # tile size = is level big and zoomed out
        self.current_tile_size = TILE_SIZE

        # get display surface
        self.display_surface = pygame.display.get_surface()
        self.all_sprites = YSortGroup()
        self.obj_map = {}
        self.ground_map = {}
        # load music
        pygame.mixer.init()
        self._reset(self.level)
        self.main_menu = True
        self.end_screen = False
        self.play_win = True

    def _reset(self, level):
        """
        :param player_obj_id: which object is movable py Player
        :param level: which level to load
        """
        self.obj_map = {}
        self.ground_map = {}
        self.level = level
        # zoom out larger levels
        if self.level in LEVEL_ZOOMED_OUT:
            self.current_tile_size = TILE_SIZE_BIG_LEVEL

        self.player_obj_id = LEVEL_PLAYER_ID_MAP[self.level]
        self.all_sprites.empty()
        self.load_level(level)
        self.player_character.current_level = self.level
        self.player_character.combined_objects = 0
        self.player_character.winner = False

        # add music to the level
        play_music(f"level{level}.mp3")

        self.all_sprites.scale(self.current_tile_size, self.current_tile_size)

    def next_level(self):
        self.level += 1
        self.player_character.current_level = self.level
        if self.level > self.max_level:
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
        # title screen
        if self.main_menu == True:
            self.display_title_screen()
            return

        # reseting level
        if self.player_character.reset_level:
            self.reset_level()
            self.player_character.reset_level = False
        # regular gameplay - moving around
        elif not self.player_character.font_on_screen and not self.player_character.winner:
            self.display_surface.fill('#' + LEVEL_BACKGROUND[self.level])
            self.all_sprites.custom_draw(self.player_character)
            self.all_sprites.update(dt, event)
        # combined 2 objects
        elif not self.player_character.winner and not self.player_character.is_combined:
            self.all_sprites.custom_draw(self.player_character)
            font_rend = self.player_character.font.render(f'...{self.player_character.text_message}?', False, 'White')
            font_rect = font_rend.get_rect(center=self.player_character.draw_position)
            pygame.draw.rect(self.display_surface, 'Black', font_rect)
            self.display_surface.blit(font_rend, font_rect)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.player_character.font_on_screen = False
                # hide objects
                for o in self.player_character.obj_to_hide:
                    self.all_sprites.remove(o)
                    # pop from object map
                    if (o.grid_position['x'], o.grid_position['y']) in self.player_character.object_map:
                        self.player_character.object_map.pop((o.grid_position['x'], o.grid_position['y']))
                self.player_character.obj_to_hide = []
        # combined self and didn't win
        elif not self.player_character.winner and self.player_character.is_combined:
            self.all_sprites.custom_draw(self.player_character)
            font_rend = self.player_character.font.render(f'{self.player_character.text_message}', False, 'White')
            font_rect = font_rend.get_rect(center=self.player_character.draw_position)
            pygame.draw.rect(self.display_surface, 'Red', font_rect)
            self.display_surface.blit(font_rend, font_rect)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.player_character.font_on_screen = False
                self.reset_level()
        # combined self and won -> next level
        elif self.player_character.winner:
            if self.play_win:
                # TODO update
                # play win music
                if (self.level == 4 or self.level == 3) and self.player_character.player_won_by != '':
                    # two different win conditions and music
                    play_music('win' + str(self.level) + str(self.player_character.player_won_by) + '.mp3')
                else:
                    play_music('win' + str(self.level) + '.mp3')
                self.play_win = False
            self.all_sprites.custom_draw(self.player_character)
            font_rend = self.player_character.font.render(f'...? You tell me ;) LEVEL COMPLETE!', False, 'White')
            font_rect = font_rend.get_rect(center=self.player_character.draw_position)
            pygame.draw.rect(self.display_surface, 'Black', font_rect)
            self.display_surface.blit(font_rend, font_rect)
            keys = pygame.key.get_pressed()

            if keys[pygame.K_SPACE]:
                self.player_character.combined_objects = 0
                self.play_win = True
                self.player_character.font_on_screen = False
                if self.level < self.max_level:
                    self.next_level()
                else:
                    self.end_screen = True

        self.display_hud()

    def load_level(self, level):
        path_to_level = MAPS_FOLDER.joinpath(f"level{level}.tmx")
        path_to_objects = MAPS_FOLDER.joinpath(f"level{level}_Objects.csv")
        path_to_ground = MAPS_FOLDER.joinpath(f"level{level}_Ground.csv")
        tmx_data = load_pygame(path_to_level)
        obj_xy_array = load_object_map(path_to_objects)
        grnd_xy_array = load_object_map(path_to_ground)
        # object map with object ids
        for (x, y), id_str in obj_xy_array.items():
            obj_id = int(id_str)
            if obj_id == -1:
                continue
            elif obj_id == self.player_obj_id:
                self.player_character = Player_Character(self.all_sprites, (x, y), 'object', self.obj_map,
                                                         self.ground_map, self.all_sprites, y, obj_id,
                                                         self.current_tile_size)
            else:
                self.obj_map[(x, y)] = Object_character(self.all_sprites, (x, y), obj_id, y + x / 100, 'object',
                                                        self.current_tile_size)
        # load tile ids from csv
        for (x, y), id_str in grnd_xy_array.items():
            self.ground_map[(x, y)] = int(id_str)  # tile id
        # ground map with tile ids
        for x, y, surface in tmx_data.get_layer_by_name('Ground').tiles():
            Tile(self.all_sprites, surface, calculate_position(x, y, self.current_tile_size), 'ground', y)

    def display_hud(self):

        # display level number
        font_level_status = self.player_character.font.render(
            'Level: ' + str(self.level + 1) + ' ' + LEVEL_NAMES[self.level], False, 'White')
        font_level_status_rect = font_level_status.get_rect(topleft=(10, 10))
        # bg under text:
        # pygame.draw.rect(self.display_surface, 'Black', font_level_status_rect)
        self.display_surface.blit(font_level_status, font_level_status_rect)

        # display number of combined objects
        font_rend = self.player_character.font.render(
            'Objects combined: ' + str(self.player_character.combined_objects) + '/' + str(
                LEVEL_WIN_CONDITION[self.level]), False, 'White')
        font_rect = font_rend.get_rect(topleft=(10, 40))
        # bg under text:
        # pygame.draw.rect(self.display_surface, 'Black', font_rect)
        self.display_surface.blit(font_rend, font_rect)

        # display control keys
        image = pygame.image.load(SCREENS_FOLDER.joinpath('controls.png'))
        self.display_surface.blit(image, (DISPLAY_WIDTH - image.get_width(), 10))

        '''
        font_rend = self.player_character.font_big.render('A', False, 'black')
        font_rect = font_rend.get_rect(topleft = (CONTROLS_TEXT_POS[0], CONTROLS_TEXT_POS[1] + CONTROLS_TEXT_POS[1] / 2))
        self.display_surface.blit(font_rend, font_rect)

        font_rend = self.player_character.font_big.render('W', False, 'black')
        font_rect = font_rend.get_rect(topleft = (DISPLAY_WIDTH - CONTROLS_TEXT_POS[0], CONTROLS_TEXT_POS[1] + CONTROLS_TEXT_POS[1] / 2))
        self.display_surface.blit(font_rend, font_rect)

        font_rend = self.player_character.font_big.render('S', False, 'black')
        font_rect = font_rend.get_rect(topleft = (DISPLAY_WIDTH - CONTROLS_TEXT_POS[0], DISPLAY_HEIGHT - CONTROLS_TEXT_POS[1]))
        self.display_surface.blit(font_rend, font_rect)

        font_rend = self.player_character.font_big.render('D', False, 'black')
        font_rect = font_rend.get_rect(topleft = (CONTROLS_TEXT_POS[0], DISPLAY_HEIGHT - CONTROLS_TEXT_POS[1]))
        self.display_surface.blit(font_rend, font_rect)
        '''

    def display_title_screen(self):
        '''
        font_rend = self.player_character.font_big.render('But have you heard of ...?', True, (100, 100, 100))
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
        '''
        image = pygame.image.load(SCREENS_FOLDER.joinpath('title_screen.jpg'))
        self.display_surface.blit(image, (0, 0))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.main_menu = False

    def display_end_screen(self):
        image = pygame.image.load(SCREENS_FOLDER.joinpath('end_screen.jpg'))
        self.display_surface.blit(image, (0, 0))
        play_music('credits.mp3')


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
                    if sprite.type[0] not in OBJECTS_INVISIBLE:
                        self.display_surface.blit(sprite.image, sprite)

    def scale(self, width, height):
        for sprite in self.sprites():
            sprite.image = pygame.transform.scale2x(sprite.image)
            sprite.image = pygame.transform.smoothscale(sprite.image, (width, height))
            # sprite.image = pygame.transform.rotozoom(sprite.image, 0, 1.5)