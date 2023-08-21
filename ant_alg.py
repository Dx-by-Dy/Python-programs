import pygame
from pygame.event import get as get_events
from pygame import display, KEYDOWN, K_q, K_s, K_p, K_r, K_9, K_0, K_7, K_8, MOUSEBUTTONDOWN, font
from pygame.time import delay
from pygame.draw import rect, line, circle
import ctypes
from math import *
from random import randint as r
from random import random

pygame.init()
win = display.set_mode((0, 0), pygame.FULLSCREEN)

user32 = ctypes.windll.user32
w = user32.GetSystemMetrics(0)
h = user32.GetSystemMetrics(1)
tt = font.Font(None, 16)

def update():
	global now, szadi, lin, delfer, ver, minras, marhras, cnt
	if cnt == 5:
		cnt = 0
		win.fill((0, 0, 0))
		#for i in range(C):
			#for j in range(C):
				#t1 = tt.render(str(round(fer[i][j], 3)), 1, (255, 255, 255))
				#win.blit(t1, (w-200+i*40, 20+j*20))
		t1 = tt.render('min ' + str(int(minras)), 1, (255, 255, 255))
		win.blit(t1, (w-270, 20))
		t1 = tt.render(str(int(marhras)), 1, (255, 255, 255))
		win.blit(t1, (w-270, 40))
		t1 = tt.render('alf ' + str(int(alf)), 1, (255, 255, 255))
		win.blit(t1, (w-270, 60))
		t1 = tt.render('bet ' + str(int(bet)), 1, (255, 255, 255))
		win.blit(t1, (w-270, 80))
		for i in list(lin.keys()):
			if lin[i] > 4: line(win, (0, 100, 0), (pos[i[0]][0], pos[i[0]][1]), (pos[i[1]][0], pos[i[1]][1]), lin[i])
		for i in range(C):
			circle(win, (200, 0, 0), (pos[i][0], pos[i][1]), 10)

		display.update()
	

	delfer = [[0 for i in range(C)] for j in range(C)]
	for ant in range(C):
		marh = []
		marhras = 0
		nachalo = r(0, C-1)
		now = nachalo
		szadi = [False]*C
		szadi[now] = True
		for j in range(C):
			ras = [0]*C
			for i in range(C):
				if szadi[i] == False: ras[i] = ((pos[now][0] - pos[i][0])**2 + (pos[now][1] - pos[i][1])**2)**0.5
			zel = 0
			for i in range(C):
				if ras[i] != 0: zel += ((bliz/ras[i])**alf)*(fer[now][i])**bet
			ver = [0]*C
			for i in range(C):
				if ras[i] != 0: 
					ver[i] = (((bliz/ras[i])**alf)*(fer[now][i])**bet)/zel
					lin[(now, i)] = int(10*ver[i])
			d = 0
			prom = []
			for i in range(C):
				prom += [(d, d+ver[i])]
				d += ver[i]
			if sum(ver) != 0:
				rnd = random()
				for i in range(C):
					if rnd > prom[i][0] and rnd < prom[i][1]:
						szadi[i] = True
						marh += [(now, i)]
						marhras += ras[i]
						now = i
			else:
				marh += [(now, nachalo)]
				marhras += ((pos[now][0] - pos[nachalo][0])**2 + (pos[now][1] - pos[nachalo][1])**2)**0.5
		for i in range(C):
			for j in range(C):
				if (i, j) in marh:
					if marhras <= minras:
						delfer[i][j] += Q/marhras*bon
						delfer[j][i] += Q/marhras*bon
					else:
						delfer[i][j] += Q/marhras
						delfer[j][i] += Q/marhras
		if marhras < minras: minras = marhras

	for i in range(C):
		for j in range(C):
			fer[i][j] = fer[i][j]*isp + delfer[i][j]
			if fer[i][j] < 0.3: fer[i][j] = 0.3
			if fer[i][j] > 0.7: fer[i][j] = 0.7
	cnt += 1

def restart():
	global C, alf, bet, Q, isp, minras, marhras, pos, lin, fer, bliz, nachalo, now, szadi, delfer, bon, cnt 
	C = 10
	alf = 3
	bet = 1
	Q = 350
	isp = 0.4
	minras = 10000000000
	marhras = 0
	pos = [(r(10, w-10), r(10, h-10)) for i in range(C)]
	lin = {}
	for i in range(C):
		for j in range(i, C):
			lin[(i, j)] = 10
	fer = [[0.3 for i in range(C)] for j in range(C)]
	bliz = 100
	bon = C//2
	cnt = 5

	nachalo = 0
	now = 0
	szadi = [False]*C
	szadi[now] = True
	delfer = [[0 for i in range(C)] for j in range(C)]

restart()

stop = False
run = True
while run:
	delay(10)

	for event in get_events():
		if event.type == KEYDOWN:
			if event.key == K_q: run = False
			if event.key == K_s: stop = True
			if event.key == K_p: stop = False
			if event.key == K_7: alf -= 1
			if event.key == K_8: bet -= 1
			if event.key == K_9: alf += 1
			if event.key == K_0: bet += 1
			if event.key == K_r: restart()

	if not stop: update()

pygame.quit()





