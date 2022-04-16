from re import I
import numpy as np

class Game:
    board = np.zeros((5,5))
    playerPiece = 1
    turnsTaken = 0
    game_over = False
    turnReward = 0
    player1score = 0
    player2score = 0

    def reset(self):
        self.board = np.zeros((5,5))
        self.playerPiece = 1
        self.turnsTaken = 0
        self.game_over = False
        self.turnReward = 0
        self.player1score = 0
        self.player2score = 0

    def getBoard(self):
        return self.board

    def playPiece(self, x):
        if isinstance(x, list):
            x = x.index(1)
        if x < 0 or x > 4:
            return 0, False, self.turnsTaken, False
        if np.all(self.board != 0):
            # Cats game
            return 0, True, self.turnsTaken, True
        if self.board[0][x] == 0:
            _, turnReward = self.__placePiece(x)
            self.turnReward += turnReward
            self.__swapTurn()
            return turnReward, self.game_over, self.turnsTaken, True
        return -50, False, self.turnsTaken, False

    def __placePiece(self, x):
        turnReward = 0
        for y in range (4, -1, -1):
            if self.board[y][x] == 0:
                self.board[y][x] = self.playerPiece
                if self.__solvingAlgorythm(x, y, self.playerPiece):
                    # print('win Player', self.playerPiece, 'In', self.turnsTaken, 'turns', '\n', self.board, flush=True)
                    turnReward += 30
                    self.game_over = True

                numBlocked = self.__blockingAlgorythm(x, y, self.playerPiece)

                if numBlocked == 2:
                    turnReward += 10

                if numBlocked == 3:
                    turnReward += 20
                return True, turnReward
        return False, turnReward

    def __swapTurn(self):
        if self.playerPiece == 1:
            self.playerPiece = 2
            self.player1score += self.turnReward
        else:
            self.playerPiece = 1
            self.player2score += self.turnReward

        self.turnsTaken += 1
        self.turnReward = 0

    def __solvingAlgorythm(self, x, y, player):
        dx = 0
        dy = 1
        cx = x
        cy = y
        rowCount = 0
        maxCount = 0
        axisCount = [0, 0, 0, 0]
        axis = 0

        # scan direction
        while True:
            if rowCount >= 4:
                self.turnReward = maxCount
                return True
            if cx >= 5 or cx < 0 or cy >= 5 or cy < 0 or self.board[cy][cx] != player:
                if rowCount > maxCount:
                    maxCount = rowCount
                cx = x
                cy = y
                rowCount = 0
                axis += 1
                if axis == 4:
                    axis = 0
                # change direction
                if dx == 0 and dy == 1:
                    dx = 1
                elif dx == 1 and dy == 1:
                    dy = 0
                elif dx == 1 and dy == 0:
                    dy = -1
                elif dx == 1 and dy == -1:
                    dx = 0
                elif dx == 0 and dy == -1:
                    dx = -1
                elif dx == -1 and dy == -1:
                    dy = 0
                elif dx == -1 and dy == 0:
                    dy = 1
                else:
                    # Check the highest axis count
                    self.turnReward = max(axisCount) - 1
                    if 5 in axisCount: return True
                    return False
                continue
            rowCount += 1
            axisCount[axis] += 1
            cx += dx
            cy += dy 

    def __blockingAlgorythm(self, x, y, player) -> int:
        enemyPiece = (lambda player : 1 if (player == 2) else 2)(player)
        dx = 0
        dy = 1
        cx = x + dx
        cy = y + dy
        rowCount = 0
        maxCount = 0
        axisCount = [0, 0, 0, 0]
        axis = 0

        # scan direction
        while True:
            if rowCount >= 3:
                self.turnReward = maxCount
                return rowCount
            if cx >= 5 or cx < 0 or cy >= 5 or cy < 0 or self.board[cy][cx] != enemyPiece:
                if rowCount > maxCount:
                    maxCount = rowCount
                cx = x + dx
                cy = y + dy
                rowCount = 0
                # change direction
                if dx == 0 and dy == 1:
                    dx = 1
                elif dx == 1 and dy == 1:
                    dy = 0
                elif dx == 1 and dy == 0:
                    dy = -1
                elif dx == 1 and dy == -1:
                    dx = 0
                elif dx == 0 and dy == -1:
                    dx = -1
                elif dx == -1 and dy == -1:
                    dy = 0
                elif dx == -1 and dy == 0:
                    dy = 1
                else:
                    self.turnReward = maxCount
                    return maxCount
                continue
            rowCount += 1
            cx += dx
            cy += dy 