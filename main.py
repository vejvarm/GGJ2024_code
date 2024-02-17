import pygame
from settings import *
from core import Core
from time import time
from sys import exit
from support import *


class Game:

    def __init__(self):
        pygame.init()
        self.level = 0
        
        #display
        self.screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        pygame.display.set_caption('But have you heard of...')

        #the game's core element
        self.core = Core()

        #clock
        self.clock = pygame.time.Clock()
        self.previous_time = time()

    def run(self):
        while True:
            # end main loop to display end screen
            if self.core.end_screen:
                break

            # otherwise, run game
            ev = None
            dt = self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    ev = event
                    break
                # if event.key == pygame.K_q:
                #     self.core.previous_level()
                # elif event.key == pygame.K_w:
                #     self.core.reset_level()
                # elif event.key == pygame.K_e:
                #     self.core.next_level()

            self.core.run(dt, ev)
            pygame.display.update()

        # Final screen loop (wait for Space to exit)
        self.core.display_end_screen()
        pygame.display.update()
        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.quit()
                    exit()

#main code
if __name__ == '__main__':
    game = Game()
    game.run()
    