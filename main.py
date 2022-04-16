from os import stat
import os
from time import sleep
from game import Game
from agent import Agent
from helper import plot

def train():
    agent1 = Agent(file_name='./model/a1model-deep.pth')
    agent2 = Agent(file_name='./model/a2model-deep.pth')
    a1_reward_total = 0
    a1_rewards = []
    a2_reward_total = 0
    a2_rewards = []
    plot_scores = []
    plot_avg_scores = []
    game_over = False
    best_score = 0
    total_score = 0
    game = Game()

    def endGame(game):
        game.reset()
        agent1.n_games += 1
        agent1.train_long_memory()
        agent2.n_games += 1
        agent2.train_long_memory()
        print('Game', agent1.n_games, flush=True)

    def plotGame(score, total_score, a1_reward_total, a2_reward_total):
        plot_scores.append(score)
        mean_score = total_score / agent1.n_games
        plot_avg_scores.append(mean_score)
        a1_rewards.append(a1_reward_total)
        a2_rewards.append(a2_reward_total)
        plot(plot_scores, plot_avg_scores, a1_rewards, a2_rewards)

    while True:
        # -----------------------------------------
        # Agent One
        # -----------------------------------------
        # get current state
        state_old = agent1.get_state(game)

        # get move
        final_move = agent1.get_action(state_old)

        # perform move and get new state
        reward, game_over, score, played = game.playPiece(final_move)
        state_new = agent1.get_state(game)

        a1_reward_total += reward
        # print(a1_reward_total)

        # train short memory
        agent1.train_short_memory(state_old, final_move, reward, state_new, game_over)

        # remember
        agent1.remember(state_old, final_move, reward, state_new, game_over)

        if game_over:
            endGame(game)
            total_score += score
            # plotGame(score, total_score, a1_reward_total, a2_reward_total)
            if a1_reward_total >= best_score:
                best_score = a1_reward_total
                agent1.model.save('a1model-deep.pth')
            losingMove = agent2.memory.pop()
            agent2.memory.append((losingMove[0], losingMove[1], -20, losingMove[3], losingMove[4]))
            a1_reward_total = 0
            a2_reward_total = 0
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
        state_new = agent2.get_state(game)

        a2_reward_total += reward

        # train short memory
        agent2.train_short_memory(state_old, final_move, reward, state_new, game_over)

        # remember
        agent2.remember(state_old, final_move, reward, state_new, game_over)

        if game_over:
            endGame(game)
            total_score += score
            # plotGame(score, total_score, a1_reward_total, a2_reward_total)
            if a2_reward_total >= best_score:
                best_score = score
                agent2.model.save('a2model-deep.pth')
            losingMove = agent1.memory.pop()
            agent1.memory.append((losingMove[0], losingMove[1], -20, losingMove[3], losingMove[4]))
            a1_reward_total = 0
            a2_reward_total = 0
            game.reset()

if __name__ == '__main__':
    train()