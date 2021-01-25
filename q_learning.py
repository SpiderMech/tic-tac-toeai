##### Game Environment #####
from abc import abstractmethod
import random

### Normal Human Game ###
class Game:
    def __init__(self):
        self.board = Board()
        self.player1 = Player('o')
        self.player2 = Player('x')
        self.player_lst = [self.player1, self.player2]
        self.move_dict = {
            7: (0, 0), 8: (0, 1), 9: (0, 2),
            4: (1, 0), 5: (1, 1), 6: (1, 2),
            1: (2, 0), 2: (2, 1), 3: (2, 2)
        }

    def load_game(self):
        self.board.reset_board()

    def play_game(self):
        turn_counter = 0
        player_input = -1
        game_over = False
        while not game_over and player_input != 0:

            turn = turn_counter % 2

            # Get valid player input
            player_input = int(input("Player {} please play your move: ".format(turn+1)))
            while not self.is_valid_move(player_input):
                player_input = int(input("INVALID MOVE, Player {} play again: ".format(turn+1)))

            current_player = self.player_lst[turn]

            # Set board value
            self.board.set_board_val_by_pos(self.move_dict.get(player_input), current_player.symbol)
            # self.board.print_board()
            print(self.board.get_board_hash())

            game_over = self.is_game_over(current_player.symbol)

            # Add to player history
            current_player.move_history.append(player_input)
            turn_counter += 1
        print("Player {} has won the game!".format(turn_counter%2))

    def is_valid_move(self, move):
        return self.board.board.get(self.move_dict.get(move), -1) == 0

    def is_game_over(self, symbol):
        streak_count = 0
        # Check row win
        for x in range(self.board.column):
            for y in range(self.board.row):
                if self.board.get_board_val_by_pos((x,y)) == symbol:
                    streak_count += 1
            if streak_count == 3:
                return True
            else:
                streak_count = 0

        # Check column win
        for x in range(self.board.column):
            for y in range(self.board.row):
                if self.board.get_board_val_by_pos((y, x)) == symbol:
                    streak_count += 1
            if streak_count == 3:
                return True
            else:
                streak_count = 0

        # Check diagonal win
        if self.board.get_board_val_by_pos((1,1)) == symbol:
            if self.board.get_board_val_by_pos((0,2)) == self.board.get_board_val_by_pos((2,0)) == symbol:
                return True
            if self.board.get_board_val_by_pos((0,0)) == self.board.get_board_val_by_pos((2,2)) == symbol:
                return True

        # Check for tie
        for x in range(self.board.column):
            for y in range(self.board.row):
                if self.board.get_board_val_by_pos((y, x)) == 0:
                    return False
        return True

### Board ###
class Board:
    def __init__(self, row=3, column=3):
        self.row = row
        self.column = column
        self.board = {(x,y):0 for (x, y) in [(x,y) for x in range(row) for y in range(column)]}
        self.move_dict = {
            7: (0, 0), 8: (0, 1), 9: (0, 2),
            4: (1, 0), 5: (1, 1), 6: (1, 2),
            1: (2, 0), 2: (2, 1), 3: (2, 2)
        }

        self.index_dict = {
            (0, 0): 7, (0, 1): 8, (0, 2): 9,
            (1, 0): 4, (1, 1): 5, (1, 2): 6,
            (2, 0): 1, (2, 1): 2, (2, 2): 3
        }
        # print(self.board)


    def print_board(self):
        for y in range(self.row):
            for x in range(self.column):
                board_val_in_pos = self.board.get((y,x), 0)
                if board_val_in_pos == 'o':
                    print(f"\033[91m{board_val_in_pos}\033[0m", end='')
                else:
                    print(board_val_in_pos, end='')
                if x != 2:
                    print('|', end='')
                else:
                    print()
        print()


    def reset_board(self):
        for key in self.board.keys():
            self.board[key] = 0


    def set_board_val_by_pos(self, pos, val):
        self.board[pos] = val


    def get_board_val_by_pos(self, pos):
        return self.board.get(pos, -1)


    def get_board_hash(self):
        hash_lst = [val for val in self.board.values()]
        hash_val = 0
        for index, val in enumerate(hash_lst):
            if type(val) == str:
                val = ord(val)
            hash_val += (index+1) * val
        return hash_val

    def get_board_string(self):
        res = ""
        for val in self.board.values():
            if val == 0:
                val = str(val)
            res += val
        return res


    def is_valid_move(self, move):
        return self.board.get(self.move_dict.get(move), -1) == 0


    def get_random_empty_spot(self):
        random_spot_lst = []
        for pos, val in self.board.items():
            if val == 0:
                random_spot_lst.append(pos)
        if len(random_spot_lst) == 1:
            return self.index_dict.get(random_spot_lst[0])
        return self.index_dict.get(random.choice(random_spot_lst))


    def is_game_over(self, symbol):
        streak_count = 0
        # Check row win
        for x in range(self.column):
            for y in range(self.row):
                if self.get_board_val_by_pos((x,y)) == symbol:
                    streak_count += 1
            if streak_count == 3:
                return True, "win", symbol
            else:
                streak_count = 0

        # Check column win
        for x in range(self.column):
            for y in range(self.row):
                if self.get_board_val_by_pos((y, x)) == symbol:
                    streak_count += 1
            if streak_count == 3:
                return True, "win", symbol
            else:
                streak_count = 0

        # Check diagonal win
        if self.get_board_val_by_pos((1,1)) == symbol:
            if self.get_board_val_by_pos((0,2)) == self.get_board_val_by_pos((2,0)) == symbol:
                return True, "win", symbol
            if self.get_board_val_by_pos((0,0)) == self.get_board_val_by_pos((2,2)) == symbol:
                return True, "win", symbol

        # Check for tie
        for x in range(self.column):
            for y in range(self.row):
                if self.get_board_val_by_pos((y, x)) == 0:
                    return False, "going", "no one"
        return True, "draw", ""

