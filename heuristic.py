import game

WIN = 10**9
def make_frame(start_row, start_col, dr, dc, n):
    return [(start_row + i * dr, start_col + i * dc) for i in range(n)]


def score_frame(board, frame):
    zeroes = 0
    ones = 0
    twos = 0
    for (row, col) in frame:
        if board[row][col] == 0:
            zeroes+=1
        elif board[row][col] == 1:
            ones+=1
        else:
            twos+=1
            
    if (ones >=1 and twos >= 1) or zeroes == len(frame):
        return 0
    
    if ones == len(frame): return WIN
    if twos == len(frame): return -WIN
    
    if ones > 0:
        return  10**(2 + ones)
    else:
        return -10**(2 + twos)



def traverse_through_frames(board, row, col, n):
    rows, cols = len(board), len(board[0])
    
    '''up down'''
    score_updown = 0
    for i in range(0, rows - n + 1):
        score_updown += score_frame(board, make_frame(i, col, 1, 0, n) )

    '''left right'''
    score_leftright = 0
    for i in range(0, cols - n + 1):
        score_leftright += score_frame(board, make_frame(row, i, 0 , 1, n))

    '''-ve diagonal'''
    score_neg_diagonal = 0
    m = min(row, col)
    new_row, new_col = row - m, col - m
    length = min(rows - new_row, cols - new_col)
    for i in range(0, length - n + 1):
        score_neg_diagonal += score_frame(board, make_frame(new_row + i , new_col + i, 1, 1, n) )

    '''+ve diagonal'''
    score_pos_diagonal = 0
    m = min(row, cols -(col+1))
    new_row, new_col = row - m, col + m
    length = min(rows - new_row, new_col + 1)
    for i in range(0, length - n + 1):
        score_pos_diagonal += score_frame(board, make_frame(new_row + i, new_col - i, 1, -1, n))


    return score_updown + score_leftright + score_neg_diagonal + score_pos_diagonal



def heuristic(board, row, col, h_old, n, piece):
    s_old = traverse_through_frames(board, row, col, n)
    board[row][col] = piece
    s_new = traverse_through_frames(board, row, col, n)
    return h_old + (s_new - s_old)

