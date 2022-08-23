import pygame
from constants import *
pygame.init()
pygame.font.init()
pygame.mixer.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Main Menu")
run = True
timer = pygame.time.Clock()
pygame.mixer.music.load("sound_fx\menu_music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)
#press enter to start playing
#press r to reset the
def draw_label(win):
    text = "Press Enter to start playing."
    text_surface = menu_font.render(text, 1, WHITE)
    win.blit(text_surface, (WIDTH//2 - text_surface.get_width()//2, 200))
    
    text = "Press R to restart the game."
    text_surface = menu_font.render(text, 1, WHITE)
    win.blit(text_surface, (WIDTH//2 - text_surface.get_width()//2, 250))
    
def draw(win):
    win.fill(MENU_BACKGROUND)
    draw_label(win)
    pygame.display.update()

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False
            break
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            run = False
            pygame.mixer.music.stop()
            break
            
            
    draw(window)
    timer.tick(FPS)
