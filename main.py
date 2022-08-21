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
    stopped = False
    state = -1
    w_king_moved = False
    b_king_moved = False
    en_pessant_pawn = [-1,-1]
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
              safe_moves, state, grid, w_king_moved, b_king_moved,
              en_pessant_pawn)

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
    text_surface = menu_font.render(text, 1, FONT_COLOR)
    win.blit(text_surface, (WIDTH//2 - text_surface.get_width()//2, HEIGHT//2 - text_surface.get_height()//2))

def draw_mate(win):
    text = "Stalemate! It's a draw!"
    text_surface = menu_font.render(text, 1, FONT_COLOR)
    win.blit(text_surface, (WIDTH//2 - text_surface.get_width()//2, WIDTH//2 - text_surface.get_height()//2))

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


def analyze_state(grid, turn, w_king_moved, b_king_moved, en_pessant_pawn):
    #find the king of responding color in the grid
    kingx, kingy = find_king(grid, turn)
    th = calculate_threats(grid, turn, w_king_moved, b_king_moved, en_pessant_pawn)
    pos = possible_king(kingx, kingy, grid, True, w_king_moved, b_king_moved,en_pessant_pawn)
    
    if len(pos) == 1:
        print("Checkmate !")
        return 1
        
    elif len(pos) == 2 and pos[1] == [kingy, kingx]:
        if turn == 1 and [kingy, kingx] != black_king_pos:
            print("Mate !")
            return 0
        if turn == 0 and [kingy, kingx] != white_king_pos:
            print("Mate !")
            return 0
    elif [kingy, kingx] in th:
        print("Check !")
    
    return -1
    
def draw(win, grid, highlighted, possible_moves, turn, state):
    draw_board(win, highlighted)
    if state == 0:
        draw_mate(win)
    if state == 1:
        draw_winning(win, (turn + 1)%2)
    if possible_moves != []:
        draw_possible(win, possible_moves, grid, turn)
    
    draw_grid(win, grid)
    pygame.display.update()

def game_loop(window, run, clock, turn, highlighted, possible_moves, 
              safe_moves, state, grid, w_king_moved, b_king_moved,
              en_pessant_pawn):
    
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    run = False
                    initialize()
                    break
            if event.type == pygame.MOUSEBUTTONDOWN and state == -1:
                temp = check_click(turn, pygame.mouse.get_pos(), grid)
                if temp != [-1,-1]:
                    highlighted = temp
                    possible_moves = calculate_possible(highlighted, grid, w_king_moved, b_king_moved, en_pessant_pawn)
                    safe_moves = check_valid_moves(highlighted, possible_moves, turn, grid, w_king_moved, b_king_moved, en_pessant_pawn)
                else:
                    click_where = pygame.mouse.get_pos()
                    #return the coordinates that corespond with the mouse click position
                    t = move_click(click_where, safe_moves)
                    if t != [-1, -1]:    
                        if en_pessant_pawn != [-1,-1]:
                            print("yes")
                            print([t[0]+1, t[1]])
                            print([t[0]-1, t[1]])        
                            if [t[0] + 1, t[1]] == [en_pessant_pawn[0] + 1, en_pessant_pawn[1]]:
                                grid[highlighted[1]][highlighted[0]], grid[t[0] + 1][t[1]] = [-1,-1], grid[highlighted[1]][highlighted[0]]
                            elif [t[0] - 1, t[1]] == [en_pessant_pawn[0] - 1, en_pessant_pawn[1]]:
                                grid[highlighted[1]][highlighted[0]], grid[t[0] - 1][t[1]] = [-1,-1], grid[highlighted[1]][highlighted[0]]

                    else:    
                        grid[highlighted[1]][highlighted[0]], grid[t[0]][t[1]] = [-1,-1], grid[highlighted[1]][highlighted[0]]
                        turn = (turn + 1) % 2
                        highlighted = [-1, -1]
                        possible_moves = []
                        safe_moves = []
                        state = analyze_state(grid, turn,  w_king_moved, b_king_moved, en_pessant_pawn)

                    #check pawn, simply by checking if the difference between y coordinates of chosen and and original positions is 2
                    if grid[highlighted[1]][highlighted[0]][0] == 0:
                        if abs(t[0] - highlighted[1]) == 2:
                            en_pessant_pawn = [t[0], t[1]]
                        
        draw(window, grid, highlighted, safe_moves, turn, state)
        clock.tick(FPS)

if __name__ == '__main__':
    initialize()