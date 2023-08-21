import pygame
from random import randint as r
import time

pygame.init()

SCREEN_SIZE = {'x' : 1200, 'y' : 800}
win = pygame.display.set_mode((SCREEN_SIZE['x'], SCREEN_SIZE['y'] + 100))
pygame.display.set_caption('bomberman')

BACKGROUND_COLOR = (0, 0, 0)
TABLE_LINE_COLOR = (50, 50, 50)
RECT_LINE_COLOR = (100, 100, 100)
RECT_COLOR = (200, 200, 200)
RECT_COLOR_BOMB = (200, 0, 0)
RECT_LINE_COLOR_BOMB = (100, 0, 0)
FIRST_CIRCLE_COLOR = (200, 200, 0)
SECOND_CIRCLE_COLOR = (220, 100, 0)
THIRD_CIRCLE_COLOR = (250, 50, 0)
CELL_SIZE = 20
TABLE_SIZE = {'x' : SCREEN_SIZE['x'] // CELL_SIZE, 'y' : SCREEN_SIZE['y'] // CELL_SIZE}
COLORS = [(0, 0, 255), (0, 255, 0), (255, 0, 0), (255, 255, 0), (255, 0, 255), (0, 255, 255), (139, 69, 19), (139, 137, 137)]

COUNT_OF_BOMBS = 200

def update(button, mouse_pos, bombs_defuse, true_bombs_defuse, recursion) -> None:
	global WIN, LOSE, open_old_cell

	touch = {'x' : mouse_pos[0]-mouse_pos[0]%CELL_SIZE, 'y' : mouse_pos[1]-mouse_pos[1]%CELL_SIZE}
	x, y = touch['x']//CELL_SIZE, touch['y']//CELL_SIZE

	if button == 3:
		PXARRAY = pygame.PixelArray(win)
		if PXARRAY[touch['x']+5, touch['y']+5] == win.map_rgb(RECT_COLOR):
			pygame.draw.rect(win, RECT_COLOR_BOMB, (touch['x']+CELL_SIZE/10+1, touch['y']+CELL_SIZE/10+1, CELL_SIZE-CELL_SIZE/5-1, CELL_SIZE-CELL_SIZE/5-1))
			pygame.draw.line(win, RECT_LINE_COLOR_BOMB, (touch['x']+1, touch['y']+1), (touch['x']+CELL_SIZE-1, touch['y']+1))
			pygame.draw.line(win, RECT_LINE_COLOR_BOMB, (touch['x']+1, touch['y']+2), (touch['x']+CELL_SIZE-2, touch['y']+2))
			pygame.draw.line(win, RECT_LINE_COLOR_BOMB, (touch['x']+1, touch['y']+3), (touch['x']+1, touch['y']+CELL_SIZE-1))
			pygame.draw.line(win, RECT_LINE_COLOR_BOMB, (touch['x']+2, touch['y']+3), (touch['x']+2, touch['y']+CELL_SIZE-2))
			pygame.display.update()

			bombs_defuse += [[x, y]]
			if [x, y] in booms_data and [x, y] not in true_bombs_defuse: true_bombs_defuse += [[x, y]]
			if len(true_bombs_defuse) == COUNT_OF_BOMBS: WIN = True

		elif PXARRAY[touch['x']+5, touch['y']+5] == win.map_rgb(RECT_COLOR_BOMB):
			pygame.draw.rect(win, RECT_COLOR, (touch['x']+CELL_SIZE/10+1, touch['y']+CELL_SIZE/10+1, CELL_SIZE-CELL_SIZE/5-1, CELL_SIZE-CELL_SIZE/5-1))
			pygame.draw.line(win, RECT_LINE_COLOR, (touch['x']+1, touch['y']+1), (touch['x']+CELL_SIZE-1, touch['y']+1))
			pygame.draw.line(win, RECT_LINE_COLOR, (touch['x']+1, touch['y']+2), (touch['x']+CELL_SIZE-2, touch['y']+2))
			pygame.draw.line(win, RECT_LINE_COLOR, (touch['x']+1, touch['y']+3), (touch['x']+1, touch['y']+CELL_SIZE-1))
			pygame.draw.line(win, RECT_LINE_COLOR, (touch['x']+2, touch['y']+3), (touch['x']+2, touch['y']+CELL_SIZE-2))
			pygame.display.update()

			bombs_defuse.remove([x, y])
			if [x, y] in true_bombs_defuse: true_bombs_defuse.remove([x, y])
		return

	if (x, y) in number_data.keys():
		number = number_data[(x, y)]
		pygame.draw.rect(win, BACKGROUND_COLOR, (touch['x']+1, touch['y']+1, CELL_SIZE-2, CELL_SIZE-2))
		text = FF.render(str(number), 1, COLORS[number-1])
		win.blit(text, (touch['x'] + 6, touch['y'] + 4))

		if recursion == 0:
			cnt_bombs_defuse_around = 0
			cnt_true_bombs_defuse_around = 0
			for x_delta in range(-1, 2, 1):
				for y_delta in range(-1, 2, 1):
					if x_delta == 0 and y_delta == 0: continue
					if [x + x_delta, y + y_delta] in bombs_defuse: cnt_bombs_defuse_around += 1
					if [x + x_delta, y + y_delta] in true_bombs_defuse: cnt_true_bombs_defuse_around += 1

			if cnt_bombs_defuse_around == number:
				if cnt_true_bombs_defuse_around != number: 
					LOSE = True
					LOSE_animation((touch['x'] + CELL_SIZE/2, touch['y'] + CELL_SIZE/2))
					return
				for x_delta in range(-1, 2, 1):
					for y_delta in range(-1, 2, 1):
						if x_delta == 0 and y_delta == 0: continue
						if x + x_delta >= 0 and x + x_delta < TABLE_SIZE['x'] and y + y_delta >= 0 and y + y_delta < TABLE_SIZE['y']:
							update(1, ((x + x_delta)*CELL_SIZE, (y + y_delta)*CELL_SIZE), bombs_defuse, true_bombs_defuse, 1)

	elif [x, y] in booms_data: 
		if [x, y] in bombs_defuse: return
		LOSE = True
		LOSE_animation((touch['x'] + CELL_SIZE/2, touch['y'] + CELL_SIZE/2))
	else:
		new_cell = []
		if [x, y] not in open_old_cell: new_cell += [[x, y]]

		while len(new_cell) > 0:
			pygame.draw.rect(win, BACKGROUND_COLOR, (x*CELL_SIZE+1, y*CELL_SIZE+1, CELL_SIZE-2, CELL_SIZE-2))
			for x_delta in range(-1, 2, 1):
				for y_delta in range(-1, 2, 1):
					if [x + x_delta, y + y_delta] in bombs_defuse: bombs_defuse.remove([x + x_delta, y + y_delta])
					if (x + x_delta, y + y_delta) in number_data.keys():
						pygame.draw.rect(win, BACKGROUND_COLOR, ((x + x_delta)*CELL_SIZE+1, (y + y_delta)*CELL_SIZE+1, CELL_SIZE-2, CELL_SIZE-2))
						number = number_data[(x + x_delta, y + y_delta)]
						text = FF.render(str(number), 1, COLORS[number-1])
						win.blit(text, ((x + x_delta)*CELL_SIZE + 6, (y + y_delta)*CELL_SIZE + 4))
						continue
					elif [x + x_delta, y + y_delta] not in open_old_cell and [x + x_delta, y + y_delta] not in new_cell:
						if x + x_delta >= 0 and x + x_delta < TABLE_SIZE['x'] and y + y_delta >= 0 and y + y_delta < TABLE_SIZE['y']:
							new_cell += [[x + x_delta, y + y_delta]]
			new_cell.remove([x, y])
			open_old_cell += [[x, y]]
			if len(new_cell) > 0: x, y = new_cell[0][0], new_cell[0][1]

	pygame.display.update()

def LOSE_animation(position) -> None:
	radius = 1
	while radius < 50:
		pygame.draw.circle(win, FIRST_CIRCLE_COLOR, position, radius)
		if radius > 15: pygame.draw.circle(win, SECOND_CIRCLE_COLOR, position, radius - 15)
		if radius > 30: pygame.draw.circle(win, THIRD_CIRCLE_COLOR, position, radius - 30)
		pygame.display.update()
		radius += 1

def start_update() -> None:
	win.fill(BACKGROUND_COLOR)

	for i in range(0, max(SCREEN_SIZE['x'], SCREEN_SIZE['y']), CELL_SIZE):
		pygame.draw.line(win, TABLE_LINE_COLOR, (i, 0), (i, SCREEN_SIZE['y']))
		if i <= SCREEN_SIZE['y']: pygame.draw.line(win, TABLE_LINE_COLOR, (0, i), (SCREEN_SIZE['x'], i))

	for x in range(0, max(SCREEN_SIZE['x'], SCREEN_SIZE['y']), CELL_SIZE):
		for y in range(0, min(SCREEN_SIZE['x'], SCREEN_SIZE['y']), CELL_SIZE):
			pygame.draw.rect(win, RECT_COLOR, (x+CELL_SIZE/10+1, y+CELL_SIZE/10+1, CELL_SIZE-CELL_SIZE/5-1, CELL_SIZE-CELL_SIZE/5-1))
			pygame.draw.line(win, RECT_LINE_COLOR, (x+1, y+1), (x+CELL_SIZE-1, y+1))
			pygame.draw.line(win, RECT_LINE_COLOR, (x+1, y+2), (x+CELL_SIZE-2, y+2))
			pygame.draw.line(win, RECT_LINE_COLOR, (x+1, y+3), (x+1, y+CELL_SIZE-1))
			pygame.draw.line(win, RECT_LINE_COLOR, (x+2, y+3), (x+2, y+CELL_SIZE-2))

	pygame.display.update()

def generate_table(booms_data, number_data) -> None:

	while len(booms_data) <= COUNT_OF_BOMBS:
		rand_coords = [r(0, TABLE_SIZE['x'] - 1), r(0, TABLE_SIZE['y'] - 1)]
		if rand_coords not in booms_data: booms_data += [rand_coords]
			#pygame.draw.rect(win, (0, 255, 0), (rand_coords[0]*CELL_SIZE+1, rand_coords[1]*CELL_SIZE+1, CELL_SIZE-2, CELL_SIZE-2))

	for i in range(COUNT_OF_BOMBS):
		x, y = booms_data[i][0], booms_data[i][1]
		for x_delta in range(-1, 2, 1):
			for y_delta in range(-1, 2, 1):
				if (x_delta == 0 and y_delta == 0) or [x + x_delta, y + y_delta] in booms_data: continue
				if x + x_delta < 0 or x + x_delta >= TABLE_SIZE['x'] or y + y_delta < 0 or y + y_delta >= TABLE_SIZE['y']: continue
				if (x + x_delta, y + y_delta) not in number_data.keys(): number_data[(x + x_delta, y + y_delta)] = 1
				else: number_data[(x + x_delta, y + y_delta)] += 1

	'''
	for x in range(60):
		for y in range(40):
			if [x, y] not in booms_data: update(1, (x*CELL_SIZE, y*CELL_SIZE), bombs_defuse, true_bombs_defuse, 0)
	'''

def time_bombs_update(START_TIME) -> None:
	pygame.draw.rect(win, BACKGROUND_COLOR, (0, SCREEN_SIZE['y'], 150, 100))

	F1 = pygame.font.Font(None, 30)
	text = F1.render('time: ' + str(int(time.time()) - START_TIME), 1, (0, 200, 200))
	win.blit(text, (10, SCREEN_SIZE['y'] + 18))

	F1 = pygame.font.Font(None, 30)
	if COUNT_OF_BOMBS - len(bombs_defuse) <= 0: text = F1.render('bombs: 0?', 1, (200, 0, 200))
	else: text = F1.render('bombs: ' + str(COUNT_OF_BOMBS - len(bombs_defuse)), 1, (200, 0, 200))
	win.blit(text, (10, SCREEN_SIZE['y'] + 65))

	pygame.display.update()

def restart() -> None:
	global booms_data, number_data, bombs_defuse, true_bombs_defuse, open_old_cell, WIN, LOSE, START_TIME

	start_update()
	number_data = {}
	booms_data = []
	bombs_defuse = []
	true_bombs_defuse = []
	open_old_cell = []
	WIN = False
	LOSE = False
	START_TIME = int(time.time())
	generate_table(booms_data, number_data)

RUN = True
FF = pygame.font.Font(None, 23)
WIN = False
LOSE = False
START_TIME = int(time.time())

number_data = {}
booms_data = []
bombs_defuse = []
true_bombs_defuse = []
open_old_cell = []
restart()

while RUN:

	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_q: RUN = False
			if event.key == pygame.K_r: restart()
		if event.type == pygame.QUIT: RUN = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1: 
				if WIN == False and LOSE == False: update(1, pygame.mouse.get_pos(), bombs_defuse, true_bombs_defuse, 0)
			if event.button == 3: 
				if WIN == False and LOSE == False: update(3, pygame.mouse.get_pos(), bombs_defuse, true_bombs_defuse, 0)
			if WIN:

				F1 = pygame.font.Font(None, 50)
				text = F1.render('YOU WIN!', 1, (0, 200, 0))
				win.blit(text, (SCREEN_SIZE['x']/2 - 130, SCREEN_SIZE['y'] + 20))

				F1 = pygame.font.Font(None, 25)
				text = F1.render('You won in ' + str(int(time.time()) - START_TIME) + ' seconds', 1, (200, 200, 200))
				win.blit(text, (SCREEN_SIZE['x']/2 - 130, SCREEN_SIZE['y'] + 70))

				pygame.draw.rect(win, BACKGROUND_COLOR, (0, SCREEN_SIZE['y'] + 40, 150, 80))
				F1 = pygame.font.Font(None, 30)
				text = F1.render('bombs: 0', 1, (200, 0, 200))
				win.blit(text, (10, SCREEN_SIZE['y'] + 65))

				pygame.display.update()

			elif LOSE:

				F1 = pygame.font.Font(None, 50)
				text = F1.render('YOU LOSE(', 1, (200, 0, 0))
				win.blit(text, (SCREEN_SIZE['x']/2 - 130, SCREEN_SIZE['y'] + 20))

				F1 = pygame.font.Font(None, 25)
				text = F1.render('Press \'R\' to restart', 1, (200, 200, 200))
				win.blit(text, (SCREEN_SIZE['x']/2 - 108, SCREEN_SIZE['y'] + 70))

				pygame.display.update()


	if WIN == False and LOSE == False: time_bombs_update(START_TIME)

pygame.quit()