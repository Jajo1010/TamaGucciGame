import pygame
from pygame.locals import *

left = 15
ring = pygame.Rect(left, 500, 80, 30)

class WaterHop:
    def __init__(self):
        pygame.init()
        self.WIDTH = 800
        self.HEIGHT = 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.FPS = 30
        self.FPS_CLOCK = pygame.time.Clock()

        self.YELLOW = (230, 230, 0)
        self.BLUE = (30,144,255)
        self.GREY = (100, 100, 100)
        self.DARK_TURQUOISE = (3, 54, 73)

        self.ended = False
        self.ring_gap = 100
        self.rings = [pygame.Rect((left+self.ring_gap)*i, 500, 80, 30) for i in range(1, 10)] 
        self.score = 0
        self.starting_y_axis = 450
        self.HERO = pygame.rect.Rect(125, self.starting_y_axis, 50, 50)
        self.BASICFONT = pygame.font.Font('freesansbold.ttf', 30)

    def main(self):
        while not self.ended:
            if pygame.event.get(QUIT):
                self.terminate()
            elif self.want_to_exit_game():
                return
            self.screen.fill(self.BLUE)
            self.draw_rings()
            pygame.draw.rect(self.screen, self.GREY, self.HERO)
            self.draw_score()
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

    def draw_rings(self):
        for i in range(len(self.rings)):
            pygame.draw.rect(self.screen, self.YELLOW, self.rings[i])

    def draw_score(self):
        score_surface = self.BASICFONT.render('Score: ' + str(self.score), True, self.DARK_TURQUOISE)
        score_rect = score_surface.get_rect()
        score_rect.topleft = (self.WIDTH - 150, 30)
        self.screen.blit(score_surface, score_rect)

    def want_to_exit_game(self):
        for event in pygame.event.get(KEYDOWN):
            if event.key == K_ESCAPE:
                return True

    def terminate(self):
        pygame.quit()
        exit()

if __name__ == "__main__":
    WaterHop().main()
