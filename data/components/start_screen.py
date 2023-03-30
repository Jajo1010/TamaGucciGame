from constants import *
import pygame
from pygame.locals import *
from helpers import terminate, image_center_x_y, to_center_of_screen
import os

dirname = os.path.dirname(__file__)

START_SURFACE = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
FPS_CLOCK = pygame.time.Clock()


def display_start_screen():
    sc_text_inactive = pygame.image.load(os.path.join(
        dirname, "..\\..\\resources\\graphics\\start_inactive.png")).convert_alpha()
    sc_text_active = pygame.image.load(os.path.join(
        dirname, "..\\..\\resources\\graphics\\start_active.png")).convert_alpha()
    sc_bg = pygame.image.load(os.path.join(
        dirname, "..\\..\\resources\\graphics\\start_screen_clean.png"))
    draw_start_screen(sc_bg)
    while True:
        draw_start_text(sc_text_inactive, sc_text_active)
        handle_quit()
        pygame.display.update()
        FPS_CLOCK.tick(FPS)


def draw_start_screen(sc_bg):
    return START_SURFACE.blit(sc_bg, (0, 0))

def draw_start_text(sc_text_inactive, sc_text_active):

    text_width, text_height = sc_text_active.get_width(), sc_text_active.get_height()

    inactive_center_x, inactive_center_y = to_center_of_screen(
        SCREEN_WIDTH, SCREEN_HEIGHT, *image_center_x_y(sc_text_inactive))
    active_center_x, active_center_y = to_center_of_screen(
        SCREEN_WIDTH, SCREEN_HEIGHT, *image_center_x_y(sc_text_active))

    if (handle_hover(*top_left_corner_text(SCREEN_WIDTH, SCREEN_HEIGHT, text_width, text_height), text_width, text_height)):
        return START_SURFACE.blit(sc_text_active, (active_center_x, active_center_y))

    return START_SURFACE.blit(sc_text_inactive, (inactive_center_x, inactive_center_y))


def handle_hover(cord_x, cord_y, width, height):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if (mouse_x >= cord_x and mouse_x <= cord_x+width) and (mouse_y >= cord_y and mouse_y <= height+cord_y):
        return True


def top_left_corner_text(bg_w, bg_h, x_obj, y_obj):
    return (bg_w-x_obj)//2, (bg_h-y_obj)//2


def handle_quit():
    """Exit game on QUIT event"""
    if pygame.event.get(QUIT):
        terminate()
