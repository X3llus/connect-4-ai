import torch
import random
import numpy as np
from collections import deque
from connectGame import ConnectGame

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:
    
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 #randomness
        self.gamma = 0 #discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        # TODO: model, trainer

    def get_state(self, game):
        pass

    def remember(self, state, action, reward, next_state, gameOver):
        pass

    def train_long_memory(self):
        pass

    def train_short_memory(self, state, action, reward, next_state, gameOver):
        pass

    def get_action(self, state):
        pass

def train():
    plot_scores = []
    plot_avg_scores = []
    total_score = 0
    best_score = 0
    agent = Agent()
    game = ConnectGame()
    while True:
        # get current state
        state_old = agent.get_state(game)

        # get move
        final_move = agent.get_action(state_old)

        # perform move and get new state
        reward, game_over, score = game.playPiece(final_move)
        state_new = agent.get_state(game)

        # train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, game_over)

        # remember
        agent.remember(state_old, final_move, reward, state_new, game_over)

        if game_over:
            # train long memory (replay memory), plot result
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()

            if score > best_score:
                best_score = score
                #agent.model.save()

            print('Game', agent.n_games, 'Score', score, 'Best Score', best_score)

            # TODO: plot

if __name__ == '__main__':
    train()