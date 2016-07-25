version = 2.4
import random
import time
from copy import deepcopy
# import numpy
# import scipy.stats
board = []
gameWon = False
hexChar = "*"
compChar = "b"
playerChar = "w"
turn = "player"
size = 3
duration = 5
cmdQuit = False
adjListo = [[0,1], #upRight
           [1,0], #right
           [1,-1],#downRight
           [0,-1],#downLeft
           [-1,0],#left
           [-1,1]]#upLeft

adjList = [[1,1], #upRight
           [1,0], #right
           [0,-1],#downRight
           [-1,-1],#downLeft
           [-1,0],#left
           [0,1]]#upLeft

#board initialization
def resetBoard(b):
    b = []
    for i in range(size):
        row = []
        for j in range(size):
            row.append(hexChar)
        b.append(row)
    return b
        
board = resetBoard(board)

def printBoard(b):
    for i in range(size - 1, -1, -1):
        printRow = []
        for row in b:
            printRow.append(row[i])
        indent = " " * ((size - i) - 1)
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
    for i in playerSpots:
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
    for i in compSpots:
        for spot in compSpots:
            adjSpots = getAdj(compChar, spot[0], spot[1], b)
            for adj in adjSpots:
                if adj in connectedToBottom and spot not in connectedToBottom:
                    connectedToBottom.append(spot)
    for spot in connectedToBottom:
        if spot in topEdge:
            return True
    return False
    
def compMove(c):
    global duration
    emptySpots = []
    winResults = []
    winResultsCount = []
    emptySpots = getSpots(hexChar, board)
    startTime = time.clock()
    count = 0
    for i in emptySpots:
        winResultsCount.append(0)
##    print("Starting search for:", duration, "seconds")
    while startTime + duration > time.clock() or len(winResults) == 0:
        for spot in emptySpots:
            if startTime + duration < time.clock() and len(winResults) > 0: break
            outcome = simulateGame(c, spot)
            if outcome:
                if spot in winResults:
                    winResultsCount[winResults.index(spot)] += 1
                else:
                    winResults.append(spot)
            count += 1
            
    best = winResults[winResultsCount.index(max(winResultsCount))]
##    print("Searched: ", count)
##    print("Chosen position won:", max(winResultsCount), "times")
    return best

def simulateGame(simPlayer, startMove):
    simBoard = deepcopy(board)
    simBoard[startMove[0]][startMove[1]] = simPlayer
    emptySpots = getSpots(hexChar, simBoard)

    if simPlayer == compChar:
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
    elif simPlayer == playerChar:
        while len(emptySpots) > 0:
            rPlayerMove = random.choice(emptySpots)
            simBoard[rPlayerMove[0]][rPlayerMove[1]] = compChar
            if checkCompWon(simBoard):
                return False
            emptySpots = getSpots(hexChar, simBoard)
            if len(emptySpots) > 0:
                rCompMove = random.choice(emptySpots)
                simBoard[rCompMove[0]][rCompMove[1]] = playerChar
            if checkPlayerWon(simBoard):
                return True
            emptySpots = getSpots(hexChar, simBoard)

##    print("Simulation board is full, but no winner. This shouldn't happen")
    

##def main():
##    global turn
##    global gameWon
##    if turn == "player":
##        printBoard(board)
##        inputCoord = list(map(int, input("Enter coordinates: (x,y): ").split(".")))
##        while not board[inputCoord[0]-1][inputCoord[1]-1] == hexChar:
##            inputCoord = list(map(int, input("Enter coordinates: (x,y): ").split(".")))
##        changeColour(playerChar, inputCoord[0]-1, inputCoord[1]-1)
####        moveCoord = compMove(playerChar)
####        changeColour(playerChar, moveCoord[0], moveCoord[1])
##        printBoard(board)
##        if checkPlayerWon(board):
##            print("WHITE WINS!")
##            printBoard(board)
##            gameWon = True
##        turn = "comp"
##    elif turn == "comp":
##        moveCoord = compMove(compChar)
##        changeColour(compChar, moveCoord[0], moveCoord[1])
####        printBoard(board)
##        if checkCompWon(board):
##            print("BLACK WINS!")
##            printBoard(board)
##            gameWon = True
##        turn = "player"   

def play(c, ac):
    acl = [0,0]
    acl[0] = ord(ac[0]) - 96
    acl[1] = abs(int(ac[1:]) - size) + 1
    changeColour(c, acl[0]-1, acl[1]-1)

def convertMove(move):
    move[0] = chr(move[0]+97)
    move[1] = abs(move[1] - size)
    move[1] = str(move[1])
    s = "".join(move)
    return s

while not cmdQuit:
    cmd = input().split(" ")
    
    if cmd[0] == "name":
        print("= textHex")
        print()
        
    elif cmd[0] == "version":
##        print("=", str(version))
        print("= 1")
        print()
    elif cmd[0] == "genmove":
        if cmd[1] == "b" or cmd[1] == "black":
            if not checkPlayerWon(board) and not checkCompWon(board):
                move = compMove(compChar)
                changeColour(compChar, move[0], move[1])
                fmove = convertMove(move)
                print("= ", fmove)
                print()
            else:
                print("= resign")
                print()
        elif cmd[1] == "w" or cmd[1] == "white":
            if not checkCompWon(board) and not checkPlayerWon(board):
                move = compMove(playerChar)
                changeColour(playerChar, move[0], move[1])
                fmove = convertMove(move)
                print("= ", fmove)
                print()
            else:
                print("= resign")
                print()
        else:
            print("? invalid color")

    elif cmd[0] == "play":
        if cmd[1] == "b" or cmd[1] == "black":
            play(compChar, cmd[2])
            print("= ")
            print()
        elif cmd[1] == "w" or cmd[1] == "white":
            play(playerChar, cmd[2])
            print("= ")
            print()
        else:
            print("? invalid color")
            print()
            
    elif cmd[0] == "undo":
        print("= ")
        print()

    elif cmd[0] == "showboard":
        print("= ")
        printBoard(board)
        print()

    elif cmd[0] == "boardsize":
        if cmd[1] == cmd[2]:
            size = int(cmd[1])
            board = resetBoard(board)
            print("= ")
            print()
        else:
            print("? incorrect board size")
            print()

    elif cmd[0] == "quit":
        print("= ")
        print()
        cmdQuit = True

    elif cmd[0] == "final_score":
        if checkPlayerWon(board):
            print("= W")
            print()
        elif checkCompWon(board):
            print("= B")
            print()
        else:
            print("=")
            print()

    elif cmd[0] == "hexgui-analyze_commands":
        print("= ")
        print()
    
