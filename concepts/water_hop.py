import pygame
from pygame.locals import *

class WaterHop:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.FPS = 30
        self.FPS_CLOCK = pygame.time.Clock()
        self.BLUE = (30,144,255)
        self.ended = False

    def main(self):
        while not self.ended:
            self.screen.fill(self.BLUE)
            pygame.display.update()
            self.FPS_CLOCK.tick(self.FPS)
            if self.was_clicked():
                self.ended = True

    def was_clicked(self):
        if pygame.event.get(eventtype=MOUSEBUTTONDOWN):
            return True

    def handle_click(self):
        for event in pygame.event.get(eventtype=MOUSEBUTTONDOWN):
            if event.button == 1:
                return True
            elif event.button == 3:
                return True

    def wait_for_clicked(self):
        while not self.was_clicked():
            self.FPS_CLOCK.tick(self.FPS)



if __name__ == "__main__":
    WaterHop().main()