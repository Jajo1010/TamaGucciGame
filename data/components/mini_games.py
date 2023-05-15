import pygame
from pygame import mixer
import simpleaudio as sa
import concepts.flappy_bird as fb
import concepts.simon as simon_game
import concepts.water_hop as wh
from components.clothing_progressbar import ProgressBar
from pygame.locals import *
from constants import *
from helpers import terminate, image_center_x_y, to_center_of_screen, file_list_from_dir, surfaces_from_file_list
from spritesheet import Spritesheet
import os

DIRNAME = os.path.dirname(__file__)


def display_games_screen(surface, fps):

    # TODO Migrate to spritesheet
    bg = pygame.image.load(os.path.join(
        DIRNAME, "..\\..\\resources\\graphics\\game_choice\\bg.png"))
    character = pygame.image.load(os.path.join(
        DIRNAME, "..\\..\\resources\\graphics\\character\\clean.png"))

    gucci_bird = pygame.image.load(os.path.join(
        DIRNAME, "..\\..\\resources\\graphics\\game_choice\\game_icons\\gucci_bird.png")).convert_alpha()
    simon = pygame.image.load(os.path.join(
        DIRNAME, "..\\..\\resources\\graphics\\game_choice\\game_icons\\simon.png")).convert_alpha()
    water_drop = pygame.image.load(os.path.join(
        DIRNAME, "..\\..\\resources\\graphics\\game_choice\\game_icons\\water_drop.png")).convert_alpha()

    soon = pygame.image.load(os.path.join(
        DIRNAME, "..\\..\\resources\\graphics\\game_choice\\game_icons\\soon.png")).convert_alpha()
    soon_hover = pygame.image.load(os.path.join(
        DIRNAME, "..\\..\\resources\\graphics\\game_choice\\game_icons\\soon_hover.png")).convert_alpha()

    icon_text = pygame.image.load(os.path.join(
        DIRNAME, "..\\..\\resources\\graphics\\game_choice\\game_icons\\icon_text.png")).convert_alpha()

    home_icon = pygame.image.load(os.path.join(
        DIRNAME, "..\\..\\resources\\graphics\\game_choice\\home_icon.png")).convert_alpha()
    home_icon_hover = pygame.image.load(os.path.join(
        DIRNAME, "..\\..\\resources\\graphics\\game_choice\\home_icon_hover.png")).convert_alpha()

    gucci_bird_hover = pygame.image.load(os.path.join(
        DIRNAME, "..\\..\\resources\\graphics\\game_choice\\game_icons\\gucci_bird_hover.png")).convert_alpha()
    simon_hover = pygame.image.load(os.path.join(
        DIRNAME, "..\\..\\resources\\graphics\\game_choice\\game_icons\\simon_hover.png")).convert_alpha()
    water_drop_hover = pygame.image.load(os.path.join(
        DIRNAME, "..\\..\\resources\\graphics\\game_choice\\game_icons\\water_drop_hover.png")).convert_alpha()

    icons = [gucci_bird, simon, water_drop]
    icons_hover = [gucci_bird_hover, simon_hover, water_drop_hover]

    icon_width, icon_height = gucci_bird.get_width(
    ), gucci_bird.get_height()

    home_icon_width, home_icon_height = home_icon.get_width(
    ), home_icon.get_height()

    icons_positions = {
        gucci_bird_hover: [110, 100],
        simon_hover: [335, 100],
        water_drop_hover: [560, 100]
    }

    icons_functions = {
        fb: [110, 100,icon_width,icon_height],
        simon_game: [335, 100,icon_width,icon_height],
        wh: [560, 100,icon_width,icon_height],
        "home_button" : [10,400,home_icon_width,home_icon_height]
    }
    
    mixer.init()
    mixer.music.set_volume(0.2)

    sound = sa.WaveObject.from_wave_file(os.path.join(
        DIRNAME, "..\\..\\resources\\sounds\\sound_effects\\pop.wav"))

    mini_games_state = False

    while not mini_games_state:
        draw_main_screen(surface, bg)
        draw_mini_games(surface, icons, icons_hover, 110,
                        100, icon_width, icon_height)
        draw_soon_games(surface, soon, 110,
                        SCREEN_HEIGHT-(200+icon_height), icon_width, icon_height)
        draw_home_icon(surface, home_icon, 10, SCREEN_HEIGHT //
                       2+100, home_icon_width, home_icon_height)

        draw_icon_text(surface, icon_text, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

        handle_hover_home_icon(surface, 10, SCREEN_HEIGHT //
                                2+100, home_icon_width, home_icon_height, home_icon_hover)
        handle_hover_game_icons(surface, icons_positions,
                                icon_width, home_icon_width)
        
        if handle_clicks(sound,icons_functions):
            mini_games_state = True

        handle_quit()
        pygame.display.update()
        fps.tick(FPS)


def draw_main_screen(surface, bg):
    return surface.blit(bg, (0, 0))


def draw_mini_games(surface, mini_games_icons: list, mini_games_icons_hover: list, cord_x, cord_y, width, height):
    for index, icon in enumerate(mini_games_icons):
        surface.blit(icon, (cord_x+(98+width)*index, cord_y, width, height))


def draw_soon_games(surface, soon: object, cord_x, cord_y, width, height):
    for index in range(3):
        surface.blit(soon, (cord_x+(98+width)*index, cord_y, width, height))


def draw_icon_text(surface, icon_text: object, cord_x, cord_y, width, height):
    return surface.blit(icon_text, (cord_x, cord_y, width, height))


def draw_home_icon(surface, home_icon: object, cord_x, cord_y, width, height):
    return surface.blit(home_icon, (cord_x, cord_y, width, height))


def handle_clicks(sound,positions: dict):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if pygame.event.get(MOUSEBUTTONUP):
        for clickable in positions:
            if clickable == "home_button" and (mouse_x >= positions[clickable][0] and mouse_x <= positions[clickable][0]+positions[clickable][2]) and (mouse_y >= positions[clickable][1] and mouse_y <= positions[clickable][3]+positions[clickable][1]) :
                sound.play()
                return True
            elif (mouse_x >= positions[clickable][0] and mouse_x <= positions[clickable][0]+positions[clickable][2]) and (mouse_y >= positions[clickable][1] and mouse_y <= positions[clickable][3]+positions[clickable][1]):
                sound.play()
                clickable.main()
                mixer.music.load(os.path.join(DIRNAME,"..\\..\\resources\\sounds\\Music_3.mp3"))
                mixer.music.play()
                

def handle_hover_game_icons(surface, positions: dict, width, height):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    for image in positions:
        if (mouse_x >= positions[image][0] and mouse_x <= positions[image][0]+width) and (mouse_y >= positions[image][1] and mouse_y <= height+positions[image][1]):
            return surface.blit(image, (positions[image][0], positions[image][1], width, height))


def handle_hover_home_icon(surface, cord_x, cord_y, width, height, hover_image):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if (mouse_x >= cord_x and mouse_x <= cord_x+width) and (mouse_y >= cord_y and mouse_y <= height+cord_y):
        return surface.blit(hover_image, (10, SCREEN_HEIGHT//2+100, width, height))


def handle_quit():
    """Exit game on QUIT event"""
    if pygame.event.get(QUIT):
        terminate()
