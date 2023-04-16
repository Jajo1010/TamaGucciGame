import pygame
from pygame.locals import *
import random
import os
from sys import exit


class Simon:
    def __init__(self):
        pygame.init()
        self.WIDTH = 800
        self.HEIGHT = 600

        self.DISPLAY_SURFACE = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.FPS = 60
        self.FPS_CLOCK = pygame.time.Clock()
        self.BASICFONT = pygame.font.Font('freesansbold.ttf', 20)
        self.dirname = os.path.dirname(__file__)

        self.GREEN_inactive = (0, 100, 0)
        self.GREEN_active = (0, 200, 0)
        self.RED_inactive = (100, 0, 0)
        self.RED_active = (200, 0, 0)
        self.BLUE_inactive = (0, 0, 100)
        self.BLUE_active = (0, 0, 200)
        self.YELLOW_inactive = (150, 150, 0)
        self.YELLOW_active = (100, 100, 0)

        self.tile_size = 150
        self.tile_gap = 10
        self.tiles = {
            "green": pygame.Rect(self.tile_size+self.tile_gap, self.tile_size-50, self.tile_size, self.tile_size),
            "red": pygame.Rect(self.tile_size*3+self.tile_gap, self.tile_size-50, self.tile_size, self.tile_size),
            "yellow": pygame.Rect(self.tile_size+self.tile_gap, self.HEIGHT-100-self.tile_size, self.tile_size, self.tile_size),
            "blue": pygame.Rect(self.tile_size*3+self.tile_gap, self.HEIGHT-100-self.tile_size, self.tile_size, self.tile_size)
            }

        self.colors_inactive = {
            "green": self.GREEN_inactive,
            "red": self.RED_inactive,
            "yellow": self.YELLOW_inactive,
            "blue": self.BLUE_inactive
        }

        self.colors_active = {
            "green": self.GREEN_active,
            "red": self.RED_active,
            "yellow": self.YELLOW_active,
            "blue": self.BLUE_active
        }

        self.tile_moves = []
        self.bg = pygame.image.load(os.path.join(self.dirname,"..\\resources\\graphics\\simon\\gucci_bg.jpg"))
        self.bg_rect = self.bg.get_rect()

        self.mouse_clicked = False
        self.mouse_coordinates = None, None

        self.tiles_clicked = []

    def main(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    exit()
                elif event.type == MOUSEBUTTONDOWN:
                    self.mouse_clicked = True
                    self.mouse_coordinates = event.pos

            curr_tile = self.tile_clicked()
            if curr_tile is not None:
                self.tiles_clicked.append(curr_tile)
                self.mouse_clicked = False
                self.mouse_coordinates = None, None
 
            self.DISPLAY_SURFACE.blit(self.bg, self.bg_rect)
            for color in self.colors_inactive.keys():
                pygame.draw.rect(self.DISPLAY_SURFACE, self.colors_inactive[color], (self.tiles[color]))

            self.FPS_CLOCK.tick(self.FPS)
            pygame.display.update()

    def tile_clicked(self):
        if self.mouse_coordinates == (None, None):
            return
        for tile in self.tiles.keys():
            if self.tiles[tile].collidepoint(self.mouse_coordinates):
                return tile
        return
if __name__ == "__main__":
    simon = Simon()
    simon.main()


