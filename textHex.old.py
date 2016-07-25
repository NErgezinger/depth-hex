import random
import time
from copy import deepcopy
from statistics import mode
import numpy
import scipy.stats
board = []
gameWon = False
hexChar = "□"
compChar = "⬡"
playerChar = "⬢"
turn = "comp"
size = 5
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

def printBoard(b):
    for i in range(size - 1, -1, -1):
        printRow = []
        for row in b:
            printRow.append(row[i])
        indent = " " * i
        print(indent + " ".join(printRow))

def changeColour(c, x, y):
    board[x][y] = c

def getAdj(colour,x,y,b):
    sameAdj = []
    for n in adjList:
        toCheck = [x + n[0], y + n[1]]
        if 0 <= toCheck[0] <= size - 1 and 0 <= toCheck[1] <= size - 1:
            if b[toCheck[0]][toCheck[1]] == colour:
                sameAdj.append(toCheck)
##    print("(" + str(x) + "," + str(y) + ") is adj to " + str(sameAdj))
    return sameAdj

def getSpots(c,b):
    spots = []
    for colNum,col in enumerate(b):
        for rowNum,row in enumerate(col):
            if row == c:
                spots.append([colNum, rowNum])
    return spots

def checkPlayerWon(b):
    searched = []
    connectedToLeft = []
    playerSpots = []
    rightEdge = []
    for i in range(size):
        rightEdge.append([size-1,i])
    for rowNum,row in enumerate(b[0]):
        if row == playerChar:
            connectedToLeft.append([0,rowNum])
    playerSpots = getSpots(playerChar, b)
    for i in range(size * size):
        for spot in playerSpots:
            adjSpots = getAdj(playerChar, spot[0], spot[1], b)
            for adj in adjSpots:
                if adj in connectedToLeft and spot not in connectedToLeft:
                    connectedToLeft.append(spot)
    for spot in connectedToLeft:
        if spot in rightEdge:
            return True
    return False

def checkCompWon(b):
    searched = []
    connectedToBottom = []
    compSpots =[]
    topEdge = []
    for i in range(size):
        topEdge.append([i,size-1])
    for colNum,col in enumerate(b):
        if col[0] == compChar:
            connectedToBottom.append([colNum,0])
    compSpots = getSpots(compChar, b)
    for i in range(size * size):
        for spot in compSpots:
            adjSpots = getAdj(compChar, spot[0], spot[1], b)
            for adj in adjSpots:
                if adj in connectedToBottom and spot not in connectedToBottom:
                    connectedToBottom.append(spot)
    for spot in connectedToBottom:
        if spot in topEdge:
            return True
    return False
    
def compMove():
    emptySpots = []
    winResult = []
    emptySpots = getSpots(hexChar, board)
    startTime = time.clock()
    duration = 10
    count = 0
    while startTime + duration > time.clock():
        for spot in emptySpots:
            outcome = simulateGame(compChar, spot)
            if outcome:
                winResult.append(spot)
            count += 1
    common = scipy.stats.mode(winResult)[0]
    common = common.astype(int)
    common = common[0]
    print("Searched: ", count)
    return common

def simulateGame(simPlayer, startMove):
    simBoard = deepcopy(board)
    simBoard[startMove[0]][startMove[1]] = simPlayer
    emptySpots = getSpots(hexChar, simBoard)

    while len(emptySpots) > 0:
        rPlayerMove = random.choice(emptySpots)
        simBoard[rPlayerMove[0]][rPlayerMove[1]] = playerChar
        if checkPlayerWon(simBoard):
            return False
        emptySpots = getSpots(hexChar, simBoard)
        if len(emptySpots) > 0:
            rCompMove = random.choice(emptySpots)
            simBoard[rCompMove[0]][rCompMove[1]] = compChar
        if checkCompWon(simBoard):
            return True
        emptySpots = getSpots(hexChar, simBoard)

    print("Simulation board is full, but no winner. This shouldn't happen")
    

def main():
    global turn
    if turn == "comp":
        moveCoord = compMove()
        changeColour(compChar, moveCoord[0], moveCoord[1])
        if checkCompWon(board):
            print("YOU LOSE!")
            gameWon = True
        turn = "player"
    elif turn == "player":
        printBoard(board)
        inputCoord = list(map(int, input("Enter coordinates: (x,y): ").split(".")))
        while not board[inputCoord[0]-1][inputCoord[1]-1] == hexChar:
            inputCoord = list(map(int, input("Enter coordinates: (x,y): ").split(".")))
        changeColour(playerChar, inputCoord[0]-1, inputCoord[1]-1)
        if checkPlayerWon(board):
            print("YOU WIN!")
            gameWon = True
        turn = "comp"
    

while not gameWon:
    main()
