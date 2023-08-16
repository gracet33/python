#TIC TAC TOE GAME
#Imports
import random

#variables

avail_pos = {
        "row1 left": (0, 0),  "row1 middle": (0, 1),  "row1 right": (0, 2),
        "row2 left": (1, 0),  "row2 middle": (1, 1),  "row2 right": (1, 2),
        "row3 left": (2, 0),  "row3 middle": (2, 1),  "row3 right": (2, 2)
    }

#Create Board by first creating row elements and rows for matrix
row1 = [" ", " ", " "]
row2 = [" ", " ", " "]
row3 = [" ", " ", " "]
board = [row1, row2, row3]

col1 = [row[0] for row in board]
col2 = [row[1] for row in board]
col3 = [row[2] for row in board]
diag1 = [board[i][i] for i in range(3)]
diag2 = [board[i][2 - i] for i in range(3)]
mapping_for_score = {"row1": row1, "row2": row2, "row3": row3,
                     "col1": col1, "col2": col2, "col3": col3,
                     "diag1": diag1, "diag2": diag2}

#Code Beginning Interface

def begin_interface():
    '''display the beginning interface'''
    ttt_display = '''
     _____  _  ____    _____  ____  ____    _____  ____  _____
    /__ __\/ \/   _\  /__ __\/  _ \/   _\  /__ __\/  _ \/  __/
      / \  | ||  /      / \  | / \||  /      / \  | / \||  \  
      | |  | ||  \__    | |  | |-|||  \__    | |  | \_/||  /_ 
      \_/  \_/\____/    \_/  \_/ \|\____/    \_/  \____/\____\
      '''
    print(ttt_display, "\n")
    print("Let's Play a Game of Tic Tac Toe!\n")

#Display board function by printing each variable in matrix so that separators are not printed
def display_board():
    '''display the board'''
    for i, row in enumerate(board):
        print("   | ".join(row))
        if i < len(board) - 1:
            print("---------------")

#Functions for player 1 and 2 selecting game piece
def player1():
    '''Allow player 1 to choose game piece (X will always go first) and returning that value'''
    while True:
        one = input("To Player One: Which game piece will you choose? ('O' or 'X', X will always go first): ")
        if one in ('O', 'X'):
            return one
        else:
            print("Invalid choice. Please choose 'O' or 'X'.")


def player2(one):
    '''Returning value of whatever game piece left'''
    if one == 'O':
        two = 'X'
    else:
        two = 'O'
    return two

#####--------PLAYER FUNCTIONS ----------####
#Functions involved in the action of placing moves
def moving_position():
    '''Ask player to give input for moving position'''
    player_move = input("Where would you like to place your piece? "
                        "('row1 left, row1 middle, row1 right, "
                        "row2 left, row2 middle, row2 right, "
                        "row3 left, row3 middle, row3 right'): ")
    return player_move


def placing_move(player):
    '''Update available positions and replace blank space with player's piece'''
    global avail_pos
    position = moving_position()
    move_indices = avail_pos.get(position)
    if move_indices is None:
        print("Move is invalid. Please retype.")
        return False
    else:
        begin_interface()
        print("Position placed!")
        row, col = move_indices
        board[row][col] = player
        display_board()
        del avail_pos[position]
        return True
        #mapping the board and update remaining available positions on board


#####--------AI FUNCTIONS ----------####
def calculate_sum(items):
    '''maps each score on each position of the board'''
    score_mapping = {
        player: 1,
        opponent: -1,
        " ": 0
    }
    return sum(score_mapping[item] for item in items)

def calculate_scores(board):
    scores = {}
    for row_index, row in enumerate(board):
        row_score = calculate_sum(row)
        scores[f"row{row_index + 1}"] = row_score

    transposed_board = list(map(list, zip(*board)))
    for col_index, col in enumerate(transposed_board):
        col_score = calculate_sum(col)
        scores[f"col{col_index + 1}"] = col_score

    diagonals = [[board[0][0], board[1][1], board[2][2]], [board[0][2], board[1][1], board[2][0]]]
    for diag_index, diagonal in enumerate(diagonals):
        diag_score = calculate_sum(diagonal)
        scores[f"diag{diag_index + 1}"] = diag_score
    return scores


def find_empty_positions(board):
    return [(row_idx, col_idx) for row_idx, row in enumerate(board) for col_idx, cell in enumerate(row) if cell == " "]

def ai_all_moves(board, score):
    '''determine possible moves with calculated score'''
    scores = calculate_scores(board)
    keys_with_score = [key for key, value in scores.items() if value == score]

    for key in keys_with_score:
        if "col" in key:
            col_index = int(key[3:]) - 1
            for row_index, row in enumerate(board):
                if row[col_index] == " ":
                    return row_index, col_index
        elif "row" in key:
            row_index = int(key[3:]) - 1
            for col_index in range(3):
                if board[row_index][col_index] == " ":
                    return row_index, col_index
        elif "diag" in key:
            diag_index = int(key[4:]) - 1
            if diag_index == 0:
                for i in range(3):
                    if board[i][i] == " ":
                        return i, i
            else:
                for i in range(3):
                    if board[i][2 - i] == " ":
                        return i, 2 - i
    return None


def best_move(board):
    '''helps ai player make a decision base on the score'''
    scores = calculate_scores(board)
    #if score is 3, player has already won. Ai lost so position will be none.
    if 3 in scores.values():
        print(" Game ends! You win!")
        avail_pos.clear()
        return None
    #if score is -2, position will be a winning move.
    position = ai_all_moves(board, -2)
    if position is not None:
        return position
    #if score is 2, position will be a move that stops player from winning.
    position = ai_all_moves(board, 2)

    #this will get the blank position.
    empty_positions = find_empty_positions(board)

    if position is not None:
        return position
    elif empty_positions:
        return random.choice(empty_positions)
    else:
        return None

def make_move(board, player):
    global avail_pos
    position = best_move(board)
    if position is not None:
        print('\n')
        print("Computer made a move")

        row_idx, col_idx = position
        board[row_idx][col_idx] = player
        value_to_find = (row_idx, col_idx)

        #identifying remaining available positions and deleting the position
        keys_to_delete = []
        for key, value in avail_pos.items():
            if value == value_to_find:
                keys_to_delete.append(key)
        for key in keys_to_delete:
            del avail_pos[key]
        display_board()
#----------END OF AI PLAYER FUNCTIONS ---------------#


#THE GAMEPLAY EXECUTION
begin_interface()
#Ask player to choose the game piece. If player chooses X, ai will go first.
player = player1()
#assign game piece to opponent
opponent = player2(player)
# Check if AI should go first
if player == 'O':
    print("Computer will go first.")
    make_move(board, opponent)
while len(avail_pos) > 0:
    if placing_move(player):
        make_move(board, opponent)
        scores = calculate_scores(board)
        if -3 in scores.values():
            avail_pos.clear()
            print("Game ends! AI wins!")
        if -3 not in scores.values() and 3 not in scores.values() and len(avail_pos) == 0:
            print("\n")
            print("It's a draw!")

