import pygame
from components.clothing_progressbar import ProgressBar
from pygame.locals import *
from constants import *
from helpers import terminate, image_center_x_y, to_center_of_screen, file_list_from_dir, surfaces_from_file_list
from spritesheet import Spritesheet
import os


def display_main_screen(surface, fps):
    surface.fill((255,255,255))
    progress_bar = ProgressBar(surface, 10)

    game_started = False
    while not game_started:
        progress_bar.draw()
        progress_bar.add_bar()
        pygame.display.update()
        pygame.event.get()
        pygame.time.wait(1000)
        fps.tick(FPS)
