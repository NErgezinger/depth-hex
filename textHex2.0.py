import random
board = []
gameWon = False
hexChar = "□"
compChar = "⬡"
playerChar = "⬢"
turn = "player"
size = 3
adjList = [[0,1], #upRight
           [1,0], #right
           [1,-1],#downRight
           [0,-1],#downLeft
           [-1,0],#left
           [-1,1]]#upLeft

vertAdjList = [[1,-1],
               [-1,1]]

#board initialization
for i in range(size):
    row = []
    for j in range(size):
        row.append(hexChar)
    board.append(row)

def printBoard():
    for i in range(size - 1, -1, -1):
        printRow = []
        for row in board:
            printRow.append(row[i])
        indent = " " * i
        print(indent + " ".join(printRow))

def changeColour(c, x, y):
    board[x][y] = c

def getAdj(colour,x,y):
    sameAdj = []
    for n in adjList:
        toCheck = [x + n[0], y + n[1]]
        if 0 <= toCheck[0] <= size - 1 and 0 <= toCheck[1] <= size - 1:
            if board[toCheck[0]][toCheck[1]] == colour:
                sameAdj.append(toCheck)
##    print("(" + str(x) + "," + str(y) + ") is adj to " + str(sameAdj))
    return sameAdj

def checkPlayerWon():
    searched = []
    connectedToLeft = []
    playerSpots = []
    rightEdge = []
    for i in range(size):
        rightEdge.append([size-1,i])
    for rowNum,row in enumerate(board[0]):
        if row == playerChar:
            connectedToLeft.append([0,rowNum])
    for colNum,col in enumerate(board):
        for rowNum,row in enumerate(col):
            if row == playerChar:
                playerSpots.append([colNum, rowNum])
    for i in range(size * size):
        for spot in playerSpots:
            adjSpots = getAdj(playerChar, spot[0], spot[1])
            for adj in adjSpots:
                if adj in connectedToLeft and spot not in connectedToLeft:
                    connectedToLeft.append(spot)
    for spot in connectedToLeft:
        if spot in rightEdge:
            return True

def checkCompWon():
    searched = []
    connectedToBottom = []
    for colNum,col in enumerate(board):
        if col[0] == compChar:
            print(colNum)
    
    
    


def main():
    if turn == "player":
        printBoard()
        inputCoord = list(map(int, input("Enter coordinates: (x,y): ").split(".")))
        while not board[inputCoord[0]-1][inputCoord[1]-1] == hexChar:
            inputCoord = list(map(int, input("Enter coordinates: (x,y): ").split(".")))
        changeColour(playerChar, inputCoord[0]-1, inputCoord[1]-1)
        if checkPlayerWon():
            print("YOU WIN!")
            gameWon = True


while not gameWon:
    main()
