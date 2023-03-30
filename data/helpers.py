import sys
import pygame

def terminate():
    pygame.quit()
    sys.exit()

def image_center_x_y(image):
    return image.get_width()//2,image.get_height()//2

def to_center_of_screen(screen_width,screen_height, obj_x,obj_y):
   return screen_width // 2 - obj_x, screen_height // 2 - obj_y