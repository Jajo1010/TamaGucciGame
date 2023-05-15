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
        self.FPS = 30
        self.FPS_CLOCK = pygame.time.Clock()
        self.BASICFONT = pygame.font.Font('freesansbold.ttf', 60)
        self.dirname = os.path.dirname(__file__)

        self.GREEN_inactive = (0, 100, 0)
        self.GREEN_active = (0, 200, 0)
        self.RED_inactive = (100, 0, 0)
        self.RED_active = (200, 0, 0)
        self.BLUE_inactive = (0, 0, 100)
        self.BLUE_active = (0, 0, 200)
        self.YELLOW_inactive = (150, 150, 0)
        self.YELLOW_active = (230, 230, 0)
        self.WHITE = (255, 255, 255)

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
        self.bg = pygame.image.load(os.path.join(self.dirname,"..\\..\\resources\\graphics\\simon\\gucci_bg.jpg"))
        self.bg_rect = self.bg.get_rect()

        self.mouse_clicked = False
        self.mouse_coordinates = None, None

        self.user_tiles_clicked = []
        self.guessed_wrong = False

        self.game_exited = False

        self.score = 0

    def main(self):
        pygame.display.update()
        self.start()
        while not self.game_exited:
            self.run_game()

    def run_game(self):
        self.guessed_wrong = False
        self.tile_moves = []
        self.user_tiles_clicked = []
        self.score = 0
        self.draw_score()
        while not self.guessed_wrong and not self.game_exited:
            pygame.time.wait(500)
            self.blit_tiles()
            self.user_moves()
            self.draw_score()
            self.FPS_CLOCK.tick(self.FPS)

    def tile_clicked(self):
        self.mouse_clicked = False
        while not self.mouse_clicked:
            if self.game_exited:
                return
            self.get_event()
            self.FPS_CLOCK.tick(self.FPS)
        for tile in self.tiles.keys():
            if self.tiles[tile].collidepoint(self.mouse_coordinates):
                return tile
        return

    def draw_starting_position(self):
        for color in self.colors_inactive.keys():
            pygame.draw.rect(self.DISPLAY_SURFACE, self.colors_inactive[color], (self.tiles[color]))

    def was_clicked(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.terminate()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                self.game_exited = True
                return
            elif event.type == MOUSEBUTTONDOWN:
                return True
        return False

    def wait_for_click(self):
        while not self.was_clicked():
            if self.game_exited:
                return
            self.FPS_CLOCK.tick(self.FPS)
            pygame.display.update()

    def blit_tiles(self):
        rand_color = random.choice(tuple(self.tiles.keys()))
        self.tile_moves.append(rand_color)
        for color in self.tile_moves:
            pygame.draw.rect(self.DISPLAY_SURFACE, self.colors_active[color], self.tiles[color])
            pygame.display.update()
            pygame.time.wait(200)
            self.draw_starting_position()
            pygame.display.update()
            pygame.time.wait(200)
            self.FPS_CLOCK.tick(self.FPS)

    def get_event(self):
        self.mouse_clicked = False
        self.mouse_coordinates = None, None
        for event in pygame.event.get():
            if event.type == QUIT:
                self.terminate()
            elif event.type == MOUSEBUTTONDOWN:
                self.mouse_clicked = True
                self.mouse_coordinates = event.pos
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                self.game_exited = True
                return

    def user_moves(self):
        for color in self.tile_moves:
            if self.get_tile() != color:
                self.guessed_wrong = True
                return
        self.score += 1

    def get_tile(self):
        curr_tile = None
        while curr_tile is None:
            if self.game_exited:
                return
            curr_tile = self.tile_clicked()
            self.FPS_CLOCK.tick(self.FPS)
        self.user_tiles_clicked.append(curr_tile)
        self.mouse_clicked = False
        self.mouse_coordinates = None, None
        pygame.draw.rect(self.DISPLAY_SURFACE, self.colors_active[curr_tile], self.tiles[curr_tile])
        pygame.display.update()
        pygame.time.wait(200)
        self.draw_starting_position()
        pygame.display.update()
        return curr_tile

    def draw_score(self):
        self.DISPLAY_SURFACE.blit(self.bg, self.bg_rect)
        self.draw_starting_position()
        score =  self.BASICFONT.render(f'Score: {self.score}', True, self.WHITE)
        score_rect = score.get_rect()
        score_rect.topleft = self.WIDTH - 300, 20

        text_font = pygame.font.Font('freesansbold.ttf', 25)
        text_surface = text_font.render("Achieve score 12 to unlock 'NEW GUCCI CLOTHES'", True, (255, 215, 0))
        text_rect = text_surface.get_rect()
        text_rect.center = 400, 550
        self.DISPLAY_SURFACE.blit(text_surface, text_rect)
        self.DISPLAY_SURFACE.blit(score, score_rect)
        pygame.display.update()

    def start(self):
        self.DISPLAY_SURFACE.blit(self.bg, self.bg_rect)
        start_msg = self.BASICFONT.render("Click to start", True, self.WHITE)
        start_msg_rect = start_msg.get_rect()
        start_msg_rect.center = self.WIDTH//2, self.HEIGHT//2
        self.DISPLAY_SURFACE.blit(start_msg, start_msg_rect)
        pygame.display.update()
        self.wait_for_click()

    def terminate(self):
        pygame.quit()
        exit()


def main():
    simon = Simon()
    simon.main()


if __name__ == "__main__":
    main()

