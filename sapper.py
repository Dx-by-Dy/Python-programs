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

COUNT_OF_BOMBS = 50

class Group():
	
	def __init__(self, body, max_number, min_number):
		self.max_number = max_number
		self.min_number = min_number
		self.body = body
		self.delete_me = False

	def check_size_number(self, cell_for_1_click, cell_for_3_click):

		if self.delete_me: return cell_for_1_click, cell_for_3_click
		if len(self.body) == self.min_number:
			for cell in self.body:
				if cell not in cell_for_3_click: cell_for_3_click += [cell]
			self.delete_me = True
		if self.max_number == 0:
			for cell in self.body:
				if cell not in cell_for_1_click: cell_for_1_click += [cell]
			self.delete_me = True

		return cell_for_1_click, cell_for_3_click

	def substraction(self, another_group) -> None:
		for cell in another_group.body:
			if cell in self.body: self.body.remove(cell)
		self.min_number = max(self.min_number - another_group.max_number, 0)
		self.max_number = min(self.max_number - another_group.min_number, len(self.body))

	def contains(self, body_another_group) -> bool:
		for cell in body_another_group:
			if cell not in self.body: return False
		return True

	def intersect(self, body_another_group) -> bool:
		for cell in body_another_group:
			if cell in self.body: return True
		return False

	def intersect_body(self, body_another_group) -> list:
		inter_body = []
		for cell in body_another_group:
			if cell in self.body: inter_body += [cell]
		return inter_body

def bot_for_sapper() -> bool:
	global Groups

	cnt_3_clicks = 0
	while True:

		cell_for_1_click = []
		cell_for_3_click = []

		for key in visible_number.keys():

			x, y = key[0], key[1]
			number = visible_number[key]
			unknown_cell_around = []

			for x_delta in range(-1, 2, 1):
				for y_delta in range(-1, 2, 1):
					if x_delta == 0 and y_delta == 0: continue
					if x + x_delta < 0 or x + x_delta >= TABLE_SIZE['x'] or y + y_delta < 0 or y + y_delta >= TABLE_SIZE['y']: continue
					if [x + x_delta, y + y_delta] in bombs_defuse: number -= 1
					elif [x + x_delta, y + y_delta] not in open_cell and (x + x_delta, y + y_delta) not in visible_number.keys():
						unknown_cell_around += [((x + x_delta)*CELL_SIZE, (y + y_delta)*CELL_SIZE)]

			'''
			if len(unknown_cell_around) != 0:
				for cell in unknown_cell_around:
					pygame.draw.rect(win, (0, 0, 200), (cell[0]+3, cell[1]+3, CELL_SIZE-5, CELL_SIZE-5))
					pygame.display.update()

				pygame.time.delay(500)

				for cell in unknown_cell_around:
					pygame.draw.rect(win, RECT_COLOR, (cell[0]+3, cell[1]+3, CELL_SIZE-5, CELL_SIZE-5))
					pygame.display.update()
			'''
			
			if len(unknown_cell_around) != 0: Groups += [Group(unknown_cell_around, number, number)]

		while True:

			groups_changes = False

			for id_group in range(len(Groups)):
				cell_for_1_click, cell_for_3_click = Groups[id_group].check_size_number(cell_for_1_click, cell_for_3_click)

			for id_first_group in range(len(Groups)):
				if Groups[id_first_group].delete_me: continue
				for id_second_group in range(len(Groups)):
					if Groups[id_second_group].delete_me: continue
					if id_first_group == id_second_group: continue
					if Groups[id_first_group].contains(Groups[id_second_group].body):
						Groups[id_first_group].substraction(Groups[id_second_group])

			for id_first_group in range(len(Groups)):
				if Groups[id_first_group].delete_me: continue
				max_len_body_intersect = 0
				id_group_with_max_len_body_intersect = -1

				for id_second_group in range(len(Groups)):
					if Groups[id_second_group].delete_me: continue
					if id_first_group == id_second_group: continue
					if len(Groups[id_second_group].body) > len(Groups[id_first_group].body): continue
					if len(Groups[id_first_group].intersect_body(Groups[id_second_group].body)) == max_len_body_intersect and max_len_body_intersect > 0:
						if min(len(Groups[id_second_group].body) - Groups[id_second_group].min_number, Groups[id_second_group].max_number) < min(len(Groups[id_group_with_max_len_body_intersect].body) - Groups[id_group_with_max_len_body_intersect].min_number, Groups[id_group_with_max_len_body_intersect].max_number):
							id_group_with_max_len_body_intersect = id_second_group
					elif len(Groups[id_first_group].intersect_body(Groups[id_second_group].body)) > max_len_body_intersect:
						max_len_body_intersect = len(Groups[id_first_group].intersect_body(Groups[id_second_group].body))
						id_group_with_max_len_body_intersect = id_second_group

				if id_group_with_max_len_body_intersect != -1:

					groups_changes = True

					new_body = Groups[id_first_group].intersect_body(Groups[id_group_with_max_len_body_intersect].body)
					new_max_number = min(min(Groups[id_first_group].max_number, Groups[id_group_with_max_len_body_intersect].max_number), len(new_body))
					len_body_first_group = len(Groups[id_first_group].body) - len(new_body)
					len_body_second_group = len(Groups[id_group_with_max_len_body_intersect].body) - len(new_body)
					new_min_number = max(max(Groups[id_first_group].min_number - len_body_first_group, Groups[id_group_with_max_len_body_intersect].min_number - len_body_second_group), 0)

					Groups += [Group(new_body, new_max_number, new_min_number)]
					Groups[id_first_group].substraction(Groups[-1])
					Groups[id_group_with_max_len_body_intersect].substraction(Groups[-1])

					cell_for_1_click, cell_for_3_click = Groups[-1].check_size_number(cell_for_1_click, cell_for_3_click)

			if groups_changes == False: break

		for cell in cell_for_3_click:
			update(3, cell, 1, True)
		for cell in cell_for_1_click:
			update(1, cell, 1, True)

		Groups = []
		cnt_3_clicks += len(cell_for_3_click)

		if len(cell_for_3_click) == 0 and len(cell_for_1_click) == 0: break
		if COUNT_OF_BOMBS - cnt_3_clicks <= 3: return True

	return False