### Player ###
class Player:
    def __init__(self, symbol):
        self.move_history = []
        self.symbol = symbol

    def start_new_game(self):
        self.move_history = []

    @abstractmethod
    def make_move(self, board: Board):
        pass
    @abstractmethod
    def update(self, result, board):
        pass

### Random Player ###
## Inherits Player Class ##
class RandomPlayer(Player):
    def __init__(self, symbol):
        super().__init__(symbol)

    def make_move(self, board: Board):
        move = board.get_random_empty_spot()
        board_pos = board.move_dict[move]
        board.set_board_val_by_pos(board_pos, self.symbol)
        return board.is_game_over(self.symbol)

    def update(self, result, board):
        pass

### Q-Learning player ###
## Inherits Player Class ##
class QPlayer(Player):
    def __init__(self, alpha, discount, initial_q, symbol):
        super().__init__(symbol)
        self.alpha = alpha
        self.discount = discount
        self.initial_q = initial_q
        self.q_table = {}

    # def get_q_values(self, board_hash_val):
    #     if board_hash_val in self.q_table:
    #         q = self.q_table[board_hash_val]
    #     else:
    #         q = [self.initial_q for i in range(9)]
    #         self.q_table[board_hash_val] = q
    #     return q

    def get_q_values(self, board_string):
        if board_string in self.q_table:
            q = self.q_table[board_string]
        else:
            q = [self.initial_q for i in range(9)]
            self.q_table[board_string] = q
        return q

    def make_move(self, board: Board):
        board_string = board.get_board_string()
        move = self.get_move(board)
        while not board.is_valid_move(move):
            move = board.get_random_empty_spot()

        board_pos = board.move_dict.get(move)
        board.set_board_val_by_pos(board_pos, self.symbol)
        self.move_history.append((board_string, move))
        return board.is_game_over(self.symbol)

    def get_move(self, board: Board):
        board_string = board.get_board_string()
        return argmax(self.get_q_values(board_string)) + 1

    def update(self, result, board):
        reward = 0
        if result == self.symbol+"win":
            reward = 1
        elif result == "draw":
            reward = 0.5

        self.move_history.reverse()
        new_max_q = -1.0
        for previous_move in self.move_history:
            q_values = self.get_q_values(previous_move[0])
            if new_max_q < 0:
                q_values[previous_move[1]-1] = reward
            else:
                q_values[previous_move[1]-1] = q_values[previous_move[1]-1] * (1 - self.alpha) + self.alpha * self.discount * new_max_q
            new_max_q = max(q_values)


