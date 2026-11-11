"""
players.py - The players. Each one has get_move(board) that returns a column.
"""

import random

import heuristic

import game

import search 

class HumanPlayer:
    """Moves come from mouse clicks in ui.py."""
    is_human = True

    def __init__(self, piece, n):
        self.piece = piece
        self.n = n


class RandomPlayer:
    """Plays a random legal column."""
    is_human = False

    def __init__(self, piece, n):
        self.piece = piece
        self.n = n

    def get_move(self, board):
        return random.choice(game.legal_moves(board))


class AIPlayer:
    """Your AI goes here."""
    is_human = False
    depth = 4
    def __init__(self, piece, n):
        self.piece = piece   # game.PLAYER1 or game.PLAYER2
        self.n = n           # how many in a row to win

    def get_move(self, board):
        # TODO: write your AI here. Return a column number that is not full.
        # For now it just plays randomly.
        return search.best_move(board, self.depth, 0, self.piece, self.n)
