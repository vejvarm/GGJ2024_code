import pygame
from settings import *
from debug import debug
from support import calculate_position
from collections import namedtuple

class Object_character(pygame.sprite.Sprite):
    def __init__(self, groups, pos, obj_class_id, y_order, layer='object'):
        super().__init__(groups)
        path_to_image = OBJECTS_FOLDER.joinpath(f"{obj_class_id}.png")
        self.image = pygame.image.load(path_to_image)
        self.type = OBJECTS[obj_class_id]
        self.grid_position = {'x':pos[0], 'y':pos[1]}
        self.draw_position = self.draw_object()
        self.z = LAYERS[layer]
        self.y_order = y_order
        self.is_combined_with = ''

    def draw_object(self):
        position = calculate_position(self.grid_position['x'], self.grid_position['y'])
        #if object is a wall then draw it higher so it aligns with tiles
        if self.type[0] == 'wall1' or self.type[0] == 'wall2':
            position = (position[0],position[1]-TILE_SIZE/3)
        self.rect = self.image.get_rect(topleft = position)
        self.y_order = self.grid_position['y'] + self.grid_position['x'] / 100
        return position

    def draw_object_combined(self):
        position = calculate_position(self.grid_position['x'], self.grid_position['y'])
        position = (position[0],position[1]-TILE_SIZE/4)
        self.rect = self.image.get_rect(topleft = position)
        self.y_order = self.grid_position['y']
        return position             