def update(button, mouse_pos, recursion, bot_request) -> None:
	global WIN, LOSE, open_old_cell, visible_number, open_cell, bombs_defuse, true_bombs_defuse

	touch = {'x' : mouse_pos[0]-mouse_pos[0]%CELL_SIZE, 'y' : mouse_pos[1]-mouse_pos[1]%CELL_SIZE}
	x, y = touch['x'] // CELL_SIZE, touch['y'] // CELL_SIZE

	if button == 3:
		if [x, y] not in bombs_defuse and [x, y] not in open_cell and (x, y) not in visible_number.keys():
			if bot_request == False:
				pygame.draw.rect(win, RECT_COLOR_BOMB, (touch['x']+CELL_SIZE/10+1, touch['y']+CELL_SIZE/10+1, CELL_SIZE-CELL_SIZE/5-1, CELL_SIZE-CELL_SIZE/5-1))
				pygame.draw.line(win, RECT_LINE_COLOR_BOMB, (touch['x']+1, touch['y']+1), (touch['x']+CELL_SIZE-1, touch['y']+1))
				pygame.draw.line(win, RECT_LINE_COLOR_BOMB, (touch['x']+1, touch['y']+2), (touch['x']+CELL_SIZE-2, touch['y']+2))
				pygame.draw.line(win, RECT_LINE_COLOR_BOMB, (touch['x']+1, touch['y']+3), (touch['x']+1, touch['y']+CELL_SIZE-1))
				pygame.draw.line(win, RECT_LINE_COLOR_BOMB, (touch['x']+2, touch['y']+3), (touch['x']+2, touch['y']+CELL_SIZE-2))
				pygame.display.update()

			bombs_defuse += [[x, y]]
			if [x, y] in booms_data and [x, y] not in true_bombs_defuse: true_bombs_defuse += [[x, y]]
			if bot_request == False and len(true_bombs_defuse) == COUNT_OF_BOMBS: WIN = True

		elif [x, y] in bombs_defuse:
			if bot_request == False:
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

		if bot_request == False:
			pygame.draw.rect(win, BACKGROUND_COLOR, (touch['x']+1, touch['y']+1, CELL_SIZE-2, CELL_SIZE-2))
			text = FF.render(str(number), 1, COLORS[number-1])
			win.blit(text, (touch['x'] + 6, touch['y'] + 4))

		if (x, y) not in visible_number.keys(): visible_number[(x, y)] = number

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
							update(1, ((x + x_delta)*CELL_SIZE, (y + y_delta)*CELL_SIZE), 1, False)

	elif [x, y] in booms_data: 
		if [x, y] in bombs_defuse: return
		LOSE = True
		LOSE_animation((touch['x'] + CELL_SIZE/2, touch['y'] + CELL_SIZE/2))
	else:
		new_cell = []
		if [x, y] not in open_old_cell: 
			new_cell += [[x, y]]

			if [x, y] not in open_cell: open_cell += [[x, y]]

		while len(new_cell) > 0:
			if bot_request == False: pygame.draw.rect(win, BACKGROUND_COLOR, (x*CELL_SIZE+1, y*CELL_SIZE+1, CELL_SIZE-2, CELL_SIZE-2))
			for x_delta in range(-1, 2, 1):
				for y_delta in range(-1, 2, 1):
					if [x + x_delta, y + y_delta] in bombs_defuse: bombs_defuse.remove([x + x_delta, y + y_delta])
					if (x + x_delta, y + y_delta) in number_data.keys():
						number = number_data[(x + x_delta, y + y_delta)]

						if bot_request == False:
							pygame.draw.rect(win, BACKGROUND_COLOR, ((x + x_delta)*CELL_SIZE+1, (y + y_delta)*CELL_SIZE+1, CELL_SIZE-2, CELL_SIZE-2))
							text = FF.render(str(number), 1, COLORS[number-1])
							win.blit(text, ((x + x_delta)*CELL_SIZE + 6, (y + y_delta)*CELL_SIZE + 4))

						if (x + x_delta, y + y_delta) not in visible_number.keys(): visible_number[(x + x_delta, y + y_delta)] = number

					elif [x + x_delta, y + y_delta] not in open_old_cell and [x + x_delta, y + y_delta] not in new_cell:
						if x + x_delta >= 0 and x + x_delta < TABLE_SIZE['x'] and y + y_delta >= 0 and y + y_delta < TABLE_SIZE['y']:
							new_cell += [[x + x_delta, y + y_delta]]
							if [x + x_delta, y + y_delta] not in open_cell: open_cell += [[x + x_delta, y + y_delta]]

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
	
