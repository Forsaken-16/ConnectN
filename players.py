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
    depth = 6
    def __init__(self, piece, n):
        self.piece = piece   # game.PLAYER1 or game.PLAYER2
        self.n = n           # how many in a row to win

    def get_move(self, board):
        # FIX (comment only): old comment said "it just plays randomly" - it now uses
        # the minimax search in search.py. Returns a column number that is not full.
        return search.best_move(board, self.depth, 0, self.piece, self.n)
