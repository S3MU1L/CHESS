import pygame
pygame.init()
pygame.mixer.init()
pygame.font.init()
WIDTH = 480
HEIGHT = 480
FPS = 40
SIDE = 60
WHITE = (255, 255, 255)
RGB_BLACK = (0,0,0)
BLACK = (154, 156, 148)
#BLACK = (154, 156, 148)
MENU_BACKGROUND = (56, 209, 92)
HIGHLIGHT = f'#90ee90'
RED = (242, 94, 109)
FONT_COLOR = (184, 30, 9)
R = 15
move_piece_sound = pygame.mixer.Sound("sound_fx\chess_move_piece_sound.wav")
move_piece_sound.set_volume(0.5)

end_game_sound = pygame.mixer.Sound("sound_fx\end_game_sound.wav")
end_game_sound.set_volume(0.5)
white_king_pos = [7, 4]
black_king_pos = [0, 4]
game_font = pygame.font.SysFont('sylfaen', 30)
menu_font = pygame.font.SysFont("sylfaen", 30)
WHITE_IMAGES = [pygame.image.load("imgs\wp.png"), pygame.image.load("imgs\wN.png"), pygame.image.load("imgs\wB.png"),
                pygame.image.load("imgs\wR.png"), pygame.image.load("imgs\wQ.png"), pygame.image.load("imgs\wK.png")]

BLACK_IMAGES = [pygame.image.load("imgs\p.png"), pygame.image.load("imgs\kN.png"), pygame.image.load("imgs\B.png"),
                pygame.image.load("imgs\R.png"), pygame.image.load("imgs\Q.png"), pygame.image.load("imgs\K.png")]
