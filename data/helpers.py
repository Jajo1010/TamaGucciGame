import sys
import os
import pygame
import json
import shutil

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

def create_save_if_not_default():
    save_found = False
    for files in os.listdir(os.getcwd()):
        if "save.json" in files:
            save_found = True
    if not save_found:
        shutil.copy("default.json", "save.json") 

def is_save():
    save_found = False
    for files in os.listdir(os.getcwd()):
        if "save.json" in files:
            save_found = True
    return save_found

def delete_save_file():
    file_path = os.path.join(os.getcwd(), "save.json")  
    if os.path.exists(file_path):
        os.remove(file_path)
