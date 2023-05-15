from constants import *
import pygame
from components import start_screen,main_screen

from pygame.locals import *
from pygame import mixer
import os


DISPLAY_SURFACE = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
FPS_CLOCK = pygame.time.Clock()
DIRNAME = os.path.dirname(__file__)

def main():
    pygame.init()
    pygame.display.set_caption("TamaGucci")
    
    mixer.init()
    mixer.music.load(os.path.join(DIRNAME,"..\\resources\\sounds\\Music_3.mp3"))
    mixer.music.set_volume(0.2)
    mixer.music.play()
    
    pygame.display.update()
    start_screen.display_start_screen(DISPLAY_SURFACE,FPS_CLOCK)
    main_screen.display_main_screen(DISPLAY_SURFACE,FPS_CLOCK)
    FPS_CLOCK.tick(FPS)
    

if __name__ == '__main__':
    main()