#
# CS1010X --- Programming Methodology
#
# Contest 10.2 Template
#
# Note that written answers are commented out to allow us to run your
# code easily while grading your problem set.

from random import *
from puzzle_AI import *

"""
0  1  2  3
4  5  6  7
8  9  10 11
12 13 14 15
"""
count = 0
def AI(mat):
    # replace the following line with your code
    CORR = {2**i: i for i in range(1, 12)}
    CORR[0] = 0
    MOVES = {'w': merge_up, 'a': merge_left, 's': merge_down, 'd': merge_right}
    MIN_SCORE = -1
    PATTERNS = [
        (0, 1, 2, 3, 7, 6, 5, 4),
        (0, 4, 8, 12, 13, 9, 5, 1),
        (3, 2, 1, 0, 4, 5, 6, 7),
        (3, 7, 11, 15, 14, 10, 6, 2),
        (12, 13, 14, 15, 11, 10, 9, 8),
        (12, 8, 4, 0, 1, 5, 9, 13),
        (15, 14, 13, 12, 8, 9, 10, 11),
        (15, 11, 7, 3, 2, 6, 10, 14)
        ]
    PATTERN_LENGTH = 8
    DEPTH = 3
    
    def get_score(mat):
        f = tuple(flatten(mat))
        max_tile = max(f)
        zeros = f.count(0)
        score = 0
        for pattern in PATTERNS:
            if f[pattern[0]] != max_tile:
                continue
            pattern_score = CORR[f[pattern[0]]]
            chain = True
            for i in range(1, PATTERN_LENGTH):
                pattern_score *= 10
                if f[pattern[i]] > f[pattern[i-1]]:
                    chain = False
                if chain:
                    pattern_score += CORR[f[pattern[i]]]
            score = max(score, pattern_score)
        score += 0.0001 * sum(f) / (16 - zeros)
        score += 0.000001 * zeros
        return score

    def add_tile(mat, i, j):
        if mat[i][j]:
            return None
        result = new_game_matrix(4)
        for i1 in range(4):
            for j1 in range(4):
                result[i1][j1] = mat[i1][j1]
        result[i][j] = 2
        return result
    
    best_move_memo = {}
    def best_move(mat, n):
        fmat = tuple(flatten(mat))
        
        if (fmat, n) in best_move_memo:
            return best_move_memo[(fmat, n)]
        
        if game_status(mat) == 'lose':
            result = (None, MIN_SCORE)
        elif n < 1:
            result = (None, get_score(mat))
        else:
            best = 's'
            max_score = MIN_SCORE
            for move, f in MOVES.items():
                next_mat, valid, _ = f(mat)
                if not valid:
                    continue
                score = place_tile(next_mat, n-1)
                if score >= max_score:
                    best = move
                    max_score = score
            result = (best, max_score)
            
        best_move_memo[(fmat, n)] = result
        return result

    place_tile_memo = {}
    def place_tile(mat, n):
        fmat = tuple(flatten(mat))
        if (fmat, n) in place_tile_memo:
            return place_tile_memo[(fmat, n)]
        sum_score = 0
        count = 0
        for i in range(4):
            for j in range(4):
                next_mat = add_tile(mat, i, j)
                if next_mat is None:
                    continue
                score = best_move(next_mat, n)[1]
                sum_score += score
                count += 1
        result = sum_score / count
        place_tile_memo[(fmat, n)] = result
        return result

    result = best_move(mat, DEPTH)[0]
    return result



# UNCOMMENT THE FOLLOWING LINES AND RUN TO WATCH YOUR SOLVER AT WORK
#game_logic['AI'] = AI
#gamegrid = GameGrid(game_logic)

# UNCOMMENT THE FOLLOWING LINE AND RUN TO GRADE YOUR SOLVER
# Note: Your solver is expected to produce only valid moves.
get_average_AI_score(AI, True)
