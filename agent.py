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
        self.model = None # TODO
        self.trainer = None # TODO
        # TODO: model, trainer

    def get_state(self, game):
        state = game.getBoard.flatten(order='C')

    def remember(self, state, action, reward, next_state, game_over):
        self.memory.append((state, action, reward, next_state, game_over)) # will popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory
        
        states, actions, rewards, next_states, game_overs = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, game_overs)

    def train_short_memory(self, state, action, reward, next_state, game_over):
        self.trainer.train_step(state, action, reward, next_state, game_over)

    def get_action(self, state):
        # random moves: tradeoff exploration / exploitation
        self.epsilon = 80 - self.n_games # allowing epsilon to decrease over time
        final_move = [0,0,0]
        if random.randint(0, 200) < self.epsilon: # randomly generating if move should be random
            move = random.randint(0, 2) # random value 0-1
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model.predict(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1
        
        return final_move

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