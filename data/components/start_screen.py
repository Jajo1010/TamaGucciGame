import pygame
from pygame.locals import *
import simpleaudio as sa
from constants import *
from helpers import terminate, image_center_x_y, to_center_of_screen, file_list_from_dir, surfaces_from_file_list,is_save,delete_save_file
from helpers import create_save_if_not_default
from spritesheet import Spritesheet
import os

DIRNAME = os.path.dirname(__file__)


def display_start_screen(surface, fps):

    sc_text_inactive = pygame.image.load(os.path.join(
        DIRNAME, "..\\..\\resources\\graphics\\start_screen\\start_inactive.png")).convert_alpha()
    sc_text_active = pygame.image.load(os.path.join(
        DIRNAME, "..\\..\\resources\\graphics\\start_screen\\start_active.png")).convert_alpha()
    sc_new_game = pygame.image.load(os.path.join(
        DIRNAME, "..\\..\\resources\\graphics\\start_screen\\new_game.png")).convert_alpha()
    sc_new_game_active = pygame.image.load(os.path.join(
        DIRNAME, "..\\..\\resources\\graphics\\start_screen\\new_game_active.png")).convert_alpha()
    sc_bg = pygame.image.load(os.path.join(
        DIRNAME, "..\\..\\resources\\graphics\\start_screen\\bg.png"))
    text_width, text_height = sc_text_active.get_width(), sc_text_active.get_height()
    new_game_text_width, new_game_text_height = sc_text_active.get_width(), sc_text_active.get_height()

    
    animation_path = os.path.join(
        DIRNAME, "..\\..\\resources\\graphics\\start_screen\\animation\\")
    character_spritesheet = Spritesheet(
        f"{animation_path}\\character_spritesheet.png")
    character_spritesheet_filenames = character_spritesheet.list_of_files()
    character_animation = [character_spritesheet.parse_sprite(
        file) for file in character_spritesheet_filenames]
    animation_frame = 0

    sound = sa.WaveObject.from_wave_file(os.path.join(
        DIRNAME, "..\\..\\resources\\sounds\\sound_effects\\pop.wav"))


    game_started = False

    while not game_started:
        animation_frame = (animation_frame +
                           1) % len(character_spritesheet_filenames)
        draw_start_screen(surface, sc_bg)
        
        if is_save():
            draw_new_game_text(surface, sc_new_game, sc_new_game_active, new_game_text_width, new_game_text_height)
            if handle_click_start_game(*top_left_corner_text(SCREEN_WIDTH, (SCREEN_HEIGHT+100+text_height), new_game_text_width, new_game_text_height), text_width, text_height):
                delete_save_file()
                create_save_if_not_default()
                game_started = True

        draw_animated_character(surface, character_animation, animation_frame)
        
        if handle_click_start_game(*top_left_corner_text(SCREEN_WIDTH, SCREEN_HEIGHT, text_width, text_height), text_width, text_height):
            sound.play()
            create_save_if_not_default()
            game_started = True
        
        handle_quit()
        draw_start_text(surface, sc_text_inactive,
                        sc_text_active, text_width, text_height)
        
        pygame.display.update()
        fps.tick(FPS)


def draw_start_screen(surface, sc_bg):
    return surface.blit(sc_bg, (0, 0))


def draw_start_text(surface, sc_text_inactive, sc_text_active, text_width, text_height):

    inactive_center_x, inactive_center_y = to_center_of_screen(
        SCREEN_WIDTH, SCREEN_HEIGHT, *image_center_x_y(sc_text_inactive))
    active_center_x, active_center_y = to_center_of_screen(
        SCREEN_WIDTH, SCREEN_HEIGHT, *image_center_x_y(sc_text_active))

    if (handle_hover(*top_left_corner_text(SCREEN_WIDTH, SCREEN_HEIGHT, text_width, text_height), text_width, text_height)):
        return surface.blit(sc_text_active, (active_center_x, active_center_y))

    return surface.blit(sc_text_inactive, (inactive_center_x, inactive_center_y))

def draw_new_game_text(surface, new_game, new_game_active, text_width, text_height):

    new_game_x, new_game_y = to_center_of_screen(
        SCREEN_WIDTH, SCREEN_HEIGHT, *image_center_x_y(new_game))
    new_game_x_active, new_game_y_active = to_center_of_screen(
        SCREEN_WIDTH, SCREEN_HEIGHT, *image_center_x_y(new_game_active))
    if (handle_hover(*top_left_corner_text(SCREEN_WIDTH, (SCREEN_HEIGHT+100+text_height), text_width, text_height), text_width, text_height)):
        return surface.blit(new_game_active, (new_game_x_active, new_game_y_active+100))
    
    return surface.blit(new_game, (new_game_x, new_game_y+100))

def draw_animated_character(surface, character, frame):
    return surface.blit(character[frame], (-35, SCREEN_HEIGHT-330))


def handle_hover(cord_x, cord_y, width, height):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if (mouse_x >= cord_x and mouse_x <= cord_x+width) and (mouse_y >= cord_y and mouse_y <= height+cord_y):
        return True


def handle_click_start_game(cord_x, cord_y, width, height):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if pygame.event.get(MOUSEBUTTONUP):
        if (mouse_x >= cord_x and mouse_x <= cord_x+width) and (mouse_y >= cord_y and mouse_y <= height+cord_y):
            return True

def handle_click_new_game(cord_x, cord_y, width, height):
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
