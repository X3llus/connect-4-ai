from os import stat
from connectGame import ConnectGame
from agent import Agent

agent1 = Agent()
agent2 = Agent()

def train():
    plot_scores = []
    plot_avg_scores = []
    total_score_1 = 0
    total_score_2 = 0
    best_score = 0
    game_over = False
    game = ConnectGame()
    while True:
        if game_over:
            game.reset()

        # get current state
        state_old = agent1.get_state(game)

        # get move
        final_move = agent1.get_action(state_old)

        # perform move and get new state
        reward, score, _ = game.playPiece(final_move)
        game_over = game.getGO()
        state_new = agent1.get_state(game)

        # train short memory
        agent1.train_short_memory(state_old, final_move, reward, state_new, game_over)

        # remember
        agent1.remember(state_old, final_move, reward, state_new, game_over)

        if game_over:
            endGame(game_over, game)
            if score > best_score:
                best_score = score
                agent1.model.save()
            agent2.memory = agent1.memory
            agent2.model = agent1.model
        else:
            # get current state
            state_old = agent2.get_state(game)

            # get move
            final_move = agent2.get_action(state_old)

            # perform move and get new state
            reward, score, _ = game.playPiece(final_move)
            game_over = game.getGO()
            state_new = agent2.get_state(game)

            # train short memory
            agent2.train_short_memory(state_old, final_move, reward, state_new, game_over)

            # remember
            agent2.remember(state_old, final_move, reward, state_new, game_over)

            if game_over:
                endGame(game_over, game)
                if score > best_score:
                    best_score = score
                    agent2.model.save()
                agent1.memory = agent2.memory
                agent1.model = agent2.model




def endGame(game_over, game):
        # train long memory (replay memory), plot result
        game.reset()
        agent1.n_games += 1
        agent1.train_long_memory()
        agent2.n_games += 1
        agent2.train_long_memory()

        if agent1.score > agent1.best_score:
            agent1.best_score = agent1.score
            agent1.model.save("a1model.pth")

        if agent2.score > agent2.best_score:
            agent2.best_score = agent2.score
            agent2.model.save("a2model.pth")

        print('Game', agent1.n_games, 'Agent 1 Score: ', agent1.score, 'Agent 1 Best Score: ', agent1.best_score, 'Agent 2 Score: ', agent2.score, 'Agent 2 Best Score: ', agent2.best_score)

        # TODO: plot

if __name__ == '__main__':
    train()