class HumanPlayer(Player):
    def __init__(self, symbol):
        super().__init__(symbol)

    def make_move(self, board: Board):
        move = int(input('Please play your move: '))
        while not board.is_valid_move(move) or move == '':
            move = int(input('Invalid move, please pick again: '))
        board_pos = board.move_dict.get(move)
        board.set_board_val_by_pos(board_pos, self.symbol)
        self.move_history.append((board.get_board_string(), move))
        return board.is_game_over(self.symbol)

    def update(self, result, board):
        pass


# argmax helper function
import math
def argmax(lst) -> int:
    max_dict = {}
    max_val = -math.inf
    for index, val in enumerate(lst):
        if val > max_val:
            max_val = val
        if val not in max_dict:
            max_dict[val] = [(index, val)]
        else:
            max_dict[val].append((index, val))
    max_lst = max_dict[max_val]
    if len(max_lst) > 1:
        index_lst = [item[0] for item in max_lst]
        return random.choice(index_lst)
    return max_lst[0][0]


# Helper function to print board directives
def print_instructions():
    print("Board Key Mappings")
    lst = [7, 4, 1]
    for s in lst:
        for num in range(3):
            if num == 0:
                print(s, end='|')
            elif num == 1:
                print(s+1, end='|')
            else:
                print(s+2)
    print()


# Utility function to play the game
def play_game(board: Board, player_1: Player, player_2: Player):
    board.reset_board()

    player_1.start_new_game()
    player_2.start_new_game()

    result = ""
    winner = ""
    game_over = False

    while not game_over:
        game_over, result, winner = player_1.make_move(board)
        if not game_over:
            game_over, result, winner = player_2.make_move(board)
    player_1.update(winner+result, board)
    player_2.update(winner+result, board)
    return winner + " " + result


def play_human_game(board: Board, player_1: Player, player_2: Player):
    board.reset_board()
    print('Starting board')
    board.print_board()
    player_1.start_new_game()
    player_2.start_new_game()

    result = ""
    winner = ""
    game_over = False

    while not game_over:
        print("{}'s move".format(player_1.symbol))
        game_over, result, winner = player_1.make_move(board)
        board.print_board()
        if not game_over:
            print("{}'s move".format(player_2.symbol))
            game_over, result, winner = player_2.make_move(board)
            board.print_board()
    player_1.update(winner+result, board)
    player_2.update(winner+result, board)
    return winner + " " + result




board_1 = Board()

randomPlayer = RandomPlayer('x')
q_learning_player1 = QPlayer(alpha=0.9, discount=0.95, initial_q=0.6, symbol='o')
q_player_2 = QPlayer(alpha=0.9, discount=0.95, initial_q=0.6, symbol='x')

q_r_win = 0
q_r_draw = 0

EPISODES = 10000

# Train against another q player
for i in range(EPISODES):
    game_result = play_game(board_1, q_learning_player1, randomPlayer)
    winner_of_game = game_result[0]
    if winner_of_game == 'o':
        q_r_win += 1
    elif winner_of_game != 'x':
        q_r_draw += 1

q_q_win = 0
q_q_draw = 0

# Train against random player
for i in range(EPISODES):
    game_result = play_game(board_1, q_learning_player1, q_player_2)
    winner_of_game = game_result[0]
    if winner_of_game == 'o':
        q_q_win += 1
    elif winner_of_game != 'x':
        q_q_draw += 1

from tabulate import tabulate
print("Q Learner results")
print(tabulate([['Random player', q_r_win, q_r_draw, EPISODES - (q_r_draw + q_r_win)], ['Q player', q_q_win, q_q_draw, EPISODES - (q_q_draw + q_q_win)]], headers=['Against', 'win', 'draw', 'lose']))
print()

print(len(q_learning_player1.q_table))

q_h_win = 0
q_h_draw = 0

GAMES = 20
# Against human player
humanPlayer = HumanPlayer('x')
print_instructions()
print("NOW PLAYING AGAINST Q PLAYER 2")
for i in range(GAMES):
    print("ROUND {}".format(i+1))
    game_result = play_human_game(board_1, q_learning_player1, humanPlayer)
    winner_of_game = game_result[0]
    if winner_of_game == 'o':
        q_h_win += 1
    elif winner_of_game != 'x':
        q_h_draw += 1
        winner_of_game = "No one"


    print("{} won this game!\n".format(winner_of_game))
print(tabulate([['Human', q_h_win, q_h_draw, GAMES - (q_h_win + q_h_draw)]], headers=['Against', 'win', 'draw', 'lose']))
