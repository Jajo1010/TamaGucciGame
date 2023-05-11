import pygame
from components.clothing_progressbar import ProgressBar
from pygame.locals import *
from constants import *
from helpers import terminate, image_center_x_y, to_center_of_screen, file_list_from_dir, surfaces_from_file_list
from spritesheet import Spritesheet
import os

DIRNAME = os.path.dirname(__file__)


def display_main_screen(surface, fps):
    bg = pygame.image.load(os.path.join(
        DIRNAME, "..\\..\\resources\\graphics\\main_screen\\bg.png"))
    character = pygame.image.load(os.path.join(
        DIRNAME, "..\\..\\resources\\graphics\\character\\clean.png"))
    mini_games = pygame.image.load(os.path.join(
        DIRNAME, "..\\..\\resources\\graphics\\main_screen\\mini_games.png")).convert_alpha()
    mini_games_hover = pygame.image.load(os.path.join(
        DIRNAME, "..\\..\\resources\\graphics\\main_screen\\mini_games_hover.png")).convert_alpha()

    mini_games_width, mini_games_height = mini_games.get_width(
    ), mini_games.get_height()

    mini_games_state = False

    while not mini_games_state:
        draw_main_screen(surface, bg)
        draw_character(surface, character)
        draw_mini_games(surface, mini_games, mini_games_hover, SCREEN_WIDTH -
                        175, SCREEN_HEIGHT//2+100, mini_games_width, mini_games_height)

        if handle_click(SCREEN_WIDTH-175, SCREEN_HEIGHT//2+100, mini_games_width, mini_games_height):
            mini_games_state = True

        handle_quit()
        pygame.display.update()
        fps.tick(FPS)


def draw_main_screen(surface, bg):
    return surface.blit(bg, (0, 0))


def draw_character(surface, character):
    return surface.blit(character, (SCREEN_WIDTH//2-130, SCREEN_HEIGHT//2-110))


def draw_mini_games(surface, mini_games_icon, mini_games_icon_hover, cord_x, cord_y, width, height):
    if handle_hover(cord_x, cord_y, width, height):
        return surface.blit(mini_games_icon_hover, (SCREEN_WIDTH-175, SCREEN_HEIGHT//2+100))
    return surface.blit(mini_games_icon, (SCREEN_WIDTH-175, SCREEN_HEIGHT//2+100))


def handle_click(cord_x, cord_y, width, height):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if pygame.event.get(MOUSEBUTTONUP):
        if (mouse_x >= cord_x and mouse_x <= cord_x+width) and (mouse_y >= cord_y and mouse_y <= height+cord_y):
            return True


def handle_hover(cord_x, cord_y, width, height):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if (mouse_x >= cord_x and mouse_x <= cord_x+width) and (mouse_y >= cord_y and mouse_y <= height+cord_y):
        return True


def handle_quit():
    """Exit game on QUIT event"""
    if pygame.event.get(QUIT):
        terminate()
