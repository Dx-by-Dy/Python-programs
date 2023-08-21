import pygame
from random import randint as rand
import ctypes
user32 = ctypes.windll.user32
w = user32.GetSystemMetrics(0)
h = user32.GetSystemMetrics(1)
pygame.init()
win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
x, y, run = 0, 0, True
while run:
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN and event.key == pygame.K_q: run = False
	r = rand(0, 100)
	if r in range(0, 1): a, b, c, d, e, f = 0, 0, 0, 0.16, 0, 0
	elif r in range(1, 80): a, b, c, d, e, f = 0.85, 0.04, -0.06, 0.85, 0, 1.6
	elif r in range(80, 90): a, b, c, d, e, f = 0.2, -0.26, 0.23, 0.22, 0, 1.6
	elif r in range(90, 101): a, b, c, d, e, f = -0.15, 0.28, 0.26, 0.24, 0, 0.44
	x = a*x + b*y + e
	y = c*x + d*y + f
	pygame.draw.rect(win, (0, 255, 0), ((x*90)+w//2, (y*90), 1, 1))
	pygame.display.update()
pygame.quit()