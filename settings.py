import pathlib

DEFAULT_LEVEL = 4

ROOT = pathlib.Path("./")

MAPS_FOLDER = ROOT.joinpath("assets/Maps")
OBJECTS_FOLDER = ROOT.joinpath("assets/objects")
AUDIO_FOLDER = ROOT.joinpath("assets/audio")
SCREENS_FOLDER = ROOT.joinpath("assets/screens")

#display resolution
DISPLAY_WIDTH = 1200
DISPLAY_HEIGHT = 800

CONTROLS_TEXT_POS = ( 200, 100 )

#tile size
TILE_SIZE = 96
TILE_SIZE_BIG_LEVEL = 64

# big levels with tiles smaller size
LEVEL_ZOOMED_OUT = (4, 5, 6)

FPS = 30

#sprite layers
LAYERS = {
    'ground': 0,
    'object': 1,
    'player': 2
}

# list of all objecs
# 0 = can't be pushed
# 1 = movable, can be pushed
# 3 = not movable but can be walked on (e.g. floor)
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
    9: ('sea', 3),
    10: ('shelf',1),
    11: ('truck-back', 0),
    12: ('tree', 0),
    13: ('wall1', 0),
    14: ('wall2', 0),
    15: ('boar', 1),
    16: ('door', 0),
    17: ('oar', 1),
    18: ('shore', 3),
    19: ('floor', 3),
}
OBJECT_NAME_MAP = {v[0]: k for k, v in OBJECTS.items()}

# objects that are displayed as tiles under the player character
# but can be combined so they are also on the object map but invisible
OBJECTS_INVISIBLE = {
    'sea',
    'shore',
    'floor'
}

# tiles that can be walked on but can also be combined with
# floor = id (6,7,8)
TILE_COMBINATIONS = {
    0: tuple(),    
    1: tuple(),    
    2: tuple(),    
    3: tuple(),    
    4: tuple(),    
    5: tuple(),    
    6: (15, 16, 17), 
    7: (15, 16, 17), 
    8: (15, 16, 17), 
    9: tuple(),    
    10: tuple(),    
    11: tuple(), 
    12: tuple(), 
    13: tuple(),     
}

# 1 = can be combined
TILES = {
    0: ('grass', 0),    
    1: ('grass', 0),    
    2: ('grass', 0),    
    3: ('sand', 0),    
    4: ('sand', 0),    
    5: ('sand', 0),    
    6: ('floor', 1), 
    7: ('floor', 1), 
    8: ('floor', 1), 
    9: ('grass', 0),    
    10: ('grass', 0),  
}
TILE_NAME_MAP = {v[0]: k for k, v in TILES.items()}

# objects that are more than 1 tile
# name, ids to combine
OBJECTS_OVERSIZED = {
    0: ('truck', (2,11)),
}        

# who is the player
LEVEL_PLAYER_ID_MAP = {
    0: 0,  # bear
    1: 0,  # bear
    2: 0,  # bear
    3: 1,  # bee
    4: 15,  # boar    
}

# objects that can be combined
OBJECT_COMBINATIONS = {
    0: (7, 3),
    1: (6, 9, 12),
    2: (4, 8),
    3: (0, 7),
    4: (2, 8, 11),
    5: (10, ),
    6: (1, 9, 12),
    7: (0, 3),
    8: (2, 4),
    9: (1, 6, 12),
    10: (5, ),
    11: (2, 4, 8),
    12: (1, 6, 9),
    13: tuple(),
    14: tuple(),
    15: (16, 17, 18, 19),
    16: (15, 17, 18, 19),
    17: (15, 16, 18, 19),
    18: (15, 16, 17, 19),
    19: (15, 16, 17, 18),
}

# how many combinaitons to win level
LEVEL_WIN_CONDITION = {
    0: 2,  # two combinations
    1: 2,  # two combinations
    2: 3,  # three combinations
    3: 3,  
    4: 4,
}

LEVEL_BACKGROUND = {
    0: '183b18',    
    1: '2c2512',
    2: '183b18', 
    3: '0689b4',
    4: '0689b4',
}
# 7b5825

LEVEL_NAMES = {
    0: 'Elf',    
    1: 'Self',
    2: 'Big ass car', 
    3: 'Desert island',  
    4: 'She sells sea shells on a ...'  
}