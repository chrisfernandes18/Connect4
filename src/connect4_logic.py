"""Classes to be used in Connect4 + Game Logic"""
import copy
from random import randint
from .connect4_globals import COLUMN_COUNT, ROW_COUNT, SUCCESS, FAILURE, \
                              INF, N_INF

class Game:
    """
    A class used to represent a game of Connect4.

    Attributes
    ----------
    player1 : Player
        A player class type which determines if its a human or bot playing.
    player2 : Player
        A player class type which determines if its a human or bot playing.

    Methods
    -------
    next_player()
        Updates the current player to the next one.
    update_board(column)
        Updates the board with the players move.
    count_winning_positions():
        Returns integer representing state of game.
    print_board()
        Prints the board to stdout.
    valid_move(column)
        Checks if selected column has free spaces.
    winning_move(piece, t_board)
        Checks if there is a winning line.
    """

    def __init__(self, player1, player2):
        self.board = [[0 for i in range(ROW_COUNT)] for i in range(COLUMN_COUNT)]
        self.curr_player = player1
        self.next = player2
        self.turn = 0

    def next_player(self):
        """
        Updates the current player to the next one.

        Parameters
        ----------
        None

        Returns
        -------
        None
            Returns None upon completion.
        """
        temp = copy.deepcopy(self.curr_player)
        self.curr_player = self.next
        self.next = temp

    def update_board(self, column):
        """
        Updates the board with the players move.

        Parameters
        ----------
        column : int
            Which column current player chose to play in.

        Returns
        -------
        None
            Returns None upon completion.
        """
        res = 0
        if self.valid_move(column):
            for row in range(len(self.board[column])):
                if self.board[column][row] != 0:
                    self.board[column][row-1] = self.curr_player.num
                    break

                if row == (len(self.board[column]) - 1):
                    self.board[column][row] = self.curr_player.num
                    break
            self.next_player()
            self.turn += 1
            res = SUCCESS
        else:
            res = FAILURE
        return res

    def count_winning_positions(self):
        """
        Returns integer representing state of game.

        If the integer is positive, that means player 1 has the upper hand.
        If the integer is negative, that means player 2 has the upper hand.
        Otherwise, it is an even game.

        Parameters
        ----------
        game : Game
            A representation of the state of connect4.

        Returns
        -------
        int
            Returns int representing state of game.
        """
        p1_count = 0
        p2_count = 0
        if self.winning_move(1, self.board):
            return 1000

        if self.winning_move(2, self.board):
            return -1000

        for col in range(COLUMN_COUNT):
            for row in range(ROW_COUNT):
                t_board = copy.deepcopy(self.board)
                if t_board[col][row] == 0:
                    t_board[col][row] = 1
                    if self.winning_move(1, t_board):
                        p1_count += 1

        for col in range(COLUMN_COUNT):
            for row in range(ROW_COUNT):
                t_board = copy.deepcopy(self.board)
                if t_board[col][row] == 0:
                    t_board[col][row] = 2
                    if self.winning_move(2, t_board):
                        p2_count += 1
        return p1_count - p2_count

    def print_board(self):
        """
        Prints the board to stdout.

        Parameters
        ----------
        None

        Returns
        -------
        None
            Returns None upon completion.
        """
        for column in self.board:
            print(column)

    def valid_move(self, column):
        """
        Checks if selected column has free spaces.

        Parameters
        ----------
        column : int
            Which column current player chose to play in.

        Returns
        -------
        Bool
            Returns True if it is a valid move, or False otherwise.
        """
        for row in self.board[column]:
            if row == 0:
                return True
        return False

    def winning_move(self, piece, t_board=None):
        """
        Checks if there is a winning line.

        Parameters
        ----------
        piece : int
            Represents which player's piece.

        Returns
        -------
        Bool
            Returns True if someone has one, or False otherwise.
        """
        board = t_board if t_board else self.board
        for col in range(COLUMN_COUNT - 3):
            for row in range(ROW_COUNT):
                if board[col][row] == piece and \
                   board[col+1][row] == piece and \
                   board[col+2][row] == piece and \
                   board[col+3][row] == piece:
                    return True

        for col in range(COLUMN_COUNT):
            for row in range(ROW_COUNT - 3):
                if board[col][row] == piece and \
                   board[col][row+1] == piece and \
                   board[col][row+2] == piece and \
                   board[col][row+3] == piece:
                    return True

        for col in range(COLUMN_COUNT - 3):
            for row in range(ROW_COUNT - 3):
                if board[col][row] == piece and \
                   board[col+1][row+1] == piece and \
                   board[col+2][row+2] == piece and \
                   board[col+3][row+3] == piece:
                    return True

        for col in range(COLUMN_COUNT - 3):
            for row in range(3, ROW_COUNT):
                if board[col][row] == piece and \
                   board[col+1][row-1] == piece and \
                   board[col+2][row-2] == piece and \
                   board[col+3][row-3] == piece:
                    return True

        return False


