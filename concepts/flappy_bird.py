import pygame
from pygame.locals import *
from sys import exit
import random
import os

WIDTH = 800
HEIGHT = 600

SKY_COLOR = (135, 206, 235)
WHITE = (255, 255, 255)
DARK_TURQUOISE = (3, 54, 73)
TOWER_COLOR = (100, 100, 100)


TOWER_WIDTH = 50
TOWER_GAP = 300

dirname = os.path.dirname(__file__)

def main():
    pygame.init()
    
    global DISPLAY_SURFACE, FPS_CLOCK, BASICFONT, FPS

    FPS = 60
    DISPLAY_SURFACE = pygame.display.set_mode((WIDTH, HEIGHT))
    FPS_CLOCK = pygame.time.Clock()
    BASICFONT = pygame.font.Font('freesansbold.ttf', 20)
    
    bg = pygame.image.load(os.path.join(dirname,"..\\resources\\graphics\\flappy_bird\\city-bg.png"))
    cloud_image = pygame.image.load(os.path.join(dirname,"..\\resources\\graphics\\flappy_bird\\cloud.png"))

    title_screen(bg)
    
    while True:
        run_game(bg,cloud_image)
        is_over()


def run_game(bg,cloud_image):
    HERO = pygame.Rect(WIDTH//3, HEIGHT-500, 50, 50)
    cloud_rect = pygame.Rect(WIDTH, 100, 92, 50)
    bg_rect = pygame.Rect(0, -125, WIDTH, HEIGHT)
    gravity = -12
    top_towers = []
    bottom_towers = []
    last_tower_passed = 0
    score = 0
    first_towers(top_towers, bottom_towers)
    ended = False

    while not ended:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                ended = True
            elif event.type == KEYUP and event.key == K_SPACE \
                    or event.type == MOUSEBUTTONDOWN:
                gravity = -12

        HERO.y += gravity
        gravity += 0.75
        move_towers(top_towers, bottom_towers)

        for i in range(len(top_towers)):
            if HERO.colliderect(top_towers[i]) or HERO.colliderect(bottom_towers[i]):
                ended = True

        if HERO.y >= HEIGHT-50 or HERO.y <= 0-50:
            ended = True

        if HERO.x > top_towers[last_tower_passed].right:
            last_tower_passed = (last_tower_passed + 1) % len(top_towers)
            score += 1

        draw_game_state(cloud_rect, bg_rect, top_towers, bottom_towers, HERO,bg,cloud_image, score)
        FPS_CLOCK.tick(FPS)
        pygame.display.flip()


def is_over():
    game_over_font = pygame.font.Font('freesansbold.ttf', 100)
    game_surface = game_over_font.render('Game', True, WHITE)
    over_surface = game_over_font.render('Over', True, WHITE)
    game_rect = game_surface.get_rect()
    over_rect = over_surface.get_rect()
    game_rect.center = (WIDTH // 2, 150)
    over_rect.center = (WIDTH // 2, 250)

    DISPLAY_SURFACE.blit(game_surface, game_rect)
    DISPLAY_SURFACE.blit(over_surface, over_rect)
    pygame.display.update()
    wait_for_key_pressed()


def draw_score(score):
    score_surface = BASICFONT.render('Score: ' + str(score), True, DARK_TURQUOISE)
    score_rect = score_surface.get_rect()
    score_rect.topleft = (WIDTH - 120, 10)
    DISPLAY_SURFACE.blit(score_surface, score_rect)


def was_key_pressed():
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            terminate()
        else:
            return True

    """Exit game on QUIT event, or return True if key was pressed."""
    if pygame.event.get(QUIT): # noqa
        terminate()
    return False # noqa


def wait_for_key_pressed():
    """Wait for a player to press any key."""
    msg_surface = BASICFONT.render('Press Space to play.', True, DARK_TURQUOISE)
    msg_rect = msg_surface.get_rect()
    msg_rect.topleft = (WIDTH - 275, WIDTH - 225)
    while not was_key_pressed():
        DISPLAY_SURFACE.blit(msg_surface, msg_rect)
        pygame.display.update()


def title_screen(bg):
    bg = pygame.transform.scale(bg, (1600, 768))
    bg_rect = pygame.Rect(0, -125, WIDTH, HEIGHT)

    title_font = pygame.font.Font('freesansbold.ttf', 100)
    title_surface = title_font.render('Gucci bird', True, (0, 45, 124))
    title_rect = title_surface.get_rect()
    title_rect.center = (WIDTH / 2, HEIGHT / 2)

    DISPLAY_SURFACE.blit(bg, bg_rect)
    msg_surface = BASICFONT.render('Press Space to play.', True, DARK_TURQUOISE)
    msg_rect = msg_surface.get_rect()
    msg_rect.center = (WIDTH//2, WIDTH//2)
    direction = 1
    iterations_to_move = 2
    counter = 0
    while not was_key_pressed():
        if msg_rect.y >= (WIDTH/2):
            direction = -1
        elif msg_rect.y <= (WIDTH/2)-20:
            direction = 1
        if counter >= iterations_to_move:
            msg_rect.y += direction
            counter = 0
        else:
            counter += 1
        DISPLAY_SURFACE.blit(bg, bg_rect)
        DISPLAY_SURFACE.blit(title_surface, title_rect)
        DISPLAY_SURFACE.blit(msg_surface, msg_rect)
        FPS_CLOCK.tick(FPS)
        pygame.display.update()

def first_towers(top_towers: list, bottom_towers: list):
    for i in range(3):
        x = WIDTH + i * (TOWER_WIDTH + TOWER_GAP)
        top_tower = pygame.Rect(x, 0, TOWER_WIDTH, random.randint(200, 400))
        bottom_tower = pygame.Rect(x, top_tower.height + TOWER_GAP, TOWER_WIDTH, HEIGHT - top_tower.height - TOWER_GAP)
        top_towers.append(top_tower)
        bottom_towers.append(bottom_tower)


def draw_towers(top_towers: list, bottom_towers: list):
    for tower in range(len(top_towers)):
        pygame.draw.rect(DISPLAY_SURFACE, TOWER_COLOR, top_towers[tower])
        pygame.draw.rect(DISPLAY_SURFACE, TOWER_COLOR, bottom_towers[tower])


def move_towers(top_towers, bottom_towers):
    for i in range(len(top_towers)):
        top_towers[i].x -= 5
        bottom_towers[i].x -= 5

        # If a pipe goes off-screen, move it to the right and randomize its height
        if top_towers[i].right < 0:
            x = max([pipe.right for pipe in top_towers]) + TOWER_GAP
            top_towers[i] = pygame.Rect(x, 0, TOWER_WIDTH, random.randint(100, 400))
            bottom_towers[i] = pygame.Rect(x, top_towers[i].height + TOWER_GAP, TOWER_WIDTH, HEIGHT - top_towers[i].height - TOWER_GAP)

def draw_bg(cloud_rect, bg_rect,bg,cloud_image):

    cloud_image = pygame.transform.scale(cloud_image, (184, 100)).convert_alpha(DISPLAY_SURFACE)
    bg = pygame.transform.scale(bg, (1600, 768))

    DISPLAY_SURFACE.fill(SKY_COLOR)
    DISPLAY_SURFACE.blit(bg, bg_rect)
    DISPLAY_SURFACE.blit(cloud_image, cloud_rect)
    
    cloud_rect.x -= 1
    bg_rect.x -= 3
    if cloud_rect.x <= -184:
        cloud_rect.x = WIDTH
    if bg_rect.x <= -800:
        bg_rect.x = 0

def draw_game_state(cloud_rect, bg_rect, top_towers, bottom_towers, HERO,bg,cloud_image, score):
    draw_bg(cloud_rect, bg_rect,bg,cloud_image)
    draw_towers(top_towers, bottom_towers)
    pygame.draw.rect(DISPLAY_SURFACE, (0, 255, 0), HERO)
    draw_score(score)

def terminate():
    pygame.quit()
    exit()

if __name__ == "__main__":
    main()

