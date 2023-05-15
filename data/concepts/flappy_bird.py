import pygame
from pygame.locals import *
from pygame import mixer
from sys import exit
import random
import os

class FlappyBirdGame:
    def __init__(self):
        pygame.init()
        self.WIDTH = 800
        self.HEIGHT = 600

        self.SKY_COLOR = (135, 206, 235)
        self.WHITE = (255, 255, 255)
        self.DARK_TURQUOISE = (3, 54, 73)
        self.TOWER_COLOR = (100, 100, 100)

        self.TOWER_WIDTH = 50
        self.TOWER_GAP = 300

        self.dirname = os.path.dirname(__file__)

        self.FPS = 60
        self.DISPLAY_SURFACE = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.FPS_CLOCK = pygame.time.Clock()
        self.BASICFONT = pygame.font.Font('freesansbold.ttf', 20)

        self.bg = pygame.image.load(os.path.join(self.dirname,"..\\..\\resources\\graphics\\flappy_bird\\city-bg.png"))
        self.bg = pygame.transform.scale(self.bg, (1600, 768))
        self.bg_rect = pygame.Rect(0, -125, self.WIDTH, self.HEIGHT)

        self.cloud_image = pygame.image.load(os.path.join(self.dirname,"..\\..\\resources\\graphics\\flappy_bird\\cloud.png"))
        self.cloud_image = pygame.transform.scale(self.cloud_image, (184, 100)).convert_alpha(self.DISPLAY_SURFACE)
        self.cloud_rect = pygame.Rect(self.WIDTH, 100, 92, 50)
        
        self.HERO = pygame.image.load(os.path.join(self.dirname,"..\\..\\resources\\graphics\\flappy_bird\\character.png"))
        self.HERO_rect = pygame.Rect(self.WIDTH//3, self.HEIGHT//2, 60, 60)

        mixer.init()
        mixer.music.load(os.path.join(self.dirname,"..\\..\\resources\\sounds\\flappy_bird\\Music_4.mp3"))
        mixer.music.set_volume(0.2)
        
        self.top_towers = []
        self.bottom_towers = []
        self.last_tower_passed = 0

        self.score = 0

        self.ended = False
        self.game_exited = False



    def main(self):
        self.title_screen() 
        mixer.music.play()
        while not self.game_exited:
            self.run_game()
            self.is_over()
        mixer.music.stop()


    def run_game(self):
        self.HERO_rect.y = self.HEIGHT//2
        self.cloud_rect.x = self.WIDTH
        self.top_towers = []
        self.bottom_towers = []
        self.last_tower_passed = 0
        self.first_towers()
        self.score = 0
        self.ended = False
        gravity = -12

        while not self.was_key_pressed_or_was_clicked():
            self.draw_game_state()
            self.FPS_CLOCK.tick(self.FPS)
            pygame.display.update()
        while not self.ended and not self.game_exited:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    self.ended = True
                elif event.type == KEYDOWN and event.key == K_SPACE \
                        or event.type == MOUSEBUTTONDOWN:
                    gravity = -12

            self.HERO_rect.y += gravity
            gravity += 0.75
            self.move_towers()

            for i in range(len(self.top_towers)):
                if self.HERO_rect.colliderect(self.top_towers[i]) or self.HERO_rect.colliderect(self.bottom_towers[i]):
                    self.ended = True

            if self.HERO_rect.y >= self.HEIGHT-50 or self.HERO_rect.y <= 0-50:
                self.ended = True

            if self.HERO_rect.x > self.top_towers[self.last_tower_passed].right:
                self.last_tower_passed = (self.last_tower_passed + 1) % len(self.top_towers)
                self.score += 1

            self.draw_game_state(bg_speed=3)
            self.FPS_CLOCK.tick(self.FPS)
            pygame.display.update()


    def is_over(self):
        game_over_font = pygame.font.Font('freesansbold.ttf', 100)
        game_surface = game_over_font.render('Game', True, self.WHITE)
        over_surface = game_over_font.render('Over', True, self.WHITE)
        game_rect = game_surface.get_rect()
        over_rect = over_surface.get_rect()
        game_rect.center = (self.WIDTH // 2, 150)
        over_rect.center = (self.WIDTH // 2, 250)

        text_font = pygame.font.Font('freesansbold.ttf', 25)
        text_surface = text_font.render("Achieve score 50 to unlock 'NEW GUCCI CLOTHES'", True, (0, 0, 0))
        text_rect = text_surface.get_rect()
        text_rect.center = 400, 435
        self.DISPLAY_SURFACE.blit(text_surface, text_rect)
        self.DISPLAY_SURFACE.blit(game_surface, game_rect)
        self.DISPLAY_SURFACE.blit(over_surface, over_rect)

        pygame.display.update()
        self.wait_for_key_pressed()


    def draw_score(self):
        score_surface = self.BASICFONT.render('Score: ' + str(self.score), True, self.DARK_TURQUOISE)
        score_rect = score_surface.get_rect()
        score_rect.topleft = (self.WIDTH - 120, 10)
        self.DISPLAY_SURFACE.blit(score_surface, score_rect)


    def was_key_pressed_or_was_clicked(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.terminate()
            elif event.type == MOUSEBUTTONDOWN:
                return True
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                self.game_exited = True
                return True
            elif event.type == KEYDOWN:
                return True
        return False


    def wait_for_key_pressed(self):
        """Wait for a player to press any key."""
        msg_surface = self.BASICFONT.render('Press Space to play.', True, self.DARK_TURQUOISE)
        msg_rect = msg_surface.get_rect()
        msg_rect.topleft = (self.WIDTH - 275, self.WIDTH - 225)
        while not self.was_key_pressed_or_was_clicked():
            self.DISPLAY_SURFACE.blit(msg_surface, msg_rect)
            pygame.display.update()


    def title_screen(self):
        title_font = pygame.font.Font('freesansbold.ttf', 100)
        title_surface = title_font.render('Gucci bird', True, (0, 45, 124))
        title_rect = title_surface.get_rect()
        title_rect.center = (self.WIDTH / 2, self.HEIGHT / 2)

        self.DISPLAY_SURFACE.blit(self.bg, self.bg_rect)
        msg_surface = self.BASICFONT.render('Press Space to play.', True, self.DARK_TURQUOISE)
        msg_rect = msg_surface.get_rect()
        msg_rect.center = (self.WIDTH//2, self.WIDTH//2)
        direction = 1
        iterations_to_move = 2
        counter = 0
        while not self.was_key_pressed_or_was_clicked():
            if msg_rect.y >= (self.WIDTH/2):
                direction = -1
            elif msg_rect.y <= (self.WIDTH/2)-20:
                direction = 1
            if counter >= iterations_to_move:
                msg_rect.y += direction
                counter = 0
            else:
                counter += 1
            self.DISPLAY_SURFACE.blit(self.bg, self.bg_rect)
            self.DISPLAY_SURFACE.blit(title_surface, title_rect)
            self.DISPLAY_SURFACE.blit(msg_surface, msg_rect)
            self.FPS_CLOCK.tick(self.FPS)
            pygame.display.update()

    def first_towers(self):
        for i in range(3):
            x = self.WIDTH + i * (self.TOWER_WIDTH + self.TOWER_GAP)
            top_tower = pygame.Rect(x, 0, self.TOWER_WIDTH, random.randint(200, 400))
            bottom_tower = pygame.Rect(x, top_tower.height + self.TOWER_GAP, self.TOWER_WIDTH, self.HEIGHT - top_tower.height - self.TOWER_GAP)
            self.top_towers.append(top_tower)
            self.bottom_towers.append(bottom_tower)


    def draw_towers(self):
        for tower in range(len(self.top_towers)):
            pygame.draw.rect(self.DISPLAY_SURFACE, self.TOWER_COLOR, self.top_towers[tower])
            pygame.draw.rect(self.DISPLAY_SURFACE, self.TOWER_COLOR, self.bottom_towers[tower])


    def move_towers(self):
        for i in range(len(self.top_towers)):
            self.top_towers[i].x -= 5
            self.bottom_towers[i].x -= 5

            # If a pipe goes off-screen, move it to the right and randomize its height
            if self.top_towers[i].right < 0:
                x = max([pipe.right for pipe in self.top_towers]) + self.TOWER_GAP
                self.top_towers[i] = pygame.Rect(x, 0, self.TOWER_WIDTH, random.randint(100, 400))
                self.bottom_towers[i] = pygame.Rect(x, self.top_towers[i].height + self.TOWER_GAP, self.TOWER_WIDTH, self.HEIGHT - self.top_towers[i].height - self.TOWER_GAP)

    def draw_bg(self, bg_speed=0):
        self.DISPLAY_SURFACE.fill(self.SKY_COLOR)
        self.DISPLAY_SURFACE.blit(self.bg, self.bg_rect)
        self.DISPLAY_SURFACE.blit(self.cloud_image, self.cloud_rect)
        
        self.cloud_rect.x -= 1
        self.bg_rect.x -= bg_speed
        if self.cloud_rect.x <= -184:
            self.cloud_rect.x = self.WIDTH
        if self.bg_rect.x <= -800:
            self.bg_rect.x = 0

    def draw_game_state(self, bg_speed=0):
        self.draw_bg(bg_speed)
        self.draw_towers()
        self.DISPLAY_SURFACE.blit(self.HERO, self.HERO_rect)
        self.draw_score()

    def terminate(self):
        pygame.quit()
        exit()

def main():
    flappy = FlappyBirdGame()
    flappy.main()

if __name__ == "__main__":
    main()

