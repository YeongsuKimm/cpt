import math

paths = []

def nextSpot(row, col, board, path=[]):
    path.append(str(row) + str(col))
    while True:
        lst = getSpots(row, col, path, board)
        if len(lst) == 1:
            path.append(lst[0])
            row = int(lst[0][0])
            col = int(lst[0][1])
        elif len(lst) > 1:
            for spot in lst:
                nextSpot(int(spot[0]), int(spot[1]), board, path.copy())
            break
        else: 
            paths.append(path)
            break
    return path

def getSpots(row, col, path, board):
    value = int(board[row][col])
    lst = []
    for i in range(3):
        for k in range(3):
            if i == 1 and k == 1:
                continue
            if row - 1 + i >= 0 and row - 1 + i < 8 and col - 1 + k >= 0 and col - 1 + k < 5:
                if int(board[row - 1 + i][col - 1 + k]) == value or int(board[row - 1 + i][col - 1 + k]) == value * 2:
                    if str(str(row - 1 + i) + str(col - 1 + k)) not in path:
                        lst.append(str(row - 1 + i) + str(col - 1 + k))
    return lst

def game2248(cBoard):
    paths.clear()
    board = cBoard.split()
    board2 = []
    count = 0
    for i in range(8):
        temp = []
        for j in range(5):
            temp.append(board[count])
            count += 1
        board2.append(temp)
    
    past = ""
    horStarts = []
    vertStarts = []
    diagStarts1 = []
    diagStarts2 = []
    
    for i in range(8):
        for k in range(5):
            if past == "":
                past = board2[i][k]
            else:
                if past == board2[i][k]:
                    horStarts.append(str(i) + str(k))
            past = board2[i][k]
        past = ""

    for i in range(5):
        for k in range(8):
            if past == "":
                past = board2[k][i]
            else:
                if past == board2[k][i]:
                    vertStarts.append(str(k) + str(i))
            past = board2[k][i]
        past = ""

    for i in range(8):
        past = ""
        for k in range(5):
            if i + k < 8:
                if past == board2[i + k][k]:
                    diagStarts1.append(str(i + k) + str(k))
                past = board2[i + k][k]
        past = ""

    for i in range(5):
        past = ""
        for k in range(4):
            if i + k < 5:
                if board2[k][i + k] == past:
                    diagStarts1.append(str(k) + str(i + k))
                past = board2[k][k + i]
        past = ""

    for i in range(8):
        past = ""
        for k in range(4, 0, -1):
            if i + (4 - k) < 8:
                if past == board2[i + (4 - k)][k]:
                    diagStarts2.append(str(i + (4 - k)) + str(k))
                past = board2[i + (4 - k)][k]
        past = ""

    for i in range(5):
        past = ""
        for k in range(4):
            if 3 - (i + k) < 5 and 3 - (i + k) >= 0:
                if board2[k][3 - (i + k)] == past:
                    diagStarts2.append(str(k) + str(3 - (i + k)))
                past = board2[k][3 - (i + k)]
        past = ""
    
    for start in horStarts:
        path = []
        nextSpot(int(start[0]), int(start[1]), board=board2, path=path)
        path = []
        nextSpot(int(start[0]), int(start[1]) - 1, board=board2, path=path)
    for start in vertStarts:
        path = []
        nextSpot(int(start[0]), int(start[1]), board=board2, path=path)
        path = []
        nextSpot(int(start[0]) - 1, int(start[1]), board=board2, path=path)
    for start in diagStarts1:
        path = []
        nextSpot(int(start[0]), int(start[1]), board=board2, path=path)
        path = []
        nextSpot(int(start[0]) - 1, int(start[1]) - 1, board=board2, path=path)
    for start in diagStarts2:
        path = []
        nextSpot(int(start[0]), int(start[1]), board=board2, path=path)
        path = []
        nextSpot(int(start[0]) - 1, int(start[1]) + 1, board=board2, path=path)
    
    maxLst = []
    maxLen = 0
    for i in paths:
        if len(i) > maxLen:
            maxLen = len(i)
    for i in paths:
        if len(i) == maxLen:
            maxLst.append(i)
        
    maxLst2 = []
    for i in maxLst:
        string = ""
        for j in i:
            string += j
        maxLst2.append(string)
    
    maxLst2 = sorted(maxLst2)
    pathString = maxLst2[0]
    path = ""
    for i in range(len(pathString)):
        if i % 2 == 1:
            path += pathString[i] + " "
        else:
            path += pathString[i]
    
    path = path[:-1]
    
    path = path.split()
    
    total = 0
    for i in path:
        total += int(board2[int(i[0])][int(i[1])])
        board2[int(i[0])][int(i[1])] = 0
    
    temp = 2
    while total > temp:
        temp *= 2
    replace = temp

    board2[int(path[-1][0])][int(path[-1][1])] = replace
    maxNum = 0
    for i in range(5):
        for k in range(8):
            if int(board2[k][i]) > maxNum:
                maxNum = int(board2[k][i])
    
    minNum = 2 ** (math.log(maxNum, 2) - 8)

    for i in range(5):
        for k in range(8):
            if int(board2[k][i]) <= minNum:
                board2[k][i] = 0

    for i in range(5):
        for j in range(8):
            if board2[j][i] == 0:
                for k in range(j, 0, -1):
                    board2[k][i] = board2[k - 1][i]
                    board2[k - 1][i] = 0
    
    String = ""
    current = maxNum
    for i in range(8):
        for j in range(5):
            if current == minNum:
                current = maxNum
            if board2[i][j] == 0:
                board2[i][j] = str(int(current))
                current /= 2
            String += str(board2[i][j]) + " "
    
    String = String[:-1]
    return String

def game(board):
    for i in range(3):
        print("_______________")
        board = game2248(board)
    return board

print(game("4 128 4 128 32 16 16 4 256 16 32 4 16 64 4 8 64 64 256 8 16 2 2 256 4 32 128 2 64 8 256 32 128 16 2 8 32 32 4 32"))

