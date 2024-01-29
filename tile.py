import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, groups, surface, pos, z, y_order):
        super().__init__(groups)
        self.image = surface                                        
        self.rect = self.image.get_rect(topleft = pos)
        self.z = LAYERS[z]
        self.y_order = y_order
