def calculate_threats(grid, turn):
    kingx, kingy = find_king(grid, turn)
    all = [[]]
    for y in range(8):
        for x in range(8):
            if x != kingx or y != kingy:
                if grid[y][x][1] != -1:
                    all.append([y, x])
            if grid[y][x][1] != -1 and grid[y][x][1] != turn:
                if grid[y][x][0] == 5:
                    all += possible_king(x, y, grid, False)
                elif grid[y][x][0] == 0:
                    all += possible_pawn(x, y, grid, True)
                else:
                    all += calculate_possible([x, y], grid)
    return all

def calculate_possible(highlighted, grid):
    x = highlighted[0]
    y = highlighted[1]
    piece = grid[y][x][0]
    if piece == 0:
        return possible_pawn(x, y, grid, False)
    elif piece == 1:
        return possible_knight(x, y, grid)
    elif piece == 2:
        return possible_bishop(x, y, grid)
    elif piece == 3:
        return possible_rook(x, y, grid)
    elif piece == 4:
        return possible_queen(x, y, grid)  
    
    return possible_king(x, y, grid, True)
    
    
def possible_pawn(x, y, grid, reduced):
    res = []
    #TODO IMPLEMENT EN PESSANT
    
    #white pawns only move up
    turn = grid[y][x][1]
    if turn == 0:
        if not reduced:
            if y == 6:
                for i in [-1,-2]:
                    if grid[y+i][x][1] != -1:
                        break
                    else:
                        res.append([y+i, x])
                        
            if y > 0 and grid[y-1][x][1] == -1:
                res.append([y-1, x])
        
        if y > 0 and x >= 0 and x < 7:
            if reduced and turn != grid[y-1][x+1][1]:
                res.append([y-1, x+1])
                
            if grid[y-1][x+1][1] != -1:
                if turn != grid[y-1][x+1][1]:
                    res.append([y-1, x+1])
        
        if y > 0 and x > 0 and x <= 7:
            if reduced and turn != grid[y-1][x-1][1]:
                res.append([y-1, x-1])
                
            if grid[y-1][x-1][1] != -1:
                if turn != grid[y-1][x-1][1]:
                    res.append([y-1, x-1])
                    
    else:
        if not reduced:
            if y == 1:
                for i in [1, 2]:
                        if grid[y+i][x][1] != -1:
                            break
                        else:
                            res.append([y+i, x])
                        
            if y < 7 and grid[y+1][x][1] == -1:
                res.append([y+1, x])
            
        if y < 7 and x >= 0 and x < 7:
            if reduced and turn != grid[y+1][x+1][1]:
                res.append([y+1, x+1])
                
            if grid[y+1][x+1][1] != -1:
                if turn != grid[y+1][x+1][1]:
                    res.append([y+1, x+1])
            
        if y < 7 and x > 0 and x <= 7:
            if reduced and turn != grid[y+1][x-1][1]:
                res.append([y+1, x-1])
                
            if grid[y+1][x-1][1] != -1:
                if turn != grid[y+1][x-1][1]:
                    res.append([y+1, x-1])                        
    return res


def possible_knight(x, y, grid):
    res = []
    values = [-2,2]
    values2 = [-1,1]
    
    for val in values:
        if y + val >= 0 and y + val <= 7:
            for val2 in values2:
                if x + val2 >= 0 and x + val2 <= 7:
                    if grid[y+val][x+val2][1] != grid[y][x][1]:
                        res.append([y + val, x + val2])
                     
    for val2 in values2:
        if y + val2 >= 0 and y + val2 <= 7:
            for val in values:
                if x + val >= 0 and x + val <= 7:
                    if grid[y+val2][x+val][1] != grid[y][x][1]:
                            res.append([y + val2, x + val])
                        
    return res

