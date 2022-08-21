import pygame
pygame.init()
WIDTH = 480
HEIGHT = 480
FPS = 40
SIDE = 60
WHITE = (255, 255, 255)
RGB_BLACK = (0,0,0)
BLACK = (154, 156, 148)
HIGHLIGHT = f'#90ee90'
RED = (242, 94, 109)
FONT_COLOR = (250, 32, 12)
R = 15
white_king_pos = [7, 4]
black_king_pos = [0, 4]
menu_font = pygame.font.SysFont('Comic Sans MS', 30)
WHITE_IMAGES = [pygame.image.load("imgs\wp.png"), pygame.image.load("imgs\wN.png"), pygame.image.load("imgs\wB.png"),
                pygame.image.load("imgs\wR.png"), pygame.image.load("imgs\wQ.png"), pygame.image.load("imgs\wK.png")]

BLACK_IMAGES = [pygame.image.load("imgs\p.png"), pygame.image.load("imgs\kN.png"), pygame.image.load("imgs\B.png"),
                pygame.image.load("imgs\R.png"), pygame.image.load("imgs\Q.png"), pygame.image.load("imgs\K.png")]