def generate_table(first_click) -> None:
	global bombs_defuse, true_bombs_defuse, WIN, LOSE, open_old_cell, visible_number, open_cell, Groups, booms_data, number_data, START_TIME

	while True:

		number_data = {}
		booms_data = []
		bombs_defuse = []
		true_bombs_defuse = []
		open_old_cell = []
		visible_number = {}
		open_cell = []
		Groups = []

		LOSE = False
		WIN = False

		while len(booms_data) < COUNT_OF_BOMBS:
			rand_coords = [r(0, TABLE_SIZE['x'] - 1), r(0, TABLE_SIZE['y'] - 1)]
			if rand_coords not in booms_data and (abs(first_click[0] - rand_coords[0]) > 1 or abs(first_click[1] - rand_coords[1]) > 1): booms_data += [rand_coords]

		for i in range(COUNT_OF_BOMBS):
			x, y = booms_data[i][0], booms_data[i][1]
			for x_delta in range(-1, 2, 1):
				for y_delta in range(-1, 2, 1):
					if (x_delta == 0 and y_delta == 0) or [x + x_delta, y + y_delta] in booms_data: continue
					if x + x_delta < 0 or x + x_delta >= TABLE_SIZE['x'] or y + y_delta < 0 or y + y_delta >= TABLE_SIZE['y']: continue
					if (x + x_delta, y + y_delta) not in number_data.keys(): number_data[(x + x_delta, y + y_delta)] = 1
					else: number_data[(x + x_delta, y + y_delta)] += 1

		update(1, (first_click[0] * CELL_SIZE, first_click[1] * CELL_SIZE), 0, True)
		if bot_for_sapper():
			start_update()

			bombs_defuse = []
			true_bombs_defuse = []
			open_old_cell = []
			visible_number = {}
			open_cell = []
			Groups = []

			LOSE = False
			WIN = False
			START_TIME = int(time.time())

			break
	

