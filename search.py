import heuristic
import game

WIN = heuristic.WIN

def search(board, cell_last, depth, h, piece, n):
    
    next_piece = 3 - piece
    row, col = cell_last

    h_new = heuristic.heuristic(board, cell_last, h, n, next_piece)
    
    if(game.winning_line(board, cell_last, next_piece, n)):
        board[row][col] = 0
        return WIN if next_piece == 1 else -WIN
    
    if(depth == 0):
        board[row][col] = 0
        return h_new
    
    heuristics_next = []
    cells = game.legal_cells(board)
    if not cells:
        board[row][col] = 0
        return 0
    for r, c in cells:
        heuristics_next.append(search(board, (r, c), depth - 1, h_new , next_piece, n))


    board[row][col] = 0
    
    if(piece == 1):
        largest_h = max(heuristics_next)      
        return largest_h
    else:
        smallest_h = min(heuristics_next)
        return smallest_h
    


def best_move(current_board, depth, h_old, current_piece, n):
    next_piece = 3 - current_piece
    if depth < 1:
        raise ValueError("Invalid depth")
    heuristics = []
    cells = game.legal_cells(current_board)
    if not cells:
        return 0
    
    for r, c in cells:
        heuristics.append((search(current_board, (r, c), depth - 1, h_old, next_piece, n), (r, c)))
        
    if current_piece == 1:
        best = max(heuristics)
    else:
        best = min(heuristics)

    return best[1][1]
    
