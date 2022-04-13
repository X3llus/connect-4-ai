from ast import If
from tkinter import END
import numpy as np

class ConnectGame:
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
        foundCount = 0
        for y in range (5):
            for x in range (5):
                if self.board[x][y] == player:
                    foundCount += 1
                else:
                    if foundCount > 0:
                        break
        if foundCount > 3:
            return True
        foundCount = 0
        for x in range (5):
            for y in range (5):
                if self.board[x][y] == player:
                    foundCount += 1
                else:
                    if foundCount > 0:
                        break
        if foundCount > 3:
            return True
        return False
