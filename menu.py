import pygame
from constants import *
pygame.init()
pygame.font.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Main Menu")
run = True
timer = pygame.time.Clock()
#press enter to start playing
#press r to reset the
#sound fx -> on/off
def draw_label(win):
    text = "Press Enter to start playing."
    text_surface = menu_font.render(text, 1, WHITE)
    win.blit(text_surface, (WIDTH//2 - text_surface.get_width()//2, 100))
    
    text = "Press R to restart a game."
    text_surface = menu_font.render(text, 1, WHITE)
    win.blit(text_surface, (WIDTH//2 - text_surface.get_width()//2, 300))
    
def draw(win):
    win.fill(RGB_BLACK)
    draw_label(win)
    pygame.display.update()

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            run = False
            
    draw(window)
    timer.tick(FPS)