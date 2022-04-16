from os import stat
from time import sleep
from game import Game
from agent import Agent
from helper import plot


def train():
    agent1 = Agent()
    game_over = False
    best_score = 0
    total_score = 0
    game = Game()

    def endGame(game):
        agent1.n_games += 1
        agent1.train_long_memory()
        print('Game', agent1.n_games, flush=True)

    def printBoard(board):
        for x in range(5):
            for y in range(5):
                if(y == 4):
                    print ((int)(board[x][y]))
                else:
                    print ((int)(board[x][y]), "| ", end="")
            

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
        while not played:
            final_move = agent1.get_action(state_old)
            reward, game_over, score, played = game.playPiece(final_move)

        state_new = agent1.get_state(game)

        # train short memory
        agent1.train_short_memory(state_old, final_move, reward, state_new, game_over)

        # remember
        agent1.remember(state_old, final_move, reward, state_new, game_over)

        if game_over:
            endGame(game)
            total_score += score
            if score <= best_score:
                best_score = score
                # agent1.model.save('a1model.pth')
            game.reset()
            continue

        # -----------------------------------------
        # Player Turn
        # -----------------------------------------

        printBoard(game.getBoard())
        userIn = int(input("Enter column to place piece in (1-5): "))
        _, game_over, _, played = game.playPiece(userIn - 1)
        while not played:
            print("Piece not able to be placed, check that you're entering 1-5 and not dropping in a full column")
            userIn = int(input("Enter column to place piece in (1-5)"))
            _, game_over, _, played = game.playPiece(userIn - 1)

        if game_over:
            losingMove = agent1.memory.pop()
            agent1.memory.append((losingMove[0], losingMove[1], -20, losingMove[3], losingMove[4]))
            endGame(game)
            game.reset()

if __name__ == '__main__':
    train()