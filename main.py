from connectGame import ConnectGame
from agent import Agent

agent1 = Agent()
agent2 = Agent()

def train():
    plot_scores = []
    plot_avg_scores = []
    total_score_1 = 0
    total_score_2 = 0
    best_score_1 = 0
    best_score_2 = 0
    game = ConnectGame()
    while True:
        if game_over:
            game.reset()

        # get current state
        state_old = agent1.get_state(game)

        # get move
        final_move = agent1.get_action(state_old)

        # perform move and get new state
        reward, game_over, score = game.playPiece(final_move)
        state_new = agent1.get_state(game)

        # train short memory
        agent1.train_short_memory(state_old, final_move, reward, state_new, game_over)

        # remember
        agent1.remember(state_old, final_move, reward, state_new, game_over)

        if game_over:
            endGame(game_over, game)
            lastentry = agent2.memory.pop()
            lastentry = (lastentry[0], lastentry[1], lastentry[2] - 10, lastentry[3], lastentry[4])
            agent2.memory.append(lastentry)
        else:
            # get current state
            state_old = agent2.get_state(game)

            # get move
            final_move = agent2.get_action(state_old)

            # perform move and get new state
            reward, game_over, score = game.playPiece(final_move)
            state_new = agent2.get_state(game)

            # train short memory
            agent2.train_short_memory(state_old, final_move, reward, state_new, game_over)

            # remember
            agent2.remember(state_old, final_move, reward, state_new, game_over)

            if game_over:
                endGame(game_over, game)
                lastentry = agent1.memory.pop()
                lastentry = (lastentry[0], lastentry[1], lastentry[2] - 10, lastentry[3], lastentry[4])
                agent1.memory.append(lastentry)




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