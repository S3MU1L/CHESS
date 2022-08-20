def king_safe(grid, turn, kingx, kingy):
    #return list of positions where the king still can go
    res = []
    #firstly we find all the positions which are threatened
    for y in range(8):
        for x in range(8):
            if (y != kingy or x != kingx) and grid[y][x][0] != -1:
                    res.append([y, x])
            if grid[y][x][1] != turn and grid[y][x][1] != -1:
                if grid[y][x][0] == 5:
                    res += all_king(x, y, grid)
                else:
                    res += calculate_possible([x, y], grid)
    #now we filter all the bad positions
    good = []
    threatened = True if [kingy, kingx] in res else False
    for y in range(8):
        for x in range(8):
            if [y, x] not in res:
                good.append([y, x])
                
    return good, threatened

def calculate_possible(highlighted, grid):
    x = highlighted[0]
    y = highlighted[1]
    piece = grid[y][x][0]
    if piece == 0:
        return possible_pawn(x, y, grid)
    elif piece == 1:
        return possible_knight(x, y, grid)
    elif piece == 2:
        return possible_bishop(x, y, grid)
    elif piece == 3:
        return possible_rook(x, y, grid)
    elif piece == 4:
        return possible_queen(x, y, grid)    
    return possible_king(x, y, grid, grid[y][x][1])[0]
    
    
def possible_pawn(x, y, grid):
    res = []
    
    #TODO IMPLEMENT EN PESSANT
    
    #white pawns only move up
    if grid[y][x][1] == 0:
        if y == 6:
            for i in [-1,-2]:
                if grid[y+i][x][1] != -1:
                    break
                else:
                    res.append([y+i, x])
                    
        # if y > 0 and grid[y-1][x][1] != grid[y][x][1]:
        #     res.append([y-1, x])
        
        if y > 0 and x >= 0 and x < 7:
            if grid[y-1][x+1][1] != -1:
                if grid[y][x][1] != grid[y-1][x+1][1]:
                    res.append([y-1,x+1])
        
        if y > 0 and x > 0 and x <= 7:
            if grid[y-1][x-1][1] != -1:
                if grid[y][x][1] != grid[y-1][x-1][1]:
                    res.append([y-1, x-1])
                    
    else:
        if y == 1:
            for i in [1, 2]:
                    if grid[y+i][x][1] != -1:
                        break
                    else:
                        res.append([y+i, x])
                    
        # if y < 7 and grid[y+1][x][1] != grid[y][x][1]:
        #     res.append([y+1, x])
        
        if y < 7 and x >= 0 and x < 7:
            if grid[y+1][x+1][1] != -1:
                if grid[y][x][1] != grid[y+1][x+1][1]:
                    res.append([y+1,x+1])
            
        if y < 7 and x > 0 and x <= 7:
            if grid[y+1][x-1][1] != -1:
                if grid[y][x][1] != grid[y+1][x-1][1]:
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
            res.append([y1,x1])
        if grid[y1][x1] != [-1,-1]:
            break
        x1 -= 1
        y1 -= 1
    
    #2.case we go topright 
    x2 = x + 1
    y2 = y - 1
    while x2 <= 7 and y2 >= 0:
        if grid[y2][x2][1] != grid[y][x][1]:
            res.append([y2,x2])
        if grid[y2][x2] != [-1,-1]:
            break
        x2 += 1
        y2 -= 1
        
    # 3.case we go downleft
    x3 = x - 1
    y3 = y + 1
    while x3 >= 0 and y3 <= 7:
        if grid[y3][x3][1] != grid[y][x][1]:
            res.append([y3, x3])
        if grid[y3][x3] != [-1,-1]:
            break
        x3 -= 1
        y3 += 1
        
    #4.case we go downright
    x4 = x + 1
    y4 = y + 1
    while x4 <= 7 and y4 <= 7:
        if grid[y4][x4][1] != grid[y][x][1]:
            res.append([y4, x4])
        if grid[y4][x4] != [-1,-1]:
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
            res.append([y1,x1])
        if grid[y1][x1] != [-1,-1]:
            break
        x1 -= 1
    
    #2.case we go right 
    x2 = x + 1
    y2 = y
    while x2 <= 7:
        if grid[y2][x2][1] != grid[y][x][1]:
            res.append([y2,x2])
        if grid[y2][x2] != [-1,-1]:
            break
        x2 += 1
        
    # 3.case we go down
    x3 = x
    y3 = y + 1
    while y3 <= 7:
        if grid[y3][x3][1] != grid[y][x][1]:
            res.append([y3, x3])
        if grid[y3][x3] != [-1,-1]:
            break
        y3 += 1

    #4.case we go up
    x4 = x
    y4 = y - 1
    while y4 >= 0:
        if grid[y4][x4][1] != grid[y][x][1]:
            res.append([y4, x4])
        if grid[y4][x4] != [-1,-1]:
            break
        y4 -= 1
    
    return res


def possible_queen(x, y, grid):
    return possible_bishop(x, y, grid) + possible_rook(x, y, grid)

def all_king(x, y, grid):
    res = []
    if y + 1 <= 7:
        for i in [-1,0,1]:
            if x + i >= 0 and x + i <= 7:
                if grid[y+1][x+i][1] != grid[y][x][1]:
                    res.append([y + 1, x + i])
        
    for i in [-1,1]:
        if x + i >= 0 and x + i <= 7:
            if grid[y][x+i][1] != grid[y][x][1]:
                res.append([y, x + i])
    
    if y - 1 >= 0:
        for i in [-1,0,1]:
            if x + i >= 0 and x + i <= 7:
                if grid[y-1][x+i][1] != grid[y][x][1]:
                    res.append([y - 1, x + i])
    return res

def possible_king(x, y, grid, turn):
    positions = all_king(x, y, grid)
    ans = king_safe(grid, turn, x, y)
    possible = ans[0]
    threatened = ans[1]
    
    res = []
    for pos in positions:
        if pos in possible:
            res.append(pos)
    return res, threatened