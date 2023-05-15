import pygame
from pygame.locals import *
from sys import exit
from random import shuffle


FPS = 30
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
CARDSIZE = 40
GAPSIZE = 10

BLACK = (0, 0, 0)

NAVYBLUE = (60, 60, 100)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)

BGCOLOR = NAVYBLUE
CARDCOLOR = WHITE
HIGHLIGHTCOLOR = BLUE

ALLCOLORS = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN)
ALLPICTURES = ('amogus', 'mike', 'lux', 'pepega', 'gigachad',
             'shrek', 'rat', 'kappa', 'clueless', 'kekw', 'frie',
            'black_man', 'sniffa', '5head', 'omegalul', 'kkonaw', 'gachihyper',
             'waytoodank', 'catjam', 'huh')


class Picture:
    def __init__(self, shape):
        self.shape = shape

    def __eq__(self, other):
        if isinstance(other, Picture):
            return self.shape == other.shape
        return False

    def __str__(self):
        return f"{self.shape}"


class Card:
    def __init__(self, picture):
        self.picture = picture
        self.face_up = False

    def __eq__(self, other):
        if isinstance(other, Card):
            return self.picture == other.picture
        return False

    def __str__(self):
        return str(self.picture)


class Board:
    def __init__(self):
        self.board = []
        self.boardwidth = 6
        self.boardheight = 6
        self.xmargin = (WINDOWWIDTH - (self.boardwidth * (CARDSIZE + GAPSIZE))) // 2
        self.ymargin = (WINDOWHEIGHT - (self.boardheight * (CARDSIZE + GAPSIZE))) // 2
        self.number_of_pairs = self.boardwidth * self.boardheight // 2
        self.pairs_found = 0
        self.game_ended = False

    def prepare_board(self):
        pictures = [Picture(picture) for picture in ALLPICTURES]
        shuffle(pictures)
        pictures = pictures[:self.number_of_pairs]
        deck = [Card(picture) for picture in pictures for _ in range(2)]
        shuffle(deck)
        self.board = [[deck.pop() for _ in range(self.boardwidth)] for _ in range(self.boardheight)]
        self.pairs_found = 0
        self.game_ended = False

    def check_game(self):
        self.game_ended = self.pairs_found == self.number_of_pairs

    def card_is_revealed(self, coordinates):
        return self.board[coordinates[0]][coordinates[1]].face_up
    
    def get_shape_color(self, x, y):
        return self.board[x][y].picture.shape

    def get_card(self, coordinates):
        return self.board[coordinates[0]][coordinates[1]]

    def check_match(self, first_card, second_card):
        match = first_card == second_card
        if match:
            self.pairs_found += 1
            self.check_game()
        return match

    def __str__(self):
        board_state = ""
        print()
        for row in self.board:
            for card in row:
                if card.face_up:
                    board_state += str(card) + " | "
                else:
                    board_state += "XXXXX XXXXX | "
            board_state += "\n"
        return board_state


def main():
    global FPSCLOCK, DISPLAY_SURFACE
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAY_SURFACE = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Pexeso')
    game_board = Board()
    game_board.prepare_board()
    start_game_animation(game_board)
    mouse_coordinates = 0, 0
    first_card = None
    while True:
        draw_board(game_board)
        mouse_clicked = False
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                end_game()
            elif event.type == MOUSEMOTION:
                mouse_coordinates = event.pos
            elif event.type == MOUSEBUTTONUP:
                mouse_coordinates = event.pos
                mouse_clicked = True

        current_card = get_card_xy(game_board, mouse_coordinates)

        if game_board.game_ended:
            end_state(mouse_coordinates, mouse_clicked, game_board)
            first_card = None
        elif current_card is not None:
            if not game_board.card_is_revealed(current_card):
                draw_card_highlight(game_board, current_card)
                if mouse_clicked:
                    flip_state(game_board, [current_card])
                    if first_card is None:
                        first_card = game_board.get_card(current_card)
                        first_card_xy = current_card
                    else:
                        if game_board.check_match(first_card, game_board.get_card(current_card)):
                            if game_board.game_ended:
                                continue
                        else:
                            pygame.time.wait(1000)
                            flip_state(game_board, [first_card_xy, current_card])
                        first_card = None

        pygame.display.update()
        FPSCLOCK.tick(FPS)



def draw_board(game_board):
    """Draw all of the boxes in their covered or revealed state."""
    DISPLAY_SURFACE.fill(BGCOLOR)
    for card in ((x, y) for x in range(game_board.boardwidth) for y in range(game_board.boardheight)):
        left, top = get_left_top_coordinates(game_board, card)
        if not game_board.card_is_revealed(card):  # Draw a covered box
            pygame.draw.rect(DISPLAY_SURFACE, CARDCOLOR, (left, top, CARDSIZE, CARDSIZE))
        else:  # Draw the (revealed) icon
            shape = game_board.get_shape_color(card[0], card[1])
            draw_icon(shape, left, top)


