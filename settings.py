import pygame as pg;
# screen stuff...

WIDTH = 800;
HEIGHT = 650;
FPS = 60;
FONT_NAME = pg.font.match_font('helvetica');

# Player stuff

PLAYER_ACC = 0.5;
FRICTION = -0.1;

# Enemy Stuff

ENEMY_VEL = 0.75;

# Colours

WHT = (255, 255, 255);		# White
GRY = (186, 186, 186); 		# Grey
BLK = (0, 0, 0);			# Black
RED = (244, 66, 66);  		# Red
GRN = (66, 244, 66);		# Green
BLU = (66, 66, 244);		# Blue
YEL = (255, 255, 0);		# Yellow
ORA = (244, 160, 66);		# Orange
PUR = (200, 66, 244);		# Purple
BRO = (115, 70, 18);		# Brown
PNK = (244, 66, 200); 		# Pink

# background images


BG_EL_SCREEN = pg.image.load('spaceBG.JPG');
BG_START_SCREEN = pg.image.load('spaceBG2.JPG');
