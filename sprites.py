import pygame as pg;
from settings import *;
import random;

vec2 = pg.math.Vector2;

class Player(pg.sprite.Sprite):
	def __init__(self, game):
		self.g = game;
		pg.sprite.Sprite.__init__(self);
		self.image = pg.Surface((60, 58));
		# self.image.fill(BLU);
		self.rect = self.image.get_rect();
		self.pos = vec2(WIDTH / 2, HEIGHT - 50);
		self.rect.center = self.pos;
		self.vel = vec2(0, 0);
		self.acc = vec2(0, 0);

		self.left = False;
		self.right = False;

		self.points = 0;

		self.HP = 100;

		self.spritesheet = pg.image.load('ships.PNG').convert_alpha();



	def update(self):

		self.image.blit(self.get_image(), (0, 0));

		# if self.HP <= 50:
		# 	self.image.fill(RED);
		# else:
		# 	self.image.fill(BLU);

		
		# all the keyboard input stuff
		keys = pg.key.get_pressed();

		if keys[pg.K_a]:
			self.left = True;
		else:
			self.left = False;
			self.acc.x = 0;
		
		if keys[pg.K_d]:
			self.right = True;
		else:
			self.right = False;
			self.acc.x = 0;

		if self.right:
			self.acc.x = PLAYER_ACC;

		if self.left:
			self.acc.x = -PLAYER_ACC;	


		# movement maths
		self.acc.x += self.vel.x * FRICTION;
		self.vel = self.vel + self.acc;

		self.pos = self.pos + self.vel + 0.5 * self.acc;

		self.rect.center = self.pos;

		if self.pos.x >= WIDTH - 40:
			self.pos.x = WIDTH - 40;

		elif self.pos.x <= 40:
			self.pos.x = 40;	

	def Shoot(self):
		
		bullet = Bullet(self.rect.centerx, self.rect.top, -10);
		self.g.all_sprites.add(bullet);
		self.g.bullets.add(bullet);

	def get_image(self):
		self.img = pg.Surface((56, 58));
		# blit to the Surface() above from the spritesheet loaded in __init__()
		# args = spritesheet, (x, y), (chunk(w, h) of sprite)
		self.img.blit(self.spritesheet, (0, 0), (400, 4, 56, 58));
		return self.img;

class Enemy(pg.sprite.Sprite):
	def __init__(self, xpos, ypos, game ):
		self.g = game;
		pg.sprite.Sprite.__init__(self);
		self.image = pg.Surface((40, 20));
		self.image.fill(RED);
		# self.sprite = pg.image.load('Enemy.PNG').convert_alpha();
		# self.image.blit(self.sprite,(0, 0));
		self.rect = self.image.get_rect();
		self.pos = vec2(xpos, ypos);
		self.rect.center = self.pos;
		self.vel = vec2(0, 0);

		# pos counter, counts how long the enemy moves
		# down for
		self.pos0 = 0;

		# next direction, so the enemy know which way to go after
		# moving down
		self.dx = 1;	# 1 = right, 0 = left...

		# movement booleans
		self.moveLeft = False;
		self.moveRight = True;
		self.moveDown = False;

		# ENEMY HEALTH????!!!

	def update(self):

		if self.moveRight:
			self.vel.x = ENEMY_VEL;

		if self.moveLeft:
			self.vel.x = -ENEMY_VEL;

		if self.moveDown:
			self.vel.y = ENEMY_VEL;
			self.vel.x = 0;
			self.pos0 += 1;
		else:
			self.pos0 = 0;


		# if enemy has moved down and next direction(dx) is 0 = Left
		# move left
		if self.moveDown and self.pos0 >= 15 and self.dx == 0:
			self.vel.y = 0;
			self.moveDown = False;
			self.moveLeft = True;

		# if enemy has moved down and next direction(dx) is 1 = Right
		# move right	
		elif self.moveDown and self.pos0 >= 15 and self.dx == 1:
			self.vel.y = 0;
			self.moveDown = False;
			self.moveRight = True;

		# if self.pos.y >= HEIGHT - 300:
		# 	self.vel.x = self.vel.x * 2;
		# 	self.vel.y = self.vel.y * 2;
		
		# add the velocity to the enemies position and
		# set its center equal to pos		
		self.pos = self.pos + self.vel;
		self.rect.center = self.pos;

	def Shoot(self):

		bullet = Bullet(self.rect.centerx, self.rect.bottom + 20, 10);
		self.g.all_sprites.add(bullet);
		self.g.bullets.add(bullet);

class Spec_Enemy(pg.sprite.Sprite):

	# after 24(might change the amount) enemies start to replace and
	# spawn special enemies

	pass;

class MotherShip(pg.sprite.Sprite):

	# intermitently spawn a mother to move acoss the top of the screen
	# above the regular enemies, player power up when killed?...

	pass;

class Bullet(pg.sprite.Sprite):
	def __init__(self, x, y, speed):
		pg.sprite.Sprite.__init__(self);
		self.image = pg.Surface((8, 20));
		self.image.fill(YEL);
		self.rect = self.image.get_rect();
		self.rect.bottom = y;
		self.rect.centerx = x;
		self.speedy = speed;

	def update(self):

		self.rect.y += self.speedy;

		if self.rect.bottom < 0:
			self.kill();

