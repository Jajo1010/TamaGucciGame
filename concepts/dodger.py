import pygame
from pygame.locals import *


class Dodger:
    def __init__(self):
        pygame.init()
        self.WIDTH = 800
        self.HEIGHT = 600
        self.screen = pygame.display.set_mode((800, 600))
        self.FPS = 30
        self.FPS_CLOCK = pygame.time.Clock()
        self.BASICFONT = pygame.font.Font('freesansbold.ttf', 20)

        self.HERO = pygame.Rect()

    