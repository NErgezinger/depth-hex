import random
import time
import sys
import cProfile
from multiprocessing import Pool, cpu_count
import numpy as np
board = []
history = []
gameWon = False
hexChar = "*"
black = "b"
white = "w"
size = 5
searchTime = 10
maxSearches = 10000
cmdQuit = False
profiling = False
version = 3.0

adjList = [[1,1], #upRight
           [1,0], #right
           [0,-1],#downRight
           [-1,-1],#downLeft
           [-1,0],#left
           [0,1]]#upLeft

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
    history.append([x,y])

def undo():
    if len(history) > 0:
        last = history.pop()
        board[last[0]][last[1]] = hexChar

def getAdj(c,x,y,b):
    sameAdj = []
    for n in adjList:
        toCheck = [x + n[0], y + n[1]]
        if 0 <= toCheck[0] <= size - 1 and 0 <= toCheck[1] <= size - 1:
            if b[toCheck[0]][toCheck[1]] == c:
                sameAdj.append(toCheck)
##    sys.stderr.write("(" + str(x) + "," + str(y) + ") is adj to " + str(sameAdj))
    return sameAdj

def getSpots(c,b):
    spots = []
    for colNum,col in enumerate(b):
        for rowNum,row in enumerate(col):
            if row == c:
                spots.append([colNum, rowNum])
    return spots

def checkWin(b,c):
    searched = []
    connected = []
    goalEdge = []

    if c == white:
        #right
        for i in range(size):
            goalEdge.append([size-1,i])
        #left
        for rowNum,row in enumerate(b[0]):
            if row == white:
                connected.append([0,rowNum])
    else:
        #top
        for i in range(size):
            goalEdge.append([i,size-1])
        #bottom
        for colNum,col in enumerate(b):
            if col[0] == black:
                connected.append([colNum,0])

    for spot in connected:
        if spot not in searched:
            searched.append(spot)
            adjSpot = getAdj(c,spot[0],spot[1],b)
            for adj in adjSpot:
                connected.append(adj)

    for goal in goalEdge:
        if goal in connected:
            return True
    return False

def compMove(c):
    possibleSpots = []
    winResultsCount = []
    timesSearched = []
    possibleSpots = getSpots(hexChar, board)
    count = 0
    sys.stderr.write("Starting search\n")
    for i in possibleSpots:
        winResultsCount.append(0)
        timesSearched.append(0)
    numSpots = len(possibleSpots) - 1
    startTime = time.perf_counter()

    p = Pool(int(cpu_count()))
    pSize = 512

    # while count < maxSearches:
    while time.perf_counter() - startTime < searchTime:
        for index, spot in enumerate(possibleSpots):
            pArgs = np.full((pSize, 2), (c, spot))
            outcomes = p.starmap(simulateGame, pArgs)
            timesSearched[index] += pSize
            count += pSize
            winResultsCount[index] += np.count_nonzero(outcomes)

    best = []
    winRate = 0
    bestWinRate = 0
    for index, spot in enumerate(possibleSpots):
        winRate = winResultsCount[index] / timesSearched[index]
        if winRate > bestWinRate:
            bestWinRate = winRate
            best = spot
        
    sys.stderr.write("Searched " + str(count) + " in " + str(time.perf_counter() - startTime) + "s\n")
    sys.stderr.write(str(best) + " won " + str(np.round(bestWinRate, 3) * 100) + "% of random games\n")

    if len(best) > 0:
        return best
    else:
        return random.choice(possibleSpots)

def simulateGame(simPlayer, startMove):
    simBoard = []
    for i in board:
        n = []
        for j in i:
            n.append(j)
        simBoard.append(n)

    simBoard[startMove[0]][startMove[1]] = simPlayer
    emptySpots = getSpots(hexChar, simBoard)

    if simPlayer == black:
        while len(emptySpots) > 0:
            rWhiteMove = random.choice(emptySpots)
            simBoard[rWhiteMove[0]][rWhiteMove[1]] = white
            emptySpots.remove(rWhiteMove)

            if len(emptySpots) > 0:
                rBlackMove = random.choice(emptySpots)
                simBoard[rBlackMove[0]][rBlackMove[1]] = black
                emptySpots.remove(rBlackMove)
                
        if checkWin(simBoard, black):
            return True
        else: return False

    elif simPlayer == white:
        while len(emptySpots) > 0:
            rBlackMove = random.choice(emptySpots)
            simBoard[rBlackMove[0]][rBlackMove[1]] = black
            emptySpots.remove(rBlackMove)

            if len(emptySpots) > 0:
                rWhiteMove = random.choice(emptySpots)
                simBoard[rWhiteMove[0]][rWhiteMove[1]] = white
                emptySpots.remove(rWhiteMove)

        if checkWin(simBoard, white):
            return True
        else: return False

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
        print("= depth-hex")
        print()

    elif cmd[0] == "version":
        print("= 1")
        print()

    elif cmd[0] == "genmove":
        if cmd[1] == "b" or cmd[1] == "black":
            if checkWin(board,white) or checkWin(board,black):
                print("= resign")
                print()
            else:
                if profiling:
                    cProfile.run('compMove(black)', sort='time')
                    move = [2,2]
                else: move = compMove(black)
                changeColour(black, move[0], move[1])
                fmove = convertMove(move)
                print("= ", fmove)
                print()
        elif cmd[1] == "w" or cmd[1] == "white":
            if checkWin(board,white) or checkWin(board,black):
                print("= resign")
                print()
            else:
                if profiling:
                    cProfile.run('compMove(white)')
                    move = [2,2]
                else: move = compMove(white)
                changeColour(white, move[0], move[1])
                fmove = convertMove(move)
                print("= ", fmove)
                print()
        else:
            print("? invalid color")

    elif cmd[0] == "play":
        if cmd[2] == "resign":
            print("= ")
            print()
        elif cmd[1] == "b" or cmd[1] == "black":
            play(black, cmd[2])
            print("= ")
            print()
        elif cmd[1] == "w" or cmd[1] == "white":
            play(white, cmd[2])
            print("= ")
            print()
        else:
            print("= ")
            print()

    elif cmd[0] == "undo":
        undo()
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
        if checkWin(board,white):
            print("= W")
            print()
        elif checkWin(board,black):
            print("= B")
            print()
        else:
            print("= ")
            print()

    elif cmd[0] == "hexgui-analyze_commands":
        print("= ")
        print()