class Player:
    """
    A class used to represent a game of player in Connect4.

    Attributes
    ----------
    name : str
        The name of the player.
    type_of_player : int
        0 if human, >0 if bot to represent difficulty.
    strategy : Strategy
        None if human, otherwise given a strategy bot can use.
    num : int
        An int that represents which number player the player is.

    Methods
    -------
    says(sound=None)
        Prints the animals name and what sound it makes
    """
    def __init__(self, name, type_of_player, num):
        self.name = name
        self.type = type_of_player
        self.num = num
        self.strategy = None if type_of_player == 0 else Strategy(self.type)

class Tree:
    """
    A class used to represent a tree of possible moves to choose from.

    Attributes
    ----------
    ply : int
        The height of the tree.
    game : Game
        A representation of the state of connect4.
    state : int
        An int representing state of game.

    Methods
    -------
    build_tree(ply)
        Builds tree of possible moves of height ply.
    """
    def __init__(self, ply, game, column=-1):
        self.game = game
        self.ply = ply
        self.column = column
        self.children = [] if ply == 0 else self.build_tree(ply)
        self.state = game.count_winning_positions()

    def build_tree(self, ply):
        """
        Builds tree of possible moves of height ply from game.

        Parameters
        ----------
        ply : int
            Number representing height of tree.

        Returns
        -------
        list fo Tree
            Returns a list of tree of possible moves.
        """
        res = []
        for i in range(COLUMN_COUNT):
            temp = copy.deepcopy(self.game)
            if temp.valid_move(i):
                temp.update_board(i)
                res.append(Tree(ply-1, temp, i))
        return res

class Strategy:
    """
    A class used to represent a strategy being used by a bot.

    Attributes
    ----------
    ply : int
        The number of moves to think ahead.

    Methods
    -------
    count_winning_positions(game)
        Takes in a game and returns who has the upper hand.
    minimaxeval(tree, ply, alpha, beta, maximizing_player)
        Given a Tree, returns integer representing state of game assuming
        potential moves the opponent may take.
    """
    def __init__(self, ply):
        self.ply = ply

    def minimaxeval(self, tree, ply, alpha, beta, maximizing_player):
        """
        Given a Tree, returns integer representing state of game assuming
        potential moves the opponent may take.

        If the integer is positive, that means player 1 has the upper hand.
        If the integer is negative, that means player 2 has the upper hand.
        Otherwise, it is an even game.

        Parameters
        ----------
        tree : Tree
            A representation of possible moves from current game.
        ply : int
            Height of tree.
        maximizing_player : bool
            True if we are taking max of height or false for min.

        Returns
        -------
        tuple
            Returns tuple representing column to play, and state of best move.
        """
        if ply == 0 or tree.state == -1000 or tree.state == 1000:
            return tree.column, tree.state

        if maximizing_player:
            max_eval = N_INF
            col = randint(0, 6)
            for child in tree.children:
                col_res, res_eval = self.minimaxeval(child, ply - 1, alpha, beta, False)
                if max_eval < res_eval:
                    col = child.column
                max_eval = max(max_eval, res_eval)
                alpha = max(alpha, res_eval)
                if beta <= alpha:
                    break
            return col, max_eval

        if not maximizing_player:
            min_eval = INF
            col = randint(0, 6)
            for child in tree.children:
                col_res, res_eval = self.minimaxeval(child, ply - 1, alpha, beta, True)
                if min_eval > res_eval:
                    col = child.column
                min_eval = min(min_eval, res_eval)
                beta = min(beta, res_eval)
                if beta <= alpha:
                    break
            return col, res_eval


    def minimaxstrategy(self, game):
        """
        Given a game decides which column to play in, based off of
        a tree.

        Parameters
        ----------
        game : Game
            A representation of the state of connect4.

        Returns
        -------
        int
            Returns column bot should play in.
        """
        res = None
        if game.curr_player.strategy:
            ply = game.curr_player.type
            tree = Tree(ply, game)
            if game.curr_player.num == 1:
                res = self.minimaxeval(tree, ply, N_INF, INF, True)
            else:
                res = self.minimaxeval(tree, ply, N_INF, INF, False)
        return res[0]
