# But have you heard of ... <br> (game from Global Game Jam 2024)

---
# Links
> [Introduction Video](https://youtu.be/IBjYyKP618Y) \
> [Game page on GGJ website](https://globalgamejam.org/games/2024/have-you-heard-3) \
> [Alpha demo build](https://ggjv4.s3.us-west-1.amazonaws.com/files/games/2024/13277/exec/but_have_you_heard_of.zip?VersionId=sVb.AnX_JYuhNRnu6XyYcY1cH_XJoP2V)


# Todo list
- number = priority

## Want to do for sure
    
    10 indicator on what level you are
    10 system for combining big objects (truck)
    10 better text when you fail
    8 disappear objects after they are combined
    7 animation/effect for disappearing objects
    6 animation for main characters
    2 animation for all objects
    1 sound effects for moving, pushing and combining
    9 song for different win states
    9 enemy that follows you (on move or moves once in 2 seconds for example)
    11 somehow comunicate that main character's name is FeeFee

## Ideas for Other mechanics

    - compound words (bookshelf + elf = book)
    - combining objects in different orderes does different things
    - tile is a word (invisible object)
    - tile can be covered up so it can be stepped on (boar on the floor, get pain on the floor to be able to walk on it)
    - multi-layer - can use starts to go level up or down, push stuff on lover level to be able to cross on higher level
    - area of a level or the whole level is a word
    - player is a compound word, has to "degrade itself" twice

## Ideas for levels

    - board on the floor
    - bear on a square (square is made of tiles and is an area of level, can't enter square until the end but must push things into square)

## Building an exe

    - pyinstaller
    - include python dll
    - pyinstaller --paths C:\Users\Fil\AppData\Local\Programs\Python\Python311\python311.dll --onefile code/main.py