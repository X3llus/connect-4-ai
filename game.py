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

    def playPiece(self, x: list[int]):
        x = x.index(1)
        if x < 0 or x > 4:
            pass
        if np.all(self.board != 0):
            # Cats game
            return 0, True, self.turnsTaken, False
        if self.board[0][x] == 0:
            self.__placePiece(x)
            return self.turnReward, self.game_over, self.turnsTaken, True
        return -10, False, self.turnsTaken, False

    def __placePiece(self, x):
        for y in range (4, -1, -1):
            if self.board[y][x] == 0:
                self.board[y][x] = self.playerPiece
                if self.__solvingAlgorythm(x, y, self.playerPiece):
                    print('win Player', self.playerPiece, 'In', self.turnsTaken, 'turns', '\n', self.board, flush=True)
                    self.turnReward += 20
                    self.turnReward += round(13 - (self.turnsTaken / 2))

                    numBlocked = self.__blockingAlgorythm(x, y, self.playerPiece)

                    if numBlocked == 2:
                        self.turnReward += 5

                    if numBlocked == 3:
                        self.turnReward += 10

                    self.game_over = True
                self.__swapTurn()
                return True
        return False

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
                    return False
                continue
            rowCount += 1
            cx += dx
            cy += dy 

    def __blockingAlgorythm(self, x, y, player) -> int:
        enemyPiece = lambda player : 1 if (player == 2) else 2 
        dx = 0
        dy = 1
        cx = x + dx
        cy = y + dy
        rowCount = 0
        maxCount = 0

        # scan direction
        while True:
            if rowCount >= 4:
                self.turnReward = maxCount
                return True
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
                    return False
                continue
            rowCount += 1
            cx += dx
            cy += dy 