"""
game.py - The rules of Connect N (no graphics).

The board is a list of rows: board[row][col]. Row 0 is the top.
Each cell is EMPTY, PLAYER1 or PLAYER2.

Rules:
  - Players take turns dropping a piece into a column that is not full.
  - The piece falls to the lowest empty cell in that column.
  - The first player with N pieces in a row (across, down or diagonal) wins.
  - If the board is full and nobody has won, it is a draw.
"""

EMPTY = 0
PLAYER1 = 1
PLAYER2 = 2

def create_board(rows, cols):
    return [[EMPTY] * cols for i in range(rows)]

def legal_moves(board):
    """Columns that are not full."""
    return [col for col in range(len(board[0])) if board[0][col] == EMPTY]

def legal_cells(board):
    legal_columns = legal_moves(board)
    cells = []
    for col in legal_columns:
        for row in range(len(board) - 1, -1, -1):
            if board[row][col] == EMPTY:
                cells.append((row,col))
                break
    return cells
        

def drop_piece(board, col, piece):
    """Put a piece in the lowest empty cell of a column. Returns the row it landed in."""
    for row in range(len(board) - 1, -1, -1):
        if board[row][col] == EMPTY:
            board[row][col] = piece
            return row
    raise ValueError("Column is full")
    

def winning_line(board, cell, piece, n):
    # FIX: was `rows, col = cell`, so `row` was undefined (NameError) and `rows`
    # got overwritten on the next line anyway.
    row, col = cell
    rows, cols = len(board), len(board[0])
    #left_right, up_down, neg_diag, pos_diag
    for dr, dc in [(0, 1), (1, 0), (1, 1), (1, -1)]:
        for i in range(-(n-1), 1):
            cells = [(row + dr*j, col + dc*j) for j in range(i, i+n)]
            if all(0 <= r< rows and 0 <= c < cols and board[r][c] == piece for r, c in cells):
                return cells
    return None
            
     

def is_draw(board):
    """The board is full (call this after checking for a win)."""
    return len(legal_moves(board)) == 0
