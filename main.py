#AUTHOR : Samuel Malec
import pygame
import time
from constants import *
from possible import *
pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")
run = True
clock = pygame.time.Clock()
turn = 0
highlighted = [-1,-1]
possible_moves = []
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

def draw_possible(win, possible_moves, grid):
    
    if len(possible_moves) > 0:
        for pos in possible_moves:
            y = pos[0]
            x = pos[1]
            if grid[y][x] == [-1, -1]:
                pygame.draw.circle(win, HIGHLIGHT, (x * SIDE + SIDE//2, y * SIDE + SIDE//2), R)

            else:
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
    return [-1,-1]


def analyze_state(grid, turn):
    #find the king of responding color in the grid
    kingx, kingy = -1, -1
    for y in range(8):
        for x in range(8):
            if grid[y][x][0] == 5 and grid[y][x][1] == turn:
                kingx, kingy = x, y
                break
    result = possible_king(kingx, kingy, grid, turn)
    good = result[0]
    print(good)
    threatened = result[1]
    print(threatened)
    if len(good) == 0 and threatened:
        print("Checkmate")
    elif len(good) != 0 and threatened:
        print("Mate")
    else:
        print("ok")
        
def draw(win, grid, highlighted, possible_moves):
    draw_board(win, highlighted)
    if possible_moves != []:
        draw_possible(win, possible_moves, grid)
    draw_grid(win, grid)
    pygame.display.update()

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
        if event.type == pygame.MOUSEBUTTONDOWN:
            temp = check_click(turn, pygame.mouse.get_pos(), grid)
            if temp != [-1,-1]:
                highlighted = temp
                possible_moves = calculate_possible(highlighted, grid)
            else:
                click_where = pygame.mouse.get_pos()
                t = move_click(click_where, possible_moves)
                if t != [-1, -1]:
                    grid[highlighted[1]][highlighted[0]], grid[t[0]][t[1]] = [-1,-1], grid[highlighted[1]][highlighted[0]]
                    turn = (turn + 1) % 2
                    highlighted = [-1, -1]
                    possible_moves = []
                    analyze_state(grid, turn)
        
    draw(window, grid, highlighted, possible_moves)
    clock.tick(FPS)

