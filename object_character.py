import pygame
from settings import *
from debug import debug
from support import calculate_position
from collections import namedtuple

from tile import Object


class ObjectCharacter(Object):
    def __init__(self, groups, pos, obj_id, fl_name, y_order, layer='object', tile_size=TILE_SIZE):
        super().__init__(groups, pos, obj_id, fl_name, y_order, layer, tile_size)

    def get_type(self, obj_id: int) -> tuple[str, int]:
        return OBJECTS[obj_id]

    def get_draw_position(self):
        position = calculate_position(self.grid_position[0], self.grid_position[1], self.tile_size)
        # if object is a wall then draw it higher so it aligns with tiles
        if self.type[0] == 'wall1' or self.type[0] == 'wall2':
            position = (position[0], position[1] - self.tile_size / 3)
        if self.type[0] not in OBJECTS_INVISIBLE:  # This is to prevent drawing of invisible objects
            self.rect = self.image.get_rect(topleft=position)
        else:
            self.kill()
        self.y_order = self.grid_position[0] + self.grid_position[1] / 100
        return position

    def get_draw_position_combined(self):
        position = calculate_position(self.grid_position[0], self.grid_position[1], self.tile_size)
        if self.type[0] not in OBJECTS_INVISIBLE:
            position = (position[0], position[1]-self.tile_size/4)
        self.rect = self.image.get_rect(topleft=position)
        self.y_order = self.grid_position[0] + self.grid_position[1] / 100
        return position