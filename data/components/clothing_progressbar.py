import pygame
from constants import *
import pygame
import os


class ProgressBar:
    def __init__(self, surface, manager) -> None:
        
        self.surface: object = surface
        
        self.clothes_manager = manager
        self.number_of_bars: int = manager.get_number_of_available_clothing()
        self.active_bars: int = manager.get_number_of_unlocked_clothing()
        

        self.dirname = os.path.dirname(__file__)
        self.inactive_bar = pygame.image.load(os.path.join(self.dirname, "..\\..\\resources\\graphics\\main_screen\\inactive_bar.png"))
        self.active_bar = pygame.image.load(os.path.join(self.dirname, "..\\..\\resources\\graphics\\main_screen\\active_bar.png"))
        self.drip_bar = pygame.image.load(os.path.join(self.dirname, "..\\..\\resources\\graphics\\main_screen\\drip_bar.png"))

        self.padding: int = 6
        self.bars_padding = self.inactive_bar.get_width() + self.padding

    def __str__(self) -> str:
        return f"Numbers of active bars : {self.active_bars}, number of bars : {self.number_of_bars}"

    def __eq__(self, __value: object) -> bool:
        return self.active_bars == __value.active_bars

    def draw(self) -> object:
        self.surface.blit(self.drip_bar,(20,0))
        for i in range(self.number_of_bars):
            if i < self.active_bars:
                self.__draw_active_bar((self.bars_padding*i)+175, self.drip_bar.get_height()//2-23)
            else:
                self.__draw_inactive_bar((self.bars_padding*i)+175, self.drip_bar.get_height()//2-23)
        
    def __draw_active_bar(self, pos_x, pos_y) -> object:
        return self.surface.blit(self.active_bar,(pos_x,pos_y))

    def __draw_inactive_bar(self, pos_x, pos_y) -> object:
        return self.surface.blit(self.inactive_bar,(pos_x,pos_y))
