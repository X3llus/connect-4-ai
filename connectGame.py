from ast import If
from time import sleep
from tkinter import END
import numpy as np

class ConnectGame:
    board = np.zeros((5,5))
    playerPiece = 1
    turnsTaken = 0
    gameOver = False
    turnReward = 0
    player1score = 0
    player2score = 0

    def reset(self):
        self.board = np.zeros((5,5))
        self.playerPiece = 1
        self.turnsTaken = 0
        self.gameOver = False
        self.turnReward = 0
        self.player1score = 0
        self.player2score = 0

    def getBoard(self):
        return self.board
    
    def getGO(self):
        return self.gameOver

    def playPiece(self, x: list[int]):
        x = x.index(1)
        if x < 0 or x > 4:
            pass
        elif self.board[0][x] == 0:
            self.__placePiece(x)
            if self.playerPiece == 1:
                return self.turnReward, self.player1score, True
            else:
                return self.turnReward, self.player2score, True
        return 0, 0, False
            
    def __placePiece(self, x):
        for y in range (4, -1, -1):
            if self.board[y][x] == 0:
                self.board[y][x] = self.playerPiece
                if self.__checkSolved(x, y):
                    self.turnReward += 10
                    self.gameOver = True
                    if self.playerPiece == 1:
                        self.player1score += self.turnReward
                    else:
                        self.player2score += self.turnReward
                self.__swapTurn()
                return True
        return False

    def __swapTurn(self):
        if self.playerPiece == 1:
            self.playerPiece = 2
        else:
            self.playerPiece = 1
        self.turnsTaken += 1
        self.turnReward = 0
        print(self.getBoard())

    def __checkSolved(self, x, y):
        if self.__solvingAlgorythm(x, y, self.playerPiece) == True:
            print("Win Player ", self.playerPiece)

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
