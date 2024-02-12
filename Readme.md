# But have you heard of ... <br> (game from Global Game Jam 2024)

---
# Links
> [Introduction Video](https://youtu.be/IBjYyKP618Y) \
> [Game page on GGJ website](https://globalgamejam.org/games/2024/have-you-heard-3) \
> [Alpha demo build](https://ggjv4.s3.us-west-1.amazonaws.com/files/games/2024/13277/exec/but_have_you_heard_of.zip?VersionId=sVb.AnX_JYuhNRnu6XyYcY1cH_XJoP2V)


# Todo list
- number = priority

## Want to do for sure
    
    99 walk over invisible objects
    11 dpad picture for controls instead of a w s d letters
    10 clean up the code and remove unnecessary stuff
    7 animation/effect for disappearing objects
    6 animation for main characters
    6 animaiton for enemy that follows you
    3 animation for all objects
    2 sound effects for moving, pushing and combining
    9 song for different win states: bear on a pear, bee on a sea
    9 enemy that follows you (on move or moves once in 2 seconds for example)
    1 somehow comunicate that main character's name is FeeFee
    0 port this whole thing on android

## Bugs

    5 Bear's but is sticking through walls
    2 Before you move object, if youstand behind it draw order is wrong, after you move object it's correct

### New assets:

    - buck (deer)
    - store
    - shore

### Win state sogs

    Done:
    - bear on a chair

    To do:
    - bear on a pear
    - bee on a sea

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