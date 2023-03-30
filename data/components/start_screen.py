from constants import *
import pygame
from pygame.locals import *
from helpers import terminate, image_center_x_y, to_center_of_screen, file_list_from_dir, surfaces_from_file_list
import os

START_SURFACE = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
FPS_CLOCK = pygame.time.Clock()

dirname = os.path.dirname(__file__)

def picovina(strpng):
    return int(strpng.split(".")[0])

def display_start_screen():
    sc_text_inactive = pygame.image.load(os.path.join(
        dirname, "..\\..\\resources\\graphics\\start_inactive.png")).convert_alpha()
    sc_text_active = pygame.image.load(os.path.join(
        dirname, "..\\..\\resources\\graphics\\start_active.png")).convert_alpha()
    sc_bg = pygame.image.load(os.path.join(
        dirname, "..\\..\\resources\\graphics\\start_screen_clean.png"))

    animation_path = os.path.join(
        dirname, "..\\..\\resources\\graphics\\animation\\pointing")

    sprite_file_names = sorted(file_list_from_dir(animation_path),key= lambda item: int(item.split('.')[0]))
    sprites = surfaces_from_file_list(animation_path, sprite_file_names)
    text_width, text_height = sc_text_active.get_width(), sc_text_active.get_height()

    animation_frame = 0

    game_started = False
    while not game_started:
        animation_frame = (animation_frame + 1) % len(sprites)


        draw_start_screen(sc_bg)
        draw_animated_character(sprites,animation_frame)
        if handle_click(*top_left_corner_text(SCREEN_WIDTH, SCREEN_HEIGHT, text_width, text_height), text_width, text_height):
            game_started = True

        handle_quit()
        draw_start_text(sc_text_inactive, sc_text_active, text_width, text_height)
        pygame.display.update()
        FPS_CLOCK.tick(FPS)


def draw_start_screen(sc_bg):
    return START_SURFACE.blit(sc_bg, (0, 0))


def draw_start_text(sc_text_inactive, sc_text_active, text_width, text_height):

    inactive_center_x, inactive_center_y = to_center_of_screen(
        SCREEN_WIDTH, SCREEN_HEIGHT, *image_center_x_y(sc_text_inactive))
    active_center_x, active_center_y = to_center_of_screen(
        SCREEN_WIDTH, SCREEN_HEIGHT, *image_center_x_y(sc_text_active))

    if (handle_hover(*top_left_corner_text(SCREEN_WIDTH, SCREEN_HEIGHT, text_width, text_height), text_width, text_height)):
        return START_SURFACE.blit(sc_text_active, (active_center_x, active_center_y))

    return START_SURFACE.blit(sc_text_inactive, (inactive_center_x, inactive_center_y))


def draw_animated_character(character, frame):
    x, y = character[frame].get_width(),character[frame].get_height()
    return START_SURFACE.blit(character[frame], (0, SCREEN_HEIGHT-y))


def handle_hover(cord_x, cord_y, width, height):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if (mouse_x >= cord_x and mouse_x <= cord_x+width) and (mouse_y >= cord_y and mouse_y <= height+cord_y):
        return True


def handle_click(cord_x, cord_y, width, height):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if pygame.event.get(MOUSEBUTTONUP):
        if (mouse_x >= cord_x and mouse_x <= cord_x+width) and (mouse_y >= cord_y and mouse_y <= height+cord_y):
            return True


def top_left_corner_text(bg_w, bg_h, x_obj, y_obj):
    return (bg_w-x_obj)//2, (bg_h-y_obj)//2


def handle_quit():
    """Exit game on QUIT event"""
    if pygame.event.get(QUIT):
        terminate()
