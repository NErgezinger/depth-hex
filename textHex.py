import random
import time
import sys
import cProfile
import numpy as np
board = []
history = []
gameWon = False
hexChar = "*"
blackChar = "b"
whiteChar = "w"
size = 5
duration = 10
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

def checkWhiteWon(b):
    searched = [] 
    connectedToLeft = []
    rightEdge = []
    for i in range(size):
        rightEdge.append([size-1,i])
    for rowNum,row in enumerate(b[0]):
        if row == whiteChar:
            connectedToLeft.append([0,rowNum])
            
    for spot in connectedToLeft:
        if spot not in searched:
            searched.append(spot)
            adjSpot = getAdj(whiteChar,spot[0],spot[1],b)
            for adj in adjSpot:
                connectedToLeft.append(adj)
    
    for right in rightEdge:
        if right in connectedToLeft:
            return True
    return False
    

def checkBlackWon(b):
    searched = []
    connectedToBottom = []
    topEdge = []
    for i in range(size):
        topEdge.append([i,size-1])
    for colNum,col in enumerate(b):
        if col[0] == blackChar:
            connectedToBottom.append([colNum,0])
    
    for spot in connectedToBottom:
        if spot not in searched:
            searched.append(spot)
            adjSpot = getAdj(blackChar,spot[0],spot[1],b)
            for adj in adjSpot:
                connectedToBottom.append(adj)
    for spot in topEdge:
        if spot in connectedToBottom:
            return True
    return False
    
def compMove(c):
    global duration
    possibleSpots = []
    winResultsCount = []
    timesSearched = []
    possibleSpots = getSpots(hexChar, board)
    startTime = time.clock()
    count = 0
    sys.stderr.write("Starting search for " + str(duration) + "s\n")
    for i in possibleSpots:
        winResultsCount.append(0)
        timesSearched.append(0)
    while startTime + duration > time.clock():
        spot = random.choice(possibleSpots)
        outcome = simulateGame(c, spot)
        count += 1
        if outcome:
            winResultsCount[possibleSpots.index(spot)] += 1
        timesSearched[possibleSpots.index(spot)] += 1
    best = []
    bestWinRate = 0
    for i,spot in enumerate(possibleSpots):
        winRate = (winResultsCount[i] / timesSearched[i])
        if winRate > bestWinRate:
            best = spot
            bestWinRate = winRate
            
    sys.stderr.write("Searched: " + str(count) + "\n")
    sys.stderr.write(str(best) + " won " + str(bestWinRate * 100) +"% of the time\n")

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

    if simPlayer == blackChar:
        while len(emptySpots) > 0:
            rWhiteMove = random.choice(emptySpots)
            simBoard[rWhiteMove[0]][rWhiteMove[1]] = whiteChar
            emptySpots.pop(emptySpots.index(rWhiteMove))

            if len(emptySpots) > 0:
                rBlackMove = random.choice(emptySpots)
                simBoard[rBlackMove[0]][rBlackMove[1]] = blackChar
                emptySpots.pop(emptySpots.index(rBlackMove))
            
        if checkWhiteWon(simBoard):
                return False
        if checkBlackWon(simBoard):
                return True
            
    elif simPlayer == whiteChar:
        while len(emptySpots) > 0:
            rBlackMove = random.choice(emptySpots)
            simBoard[rBlackMove[0]][rBlackMove[1]] = blackChar
            emptySpots.pop(emptySpots.index(rBlackMove))

            if len(emptySpots) > 0:
                rWhiteMove = random.choice(emptySpots)
                simBoard[rWhiteMove[0]][rWhiteMove[1]] = whiteChar
                emptySpots.pop(emptySpots.index(rWhiteMove))

        if checkWhiteWon(simBoard):
                return True
        if checkBlackWon(simBoard):
                return False

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
        print("= 1")
        print()
        
    elif cmd[0] == "genmove":
        if cmd[1] == "b" or cmd[1] == "black":
            if checkWhiteWon(board) or checkBlackWon(board):
                print("= resign")
                print()
            else:
                if profiling:
                    cProfile.run('compMove(whiteChar)')
                    move = [2,2]
                else: move = compMove(blackChar)
                changeColour(blackChar, move[0], move[1])
                fmove = convertMove(move)
                print("= ", fmove)
                print()
        elif cmd[1] == "w" or cmd[1] == "white":
            if checkBlackWon(board) or checkWhiteWon(board):
                print("= resign")
                print()
            else:
                if profiling:
                    cProfile.run('compMove(whiteChar)')
                    move = [2,2]
                else: move = compMove(whiteChar)
                changeColour(whiteChar, move[0], move[1])
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
            play(blackChar, cmd[2])
            print("= ")
            print()
        elif cmd[1] == "w" or cmd[1] == "white":
            play(whiteChar, cmd[2])
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
        if checkWhiteWon(board):
            print("= W")
            print()
        elif checkBlackWon(board):
            print("= B")
            print()
        else:
            print("= ")
            print()

    elif cmd[0] == "hexgui-analyze_commands":
        print("= ")
        print()
    
