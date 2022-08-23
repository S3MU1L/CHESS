#AUTHOR : Samuel Malec
import pygame
from constants import *
from possible import *
import menu
pygame.init()

def initialize():
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess")
    run = True
    clock = pygame.time.Clock()
    turn = 0
    highlighted = [-1,-1]
    possible_moves = []
    safe_moves = []
    state = -1
    transformation = False
    trans_pawn = [-1, -1]
    click = -1
    pieces = [4,3,2,1]
    #we will represent castling by states
    #0 means that the king, both rooks haven't moved yet
    #1 means only the rook, that is on the left side of the board (rook [0,0] or rook [7,0]) has moved
    #2 means only the rook, that is on the right side of the board (rook [0, 7] or rook[7,7] ) has moved and 
    #3 means that either the king or both rooks have moved
    w_castlable_state = 0
    b_castlable_state = 0
    en_passant_pawn = [-1,-1]
    #the pieces are numbered accordingly : pawn : 0, knight : 1, bishop : 2, rook : 3, queen : 4, king : 5
    #if nothing is placed on the position, both arguments will be -1
    #the grid will be represented by 2D array of 2 element lists, the first value in the list means what piece is on the position
    #the second value represents the color, 0 means white and 1 means black.
    #we start from default position on the grid and then we will modify it when player makes a move
    grid = [
            [[3,1],[1,1],[2,1],[4,1],[5,1],[2,1],[1,1],[3,1]],
            [[0,1],[0,1],[0,1],[0,1],[0,1],[0,1],[0,1],[0,1]],
            [[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1]],
            [[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1]],
            [[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1]],
            [[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1]],
            [[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]],
            [[3,0],[1,0],[2,0],[4,0],[5,0],[2,0],[1,0],[3,0]]
            ]
    game_loop(window, run, clock, turn, highlighted, possible_moves, 
              safe_moves, state, grid, w_castlable_state, b_castlable_state,
              en_passant_pawn, transformation, trans_pawn, click, pieces)

def draw_board(win, highlighted):
    black = True
    for y in range(0, WIDTH + 1, SIDE):
        black = not black
        for x in range(0, WIDTH + 1, SIDE):
            if [x//SIDE, y//SIDE] == highlighted:
                fill = HIGHLIGHT
                
            elif black:
                fill = BLACK
            else:
                fill = WHITE
            pygame.draw.rect(win, fill, (x, y, SIDE, SIDE))
            black = not black
        black = not black

def draw_grid(win, grid):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] != [-1,-1]:
                image_list = []
                if grid[y][x][1] == 0:
                    image_list = WHITE_IMAGES
                else:
                    image_list = BLACK_IMAGES
                win.blit(image_list[grid[y][x][0]], (x * SIDE, y * SIDE))