def set_vis_unvis_bombs(VISIBLE_BOMBS):

	if VISIBLE_BOMBS:
		for bomb in booms_data:
			if bomb not in true_bombs_defuse: pygame.draw.rect(win, (0, 0, 200), (bomb[0]*CELL_SIZE+3, bomb[1]*CELL_SIZE+3, CELL_SIZE-5, CELL_SIZE-5))
	else:
		for bomb in booms_data:
			if bomb not in true_bombs_defuse: pygame.draw.rect(win, RECT_COLOR, (bomb[0]*CELL_SIZE+3, bomb[1]*CELL_SIZE+3, CELL_SIZE-5, CELL_SIZE-5))
	
	pygame.display.update()

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
	global booms_data, number_data, bombs_defuse, true_bombs_defuse, open_old_cell, WIN, LOSE, START_TIME, open_cell, visible_number, VISIBLE_BOMBS, Groups, first_click

	start_update()
	number_data = {}
	booms_data = []
	bombs_defuse = []
	true_bombs_defuse = []
	open_old_cell = []
	first_click = []

	WIN = False
	LOSE = False
	START_TIME = int(time.time())
	VISIBLE_BOMBS = False

	visible_number = {}
	open_cell = []

	Groups = []

	time_bombs_update(START_TIME)

	'''
	while True:
		rand_coords = [r(0, TABLE_SIZE['x'] - 1), r(0, TABLE_SIZE['y'] - 1)]
		if rand_coords not in booms_data and tuple(rand_coords) not in number_data.keys():
			update(1, (rand_coords[0]*CELL_SIZE, rand_coords[1]*CELL_SIZE), bombs_defuse, true_bombs_defuse, 1)
			break
	'''

RUN = True
FF = pygame.font.Font(None, 23)
WIN = False
LOSE = False
START_TIME = int(time.time())
VISIBLE_BOMBS = False

number_data = {}
booms_data = []
bombs_defuse = []
true_bombs_defuse = []
open_old_cell = []

visible_number = {}
open_cell = []
Groups = []
first_click = []

restart()

while RUN:

	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_q: RUN = False
			if event.key == pygame.K_r: restart()
			if event.key == pygame.K_SPACE: print(bot_for_sapper())
			if event.key == pygame.K_b:
				VISIBLE_BOMBS = not VISIBLE_BOMBS 
				set_vis_unvis_bombs(VISIBLE_BOMBS)
		if event.type == pygame.QUIT: RUN = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1: 
				if WIN == False and LOSE == False: 
					if len(first_click) == 0:
						first_click = [(pygame.mouse.get_pos()[0] - pygame.mouse.get_pos()[0] % CELL_SIZE) // CELL_SIZE, (pygame.mouse.get_pos()[1] - pygame.mouse.get_pos()[1] % CELL_SIZE) // CELL_SIZE]
						generate_table(first_click)
					update(1, pygame.mouse.get_pos(), 0, False)
			if event.button == 3: 
				if WIN == False and LOSE == False and len(first_click) != 0: update(3, pygame.mouse.get_pos(), 0, False)
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


	if WIN == False and LOSE == False and len(first_click) != 0: time_bombs_update(START_TIME)

pygame.quit()