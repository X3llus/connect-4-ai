from connectGame import ConnectGame

def main():
    game = ConnectGame()
    for i in range (7):
        if i % 2 == 0:
            game.playPiece(2)
        else:
            game.playPiece(3)

if __name__ == '__main__':
    main()