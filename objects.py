import pygame
from settings import *

import pygame
from settings import *
from support import calculate_position


class Object(pygame.sprite.Sprite):
    def __init__(self, groups, pos: tuple[int, int], obj_id: int, fl_name: str, y_order, layer: str = None, tile_size: int = TILE_SIZE):
        super().__init__(groups)
        self.grid_position = pos
        self.id = obj_id
        self.name = fl_name
        self.y_order = y_order
        self.tile_size = tile_size

        self.type = self.get_type(obj_id)
        self.image = self._load_image(fl_name)
        self.draw_position = self.get_draw_position()
        self.z = LAYERS[layer]
        self.is_combined_with = ''

    def _load_image(self, name_or_id: str):
        path_to_tile = TILES_FOLDER.joinpath(f"{name_or_id}.png")
        path_to_object = OBJECTS_FOLDER.joinpath(f"{name_or_id}.png")
        if path_to_tile.exists():
            return pygame.image.load(path_to_tile)
        elif path_to_object.exists():
            return pygame.image.load(path_to_object)
        else:
            print(f"Tile/Object with id `{name_or_id}` does not exist. Removing from sprite groups.")
            self.kill()
            return pygame.Surface((self.tile_size, self.tile_size))

    def get_type(self, obj_id: int) -> tuple[str, int]:
        # override this method in subclasses
        ...

    def get_draw_position(self):
        # override this method in subclasses
        ...


class Tile(Object):
    def __init__(self, groups, pos: tuple[int, int], tile_id: int, tile_name: str, y_order, layer: str = 'ground'):
        super().__init__(groups, pos, tile_id, tile_name, y_order, layer)
        if self.id >= 0:
            self.rect = self.image.get_rect(topleft=self.draw_position)

    def get_type(self, obj_id: int) -> tuple[str, int]:
        return TILES[obj_id]

    def get_draw_position(self):
        return self.grid_position


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