def possible_bishop(x, y, grid):
    res = []
    
    #1.case we go topleft
    x1 = x - 1
    y1 = y - 1
    while x1 >= 0 and y1 >= 0:
        if grid[y1][x1][1] != grid[y][x][1]:
            res.append([y1, x1])
        if grid[y1][x1][1] != -1:
            break
            
        x1 -= 1
        y1 -= 1
    
    #2.case we go topright 
    x2 = x + 1
    y2 = y - 1
    while x2 <= 7 and y2 >= 0:
        if grid[y2][x2][1] != grid[y][x][1]:
            res.append([y2, x2])
        if grid[y2][x2][1] != -1:
            break
        x2 += 1
        y2 -= 1
        
    # 3.case we go downleft
    x3 = x - 1
    y3 = y + 1
    while x3 >= 0 and y3 <= 7:
        if grid[y3][x3][1] != grid[y][x][1]:
            res.append([y3, x3])
        if grid[y3][x3][1] != -1:
            break
        x3 -= 1
        y3 += 1
        
    #4.case we go downright
    x4 = x + 1
    y4 = y + 1
    while x4 <= 7 and y4 <= 7:
        if grid[y4][x4][1] != grid[y][x][1]:
            res.append([y4, x4])
        if grid[y4][x4][1] != -1:
            break
        x4 += 1
        y4 += 1
    
    return res

def possible_rook(x, y, grid):
    res = []
    #1.case we go left
    x1 = x - 1
    y1 = y
    while x1 >= 0:
        if grid[y1][x1][1] != grid[y][x][1]:
            res.append([y1, x1])
        if grid[y1][x1][1] != -1:
            break
        x1 -= 1
    
    #2.case we go right 
    x2 = x + 1
    y2 = y
    while x2 <= 7:
        if grid[y2][x2][1] != grid[y][x][1]:
            res.append([y2, x2])
        if grid[y2][x2][1] != -1:
            break
        x2 += 1
        
    # 3.case we go down
    x3 = x
    y3 = y + 1
    while y3 <= 7:
        if grid[y3][x3][1] != grid[y][x][1]:
            res.append([y3, x3])
        if grid[y3][x3][1] != -1:
            break
        y3 += 1

    #4.case we go up
    x4 = x
    y4 = y - 1
    while y4 >= 0:
        if grid[y4][x4][1] != grid[y][x][1]:
            res.append([y4, x4])
        if grid[y4][x4][1] != -1:
            break
        y4 -= 1
    
    return res


def possible_queen(x, y, grid):
    res = []
    res = possible_bishop(x, y, grid) + possible_rook(x, y, grid)
    return res

def possible_king(x, y, grid, reduced):
    #TODO IMPLEMENT CASTLING
    kingx = x
    kingy = y
    turn = grid[kingy][kingx][1]
    res = [[y, x]]
    if y + 1 <= 7:
        for i in [-1,0,1]:
            if x + i >= 0 and x + i <= 7:
                if grid[y+1][x+i][1] != turn:
                    res.append([y + 1, x + i])
        
    for i in [-1,1]:
        if x + i >= 0 and x + i <= 7:
            if grid[y][x+i][1] != turn:
                res.append([y, x + i])
    
    if y - 1 >= 0:
        for i in [-1,0,1]:
            if x + i >= 0 and x + i <= 7:
                if grid[y-1][x+i][1] != turn:
                    res.append([y - 1, x + i])
    if reduced:
        return check_valid_moves([kingx, kingy], res, turn, grid)
    return res

def check_valid_moves(highlighted, positions, turn, grid):
    res = [[]]
    kingx, kingy = find_king(grid, turn)
    y_piece = highlighted[1]
    x_piece = highlighted[0]
    for pos in positions:
            if pos != []:
                temp = grid[pos[0]][pos[1]]
                grid[pos[0]][pos[1]], grid[y_piece][x_piece] = grid[y_piece][x_piece], [-1, -1]
                if [kingy, kingx] == [y_piece, x_piece]:
                    if pos not in calculate_threats(grid, turn):
                        res.append(pos)
                else:
                    if [kingy, kingx] not in calculate_threats(grid, turn):
                        res.append(pos)
                grid[y_piece][x_piece], grid[pos[0]][pos[1]] = grid[pos[0]][pos[1]], temp
    return res

def find_king(grid, turn):
    kingx, kingy = -1, -1
    for y in range(8):
        for x in range(8):
            if grid[y][x][0] == 5 and grid[y][x][1] == turn:
                kingx = x
                kingy = y
                break
    return kingx, kingy
