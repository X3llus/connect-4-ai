import os
from time import sleep
from game import Game
from agent import Agent
from rich.console import Console
from rich.table import Table
from getpass import getpass

def main():
    os.system('Connect 4!')
    agent1 = Agent()
    game_over = False
    best_score = 0
    total_score = 0
    game = Game()
    clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')
    console = Console()

    def endGame():
        agent1.n_games += 1
        agent1.train_long_memory()

    def printBoard(board):
        table = Table(show_header=False, show_lines=True)
        for c in range(5):
            table.add_column()
        for x in range(5):
            row = []
            for y in range(5):
                piece = (int)(board[x][y])
                if piece == 0:
                    row.append('⚪')
                if piece == 1:
                    row.append('🔴')
                if piece == 2:
                    row.append('⚫')
            table.add_row(*row)
        console.print(table, style='default on blue')
            

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
            endGame()
            total_score += score
            if score <= best_score:
                best_score = score
                # agent1.model.save('a1model.pth')
            game.reset()
            console.print("Loser!")
            getpass('Press enter to continue.')
            continue

        # -----------------------------------------
        # Player Turn
        # -----------------------------------------
        played = False
        err = False
        while not played:
            clearConsole()
            printBoard(game.getBoard())
            if err:
                console.print('Piece not able to be placed, check that you\'re entering 1-5 and not dropping in a full column')
            userIn = int(console.input('Enter column to place piece in (1-5)'))
            _, game_over, _, played = game.playPiece(userIn - 1)
            err = True if not played else False

        if game_over:
            losingMove = agent1.memory.pop()
            agent1.memory.append((losingMove[0], losingMove[1], -20, losingMove[3], losingMove[4]))
            endGame()
            clearConsole()
            printBoard(game.getBoard())
            game.reset()
            console.print("Winner!")
            sleep(1)
            getpass('Press enter to continue.')

if __name__ == '__main__':
    main()