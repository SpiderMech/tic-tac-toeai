import numpy as np
import math
import matplotlib.pyplot as plt

LEARNING_RATE = 0.1
DISCOUNT = 0.95
EPISODES = 25000

SHOW_EVERY = 2000

epsilon = 0.5
START_EPSILON_DECAY = 1
END_EPSILON_DECAY = EPISODES //2

epsilon_decay_value = epsilon/(END_EPSILON_DECAY-START_EPSILON_DECAY)

class Board:
    def __init__(self, row=3, column=3):
        self.row = row
        self.column = column
        self.board = [[0 for i in range(3)] for j in range(3)]

    def printBoard(self):
        for x in range(self.row):
            print()
            for y in range(self.column):
                print(self.board[x][y], end = '|')
        print()

    def getBoard(self):
        return self.board

    def getBoardState(self):
        state = ((self.board[0][0], self.board[0][1], self.board[0][2]),(self.board[1][0],self.board[1][1],self.board[1][2]), (self.board[2][0],self.board[2][1],self.board[2][2]))
        return state

    def resetBoard(self):
        self.board = [[0 for i in range(3)] for j in range(3)]


def validMove(board, s):
    if board[int(s.split(' ')[0])][int(s.split(' ')[1])] != 0:
        # print("Invalid move, please pick another move")
        return False
    return True


class Player:
    def __init__(self, playerId):
        self.playerID = playerId

    def makeMove(self, board, playerId, action):
        s = getActionString(action)
        while not validMove(board, s):
            action += 1
            if action == 9:
                action = 0
            s = getActionString(action)
        coordinates = [int(s.split(' ')[0]), int(s.split(' ')[1])]
        if playerId == "0":
            board[coordinates[0]][coordinates[1]] = 'x'
        else:
            board[coordinates[0]][coordinates[1]] = 'o'
        return action

    def getPlayerID(self):
        return self.playerID


def getActionString(action):
    s = ""
    if action == 0:
        s = "0 0"
    if action == 1:
        s = "0 1"
    if action == 2:
        s = "0 2"
    if action == 3:
        s = "1 0"
    if action == 4:
        s = "1 1"
    if action == 5:
        s = "1 2"
    if action == 6:
        s = "2 0"
    if action == 7:
        s = "2 1"
    if action == 8:
        s = "2 2"
    return s


class Game:
    def __init__(self):
        self.board = Board()
        self.player0 = Player("0")
        self.player1 = Player("1")

    def PlayGame(self, ep_reward):
        self.board.resetBoard()
        game_over = False
        turn = 1
        while not game_over:
            reward = 0
            current_state = self.board.getBoardState()

            if np.random.random() >= epsilon:
                action = np.argmax(q_table[self.board.getBoardState()])
            else:
                action = np.random.randint(0, 9)

            if turn:
                action = self.player0.makeMove(self.board.getBoard(), self.player0.getPlayerID(), action)
                turn -= 1
                game_over = self.isWon('x')
                if game_over:
                    reward = 1
                if self.isTie():
                    reward = 0.5
                    game_over = True
                ep_reward += reward
            else:
                action = self.player1.makeMove(self.board.getBoard(), self.player1.getPlayerID(), action)
                turn += 1
                game_over = self.isWon('o')
                if game_over:
                    reward = -1
                if self.isTie():
                    reward = 0.5
                    game_over = True
            new_state = self.board.getBoardState()

            if not game_over and not turn:
                max_future_q = np.max(q_table[new_state])
                current_q = q_table[current_state][action]
                new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)
                q_table[current_state][action] = new_q
            else:
                q_table[current_state][action] = 0
        return ep_reward

    def playHumanGame(self):
        self.board.resetBoard()
        game_over = False
        turn = 1
        while not game_over:
            if turn:
                action = np.argmax(q_table[self.board.getBoardState()])
                print(q_table[self.board.getBoardState()])
                self.player0.makeMove(self.board.getBoard(), self.player0.getPlayerID(), action)
                turn -= 1
                game_over = self.isWon('x')
            else:
                print("your move: ", end = '')
                s = int(input())
                self.player1.makeMove(self.board.getBoard(), self.player1.getPlayerID(), s)
                turn += 1
                game_over = self.isWon('o')
            if self.isTie():
                game_over = True
            self.board.printBoard()
        print("win")

    def isWon(self, symbol):
        current_board = self.board.getBoard()
        corners = [[0,0], [0,2], [2,0], [2,2]]
        mids = [[0,1], [1,2], [2,1], [1,1]]
        if current_board[1][1] == symbol:
            for i, corner in enumerate(corners):
                if current_board[corner[0]][corner[1]] == symbol:
                    k = i*-1 + 3
                    if current_board[corners[k][0]][corners[k][1]] == symbol:
                        return True
            if current_board[1][0] == symbol and current_board[1][2] == symbol:
                return True
            if current_board[0][1] == symbol and current_board[2][1] == symbol:
                return True
        else:
            for j, mid in enumerate(mids):
                if current_board[mid[0]][mid[1]] == symbol:
                    if j == 0 or j == 2:
                        if current_board[mid[0]][mid[1]-1] == symbol and current_board[mid[0]][mid[1]+1] == symbol:
                            return True
                    elif j == 1 or j == 3:
                        if current_board[mid[0]-1][mid[1]] == symbol and current_board[mid[0]+1][mid[1]] == symbol:
                            return True
        return False

    def isTie(self):
        current_board = self.board.getBoard()
        for x in current_board:
            for y in x:
                if y == 0:
                    return False
        return True


DISCRETE_OS_SIZE = math.factorial(9)

import itertools
symbols = ['o', 'x', 0]
layouts = [[i[0:3], i[3:6], i[6:9]] for i in itertools.product(symbols, repeat=3^9)]
q_table = {}
for layout in layouts:
    q_table[(layout[0], layout[1], layout[2])] = [np.random.uniform(low=0, high=2) for i in range(9)]

game = Game()

ep_rewards = []
aggr_ep_rewards = {'ep' : [], 'avg' : [], 'min' : [], 'max' : []}

for episode in range(EPISODES):
    episode_reward = 0
    episode_reward = game.PlayGame(episode_reward)
    print(f"episode reward: {episode_reward}")
    if episode % SHOW_EVERY == 0:
        print("winning state: {}".format(game.board.printBoard()))

    if END_EPSILON_DECAY >= episode >= START_EPSILON_DECAY:
        epsilon -= epsilon_decay_value
    ep_rewards.append(episode_reward)
    if not episode % SHOW_EVERY:
        average_reward = sum(ep_rewards[-SHOW_EVERY:])/len(ep_rewards[-SHOW_EVERY:])
        aggr_ep_rewards['ep'].append(episode)
        aggr_ep_rewards['avg'].append(average_reward)
        aggr_ep_rewards['min'].append(min(ep_rewards[-SHOW_EVERY:]))
        aggr_ep_rewards['max'].append(max(ep_rewards[-SHOW_EVERY:]))

        print(f"Episode:{episode}, Average:{average_reward}, Min:{min(ep_rewards[-SHOW_EVERY:])}, Max:{max(ep_rewards[-SHOW_EVERY:])}")

plt.plot(aggr_ep_rewards['ep'], aggr_ep_rewards['avg'], label='avg')
plt.plot(aggr_ep_rewards['ep'], aggr_ep_rewards['min'], label='min')
plt.plot(aggr_ep_rewards['ep'], aggr_ep_rewards['max'], label='max')
plt.legend(loc=4)
plt.show()

ROUNDS = 10
for round in range(ROUNDS):
    game.playHumanGame()









