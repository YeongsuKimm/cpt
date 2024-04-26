import math
def game2248(cBoard):
    board = cBoard.split()
    board2 = []
    count = 0
    paths = []
    diagStarts1 = []
    diagStarts2 = []
    horStarts = []
    vertStarts = []
    for i in range(8):
        temp = []
        for j in range(5):
            temp.append(board[count])
            count+=1
        board2.append(temp)
    
    for i in board2:
        print(i)
    # check horizontal
    past = ""    
    for i in range(8):
        for k in range(5):
            if past == "":
                past = board2[i][k];
            else:
                if(past == board2[i][k]):
                    pass
                    # print("hori double " + str(i) +" + " +str(k) + " past :  " + past)
                    horStarts.append(str(i)+str(k))
                if(k == 4):
                    past="";
                past = board2[i][k]
    # check vertical
    past = "";
    for i in range(5):
        for k in range(8):
            if past == "":
                past = board2[k][i];
            else:
                if(past == board2[k][i]):
                    pass
                    # print("vert double " + str(k) +" + " +str(i) + " past :  " + past)
                    vertStarts.append(str(k)+str(i))
                if(k == 7):
                    past="";
                past = board2[k][i]
    # check diagonal (left to right)
    past = "";
    for i in range(8):#checks vert
        past = "";
        for k in range(5):
            if(i+k<8):
                # print(str(i+k) + str(k));
                if(past == board2[i+k][k]):
                    pass
                    diagStarts1.append(str(i+k)+str(k))
                    # print("diag double(l-r)" + str(i+k) + str(k))
                past = board2[i+k][k]
    past = "";
    for i in range(5):
        past=""
        for k in range(4):
            if(i+k<5):
                # print("diag double(l-r)" + str(k) + str(i+k))
                if(board2[k][i+k] == past):
                    diagStarts1.append(str(k)+str(i+k))
                    # print("diag double(l-r)" + str(k) + str(i+k))
                past = board2[k][k+i]

    
    # check diagonal (right to left)
    past = "";
    for i in range(8):#checks vert
        past=""
        for k in range(4,0,-1):
            if(i+(4-k)<8):
                if(past == board2[i+(4-k)][k]):
                    pass
                    diagStarts2.append(str(i+(4-k))+str(k))
                    # print("diag double(r-l)" + str(i+(4-k)) + str(k))
                past = board2[i+(4-k)][k]
    
    past = "";
    for i in range(5):
        past=""
        for k in range(4):
            if(3-(i+k)<5 and 3-(i+k) >= 0):
                if(board2[k][3-(i+k)] == past):
                    diagStarts2.append(str(k)+str(3-(i+k)))
                    # print("diag double(r-l)" + str(k) + str(3-(i+k)))
                past = board2[k][3-(i+k)]
    
    print(horStarts)
    for start in horStarts:
        print(nextSpot(int(start[0]),int(start[1]),paths,board2));
        break
    
    path = "13 23 32 41 51 61 72 82 83";
    path = path.split()
    total = 0;
    for i in path:
        total += int(board2[int(i[0])-1][int(i[1])-1])
        board2[int(i[0])-1][int(i[1])-1] = 0;
    
    temp = 2;
    while(total > temp):
        temp*=2;
    replace = temp;
   
    board2[int(path[-1][0])-1][int(path[-1][1])-1] = replace
    max = 0;
    for i in range(5):
        for k in range(8):
            if(int(board2[k][i])> max):
                max = int(board2[k][i])
    
    min = 2**(math.log(max,2)-8)

    for i in range(5):
        for k in range(8):
            if(int(board2[k][i])<=min):
                board2[k][i] = 0

    
    # bring stuff down
    for i in range(5):
        for j in range(8):
            if board2[j][i] == 0:
                for k in range(j,0,-1):
                    board2[k][i] = board2[k-1][i]
                    board2[k-1][i] = 0
    # print()
    # for i in board2:
    #     print(i)
        
    
    # fill in
    # for i in range()
    String = ""
    current = max
    for i in range(8):
        for j in range(5):
            if current == min:
                current = max
            if board2[i][j] == 0:
                board2[i][j] = str(int(current))
                current/=2
            String += str(board2[i][j]) + " "
            
    String = String[:-1]        
    # print()
    # for i in board2:
    #     print(i)  
    # print(String)


def nextSpot(row, col, path, board):
    value = int(board[row][col])
    print("_________________________________")
    print(str(row)+str(col)+"=============>")
    path.append(str(row)+str(col))
    lst = []
    # print(path)
    for i in range(3):
        for k in range(3):
            if(i==1 and k==1):
                continue
            if((row-1+i >= 0 and row-1+i < 5) and (col-1+k >= 0 and col-1+k< 8)):
                if(int(board[row-1+i][col-1+k]) == value or int(board[row-1+i][col-1+k]) == value*2):
                    if(str(str(row-1+i)+str(col-1+k)) in path):
                        pass
                    else:
                        lst.append(str(row-1+i)+str(col-1+k))
                        lst.append(nextSpot(row-1+i,col-1+k,path,board))
                        print(lst)
    return lst
        
        
game2248("4 128 4 128 32 16 16 4 256 16 32 4 16 64 4 8 64 64 256 8 16 2 2 256 4 32 128 2 64 8 256 32 128 16 2 8 32 32 4 32")
