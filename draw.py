import pygame
import ctypes

pygame.init()
win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

user32 = ctypes.windll.user32
screen_size = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

def update():
	win.fill((255, 255, 255))

	for i in range(1, screen_size[0]//cof + 1):
		i *= cof
		pygame.draw.line(win, (0, 0, 0), (i, 0), (i, screen_size[1] - 68))

	for i in range(1, screen_size[1]//cof + 1):
		i *= cof
		if screen_size[1] - i >= 68: pygame.draw.line(win, (0, 0, 0), (0, i), (screen_size[0], i))

	for dr in draw: pygame.draw.rect(win, dr[2], ((dr[0] - cx)*cof + 1, (dr[1] - cy)*cof + 1, cof - 1, cof - 1))

	pygame.draw.rect(win, (255, 255, 255), (0, screen_size[1] - 68, screen_size[0], 68))

	for i in range(len(color)):
		cl = color[i]
		i = i*48 + (i+1)*20
		pygame.draw.rect(win, cl, (i, screen_size[1] - 58, 48, 48))
		pygame.draw.rect(win, (0, 0, 0), (i - 2, screen_size[1] - 60, 50, 50), 2)

	pygame.display.update()

def tauch(pm):
	global idx_color

	pm[0] //= 1
	pm[1] //= 1
	if pm[1] < screen_size[1] - 68: draw.append([(pm[0] - (pm[0]%cof))//cof + cx, (pm[1] - (pm[1]%cof))//cof + cy, color[idx_color]])
	else:
		if pm[1] in range(screen_size[1] - 58, screen_size[1] - 10):
			for i in range(len(color)):
				d = i
				i = i*48 + (i+1)*20
				if pm[0] in range(i, i+48): idx_color = d 

draw = []
cx, cy = 0, 0
run = True
color = [(0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255), (139, 69, 19), (139, 137, 137), (238, 64, 0), (122, 55, 139)]
idx_color = 0
cof = 128
while run:
	pygame.time.delay(10)

	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_q: run = False
			if event.key == pygame.K_UP and cy - ((screen_size[1] - 68)//cof) > 0:
				if (screen_size[1] - 68) % cof > 0: cy -= (screen_size[1] - 68)//cof + 1
				else: cy -= (screen_size[1] - 68)//cof
			elif event.key == pygame.K_DOWN:
				if (screen_size[1] - 68) % cof > 0: 
					if (cof == 8 and cy < (screen_size[1] - 68)//cof + 1) or (cof == 16 and cy < 3*((screen_size[1] - 68)//cof + 1)) or (cof == 32 and cy < 7*((screen_size[1] - 68)//cof + 1)) or (cof == 64 and cy < 15*((screen_size[1] - 68)//cof + 1)) or (cof == 128 and cy < 28*((screen_size[1] - 68)//cof + 1)): cy += (screen_size[1] - 68)//cof + 1
				else: 
					if (cof == 8 and cy < (screen_size[1] - 68)//cof) or (cof == 16 and cy < 3*((screen_size[1] - 68)//cof)) or (cof == 32 and cy < 7*((screen_size[1] - 68)//cof)) or (cof == 64 and cy < 15*((screen_size[1] - 68)//cof)) or (cof == 128 and cy < 28*((screen_size[1] - 68)//cof)): cy += (screen_size[1] - 68)//cof
			elif event.key == pygame.K_LEFT and cx - (screen_size[0]//cof) > 0:
				if screen_size[0] % cof > 0: cx -= screen_size[0]//cof + 1
				else: cx -= screen_size[0]//cof
			elif event.key == pygame.K_RIGHT:
				if screen_size[0] % cof > 0: 
					if (cof == 8 and cx < screen_size[0]//cof + 1) or (cof == 16 and cx < 3*(screen_size[0]//cof + 1)) or (cof == 32 and cx < 7*(screen_size[0]//cof + 1)) or (cof == 64 and cx < 15*(screen_size[0]//cof + 1)) or (cof == 128 and cx < 31*(screen_size[0]//cof + 1)): cx += screen_size[0]//cof + 1
				else: 
					if (cof == 8 and cx < screen_size[0]//cof) or (cof == 16 and cx < 3*(screen_size[0]//cof)) or (cof == 32 and cx < 7*(screen_size[0]//cof)) or (cof == 64 and cx < 15*(screen_size[0]//cof)) or (cof == 128 and cx < 31*(screen_size[0]//cof)): cx += screen_size[0]//cof
		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1: tauch(list(pygame.mouse.get_pos()))
			elif event.button == 4 and cof < 128: 
				cof *= 2
				cx *= 2
				cy *= 2
				for dr in draw:
					dr[0] += cx
					dr[1] += cy
			elif event.button == 5 and cof > 4:
				cof //= 2
				cx = 0
				cy = 0

	update()

pygame.quit()