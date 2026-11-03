from __future__ import print_function
import random


#initial state
board = [0, 0, 0, 0]
initial_board = board

#current state of the board
def show_board(board_p):

    new_board = []
    for i in range(len(board)):
        new_board.append([i, board_p[i]])

    print(new_board)

    for i in range(len(board)):
        for j in range(len(board)):
            if [j, i] in new_board:
                print("Q", end=" ")
            else:
                print(".", end=" ")
        print()
    print()

#function to determine the heuristic cost of the board
#heuristic cost = number of queens attacking one another
def determine_h_cost(board):
    h = 0

    # check all queens
    for i in range(len(board)):
        # check interaction with remaining queens
        for j in range(i + 1, len(board)):
            # if queen in same column
            if board[i] == board[j]:
                h += 1

            # get offset
            offset = i - j

            # check if there is diagonal interaction
            if board[i] == board[j] + offset or board[i] == board[j] - offset:
                h += 1
    return h

#function to determine the next best move based on the h cost of all neighbouring states
#there are 56 neighbouring states
def best_move(board):
    moves = []
    moves.append([board, determine_h_cost(board)])

    for col in range(len(board)):
        for row in range(len(board)):
            board_copy = list(board)
            if board[col] == row:
                continue
            board_copy[col] = row
            cost_of_state = determine_h_cost(board_copy)
            moves.append([board_copy, cost_of_state])

    current = determine_h_cost(board)

    for row in moves:
        if row[1] < current:
            current = row[1]

    #there can be more than 1 best neighbouring state due to same h values
    best_moves = []
    for row in moves:
        if row[1] == current:
            best_moves.append(row[0])

    #randomly select one move out of all the best moves
    next_move = random.choice(best_moves)

    return next_move

#show initial state of the board and its h cost
show_board(board)
print("h = " + str(determine_h_cost(board)))
print()

action_sequence = []

h_cost = determine_h_cost(board)
action_sequence.append([board, h_cost])

#loop through until the minimum h cost state is achieved
#the program chooses the best moves until it reaches an optimum state
number_of_steps = 0
state = 1
while (state == 1):

    board_next_state = best_move(board)

    #if the next best state is the current state, it has reached a maximum state
    if board == board_next_state or h_cost == determine_h_cost(board_next_state):
        state = 0
        show_board(board)
        cost = determine_h_cost(board)
        print("h = " + str(cost))
        if cost == 0:
            print("Global Maximum!")
            print()
        else:
            print("Local Maximum")
            print()

            # if the result is a local minimum, then reinitialize the board and try again
            state = 1
            board = initial_board
    else:
        board = board_next_state
        state = 1
        h_cost = determine_h_cost(board)
        action_sequence.append([board, h_cost])
        number_of_steps += 1
        # show_board(board)

print("Steps taken: ")
for row in action_sequence:
    print(row)

print()
print("Number of steps: " + str(number_of_steps))
