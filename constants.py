import pygame
pygame.init()
WIDTH = 480
HEIGHT = 480
FPS = 40
SIDE = 60
WHITE = (255, 255, 255)
BLACK = (154, 156, 148)
HIGHLIGHT = f'#90ee90'
RED = (242, 94, 109)
R = 15
WHITE_IMAGES = [pygame.image.load("imgs\wp.png"), pygame.image.load("imgs\wN.png"), pygame.image.load("imgs\wB.png"),
                pygame.image.load("imgs\wR.png"), pygame.image.load("imgs\wQ.png"), pygame.image.load("imgs\wK.png")]

BLACK_IMAGES = [pygame.image.load("imgs\p.png"), pygame.image.load("imgs\kN.png"), pygame.image.load("imgs\B.png"),
                pygame.image.load("imgs\R.png"), pygame.image.load("imgs\Q.png"), pygame.image.load("imgs\K.png")]

