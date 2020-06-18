"""Implements the graphics for Connect4"""
import pygame
from .connect4_globals import BLACK, YELLOW, RED, BLUE, TAN, \
                              COLUMN_COUNT, ROW_COUNT, SUCCESS, FAILURE,\
                              HEIGHT, WIDTH, SIZE, PADDING

def welcome(screen):
    """
    Draws the welcome screen of Connect4.

    Parameters
    ----------
    screen : Surface
        A pygame Surface.

    Returns
    -------
    None
        Returns None upon completion.
    """
    font = pygame.font.SysFont("monospace", int(PADDING / 2))
    pygame.draw.rect(screen, TAN, (0, PADDING, WIDTH, HEIGHT - (2 * PADDING)))
    welcome_txt = "Welcome to Connect 4!"
    screen.blit(font.render(welcome_txt, 1, BLACK), \
                (int((WIDTH - font.size(welcome_txt)[0])/2), int(HEIGHT / 3)))
    continue_txt = "Click to continue."
    screen.blit(font.render(continue_txt, 1, BLACK), \
                (int((WIDTH - font.size(continue_txt)[0])/2), int(HEIGHT / 2)))
    pygame.display.update()

def init_game():
    """
    Draws and takes input for players.

    Parameters
    ----------
    None

    Returns
    -------
    list of str
        List containing each player's name and if they are a bot or human.
    """
    i = 0
    res = ["", "", "", ""]
    screen = pygame.display.set_mode(SIZE)
    font = pygame.font.SysFont("monospace", int(PADDING / 3))
    welcome(screen)
    texts = ["Enter Player 1's Name:", "Enter Player 1's Type (0-3):",\
             "Enter Player 2's Name:", "Enter Player 2's Type (0-3):"]
    new_font = pygame.font.SysFont("monospace", int(PADDING / 5))
    flag = 0
    while flag == 0:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, TAN, (0, PADDING, WIDTH, HEIGHT - (2 * PADDING)))
                screen.blit(font.render(texts[i], 1, BLACK),\
                            (int((WIDTH - font.size(texts[i])[0]) / 2), int(HEIGHT / 3)))
                flag = 1
            pygame.display.update()

    while i != 4:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key != pygame.K_RETURN:
                    pygame.draw.rect(screen, TAN, (0, int(HEIGHT / 2), WIDTH, PADDING))
                    pygame.draw.rect(screen, TAN, (0, int(HEIGHT / 2) + PADDING, WIDTH, PADDING))
                    if event.key == pygame.K_BACKSPACE:
                        res[i] = res[i][:-1]
                    elif not event.key in [301, 303, 304]:
                        res[i] += chr(event.key).upper() if len(res[i]) == 0 else chr(event.key)
                    screen.blit(font.render(res[i], 1, BLACK),\
                                (int((WIDTH - font.size(res[i])[0]) / 2), \
                                int(HEIGHT / 2)))
                    if (i % 2) == 1:
                        err = "Please enter single number between 0-3."
                        try:
                            int(res[i])
                            if not 0 <= int(res[i]) <= 3:
                                screen.blit(new_font.render(err, 1, BLACK),\
                                    (int((WIDTH - new_font.size(err)[0]) / 2), \
                                    int(HEIGHT / 2) + PADDING))
                        except ValueError:
                            screen.blit(new_font.render(err, 1, BLACK),\
                                    (int((WIDTH - new_font.size(err)[0]) / 2), \
                                    int(HEIGHT / 2) + PADDING))
                elif len(res[i]) == 0 and event.key == pygame.K_RETURN:
                    pygame.draw.rect(screen, TAN, (0, int(HEIGHT / 2) + PADDING, WIDTH, PADDING))
                    err = "Please enter a value."
                    screen.blit(new_font.render(err, 1, BLACK),\
                                (int((WIDTH - new_font.size(err)[0]) / 2), \
                                int(HEIGHT / 2) + PADDING))
                else:
                    i += 1
                    if i != 4:
                        pygame.draw.rect(screen, TAN, (0, PADDING, WIDTH, HEIGHT - (2 * PADDING)))
                        screen.blit(font.render(texts[i], 1, BLACK),\
                                    (int((WIDTH - font.size(texts[i])[0]) / 2), int(HEIGHT / 3)))
                    if (i % 2) == 1:
                        type_rules = "0 = Human, 1-3 = Bot"
                        screen.blit(new_font.render(type_rules, 1, BLACK), \
                                (int((WIDTH - new_font.size(type_rules)[0]) / 2), \
                                 int((int(HEIGHT / 3) + int(HEIGHT / 2)) / 2)))

            pygame.display.update()
    res[1] = int(res[1])
    res[3] = int(res[3])
    return res


def draw_game(game, failed=SUCCESS):
    """
    Draws the current state of the board.

    Parameters
    ----------
    game : Game
        A representation of the state of connect4.
    failed : int
        Default set to SUCCESS, but can be changed to FAILURE to notify full column.

    Returns
    -------
    screen : Surface
        A pygame Surface.
    """
    halfpad = int(PADDING / 2)
    screen = pygame.display.set_mode(SIZE)
    font = pygame.font.SysFont("monospace", halfpad)
    for col in range(COLUMN_COUNT):
        for row in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (col*PADDING, (row*PADDING)+PADDING, PADDING, PADDING))
            if game.board[col][row] == 0:
                pygame.draw.circle(screen,\
                                   BLACK,\
                                   (col*PADDING+halfpad, \
                                    (row*PADDING)+PADDING+halfpad),\
                                    halfpad-10)
            elif game.board[col][row] == 1:
                pygame.draw.circle(screen,\
                                   YELLOW,\
                                   (col*PADDING+halfpad, \
                                    (row*PADDING)+PADDING+halfpad),\
                                    halfpad-10)
            else:
                pygame.draw.circle(screen,\
                                   RED,\
                                   (col*PADDING+halfpad, \
                                    (row*PADDING)+PADDING+halfpad),\
                                    halfpad-10)
    pygame.draw.rect(screen, TAN, (0, HEIGHT-PADDING, WIDTH, PADDING))
    win = 0
    pos_y = HEIGHT - int((PADDING*3)/4)

    if game.winning_move(1) or game.winning_move(2):
        win = 1
        winner = game.next.name
        winner += " won!"
        screen.blit(font.render(winner, 1, BLACK),\
                                (int(((WIDTH) - font.size(winner)[0])/2), pos_y))
    elif failed == FAILURE:
        err = "Column is full."
        screen.blit(font.render(err, 1, BLACK), \
                                (int(((WIDTH) - font.size(err)[0])/2), pos_y))
    else:
        text = game.curr_player.name + "'s Turn"
        screen.blit(font.render(text, 1, BLACK),\
                    (int(((WIDTH) - font.size(text)[0])/2), pos_y))

    pygame.display.update()
    return (screen, win)


def draw_floating_circle(game, screen, pos_x):
    """
    Draws floating at top of screen.

    Parameters
    ----------
    game : Game
        A representation of the state of connect4.
    screen : Surface
        A pygame Surface object.
    pos_x : int
        The position of the mouses' x-coordinate.

    Returns
    -------
    None
        Returns None upon completion.
    """
    pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, PADDING))
    if game.curr_player.num == 1:
        pygame.draw.circle(screen, YELLOW, \
                        (pos_x, int(PADDING/2)), int((PADDING/2)-10))
    else:
        pygame.draw.circle(screen, RED, \
                        (pos_x, int(PADDING/2)), int((PADDING/2)-10))
    pygame.display.update()
    