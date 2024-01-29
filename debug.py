import pygame

#pygame
pygame.init()

#font
font = pygame.font.Font(None, 30)  #stored/creates a font where "None" indicates the file path

#debugger
def debug(info, y = 10, x = 10):
    display_surface = pygame.display.get_surface()  #stored/gets a surface
    debug_rend = font.render(str(info), True, 'White')  #stored/renders a specified string and with antialiasing "True"
    debug_rect = debug_rend.get_rect(topleft = (x, y))  #stored/gets a rectangle for the render
    pygame.draw.rect(display_surface, 'Black', debug_rect)  #draws a rectangle with a color on the surface
    display_surface.blit(debug_rend, debug_rect)  #draws the render onto the rectangle
