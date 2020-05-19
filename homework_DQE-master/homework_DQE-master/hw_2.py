import random
import sys

game_board = (1, 2, 3, 4, 5, 6, 7, 8, 9)
marks = ('X', 'O')


def rules():
    print("*** TIC-TAC-TOE ***")
    print("Rules:\nThe first player to get 3 of her marks (\'X\' or \'O\' in a row (up, down, across, or diagonally) "
          "is the winner"
          "\nWhen all 9 squares are full, the game is over.")
    print("****************************************************\n")


def choose_names():
    print("Players:")
    first_player = input("first player (X mark) - ")
    second_player = input("second player (O mark) - ")
    print("---------------------------")
    return first_player, second_player


def choose_rounds():
    rounds_number = input("How many rounds do you want to have: ")
    while rounds_number.isdigit() == 0 or (int(rounds_number) < 1 or int(rounds_number) > 100):
        sys.stdout.flush()
        rounds_number = input("How many rounds do you want to have: ")

    print("---------------------------")
    return rounds_number


def start_game():
    print("\tGAME STARTS")
    print("---------------------------")


def who_first(players):
    turning = players[random.randint(0, 1)]
    print(turning, " starts the game")
    if turning == 0:
        return 0, 1  # for setting turn in the battle (порядок ходів)
    else:
        return 1, 0


def building_board(board):
    print('_____________')
    for i in range(3):
        print('|', board[i * 3 + 0], '|', board[i * 3 + 1], '|', board[i * 3 + 2], '|')
        print('-------------')


def battle(players, rounds, turn):
    score = [0, 0]
    turn = list(turn)
    for round_battle in range(int(rounds)):
        winner = -1
        board = list(game_board)
        print(f"🔥{round_battle + 1} round🔥 ")

        while winner == -1 and space_end(board) == 0:
            step_player(players[turn[0]], marks[turn[0]], board)
            winner = check(board)
            if winner != -1:
                break

            step_player(players[turn[1]], marks[turn[1]], board)
            winner = check(board)

        change_turn(turn)  # in the next round another player starts

        round_winner_announce(players, winner, board, score)
    winner_announce(players, score)


def winner_announce(players, score):
    print(f"Congratulations to {players[0] if score[0] > score[1] else players[1]} 🔥🔥🔥"
          f"\nTotal score in the battle {score[0]}:{score[1]}")


def round_winner_announce(players, winner, board, score):
    if winner != -1:
        print("-------------------------")
        print("Final combination")
        building_board(board)
        print("\n-------------------------")
        score[winner] += 1
        print(players[winner], "win this round 🎉\n",
              f"score is {score[0]}:{score[1]}")
    else:
        print("This round has ended with draw ⭕️")
    print("-------------------------\n")


def change_turn(turn):
    temp = turn[0]
    turn[0] = turn[1]
    turn[1] = temp


def step_player(player, mark, board):
    building_board(board)

    sys.stdout.flush()  # clear buffer
    step = "0"
    print(f'\n--{player} with \'{mark}\'')
    while step.isdigit() == 0 or (int(step) < 1 or int(step) > 9) or str(board[int(step) - 1]).isdigit() == 0:
        step = input("Your turn: ")
    board[int(step) - 1] = mark


def check(board):
    t_hor1, t_hor2, t_hor3 = (1, 2, 3), (4, 5, 6), (7, 8, 9)
    t_ver1, t_ver2, t_ver3 = (1, 4, 7), (2, 5, 8), (3, 6, 9)
    t_cross1, t_cross2 = (1, 5, 9), (3, 5, 7)
    t_comb = (t_hor1, t_hor2, t_hor3, t_ver1, t_ver2, t_ver3, t_cross1, t_cross2)

    winner = 0  # -1 - none, 0 -- first player, 1 -- second player
    winner = check_combination(t_comb, board)
    return winner


def check_combination(tup_combinations, board):
    for comb in tup_combinations:
        if board[comb[0] - 1] == 'X' and board[comb[1] - 1] == 'X' and board[comb[2] - 1] == 'X':
            return 0
        elif board[comb[0] - 1] == 'O' and board[comb[1] - 1] == 'O' and board[comb[2] - 1] == 'O':
            return 1
    return -1


def space_end(board):
    for i in board:
        if str(i).isdigit():
            return 0
    return 1


def game():
    rules()
    players = choose_names()
    rounds = choose_rounds()
    start_game()
    turn = who_first(players)
    battle(players, rounds, turn)


game()

"""
1. Clarify and rules
2. Set names 
3. How many rounds
4. Who's turn (random)
5. Step by step 
6. Announcing winner
"""
