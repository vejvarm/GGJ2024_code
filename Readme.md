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

## for later
    10 Script for copying tile level to ground level (csv) 

    6 enemy that follows you (on move or moves once in 2 seconds for example)
    - on move probably more fun and easier to do

    5 clean up the code and remove unnecessary stuff

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

    5 Bear's butt is sticking through walls    

## Ideas for Other mechanics

    - compound words (bookshelf + elf = book)
    - combining objects in different orderes does different things
    - tile is a word (invisible object)
    - tile can be covered up so it can be stepped on (boar on the floor, get pain on the floor to be able to walk on it)
    - multi-layer - can use starts to go level up or down, push stuff on lover level to be able to cross on higher level
    - area of a level or the whole level is a word
    - player is a compound word, has to "degrade itself" twice

## Building an exe

    - pyinstaller
    - include python dll
    - pyinstaller --paths C:\Users\Fil\AppData\Local\Programs\Python\Python311\python311.dll --onefile --noconsole code/main.py

## building and android version

    - https://www.youtube.com/watch?v=L6XOqakZOeA