def get_left_top_coordinates(game_board, card):
    """Convert game_board coordinates to pixel coordinates."""
    x, y = card[0], card[1]
    left = x * (CARDSIZE + GAPSIZE) + game_board.xmargin
    top = y * (CARDSIZE + GAPSIZE) + game_board.ymargin
    return left, top


def get_card_xy(game_board, coordinates):
    """Convert pixel coordinates to game_board coordinates."""
    for card_xy in ((x, y) for x in range(game_board.boardwidth) for y in range(game_board.boardheight)):
        left, top = get_left_top_coordinates(game_board, card_xy)
        card_rect = pygame.Rect(left, top, CARDSIZE, CARDSIZE)
        if card_rect.collidepoint(coordinates):
            return card_xy
    return None


def draw_icon(shape, left, top):
    """Draw a revealed icon."""
    for i in ALLPICTURES:
        if i == shape:
            image = pygame.image.load(f"./resources/graphics/pexeso/{i}.png")
            image = pygame.transform.scale(image, (CARDSIZE, CARDSIZE))
            image_rect = pygame.Rect(left, top, CARDSIZE, CARDSIZE)
            DISPLAY_SURFACE.blit(image, image_rect)

    if shape not in ALLPICTURES:
        raise ValueError('Unknown shape: ' + shape)


def draw_card_highlight(game_board, card_xy):
    """Draw a highlight around the box on mouse hover."""
    left, top = get_left_top_coordinates(game_board, card_xy)
    highlight_rect = (left - 5, top - 5, CARDSIZE + 10, CARDSIZE + 10)
    pygame.draw.rect(DISPLAY_SURFACE, HIGHLIGHTCOLOR, highlight_rect, 4)


def start_game_animation(game_board):
    cards = [(x, y) for x in range(game_board.boardwidth) for y in range(game_board.boardheight)]
    shuffle(cards)
    card_groups = (cards[i:i+8] for i in range(0, len(cards), 8))
    for card_group in card_groups:
        flip_state(game_board, card_group)
        pygame.time.wait(200)
        flip_state(game_board, card_group)


def flip_state(game_board, cards_to_flip):
    for card in cards_to_flip:
        x, y = card[0], card[1]
        game_board.board[x][y].face_up = not game_board.board[x][y].face_up
    draw_board(game_board)
    pygame.display.update()


def end_state(mouse_coordinates, mouse_clicked, game_board):
    font_object = pygame.font.Font("freesansbold.ttf", 32)
    text_surface_object = font_object.render("Congratulations!", True, BLACK)
    text_rect_object = text_surface_object.get_rect()
    text_rect_object.center = (WINDOWWIDTH//2, 150)
    DISPLAY_SURFACE.fill(BGCOLOR)
    DISPLAY_SURFACE.blit(text_surface_object, text_rect_object)

    text_surface_object = font_object.render("Do you want to play again?", True, BLACK)
    text_rect_object = text_surface_object.get_rect()
    text_rect_object.center = (WINDOWWIDTH//2, 200)
    DISPLAY_SURFACE.blit(text_surface_object, text_rect_object)

    check_mark = pygame.image.load(f"./resources/graphics/pexeso/check_mark.jpeg")
    check_mark = pygame.transform.scale(check_mark, (CARDSIZE, CARDSIZE))
    check_rect = pygame.Rect(WINDOWWIDTH//3, 250, CARDSIZE, CARDSIZE)
    DISPLAY_SURFACE.blit(check_mark, check_rect)
    
    cross_mark = pygame.image.load("./resources/graphics/pexeso/cross_mark.png")
    cross_mark = pygame.transform.scale(cross_mark, (CARDSIZE, CARDSIZE))
    cross_rect = pygame.Rect(WINDOWWIDTH//3*2-CARDSIZE, 250, CARDSIZE, CARDSIZE)
    DISPLAY_SURFACE.blit(cross_mark, cross_rect)
    
    if check_rect.collidepoint(mouse_coordinates):
        highlight_rect = (WINDOWWIDTH//3 - 5, 250 - 5, CARDSIZE + 10, CARDSIZE + 10)
        pygame.draw.rect(DISPLAY_SURFACE, HIGHLIGHTCOLOR, highlight_rect, 4)
        if mouse_clicked:
            game_board.prepare_board()
            start_game_animation(game_board)
    elif cross_rect.collidepoint(mouse_coordinates):
        highlight_rect = (WINDOWWIDTH//3*2 - CARDSIZE - 5, 250 - 5, CARDSIZE + 10, CARDSIZE + 10)
        pygame.draw.rect(DISPLAY_SURFACE, HIGHLIGHTCOLOR, highlight_rect, 4)
        if mouse_clicked:
            exit()

def end_game():
    pygame.quit()
    exit()


if __name__ == '__main__':
    main()