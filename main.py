import pygame as pg;
import random;
from settings import *;
from sprites import *;

class Game:

	def __init__(self):

		pg.init();
		self.scr = pg.display.set_mode((WIDTH, HEIGHT));
		self.clk = pg.time.Clock();
		self.running = True;
		self.intro = True;

		# co-ords for spawning first enemy...
		self.x = 101;
		self.y = 100;

		# self.enemList = [];

		# keep track of levels player has completed...
		self.level = 1;

	def new(self):

		self.all_sprites = pg.sprite.Group();
		self.enemies = pg.sprite.Group();
		self.bullets = pg.sprite.Group();
		self.ray_sprite = pg.sprite.Group();

		# Try spawning a row of enemies below the first row
		# this also needs to be called somewhere else...
		for x in range(0, 8):
			self.spawnEnemy();

		self.player = Player(self);

		self.bg = pg.image.load('space2.PNG').convert();

		self.all_sprites.add(self.player);

		self.run();

	def run(self):

		self.playing = True;

		while self.playing:
			self.clk.tick(FPS);
			self.events();
			self.update();
			self.draw();

	def update(self):

		keys = pg.key.get_pressed();

		for e in self.enemies:
			if e.pos.x >= WIDTH - 50:
				for e in self.enemies:
					e.moveDown = True;
					e.moveRight = False;
					e.dx = 0;

			if e.pos.x <= 50:
				for e in self.enemies:
					e.moveDown = True;
					e.moveLeft = False; 
					e.dx = 1;

		# if not self.enemies and player.HP > 0? for this bit...
		if not self.enemies:
			print('there are no enemies left');
			self.playing = False;
			self.running = False;
			self.level += 1;

		self.all_sprites.update();
		self.enemies.update();

		
		print(self.level);
		print(self.player.points);


	def events(self):

		for e in pg.event.get():
			if e.type == pg.QUIT:
				if self.playing:
					self.playing = False;

				self.running = False;

			if e.type == pg.KEYDOWN:
				if e.key == pg.K_SPACE:
					self.player.Shoot();

		hits = pg.sprite.groupcollide(self.bullets, self.enemies, True, True);
		if hits:
			print(hits);
			self.player.points += 10;

		



	def draw(self):

		self.scr.blit(self.bg, (0, 0));
		self.all_sprites.draw(self.scr);
		pg.display.flip();

	def spawnEnemy(self):
		
		e = Enemy(self.x, self.y, self);
		
		self.enemies.add(e);
		self.all_sprites.add(e);
		
		# print(self.x, self.y);

		self.x += 75;

	def show_start_scrn(self):

		# while self.intro:
		# 	for e in pg.event.get():
		# 		if e.type == pg.K_SPACE:
		# 			self.intro = False;
		# 			self.playing = True;
		# 			self.running = True;

		# 	self.scr.fill(RED);
		# 	pg.display.update();
		# 	self.clk.tick(60);

		pass;

	def show_go_scrn(self):

		pass;

	def show_endlevel_scrn(self):

		# screen that comes when the player completes a level
		# -- show the scores on it?

		pass;

g = Game();

g.show_start_scrn();

while g.running:

	g.new();
	g.show_go_scrn();

pg.quit();
