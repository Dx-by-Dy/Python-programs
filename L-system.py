import pygame
from pygame.event import get as get_events
from pygame import display, KEYDOWN, K_q, K_SPACE, K_LEFT, K_RIGHT, K_UP, K_DOWN, K_s, K_w
from pygame.time import delay
from pygame.draw import line
import ctypes

pygame.init()
win = display.set_mode((0, 0), pygame.FULLSCREEN)

user32 = ctypes.windll.user32
w = user32.GetSystemMetrics(0)
h = user32.GetSystemMetrics(1)

def update():
	global vect, S, x, y
	
	win.fill((0, 0, 0))
	x, y = w//2 + vx, h//2 + vy
	vect = 0

	for i in S:
		if i == '+': vect+=1
		elif i == '-': vect-=1
		elif i == 'F':
			if vect%4 == 0: 
				line(win, (255, 255, 255), (x, y), (x+ln, y))
				x += ln
			elif vect%4 == 1: 
				line(win, (255, 255, 255), (x, y), (x, y+ln))
				y += ln
			elif vect%4 == 2: 
				line(win, (255, 255, 255), (x, y), (x-ln, y))
				x -= ln
			elif vect%4 == 3: 
				line(win, (255, 255, 255), (x, y), (x, y-ln))
				y -= ln

	display.update()

run = True
vect = 0
vx, vy = 0, 0
ln = 10
S = 'F'
dct = {'+' : '+', '-' : '-', 'F' : 'FF++FF+FF+FF'} # '+F-F-F+', '-F+FF+F-', 'FF++FF+FF+FF', 'FF--F+F+FF', 'FF-+F+F++FF', 'F+F-FFF++FFF-F+F'
while run:

	for event in get_events():
		if event.type == KEYDOWN:
			if event.key == K_SPACE:
				t = ''
				for i in S:
					t += dct[i]
				S = t
				update()
			if event.key == K_q: run = False
			if event.key == K_s and ln-1 > 0: 
				ln -= 1
				update()
			if event.key == K_w:
				ln += 1
				update()

	keys = pygame.key.get_pressed()
	if keys[K_LEFT] or keys[K_RIGHT] or keys[K_UP] or keys[K_DOWN]: update()
	if keys[K_LEFT]: vx += 10
	if keys[K_RIGHT]: vx -= 10
	if keys[K_UP]: vy += 10
	if keys[K_DOWN]: vy -= 10

pygame.quit()