import pygame
import pathlib
import time
from settings import *
from stopwatch import Stopwatch
from debug import debug
from support import calculate_position
from collections import namedtuple


class Player_Character(pygame.sprite.Sprite):
    def __init__(self, groups, pos: tuple[int, int], z, object_map, ground_map, y_order, obj_class_id: int):
        super().__init__(groups)
        path_to_image = OBJECTS_FOLDER.joinpath(f"{obj_class_id}.png")
        self.image = pygame.image.load(path_to_image)
        self.type = OBJECTS[obj_class_id]
        self.z = LAYERS[z]
        self.grid_position = {'x': pos[0], 'y': pos[0]}
        self.draw_position = self.update_player_position()
        self.object_map = object_map
        self.ground_map = ground_map
        self.y_order = y_order
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(None, 30)
        self.font_on_screen = False
        self.winner = False
        self.combined_objects = 0
        self.current_level = 0
        self.is_combined = False
        self.text_message = ''
        self.loser = False

    def update_player_position(self):
        position = calculate_position(self.grid_position['x'], self.grid_position['y'])
        self.rect = self.image.get_rect(topleft=position)
        self.y_order = self.grid_position['y']
        return position

    def get_input(self, event):
        # movement, tool use, and tool switch
        # if not self.stopwatches['any use'].active:
        dx = 0
        dy = 0
        move = False
        if event is not None and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                dx += 1
                move = True
            if event.key == pygame.K_LEFT:
                dx -= 1
                move = True
                # self.move_player(self.grid_position, (self.grid_position['x']-1, self.grid_position['y']))
            if event.key == pygame.K_UP:
                dy -= 1
                move = True
            if event.key == pygame.K_DOWN:
                dy += 1
                move = True

        if move:
            self.move_player(self.grid_position, (self.grid_position['x'] + dx, self.grid_position['y'] + dy))

    def move_player(self, from_position, to_position):
        from_position = (from_position['x'], from_position['y'])
        # check level exists = can't go outside of level
        if to_position in self.ground_map.keys():
            # check object exists where we're moving
            if to_position in self.object_map.keys():
                self.winner = self.level_win_conditions_met()
                # check if object combines with player
                obj_a = self.type[0]
                obj_b = self.object_map[to_position].type[0]
                if self.objects_can_be_combined(obj_a, obj_b):
                    # COMBINE PLAYER AND OBJECT!
                    self.combined_objects += 1
                    self.grid_position = {'x': to_position[0], 'y': to_position[1]}
                    self.draw_position = self.update_player_position()
                    # draw player on top of object
                    self.is_combined = True
                    self.y_order = 9001
                    self.draw_position = (self.draw_position[0], self.draw_position[1] - TILE_SIZE / 4)
                    self.rect = self.image.get_rect(topleft=self.draw_position)
                    return
                # check object can be moved = type[1] == "1"
                if self.object_map[to_position].type[1] == 1:
                    # check if object can be moved - is there edge of level
                    pos_direction_vector = (to_position[0] - from_position[0], to_position[1] - from_position[1])
                    beyond_object_pos = (
                    to_position[0] + pos_direction_vector[0], to_position[1] + pos_direction_vector[1])
                    if beyond_object_pos not in self.ground_map.keys():
                        # cant move, no map
                        return
                        # check if object can be moved - is there another object
                    if beyond_object_pos in self.object_map.keys():
                        # or another object then check if it can be combined
                        obj_a = self.object_map[beyond_object_pos].type[0]
                        obj_b = self.object_map[to_position].type[0]
                        if self.objects_can_be_combined(obj_a, obj_b):
                            # COMBINE!
                            if not self.is_combined:
                                # Combine normal stuff
                                self.combined_objects += 1
                                self.grid_position = {'x': to_position[0], 'y': to_position[1]}
                                self.draw_position = self.update_player_position()
                                # draw objects on top of each other
                                self.update_object_position(to_position, from_position, True, False)
                                # dray the on top over the one on the bottom
                                self.object_map[beyond_object_pos].y_order = 9001
                                # dispaly text
                                self.text_message = f'{obj_b} on a {obj_a}'
                                self.font_on_screen = True
                                # hide objects
                                self.object_map.pop(beyond_object_pos)
                            return
                    else:
                        # if not combining and movable, move player and object
                        self.grid_position = {'x': to_position[0], 'y': to_position[1]}
                        self.draw_position = self.update_player_position()
                        # and move object and update object map
                        self.update_object_position(to_position, from_position, False, False)
            else:
                self.grid_position = {'x': to_position[0], 'y': to_position[1]}
                self.draw_position = self.update_player_position()
        # print(self.combined_objects)

    def level_win_conditions_met(self):
        if LEVEL_WIN_CONDITION[self.current_level] == self.combined_objects:
            return True
        else:
            return False

    def update_object_position(self, to_position, from_position, combining, large_object):
        pos = (to_position[0] - from_position[0], to_position[1] - from_position[1])
        final_pos = (to_position[0] + pos[0], to_position[1] + pos[1])
        self.object_map[final_pos] = self.object_map[to_position]
        self.object_map.pop(to_position)
        self.object_map[final_pos].grid_position = {'x': final_pos[0], 'y': final_pos[1]}
        if (combining):
            self.object_map[final_pos].draw_object_combined()
        else:
            self.object_map[final_pos].draw_object()

    def objects_can_be_combined(self, obj_a, obj_b):
        # obj_a = 'bear'
        obj_a_id = OBJECT_NAME_MAP[obj_a]
        obj_b_id = OBJECT_NAME_MAP[obj_b]

        if obj_b_id in OBJECT_COMBINATIONS[obj_a_id]:
            return True
        else:
            return False

    def update(self, dt, event=None):
        self.get_input(event)
