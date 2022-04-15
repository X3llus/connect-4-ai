from os import stat
import os
from time import sleep
from connectGame import ConnectGame
from agent import Agent
from helper import plot


def train():
    agent1 = Agent()
    agent2 = Agent()
    plot_scores = []
    plot_avg_scores = []
    game_over = False
    best_score = 0
    total_score = 0
    game = ConnectGame()

    def endGame(game):
        game.reset()
        agent1.n_games += 1
        # agent1.train_long_memory()
        agent2.n_games += 1
        # agent2.train_long_memory()

        # os.system('cls')
        print('Game', agent1.n_games, flush=True)

    def plotGame(score, total_score):
        plot_scores.append(score)
        total_score += score
        mean_score = total_score / agent1.n_games
        plot_avg_scores.append(mean_score)
        plot(plot_scores, plot_avg_scores)

    while True:
        if agent1.n_games >= 500:
            exit()
        # if game_over:
            # plotGame(score, total_score)
        # -----------------------------------------
        # Agent One
        # -----------------------------------------
        # get current state
        state_old = agent1.get_state(game)

        # get move
        final_move = agent1.get_action(state_old)

        # perform move and get new state
        reward, game_over, score, _ = game.playPiece(final_move)
        print('over?', game_over)
        state_new = agent1.get_state(game)

        # train short memory
        agent1.train_short_memory(state_old, final_move, reward, state_new, game_over)

        # remember
        agent1.remember(state_old, final_move, reward, state_new, game_over)

        if game_over:
            endGame(game)
            if score <= best_score:
                best_score = score
                agent1.model.save('a1model.pth')
            # agent2.memory = agent1.memory
            # agent2.model = agent1.model
            agent2.remember(state_old, [0, 0, 0, 0, 0], -10, state_new, game_over)
            game.reset()
            continue

        # -----------------------------------------
        # Agent Two
        # -----------------------------------------
        # get current state
        state_old = agent2.get_state(game)

        # get move
        final_move = agent2.get_action(state_old)

        # perform move and get new state
        reward, game_over, score, _ = game.playPiece(final_move)
        print('over2?', game_over)
        state_new = agent2.get_state(game)

        # train short memory
        agent2.train_short_memory(state_old, final_move, reward, state_new, game_over)

        # remember
        agent2.remember(state_old, final_move, reward, state_new, game_over)

        if game_over:
            endGame(game)
            if score <= best_score:
                best_score = score
                agent2.model.save('a2model.pth')
            # agent1.memory = agent2.memory
            # agent1.model = agent2.model
            agent1.remember(state_old, [0, 0, 0, 0, 0], -10, state_new, game_over)
            game.reset()

if __name__ == '__main__':
    train()