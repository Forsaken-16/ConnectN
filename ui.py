"""
ui.py - The game window. Run:  python ui.py

Click a column to drop a piece. Press R to restart.
"""

import sys

import pygame

import game
import players

# ---- Settings: change these ----
ROWS = 6
COLS = 7
N = 4
PLAYER1 = players.HumanPlayer   # Red, moves first
PLAYER2 = players.AIPlayer      # Yellow

CELL = 90              # size of one square in pixels
RADIUS = 38            # size of a piece
TOP = 60               # space for the text at the top
WIDTH = COLS * CELL
HEIGHT = TOP + (ROWS + 1) * CELL   # +1 row above the board for the hovering piece

BLUE = (30, 90, 200)
BLACK = (20, 20, 30)
WHITE = (255, 255, 255)
COLORS = {game.PLAYER1: (220, 50, 50), game.PLAYER2: (240, 210, 40)}
NAMES = {game.PLAYER1: "Red", game.PLAYER2: "Yellow"}


def cell_center(row, col):
    """Pixel position of a board cell (row -1 is the hover row above the board)."""
    return col * CELL + CELL // 2, TOP + (row + 1) * CELL + CELL // 2


class Game:
    def __init__(self):
        self.players = {game.PLAYER1: PLAYER1(game.PLAYER1, N),
                        game.PLAYER2: PLAYER2(game.PLAYER2, N)}
        self.restart()

    def restart(self):
        self.board = game.create_board(ROWS, COLS)
        self.turn = game.PLAYER1
        self.winner = None
        self.win_line = None
        self.draw = False
        self.falling = None   # the piece currently falling: [col, y, speed]
        self.wait_until = 0   # small pause before the computer moves

    def is_over(self):
        return self.winner is not None or self.draw

    def start_drop(self, col):
        if col in game.legal_moves(self.board):
            self.falling = [col, cell_center(-1, col)[1], 0]

    def click(self, x):
        if not self.is_over() and self.falling is None and self.players[self.turn].is_human:
            self.start_drop(x // CELL)

    def update(self):
        # Animate the falling piece (it speeds up like gravity).
        if self.falling:
            col, y, speed = self.falling
            speed += 2
            y += speed
            target_row = max(r for r in range(ROWS) if self.board[r][col] == game.EMPTY)
            target_y = cell_center(target_row, col)[1]
            if y >= target_y:
                self.falling = None
                self.land(col)
            else:
                self.falling = [col, y, speed]
            return

        # Computer's turn: wait a moment, then ask it for a move.
        player = self.players[self.turn]
        if not self.is_over() and not player.is_human:
            now = pygame.time.get_ticks()
            if self.wait_until == 0:
                self.wait_until = now + 400
            elif now >= self.wait_until:
                self.wait_until = 0
                board_copy = [row[:] for row in self.board]
                self.start_drop(player.get_move(board_copy))

    def land(self, col):
        """The piece reached the bottom: add it to the board and check the result."""
        row =game.drop_piece(self.board, col, self.turn)
        self.win_line = game.winning_line(self.board, (row, col),  self.turn, N)
        if self.win_line:
            self.winner = self.turn
        elif game.is_draw(self.board):
            self.draw = True
        else:
            self.turn = game.PLAYER2 if self.turn == game.PLAYER1 else game.PLAYER1

    def draw_screen(self, screen, font):
        screen.fill(BLACK)

        # Text at the top
        if self.winner:
            text, color = f"{NAMES[self.winner]} wins!  (R to restart)", COLORS[self.winner]
        elif self.draw:
            text, color = "Draw!  (R to restart)", WHITE
        else:
            text, color = f"{NAMES[self.turn]}'s turn", COLORS[self.turn]
        label = font.render(text, True, color)
        screen.blit(label, label.get_rect(center=(WIDTH // 2, TOP // 2)))

        # Piece hovering above the column under the mouse
        if not self.is_over() and self.falling is None and self.players[self.turn].is_human:
            col = pygame.mouse.get_pos()[0] // CELL
            pygame.draw.circle(screen, COLORS[self.turn], cell_center(-1, col), RADIUS)

        # Board and pieces
        pygame.draw.rect(screen, BLUE, (0, TOP + CELL, WIDTH, ROWS * CELL))
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                color = COLORS[piece] if piece else BLACK
                pygame.draw.circle(screen, color, cell_center(row, col), RADIUS)

        # Falling piece (drawn after the board so it stays visible)
        if self.falling:
            col, y, _ = self.falling
            pygame.draw.circle(screen, COLORS[self.turn], (cell_center(0, col)[0], y), RADIUS)

        # Winning line: white rings around the winning pieces
        if self.win_line:
            for row, col in self.win_line:
                pygame.draw.circle(screen, WHITE, cell_center(row, col), RADIUS, 5)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(f"Connect {N}")
    font = pygame.font.SysFont(None, 44)
    clock = pygame.time.Clock()
    g = Game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                g.click(event.pos[0])
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                g.restart()

        g.update()
        g.draw_screen(screen, font)
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
