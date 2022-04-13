from ast import If
from time import sleep
from tkinter import END
import numpy as np

class ConnectGame:
    board = np.zeros((5,5))
    playerPiece = 1
    turnsTaken = 0

    def reset():
        board = np.zeros((5,5))
        playerPiece = 1
        turnsTaken = 0

    def getBoard(self):
        return self.board
    
    def playPiece(self, x):
        if x < 0 or x > 4:
            return False
        elif self.board[0][x] == 0:
            self.__placePiece(x)
            return True
        else:
            return False
            
    def __placePiece(self, x):
        for y in range (4, -1, -1):
            if self.board[y][x] == 0:
                self.board[y][x] = self.playerPiece
                if self.__checkSolved(x, y):
                    exit()
                self.__swapTurn()
                return True
        return False

    def __swapTurn(self):
        if self.playerPiece == 1:
            self.playerPiece = 2
        else:
            self.playerPiece = 1
        self.turnsTaken += 1
        print(self.getBoard())

    def __checkSolved(self, x, y):
        if self.__solvingAlgorythm(x, y, self.playerPiece) == True:
            print("Weenor")
        else:
            print("Tiny Weenor")

    def __solvingAlgorythm(self, x, y, player):
        dx = 0
        dy = 1
        cx = x
        cy = y
        rowCount = 0

        # scan direction
        while True:
            if rowCount >= 4:
                return True
            if cx >= 5 or cx < 0 or cy >= 5 or cy < 0 or self.board[cy][cx] != player:
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
                    return False
                continue
            rowCount += 1
            cx += dx
            cy += dy 
