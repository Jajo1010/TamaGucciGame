import sys
import os
import pygame

def terminate():
    pygame.quit()
    sys.exit()

def image_center_x_y(image):
    return image.get_width()//2,image.get_height()//2

def to_center_of_screen(screen_width,screen_height, obj_x,obj_y):
   return screen_width // 2 - obj_x, screen_height // 2 - obj_y

def file_list_from_dir(path):
    return [file for file in os.listdir(path)]

def surfaces_from_file_list(path,files_list):
    return [pygame.image.load(f"{path}\\{sprite}").convert_alpha() for sprite in files_list]