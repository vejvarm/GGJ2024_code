import pathlib
from csv import reader
from os import walk  #walks through the file system
import pygame
from settings import TILE_SIZE, DISPLAY_HEIGHT, DISPLAY_WIDTH, AUDIO_FOLDER


def import_layout(path):
    layout = []

    with open(path) as file:
        read_file = reader(file, delimiter = ',')
        for row in read_file:
            layout.append(list(row))
        return layout


def import_folder(path):
    folder = []

    for _, __, files in walk(path):  #_ is taking the place of the folder name and __ is taking the place of the list of subfolder names in the directory
        for file in files:
            file_path = path + '/' + file
            file_surf = pygame.image.load(file_path).convert_alpha()  #loads an image and converts it
            folder.append(file_surf)
    return folder

def calculate_position(x, y, tile_size = TILE_SIZE): 
    xx = (x - y) * tile_size/2 + DISPLAY_WIDTH//2
    yy = (y+x)*tile_size/4 + DISPLAY_HEIGHT//4       
    return (xx, yy)


def load_object_map(path_to_csv: str):
    map = {}
    with open(path_to_csv) as file:
        read_file = reader(file, delimiter = ',')
        for i, row in enumerate(read_file):
            for j, val in enumerate(row):
                map[(j, i)] = val
        return map
    

def play_music(file_name: str):
    music_file = AUDIO_FOLDER.joinpath(file_name)

    # Load and play the music
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.play(-1)  # -1 means loop indefinitely