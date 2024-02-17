import pygame
import pathlib
import time
from settings import *
from stopwatch import Stopwatch
from debug import debug
from support import calculate_position
from collections import namedtuple

class Player_Character(pygame.sprite.Sprite):
    def __init__(self, groups, pos: tuple[int, int], z, object_map, ground_map, all_sprites, y_order, obj_class_id: int, tile_size = TILE_SIZE):
        super().__init__(groups)
        path_to_image = OBJECTS_FOLDER.joinpath(f"{obj_class_id}.png")
        self.image = pygame.image.load(path_to_image)
        self.type = OBJECTS[obj_class_id]
        self.z = LAYERS[z]
        self.grid_position = {'x': pos[0], 'y': pos[1]}
        self.tile_size = tile_size
        self.draw_position = self.update_player_position()
        self.object_map = object_map
        self.ground_map = ground_map
        self.all_sprites = all_sprites
        self.y_order = y_order
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(None, 30)
        self.font_big = pygame.font.Font(None, 66)
        self.font_on_screen = False
        self.winner = False
        self.combined_objects = 0
        self.current_level = 0
        self.is_combined = False
        self.text_message = ''
        self.reset_level = False
        self.obj_to_hide = []
        self.player_won_by = ''

    def update_player_position(self):
        position = calculate_position(self.grid_position['x'], self.grid_position['y'], self.tile_size)
        self.rect = self.image.get_rect(topleft=position)
        self.y_order = self.grid_position['y'] + self.grid_position['x'] / 100
        return position

    def get_input(self, event):
        # movement, tool use, and tool switch
        # if not self.stopwatches['any use'].active:
        dx = 0
        dy = 0
        move = False
        if event is not None and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                dx += 1
                move = True
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                dx -= 1
                move = True
                # self.move_player(self.grid_position, (self.grid_position['x']-1, self.grid_position['y']))
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                dy -= 1
                move = True
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                dy += 1
                move = True
            if event.key == pygame.K_r:
                self.reset_level = True    

        if move:
            self.move_player(self.grid_position, (self.grid_position['x'] + dx, self.grid_position['y'] + dy))

    def move_player(self, from_position, to_position):
        from_position = (from_position['x'], from_position['y'])
        # check level exists = can't go outside of level
        if to_position in self.ground_map.keys() and self.ground_map[to_position] != -1:
            # check object exists where we're moving
            if to_position in self.object_map.keys():                
                # check if object combines with player
                obj_a = self.type[0]
                obj_b = self.object_map[to_position].type[0]
                if self.objects_can_be_combined(obj_a, obj_b):
                    # COMBINE PLAYER AND OBJECT!
                    self.combined_objects += 1
                    self.winner = self.level_win_conditions_met()
                    self.grid_position = {'x': to_position[0], 'y': to_position[1]}
                    self.draw_position = self.update_player_position()
                    # draw player on top of object
                    self.is_combined = True
                    if not self.winner:
                        self.text_message = "You're a " + f'{obj_a} on a {obj_b}' + "... FAILED: Objects combined: " + str(self.combined_objects) + '/' + str(LEVEL_WIN_CONDITION[self.current_level])
                        self.font_on_screen = True
                    self.y_order = 9001
                    if obj_b not in OBJECTS_INVISIBLE:
                        self.draw_position = (self.draw_position[0], self.draw_position[1] - self.tile_size / 4)
                    else:
                        self.draw_position = (self.draw_position[0], self.draw_position[1])
                    self.rect = self.image.get_rect(topleft=self.draw_position)

                    #for winner music
                    self.player_won_by = obj_b
                    #return
                # check immovable object
                elif self.object_map[to_position].type[1] == 0:
                    pass
                # check object can be moved = type[1] == "1"                
                elif self.object_map[to_position].type[1] == 1:
                    # check if object can be moved - is there edge of level
                    pos_direction_vector = (to_position[0] - from_position[0], to_position[1] - from_position[1])
                    beyond_object_pos = (to_position[0] + pos_direction_vector[0], to_position[1] + pos_direction_vector[1])
                    if beyond_object_pos not in self.ground_map.keys():
                        # can't move, no map
                        pass
                        #return
                        # check if object can be moved - is there another object
                    elif beyond_object_pos in self.object_map.keys():
                        # or another object then check if it can be combined
                        obj_a = self.object_map[beyond_object_pos].type[0]
                        obj_b = self.object_map[to_position].type[0]
                        if self.objects_can_be_combined(obj_a, obj_b):
                            # COMBINE!
                            if not self.is_combined:
                                #special case of oversized object e.g. TRUCK 
                                if self.is_part_of_oversized_object(OBJECT_NAME_MAP[obj_a]):
                                    self.combined_objects += 1
                                    self.object_map[beyond_object_pos].is_combined_with = obj_b
                                    self.grid_position = {'x':to_position[0], 'y': to_position[1]} 
                                    self.draw_position = self.update_player_position()    
                                    self.obj_to_hide.append(self.object_map[beyond_object_pos])                    
                                    self.update_object_position(to_position, from_position, True, True)
                                    self.object_map[to_position].y_order = 9001
                                    self.combine_oversized_object(OBJECT_NAME_MAP[obj_a])
                                    self.obj_to_hide.append(self.object_map[to_position])
                                    self.object_map.pop(to_position)
                                else:
                                    # Combine normal stuff
                                    self.combined_objects += 1
                                    self.winner = self.level_win_conditions_met()
                                    self.grid_position = {'x': to_position[0], 'y': to_position[1]}
                                    self.draw_position = self.update_player_position()
                                    # draw objects on top of each other
                                    self.obj_to_hide.append(self.object_map[beyond_object_pos])
                                    self.update_object_position(to_position, from_position, True, False)
                                    # draw the on top over the one on the bottom
                                    self.object_map[beyond_object_pos].y_order = 9001
                                    # display text
                                    self.text_message = f'{obj_b} on a {obj_a}'
                                    self.font_on_screen = True
                                    # hide objects
                                    self.obj_to_hide.append(self.object_map.pop(beyond_object_pos))                                    
                            #return
                        elif self.object_map[beyond_object_pos].type[1] in (0, 3):
                            # can't combine and beyond object is immovable
                            pass
                        else:
                            # cant combine and both objects are movable, move both
                            # is there space to move beyond second object
                            # is there an object, can it be combined
                            beyond_beyond_object_pos = (beyond_object_pos[0] + pos_direction_vector[0], beyond_object_pos[1] + pos_direction_vector[1])
                            if beyond_beyond_object_pos in self.ground_map.keys():
                                if beyond_beyond_object_pos in self.object_map.keys():
                                    # or another object then check if it can be combined
                                    obj_a = self.object_map[beyond_object_pos].type[0]
                                    obj_b = self.object_map[beyond_beyond_object_pos].type[0]
                                    if self.objects_can_be_combined(obj_a, obj_b):
                                        self.combined_objects += 1
                                        self.winner = self.level_win_conditions_met()
                                        self.grid_position = {'x': to_position[0], 'y': to_position[1]}
                                        self.draw_position = self.update_player_position()
                                        self.obj_to_hide.append(self.object_map[beyond_beyond_object_pos])
                                        self.obj_to_hide.append(self.object_map[beyond_object_pos])
                                        self.update_object_position(beyond_object_pos, to_position, True, False)
                                        self.update_object_position(to_position, from_position, False, False) 
                                        # draw objects on top of each other
                                        self.object_map[beyond_beyond_object_pos].y_order = 9001
                                        self.text_message = f'{obj_a} on a {obj_b}'
                                        self.font_on_screen = True
                                                                              
                                    #return    
                                else:
                                    #move to empty space     
                                    self.grid_position = {'x': to_position[0], 'y': to_position[1]}
                                    self.draw_position = self.update_player_position()
                                    self.update_object_position(beyond_object_pos, to_position, False, False)
                                    self.update_object_position(to_position, from_position, False, False)                                                  
                            #return
                    else:
                        # if not combining and movable, move player and object
                        self.grid_position = {'x': to_position[0], 'y': to_position[1]}
                        self.draw_position = self.update_player_position()
                        # and move object and update object map
                        self.update_object_position(to_position, from_position, False, False)
            else:
                # move normally
                self.grid_position = {'x': to_position[0], 'y': to_position[1]}
                self.draw_position = self.update_player_position()

            self.check_player_on_tile(to_position)

    def check_player_on_tile(self, to_position):
        # check if tile can be combined with player (boar on a floor)
        if to_position in self.object_map and self.object_map[to_position].type[1] == 0:
            return

        if self.tile_and_object_can_be_combined(self.ground_map[to_position], self.type[0]):
            self.combined_objects += 1
            self.is_combined = True
            self.winner = self.level_win_conditions_met()
            self.grid_position = {'x': to_position[0], 'y': to_position[1]}
            self.draw_position = self.update_player_position()
            if not self.winner:
                self.text_message = "You're a " + f'{self.type[0]} on a {TILES[self.ground_map[to_position]][0]}' + "... FAILED: Objects combined: " + str(self.combined_objects) + '/' + str(LEVEL_WIN_CONDITION[self.current_level])
                self.font_on_screen = True
            else:
                self.text_message = f'{self.type[0]} on a ...'
                #for winner music
                self.player_won_by = TILES[self.ground_map[to_position]][0]

            self.y_order = 9001
            self.draw_position = (self.draw_position[0], self.draw_position[1] - self.tile_size / 4)
            self.rect = self.image.get_rect(topleft=self.draw_position)

    def combine_oversized_object(self, obj_id):  
  
        for values in OBJECTS_OVERSIZED.values():
            if obj_id in values[1]:             
                obj_size = len(values[1])
                num_of_parts_combined = 0
                list_of_parts = []                
                #for each part (obj id) find in map and check if combined
                for v in values[1]:
                    for o in self.object_map:
                        if self.object_map[o].type[0] == OBJECTS[v][0] and self.object_map[o].is_combined_with != '':
                        #if o.type[0] == OBJECT_NAME_MAP[v] and o.is_combined == True:
                            num_of_parts_combined += 1
                            list_of_parts.append(self.object_map[o].grid_position)
                if num_of_parts_combined == obj_size:
                    #all parts combined
                    names_of_parts = []
                    for o_pos in list_of_parts:
                        names_of_parts.append(self.object_map[(o_pos['x'],o_pos['y'])].is_combined_with)
                        self.object_map.pop((o_pos['x'],o_pos['y']))
                    #display final text for all parts
                    #prepare message
                    final_message = ' and '.join(names_of_parts)   
                    self.text_message = f'{final_message} on a {values[0]}'
                    self.font_on_screen = True    
                
    def is_part_of_oversized_object(self, obj_id):
        for values in OBJECTS_OVERSIZED.values():
            if obj_id in values[1]:
                return True
        return False

    def level_win_conditions_met(self):
        if self.combined_objects >= LEVEL_WIN_CONDITION[self.current_level]:
            return True
        else:
            return False

    def update_object_position(self, to_position, from_position, combining, oversized_object):
        pos = (to_position[0] - from_position[0], to_position[1] - from_position[1])
        final_pos = (to_position[0] + pos[0], to_position[1] + pos[1])          
        # example
        # to pos = puck
        # final pos = truck
        if oversized_object == True:
            self.object_map[to_position].grid_position = {'x': final_pos[0], 'y': final_pos[1]}
            self.object_map[to_position].draw_object_combined()
        else:            
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

    def tile_and_object_can_be_combined(self, tile_id, obj_name):
        obj_id = OBJECT_NAME_MAP[obj_name]
        if obj_id in TILE_COMBINATIONS[tile_id]:
            return True
        else:
            return False

    def update(self, dt, event=None):
        self.get_input(event)