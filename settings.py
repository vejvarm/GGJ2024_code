import pathlib

ROOT = pathlib.Path("./")

MAPS_FOLDER = ROOT.joinpath("assets/Maps")
OBJECTS_FOLDER = ROOT.joinpath("assets/objects")
AUDIO_FOLDER = ROOT.joinpath("assets/audio")

#display resolution
DISPLAY_WIDTH = 1600
DISPLAY_HEIGHT = 800

#tile size
TILE_SIZE = 96

FPS = 30

#sprite layers
LAYERS = {
    'ground': 0,
    'object': 1,
    'player': 2
}

#player character stats
player_character_stats = {
    'player_character_1': {'strength': 3, 'endurance': 5, 'intelligence': 1, 'spirit': 1, 'dexterity': 2, 'luck': 0,
                    'health': 50, 'mana': 10, 'exp': 0, 'speed': 160}
    }

#1 = movable
OBJECTS = {
    -1: ('empty', 0),
    0: ('bear', 1),
    1: ('bee', 1),
    2: ('truck-front', 0),
    3: ('chair', 1),
    4: ('duck', 1),
    5: ('elf', 1),
    6: ('flea', 1),
    7: ('pear', 1),
    8: ('puck', 1),
    9: ('sea', 0),
    10: ('shelf',1),
    11: ('truck-back', 0),
    12: ('tree', 0),
    13: ('wall1', 0),
    14: ('wall2', 0),
}

# objects that are displayed as tiles under the player character
# but can be combined so they are also on the object map but invisible
OBJECTS_INVISIBLE = {
    'sea',
}

# name, ids to combine, number of combined
OBJECTS_OVERSIZED = {
    0: ('truck', (2,11)),
}        

OBJECT_NAME_MAP = {v[0]: k for k, v in OBJECTS.items()}

# TODO: check for truck-front and truck-back

#change to not hook
DEFAULT_LEVEL = 3
LEVEL_PLAYER_ID_MAP = {
    0: 0,  # bear
    1: 0,  # bear
    2: 0,  # bear
    3: 1,  # bee
}

OBJECT_COMBINATIONS = {
    0: (7, 3),
    1: (6, 9, 12),
    2: (4, 8),
    3: (0, 7),
    4: (2, 8, 11),
    5: (10, ),
    6: (1, 9),
    7: (0, 3),
    8: (2, 4),
    9: (1, 6, 12),
    10: (5, ),
    11: (2, 4, 8),
    12: (1, 6, 9),
    13: tuple(),
    14: tuple(),
}


LEVEL_WIN_CONDITION = {
    0: 2,  # two combinations
    1: 2,  # two combinations
    2: 3,  # three combinations
    3: 3,  
}

LEVEL_BACKGROUND = {
    0: '183b18',    
    1: '2c2512',
    2: '183b18', 
    3: '0689b4',
    4: '7b5825',
}

LEVEL_NAMES = {
    0: 'Elf',    
    1: 'Self',
    2: 'Big ass car', 
    3: 'Desert island',    
}