def draw_winning(win, turn):
    winner = "White" if turn == 0 else "Black"
    text = "The " + winner + " has won!"
    text2 = "Press R to play again!"
    text_surface = game_font.render(text, 1, FONT_COLOR)
    text_surface2 = game_font.render(text2, 1, FONT_COLOR)
    win.blit(text_surface, (WIDTH//2 - text_surface.get_width()//2, HEIGHT//2 - text_surface.get_height()//2))
    win.blit(text_surface2, (WIDTH//2 - text_surface2.get_width()//2, HEIGHT//2 + 40))

def draw_mate(win):
    text = "Stalemate, it's a draw!"
    text2 = "Press R to play again!"
    text_surface = game_font.render(text, 1, FONT_COLOR)
    text_surface2 = game_font.render(text2, 1, FONT_COLOR)
    win.blit(text_surface, (WIDTH//2 - text_surface.get_width()//2, WIDTH//2 - text_surface.get_height()//2))
    win.blit(text_surface2, (WIDTH//2 - text_surface2.get_width()//2, HEIGHT // 2 + 40))
    
def draw_possible(win, possible_moves, grid, turn):
    for pos in possible_moves:
        if pos != []:
            y = pos[0]
            x = pos[1]
            if grid[y][x] == [-1, -1]:
                pygame.draw.circle(win, HIGHLIGHT, (x * SIDE + SIDE//2, y * SIDE + SIDE//2), R)

            elif grid[y][x] != [-1, -1] and grid[y][x][1] != turn:
                pygame.draw.rect(win, RED, (x*SIDE, y * SIDE, SIDE, SIDE))


def check_click(turn, position, grid):
    y = (position[1]//SIDE)
    x = (position[0]//SIDE)
    if grid[y][x][1] == turn:
        return [x, y]
    return [-1, -1]

def move_click(mouse_pos, possible_moves):
    x = mouse_pos[0]//SIDE
    y = mouse_pos[1]//SIDE
    for move in possible_moves:
        if move == [y, x]:
            return [y, x]
    return [-1, -1]


def analyze_state(grid, turn, w_castlable_state, b_castlable_state, en_passant_pawn, state):
    #find the king of responding color in the grid
    kingx, kingy = find_king(grid, turn)
    th = calculate_threats(grid, turn, w_castlable_state, b_castlable_state, en_passant_pawn, state)
    pos = possible_king(kingx, kingy, grid, True, w_castlable_state, b_castlable_state, en_passant_pawn, state)
    is_mate(grid, (turn), en_passant_pawn, w_castlable_state, b_castlable_state, state)
    if len(pos) == 1:
        print("Checkmate !")
        pygame.mixer.Sound.play(end_game_sound)
        return 2
        
    elif len(pos) == 2 and pos[1] == [kingy, kingx] and is_mate(grid, (turn), en_passant_pawn, w_castlable_state, b_castlable_state, state):
        print("Mate !")
        pygame.mixer.Sound.play(end_game_sound)
        return 1
    elif [kingy, kingx] in th:
        print("Check !")
        return 0
    
    return -1

def draw_transformation(win):
    text = "Click on pawn to change the piece"
    text2 = "Press enter to play"
    text_surface = game_font.render(text, 1, FONT_COLOR)
    text_surface2 = game_font.render(text2, 1, FONT_COLOR)
    win.blit(text_surface, (WIDTH//2 - text_surface.get_width()//2, 200))
    win.blit(text_surface2, (WIDTH//2 - text_surface2.get_width()//2, 230))


def draw(win, grid, highlighted, possible_moves, turn, state, transformation):
    draw_board(win, highlighted)
    if state == 1:
        draw_mate(win)
    elif state == 2:
        draw_winning(win, (turn + 1)%2)
    elif possible_moves != []:
        draw_possible(win, possible_moves, grid, turn)
    draw_grid(win, grid)
    if transformation:
        draw_transformation(win)
    
    pygame.display.update()

def game_loop(window, run, clock, turn, highlighted, possible_moves, 
              safe_moves, state, grid, w_castlable_state, b_castlable_state,
              en_passant_pawn, transformation, trans_pawn, click, pieces):
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    run = False
                    initialize()
                    pygame.quit()
                if event.key == pygame.K_RETURN and transformation:
                    transformation = False
                    trans_piece = [-1, -1]
                    click = -1
                    turn = (turn + 1) % 2
                    highlighted = [-1, -1]
                    possible_moves = []
                    safe_moves = []
                    state = analyze_state(grid, turn,  w_castlable_state, b_castlable_state, en_passant_pawn, state)

            if event.type == pygame.MOUSEBUTTONDOWN and state < 1 and not transformation:
                temp = check_click(turn, pygame.mouse.get_pos(), grid)
                if temp != [-1,-1]:
                    highlighted = temp
                    possible_moves = calculate_possible(highlighted, grid, w_castlable_state, b_castlable_state, en_passant_pawn, state)
                    safe_moves = check_valid_moves(highlighted, possible_moves, turn, grid, w_castlable_state, b_castlable_state, en_passant_pawn, state)
                    if grid[highlighted[1]][highlighted[0]][0] == 5:
                        safe_moves += check_castling(grid, highlighted, w_castlable_state, b_castlable_state, state, turn, en_passant_pawn)
                else:
                    click_where = pygame.mouse.get_pos()
                    #return the coordinates that corespond with the mouse click position
                    t = move_click(click_where, safe_moves)
                    if t != [-1, -1]:
                        #if we aren't moving with a pawn we don't have to check for en_pessant
                        if grid[highlighted[1]][highlighted[0]][0] != 0 and grid[highlighted[1]][highlighted[0]][0] != 5:
                            #quickly check if we haven't moved with rooks, in order to correctly implement castling
                            if grid[highlighted[1]][highlighted[0]][0] == 3:
                                if turn == 1:
                                    if highlighted == [0, 0]:
                                        if b_castlable_state == 0:
                                            b_castlable_state = 1
                                        else:
                                            b_castlable_state = 3
                                        
                                    if highlighted == [7, 0]:
                                        if b_castlable_state == 0:
                                            b_castlable_state = 2
                                        else:
                                            b_castlable_state = 3  
                                if turn == 0:
                                    if highlighted == [0, 7]:
                                        if w_castlable_state == 0:
                                            w_castlable_state = 1
                                        else:
                                            w_castlable_state = 3
                                    
                                    if highlighted == [7, 7]:
                                        if w_castlable_state == 0:
                                            w_castlable_state = 2
                                        else:
                                            w_castlable_state = 3
                                
                                    
                            grid[highlighted[1]][highlighted[0]], grid[t[0]][t[1]] = [-1,-1], grid[highlighted[1]][highlighted[0]]
                            en_passant_pawn = [-1,-1]
                        
                        
                        elif grid[highlighted[1]][highlighted[0]][0] == 0:
                            #pawn movement implementation
                            if en_passant_pawn != [-1, -1]:
                                if [highlighted[1], highlighted[0] - 1] == en_passant_pawn or [highlighted[1], highlighted[0] + 1] == en_passant_pawn:
                                    if [t[0], t[1]] == [en_passant_pawn[0] + 1, en_passant_pawn[1]]:
                                        grid[highlighted[1]][highlighted[0]], grid[t[0]][t[1]] = [-1,-1], grid[highlighted[1]][highlighted[0]]
                                        grid[en_passant_pawn[0]][en_passant_pawn[1]] = [-1, -1]
                                        en_passant_pawn = [-1,-1]
                                        
                                    elif [t[0], t[1]] == [en_passant_pawn[0] - 1, en_passant_pawn[1]]:
                                        grid[highlighted[1]][highlighted[0]], grid[t[0]][t[1]] = [-1,-1], grid[highlighted[1]][highlighted[0]]
                                        grid[en_passant_pawn[0]][en_passant_pawn[1]] = [-1, -1]
                                        en_passant_pawn = [-1,-1]
                                    
                                    else:
                                        grid[highlighted[1]][highlighted[0]], grid[t[0]][t[1]] = [-1,-1], grid[highlighted[1]][highlighted[0]]
                                else:
                                    en_passant_pawn = [-1,-1]
                                    if(abs(t[0] - highlighted[1])) == 2:
                                        en_passant_pawn = [t[0], t[1]]
                                    grid[highlighted[1]][highlighted[0]], grid[t[0]][t[1]] = [-1,-1], grid[highlighted[1]][highlighted[0]]
                            else:
                                en_passant_pawn = [-1,-1]
                                if(abs(t[0] - highlighted[1])) == 2:
                                    en_passant_pawn = [t[0], t[1]]
                                grid[highlighted[1]][highlighted[0]], grid[t[0]][t[1]] = [-1,-1], grid[highlighted[1]][highlighted[0]]
                                

                        else:
                            #if we can't castle we will just move kings like other pieces
                            if turn == 0 and w_castlable_state == 3 or turn == 1 and b_castlable_state == 3:
                                grid[highlighted[1]][highlighted[0]], grid[t[0]][t[1]] = [-1,-1], grid[highlighted[1]][highlighted[0]]
                            else:
                                if turn == 0:
                                    if t == [7, 2]:
                                        grid[highlighted[1]][highlighted[0]], grid[t[0]][t[1]] = [-1,-1], grid[highlighted[1]][highlighted[0]]
                                        grid[7][3], grid[7][0] = grid[7][0], grid[7][3]
                                    
                                    elif t == [7, 6]:
                                        grid[highlighted[1]][highlighted[0]], grid[t[0]][t[1]] = [-1,-1], grid[highlighted[1]][highlighted[0]]
                                        grid[7][7], grid[7][5] = grid[7][5], grid[7][7]
                                    else:
                                        grid[highlighted[1]][highlighted[0]], grid[t[0]][t[1]] = [-1,-1], grid[highlighted[1]][highlighted[0]]
                                if turn == 1:
                                    if t == [0, 2]:
                                        grid[highlighted[1]][highlighted[0]], grid[t[0]][t[1]] = [-1,-1], grid[highlighted[1]][highlighted[0]]
                                        grid[0][3], grid[0][0] = grid[0][0], grid[0][3]
                                    
                                    elif t == [0, 6]:
                                        grid[highlighted[1]][highlighted[0]], grid[t[0]][t[1]] = [-1,-1], grid[highlighted[1]][highlighted[0]]
                                        grid[0][7], grid[0][5] = grid[0][5], grid[0][7]   
                                    
                                    else:
                                        grid[highlighted[1]][highlighted[0]], grid[t[0]][t[1]] = [-1,-1], grid[highlighted[1]][highlighted[0]]
                                        
                            #anytime we move the king we cannot castle anytime in the future
                            if turn == 0:
                                w_castlable_state = 3
                                
                            if turn == 1:
                                b_castlable_state = 3
                            
                            #since we have't moved with the pawn we have to do this
                            en_passant_pawn = [-1, -1]
                            
                        #TODO here we have to check if there are any pawns on the 0 or the 7 row,
                        for y in [0,7]:
                            for x in range(8):
                                if grid[y][x][0] == 0:
                                    transformation = True
                                    trans_pawn = [y, x]
                                    click = -1
                                    turn -= 1

                        #if there are then we need to ask the player what piece does he want to change the pawn into
                        pygame.mixer.Sound.play(move_piece_sound)
                        turn = (turn + 1) % 2
                        highlighted = [-1, -1]
                        possible_moves = []
                        safe_moves = []
                        state = analyze_state(grid, turn,  w_castlable_state, b_castlable_state, en_passant_pawn, state)
            if event.type == pygame.MOUSEBUTTONDOWN and state < 1 and transformation:
                t = check_click(turn, pygame.mouse.get_pos(), grid)
                if t != [-1,-1]:
                    if [t[1], t[0]] == [trans_pawn[0], trans_pawn[1]]:
                        click += 1
                        new_piece = pieces[click%4]
                        grid[trans_pawn[0]][trans_pawn[1]] = [new_piece, turn]

        draw(window, grid, highlighted, safe_moves, turn, state, transformation)
        clock.tick(FPS)


if __name__ == '__main__':
    initialize()

