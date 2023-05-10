import pygame
from constants import *
import pygame


class ProgressBar:
    def __init__(self, surface, max) -> None:
        self.number_of_bars: int = max
        self.active_bars: int = 0
        self.bar_height: int = 50
        self.bar_width: int = 50
        self.padding: int = self.bar_width + 10
        self.surface: object = surface

    def __str__(self) -> str:
        return f"Numbers of active bars : {self.active_bars}, number of bars : {self.number_of_bars}"

    def __eq__(self, __value: object) -> bool:
        return self.active_bars == __value.active_bars

    def add_bar(self) -> None:
        if self.active_bars + 1 <= self.number_of_bars:
            self.active_bars += 1

    def remove_bar(self) -> None:
        if self.active_bars - 1 >= 0:
            self.active_bars -= 1

    def draw(self) -> object:
        pygame.draw.rect(self.surface, (124, 124, 124),
                         pygame.Rect(0, 0, SCREEN_WIDTH, 100))
        for i in range(self.number_of_bars):
            if i <= self.active_bars:
                self.__draw_active_bar(self.padding*i, 50)
            else:
                self.__draw_inactive_bar(self.padding*i, 50)

    def __draw_active_bar(self, pos_x, pos_y) -> object:
        return pygame.draw.rect(self.surface, (255, 255, 255), pygame.Rect(pos_x, pos_y, self.bar_width, self.bar_height))

    def __draw_inactive_bar(self, pos_x, pos_y) -> object:
        return pygame.draw.rect(self.surface, (0, 0, 0), pygame.Rect(pos_x, pos_y, self.bar_width, self.bar_height))
