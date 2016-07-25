import random
grid = []
playerWon = False
compWon = False
hexChar = "□"
compChar = "⬡"
playerChar = "⬢"
turnCurrent = "player"
size = 3
neighbors = [[0,1],     #upRight
              [1,0],    #right
              [1,-1],    #downRight
              [0,-1],    #downLeft
              [-1,0],    #left
              [-1,1]]   #upLeft

smartNeighbors = [[1,-1],
                  [-1,1]]


for i in range(size):
    columns = []
    for j in range(size):
        columns.append(hexChar)
    grid.append(columns)
    
def changeColour(colour, x, y):
    grid[x][y] = colour

def clamp(n, smallest, largest): return max(smallest, min(n, largest))
def clampBoard(n): return max(0, min(n, size - 1))

def checkPlayerWon():
    startList = []
    for rowNumber, row in enumerate(grid):
        if row[0] == playerChar:
            startList.append(rowNumber)
    for startRow in startList:
        col = 0
        prevRow = startRow
        stillLooking = True
        while stillLooking:
            stillLooking = False
            col += 1
            if grid[clampBoard(prevRow + 1)][clampBoard(col - 1)] == playerChar and prevRow < size - 1:
                col -= 1
                prevRow += 1
                stillLooking = True
            elif grid[clampBoard(prevRow)][clampBoard(col)] == playerChar:
                stillLooking = True
            elif grid[clampBoard(prevRow - 1)][clampBoard(col)] == playerChar:
                prevRow -= 1
                stillLooking = True
            if col >= size:
                return True
        return False
            
def checkCompWon():
    startList = []
    for colNumber, col in enumerate(grid[0]):
        if col == compChar:
            startList.append(colNumber)
    for startCol in startList:
        row = 0
        prevCol = startCol
        stillLooking = True
        while stillLooking:
            stillLooking = False
            row += 1
            if grid[clampBoard(row)][clampBoard(prevCol)] == playerChar:
                stillLooking = True
            elif grid[clampBoard(row)][clampBoard(prevCol - 1)] == playerChar:
                prevCol -= 1
                stillLooking = True
            if row >= size:
                return True
        return False

def compMove():
    playerSpots = []
    compSpots =[]
    emptySpots = []
    possibleMoves = []
    for i, row in enumerate(grid):
        for j, col in enumerate(row):
            if col == playerChar:
                playerSpots.append([i,j])
            elif col == compChar:
                compSpots.append([i,j])
            elif col == hexChar:
                emptySpots.append([i,j])
    for spot in emptySpots:
        for neighbor in smartNeighbors:
            coordToCheck = [clampBoard(spot[1] + neighbor[0]), clampBoard(spot[0] + neighbor[1])]
            spotToCheck = grid[coordToCheck[1]][coordToCheck[0]]
            if spotToCheck == compChar and possibleMoves.count(spot) == 0:
                possibleMoves.append(spot)
    if len(possibleMoves) > 0:
        return random.choice(possibleMoves)
    else:
        start = [int((size - 1) / 2) , int((size - 1) / 2)]
        if grid[start[0]][start[1]] == hexChar:
            return start
        else:
            rand = [random.randint(0,size - 1) , random.randint(0,size - 1)]
            return rand
    
while not playerWon and not compWon:
    if turnCurrent == "comp":
        colour = compChar
        tries = 0
        while tries < 10:
            compMoveXY = compMove()
            compMoveX = compMoveXY[0]
            compMoveY = compMoveXY[1]
            tries += 1
            if grid[compMoveX][compMoveY] == hexChar and tries <= 10:
                changeColour(colour, compMoveX, compMoveY)
                break
            elif tries >= 10:
                break
                print("computer can't move")
        if checkCompWon():
            print("You Lose!")
            compWon = True
    elif turnCurrent == "player":
        for i in range(size - 1, -1, -1):
            indent = " " * i
            print(indent + " ".join(grid[i]))
        colour = playerChar
        inputCoord = list(map(int, input("Enter coordinates: (x,y): ").split(".")))
        while not grid[inputCoord[1]-1][inputCoord[0]-1] == hexChar:
            inputCoord = list(map(int, input("Enter coordinates: (x,y): ").split(".")))
        changeColour(colour, inputCoord[1]-1, inputCoord[0]-1)
        if checkPlayerWon():
            print("You win!")
            playerWon = True
    if turnCurrent == "player":
        turnCurrent = "comp"
    else:
        turnCurrent = "player"


for i in range(size - 1, -1, -1):
    indent = " " * i
    print(indent + " ".join(grid[i]))

##def oldCheckCompWon():
##    startList = []
##    for i, col in enumerate(grid[0]):
##        if col == compChar:
##            startList.append(i)
##    col = 1
##    for start in startList:
##        while grid[clamp(col,0,size - 1)][start] == compChar:
##            if col >= size - 1:
##                return True
##            col += 1
##        col = 1
##        while grid[col][start - 1] == compChar:
##            if col >= size - 1:
##                return True
##            col += 1
##        col = 1
##        while grid[col][clamp(start + 1,0,size -1 )] == compChar:
##            if col >= size - 1:
##                return True
##            col += 1
