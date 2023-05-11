import pygame
from pygame.locals import *


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
        self.ring_gap = 115
        self.rings = [pygame.Rect(self.ring_gap*i, 500, 80, 30) for i in range(1, 11)] 
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

            self.draw_screen()
            self.handle_click()
            pygame.display.update()
            self.FPS_CLOCK.tick(self.FPS)
            

    def was_clicked(self):
        if pygame.event.get(eventtype=MOUSEBUTTONDOWN):
            return True

    def handle_click(self):
        for event in pygame.event.get(eventtype=MOUSEBUTTONDOWN):
            if event.button == 1:
                self.score += 1
                self.move_rings()
            elif event.button == 3:
                self.score += 2
                self.move_rings()
                self.move_rings()

    def wait_for_click(self):
        while not self.was_clicked():
            self.FPS_CLOCK.tick(self.FPS)

    def move_rings(self):
        for ring in self.rings:
            ring.x -= 115
            if ring.right <= 0:
                ring.left = 1035

    def draw_screen(self):
        self.screen.fill(self.BLUE)
        self.draw_rings()
        pygame.draw.rect(self.screen, self.GREY, self.HERO)
        self.draw_score()

    def draw_rings(self):
        for ring in self.rings:
            pygame.draw.rect(self.screen, self.YELLOW, ring)

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
