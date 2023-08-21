import pygame
from pygame.event import get as get_events
from pygame import display, KEYDOWN, K_q, MOUSEBUTTONDOWN
from pygame.time import delay
from pygame.draw import rect, polygon
import ctypes

pygame.init()
win = display.set_mode((0, 0), pygame.FULLSCREEN)

user32 = ctypes.windll.user32
w = user32.GetSystemMetrics(0)
h = user32.GetSystemMetrics(1)

def update():
	win.fill((0, 0, 0))
	display.update()

run = True
while run:
	delay(100)

	for event in get_events():
		if event.type == KEYDOWN:
			if event.key == K_q: run = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1: pass

	keys = pygame.key.get_pressed()
	if keys[K_q]: pass
	update()

pygame.quit()
