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
		self.playing = False;
		# co-ords for spawning first enemy...
		self.x = 101;
		self.y = 100;

		# keep track of levels player has completed...
		self.level = 1;

		# eventually have bonus points for killing while firing less
		# this can be displayed at go_scrn and endlevel_scrn...
		self.bullets_fired = 0.0;
		self.enemies_killed = 0.0;

		self.total_score = 0;

		self.startBG = pg.image.load('spaceBG2.JPG').convert();

	def new(self):

		self.all_sprites = pg.sprite.Group();
		self.enemies = pg.sprite.Group();
		self.bullets = pg.sprite.Group();
		# self.ray_sprite = pg.sprite.Group();

		# Try spawning a row of enemies below the first row
		# this also needs to be called somewhere else...
		

		self.player = Player(self);

		self.bg = pg.image.load('space2.PNG').convert();
		

		self.all_sprites.add(self.player);

		self.run();

	def run(self):

		# Main game loop...

		enem = self.level * 4;

		for x in range(0, enem):
			self.spawnEnemy();

		while self.playing:
			self.clk.tick(FPS);
			self.events();
			self.update();
			self.draw();

	def update(self):

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

		# if not self.enemies and player.HP > 0 for this bit?,
		# if there is no enemies or they're all dead...
		if not self.enemies and self.player.HP > 0 and self.player.points != 0:
			self.playing = False;
			self.show_endlevel_scrn();

		self.all_sprites.update();
		self.enemies.update();
		
		print(self.player.HP);

	def events(self):

		for e in pg.event.get():
			if e.type == pg.QUIT:
				#if self.playing:
				self.playing = False;
				self.running = False;

				

			if e.type == pg.KEYDOWN:
				if e.key == pg.K_SPACE and self.playing == True:
					self.player.Shoot();
					self.bullets_fired += 1;		# part of STATS...

		# bullets colliding with enemies...
		hits = pg.sprite.groupcollide(self.bullets, self.enemies, True, True);
		if hits:
			print(hits);
			self.player.points += 10;
			self.enemies_killed += 1;

		# enemies colliding with player...
		coll = pg.sprite.spritecollide(self.player, self.enemies, True, False);
		if coll:
			self.player.HP -= 50;

	def draw(self):

		self.scr.blit(self.bg, (0, 0));
		pg.draw.rect(self.scr, YEL, (WIDTH - 200, 0, 200, 40), 3);
		self.draw_text('SCORE : ' + str(self.player.points), 20, WHT, WIDTH - 120, 10);
		pg.draw.rect(self.scr, RED, (0, 0, 200, 40), 3);
		self.draw_text('HEALTH : ' + str(self.player.HP), 20, WHT, 75, 10);
		self.all_sprites.draw(self.scr);
		pg.display.flip();

	def spawnEnemy(self):

		if len(self.enemies) >= 24:
			return;

		e = Enemy(self.x, self.y, self);
		
		self.enemies.add(e);
		self.all_sprites.add(e);

		if self.level < 2:
			self.x += 150;
		else:
			self.x += 75;

		if self.x > WIDTH - 100:
			self.x = 101;
			self.y += 50;

	def show_start_scrn(self):

		# opening screen to start a new game

		self.scr.blit(self.startBG, (0, 0));
		self.draw_text('TITLE HERE', 22, BLK, WIDTH / 2, 100);
		self.draw_text('a = Left, d = Right, Space = Shoot', 14, BLK, WIDTH / 2, 200);
		self.draw_text('press ENTER to start or ESC to quit', 20, BLK, WIDTH / 2, 400);
		pg.display.flip();
		self.wait_for_key();

		self.playing = True;

	def show_go_scrn(self):

		# game over screen
		
		pass;

	def show_endlevel_scrn(self):

		# screen that appears when the player completes a level
		# contains player stats from previous level as well as overall
		# score...
		# need to kill all sprites in bullet groups
		self.level_bonus = 0;
		self.total_score += self.player.points;
		self.s_r = self.enemies_killed / self.bullets_fired;
		self.shoot_perc = self.s_r * 100;
		if self.shoot_perc >= 50 and self.shoot_perc <= 74:
			self.level_bonus = 100;
		elif self.shoot_perc >= 75 and self.shoot_perc <= 99:
			self.level_bonus = 250;
		elif self.shoot_perc == 100:
			self.level_bonus = 500;

		self.total_score += self.level_bonus;

		self.scr.blit(BG_EL_SCREEN, (0, 0));
		self.draw_text('LEVEL ' + str(self.level) + ' COMPLETE!!', 40, BLK, WIDTH / 2, 100);
		self.draw_text('TOTAL SCORE : ' + str(self.total_score), 22, BLK, WIDTH / 2, 200);
		self.draw_text('LEVEL SCORE : ' + str(self.player.points), 14, BLK, WIDTH / 2, 300);
		self.draw_text('BULLETS FIRED : %i' % (self.bullets_fired), 14, BLK, WIDTH / 2, 320);
		self.draw_text('ENEMIES KILLED : %i' % (self.enemies_killed), 14, BLK, WIDTH / 2, 340);
		self.draw_text('ACCURACY PERCENTAGE : %i' % (self.shoot_perc) + '%', 14, BLK, WIDTH / 2, 360);
		self.draw_text('LEVEL BONUS : ' + str(self.level_bonus), 14, BLK, WIDTH / 2, 380);
		self.draw_text('press ENTER to continue or ESC to quit', 20, RED, WIDTH / 2, 600);
		pg.display.flip();
		self.wait_for_key();
		
		self.level += 1;

		
		self.player.points = 0;
		self.bullets_fired = 0.0;
		self.enemies_killed = 0.0;

		# reset enemy x and y to respawn new enemies for the next level...
		self.x = 101;
		self.y = 100;

		self.playing = True;
		self.new();
		print(self.total_score);
		
	def draw_text(self, text, size, colour, x, y):
		font = pg.font.Font(FONT_NAME, size);
		text_surface = font.render(text, True, colour);
		text_rect = text_surface.get_rect();
		text_rect.midtop = (x, y);
		self.scr.blit(text_surface, text_rect);

	def wait_for_key(self):

		# wait for player to start, continue or quit
		# use on splash screens 

		waiting = True;

		while waiting:
			self.clk.tick(FPS);
			for e in pg.event.get():
				if e.type == pg.QUIT:
					self.running = False;
					self.playing = False;
					waiting = False;
				if e.type == pg.KEYUP:
					if e.key == pg.K_RETURN:
						waiting = False;
					if e.key == pg.K_ESCAPE:
						self.running = False;
						self.playing = False;
						waiting = False;
						
g = Game();

g.show_start_scrn();

while g.running:

	g.new();
	g.show_go_scrn();

pg.quit();