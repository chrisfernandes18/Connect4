"""Main program which executes Connect 4"""
import math
import sys
import pygame
from src.connect4_graphics import init_game, draw_game, draw_floating_circle
from src.connect4_logic import Game, Player
from src.connect4_globals import PADDING

def main():
    """
    Executes all the functions necessary to run Connect4.

    Parameters
    ----------
    None

    Returns
    -------
    None
        Returns None upon completion.
    """
    pygame.init()
    inputs = init_game()
    player1 = Player(inputs[0], inputs[1], 1)
    player2 = Player(inputs[2], inputs[3], 2)
    pygame.init()
    game = Game(player1, player2)
    screen = draw_game(game)

    while screen[1] == 0:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                print(event.key, chr(event.key))

            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                draw_floating_circle(game, screen[0], event.pos[0])

            if event.type == pygame.MOUSEBUTTONDOWN:
                worked = game.update_board(math.floor(event.pos[0] / PADDING))
                screen = draw_game(game, worked)

            if game.curr_player.strategy and not (game.winning_move(1) or game.winning_move(2)):
                col = game.curr_player.strategy.minimaxstrategy(game)
                worked = game.update_board(col)
                screen = draw_game(game, worked)

    pygame.time.wait(3000)

if __name__ == "__main__":
    main()
