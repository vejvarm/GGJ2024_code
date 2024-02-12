# But have you heard of ... <br> (game from Global Game Jam 2024)

---
# Links
> [Introduction Video](https://youtu.be/IBjYyKP618Y) \
> [Game page on GGJ website](https://globalgamejam.org/games/2024/have-you-heard-3) \
> [Alpha demo build](https://ggjv4.s3.us-west-1.amazonaws.com/files/games/2024/13277/exec/but_have_you_heard_of.zip?VersionId=sVb.AnX_JYuhNRnu6XyYcY1cH_XJoP2V)

# Stuff that has been done
    - title screen added
    - show what level you are on and how many opbejcts combined / how many to win
    - big object logic settings: OBJECTS_OVERSIZED
    - objects disappear after combination
    - corrected drawing order (moved walls up so they align with tiles, player correctly in front of walls)
    - hidden objects (sea, shore) setting: OBJECTS_INVISIBLE (these objects are twice - on tile layer, also on object level, on object level they are invisible but can be combined with)
    - 2 objects in a row can be pushed
    - fail message says how many combined and what happened
    - floor tiles can be combined with - settings: TILES, TILE_COMBINATIONS (this works only on player for now, not objects)
    - !!! level 4 csv were written manually, don't export and don't overwrite the files

# Todo list
- number = priority

## Want to do for sure

    10 Win Songs:    
    - bear on a pear (end of level 1)
    - bee on a sea (end of level 3)
    - boar on a floor (end of level 4)
    - boar on a shore (other end of level 4)
    
    9 Fix: combining 2 objects at once
    9 Fix: combining with wall in level 4
    
    7 Fix: combining puck on a truck on a duck (not a bug?)

    6 enemy that follows you (on move or moves once in 2 seconds for example)
    - on move probably more fun and easier to do

    9 d-pad picture for controls instead of A W S D letters (show a picture top right)
    5 clean up the code and remove unnecessary stuff

    10 Add "game complete" screen with credits and send us feedbakc at email

## Probably canceled:    
    2 other sounds
    - 2 sound effects for moving, pushing and combining

    1 Animations - do we want to do that? mechanics and puzzles are probably more interesting than anim.
    - animation/effect for disappearing objects
    - animation for main characters
    - animaiton for enemy that follows you
    - animation for all objects

    1 somehow comunicate that main character's name is FeeFee
    0 port this whole thing on android

## Bugs

    5 Bear's but is sticking through walls
    2 Before you move object, if youstand behind it draw order is wrong, after you move object it's correct

### Win state songs

    Done:
    - bear on a chair

    To do:
    - bear on a pear
    - bee on a sea
    - boar on a floor
    - boar on a shore

## Ideas for Other mechanics

    - compound words (bookshelf + elf = book)
    - combining objects in different orderes does different things
    - tile is a word (invisible object)
    - tile can be covered up so it can be stepped on (boar on the floor, get pain on the floor to be able to walk on it)
    - multi-layer - can use starts to go level up or down, push stuff on lover level to be able to cross on higher level
    - area of a level or the whole level is a word
    - player is a compound word, has to "degrade itself" twice

## Ideas for levels

### LEVEL 3 

    - flea on the sea
    - bee on a tree
    - fail: bee on flea or sea
    - flea is following player = bee

### LEVEL 4

    - boar on the floor is fail
    - avoid floor as a boar
    - push bee on tree
    - end on an oar 

### LEVEL 5

    - part of the level is a square, bear has to finish in that area     

## Building an exe

    - pyinstaller
    - include python dll
    - pyinstaller --paths C:\Users\Fil\AppData\Local\Programs\Python\Python311\python311.dll --onefile code/main.py

## building and android version

    - https://www.youtube.com/watch?v=L6XOqakZOeA