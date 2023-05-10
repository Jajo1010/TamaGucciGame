from constants import *
import pygame
from components import start_screen,main_screen
from pygame.locals import *


DISPLAY_SURFACE = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
FPS_CLOCK = pygame.time.Clock()

def main():
    pygame.init()
    
    pygame.display.set_caption("TamaGucci")

    pygame.display.update()
    start_screen.display_start_screen(DISPLAY_SURFACE,FPS_CLOCK)
    main_screen.display_main_screen(DISPLAY_SURFACE,FPS_CLOCK)
    FPS_CLOCK.tick(FPS)
    

if __name__ == '__main__':
    main()