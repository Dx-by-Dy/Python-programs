import pygame
from pygame.event import get as get_events
from pygame import display, KEYDOWN, K_q, MOUSEBUTTONDOWN, mouse, K_DOWN, K_UP, K_LEFT, K_RIGHT, K_w, K_s, K_e, K_p
from pygame.time import delay
from pygame.draw import line, rect
import ctypes

pygame.init()
win = display.set_mode((0, 0), pygame.FULLSCREEN)

user32 = ctypes.windll.user32
w = user32.GetSystemMetrics(0)
h = user32.GetSystemMetrics(1)

def update():
	global sec, rects
	win.fill((0, 0, 0))

	newRect = {1 : [], 2 : [], 3 : []}

	for i in range(w//sz+1):
		line(win, (150, 150, 150), (i*sz, 0), (i*sz, h))
	for i in range(h//sz+1):
		line(win, (150, 150, 150), (0, i*sz), (w, i*sz))
	for j in range(1, 4):
		for i in rects[j]:
			if j == 1: rect(win, (255, 255, 0), (int(i[0])+1, int(i[1])+1, sz-1, sz-1))
			elif j == 2: rect(win, (0, 0, 255), (int(i[0])+1, int(i[1])+1, sz-1, sz-1))
			else: rect(win, (150, 0, 0), (int(i[0])+1, int(i[1])+1, sz-1, sz-1))

	if sec > spd and not pause:
		sec = 0
		newRect[3] += rects[2]
		newRect[1] += rects[3]

		for i in range(len(rects[1])):
			z = 0
			for k in range(-1, 2):
				for p in range(-1, 2):
					if k == 0 and p == 0: continue
					if (rects[1][i][0] + sz*k, rects[1][i][1] + sz*p) in rects[2]: z += 1
			if z < 3 and z > 0 and rects[1][i] not in rects[3] and rects[1][i] not in rects[2]: newRect[2] += [rects[1][i]]

		for i in range(len(rects[1])):
			if rects[1][i] not in newRect[2]: newRect[1] += [rects[1][i]]

		rects[1], rects[2], rects[3] = newRect[1], newRect[2], newRect[3]

	display.update()
	sec += 1

run, pause = True, False
sec, spd = 0, 50
dl = [i for i in range(2, min(w, h)) if w%i == 0 and h%i == 0]
sz = dl[0]
rects = {1: [(480, 320), (640, 440), (480, 560), (840, 360), (520, 320), (600, 400), (520, 560), (800, 360), (560, 360), (560, 360), (560, 560), (720, 360), (680, 360), (760, 360), (1000, 360), (520, 400), (600, 560), (720, 400), (960, 360), (960, 360), (440, 160), (480, 160), (520, 160), (560, 160), (600, 160), (720, 320), (640, 200), (680, 200), (720, 200), (720, 280), (680, 240), (640, 280), (680, 560), (680, 160)], 2: [(480, 400), (640, 520), (720, 520), (680, 520), (720, 440), (920, 360)], 3: [(440, 360), (680, 480), (440, 560), (880, 360)]}
sz = 40

while run:

	for event in get_events():
		if event.type == KEYDOWN:
			if event.key == K_q: run = False
			if event.key == K_w: spd -= 5
			if event.key == K_s: spd += 5
			if event.key == K_e: print(rects, sz)
			if event.key == K_p: 
				if not pause: pause = True
				else: pause = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 4 and dl.index(sz) != len(dl)-1: 
				sz = dl[dl.index(sz)+1]
				for j in range(1, 4):
					for i in range(len(rects[j])):
						x, y = rects[j][i][0]*(sz/dl[dl.index(sz)-1]), rects[j][i][1]*(sz/dl[dl.index(sz)-1])
						rects[j][i] = (x, y)
			if event.button == 5 and dl.index(sz) != 0: 
				sz = dl[dl.index(sz)-1]
				for j in range(1, 4):
					for i in range(len(rects[j])):
						x, y = rects[j][i][0]*(sz/dl[dl.index(sz)+1]), rects[j][i][1]*(sz/dl[dl.index(sz)+1])
						rects[j][i] = (x, y)
			if event.button == 1:
				x, y = list(mouse.get_pos())
				x, y = x-x%sz, y-y%sz
				if (x, y) not in rects[1]: rects[1] += [(x, y)]
				else: rects[2] += [(x, y)]
			if event.button == 3:
				x, y = list(mouse.get_pos())
				x, y = x-x%sz, y-y%sz
				if (x, y) in rects[1]: rects[1].pop(rects[1].index((x, y)))
				elif (x, y) in rects[2]: rects[2].pop(rects[2].index((x, y)))
				elif (x, y) in rects[3]: rects[3].pop(rects[3].index((x, y)))

	keys = pygame.key.get_pressed()
	if keys[K_UP]:
		for j in range(1, 4):
			for i in range(len(rects[j])):
				x, y = rects[j][i][0], rects[j][i][1] + sz
				rects[j][i] = (x, y)
	if keys[K_DOWN]:
		for j in range(1, 4):
			for i in range(len(rects[j])):
				x, y = rects[j][i][0], rects[j][i][1] - sz
				rects[j][i] = (x, y)
	if keys[K_LEFT]:
		for j in range(1, 4):
			for i in range(len(rects[j])):
				x, y = rects[j][i][0] + sz, rects[j][i][1]
				rects[j][i] = (x, y)
	if keys[K_RIGHT]:
		for j in range(1, 4): 
			for i in range(len(rects[j])):
				x, y = rects[j][i][0] - sz, rects[j][i][1]
				rects[j][i] = (x, y)

	update()

pygame.quit()