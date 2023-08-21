import pygame
from random import randint as r

pygame.init()

SCREEN_SIZE = (800, 500)
win = pygame.display.set_mode(SCREEN_SIZE, pygame.RESIZABLE)
pygame.display.set_caption('ball physics')

BACKGROUND_COLOR = (0, 0, 0)
BLACK = (0, 0, 0)
GREY = (100, 100, 100)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

COLORS = [GREY, RED, WHITE, GREEN, BLUE]

class Circle:
	def __init__(self, pos, x_vel = 0, y_vel = 0, color = GREY, radius = 10, mass = 1, recover_coef = 1):
		self.color = color
		self.pos_x, self.pos_y = pos
		self.radius = radius
		self.x_vel = x_vel
		self.y_vel = y_vel
		self.recover_coef = recover_coef
		self.mass = mass

	def set_vel(self, x_vel, y_vel):
		self.x_vel = x_vel
		self.y_vel = y_vel

	def set_pos(self, pos_x, pos_y):
		self.pos_x = pos_x
		self.pos_y = pos_y

def dist(pos_x1, pos_y1, pos_x2, pos_y2) -> float:
	return ((pos_x1 - pos_x2)**2 + (pos_y1 - pos_y2)**2)**0.5

def normalize_vec(x_coor, y_coor) -> tuple:
	norm = (x_coor**2 + y_coor**2)**0.5
	return (x_coor/norm, y_coor/norm)

def scalar_prod(pos_x1, pos_y1, pos_x2, pos_y2) -> float:
	return pos_x1 * pos_x2 + pos_y1 * pos_y2

def collision(Circles) -> None:
	count_of_circles = len(Circles)

	for circle_1 in range(count_of_circles):
		for circle_2 in range(circle_1 + 1, count_of_circles):

			pos_x1, pos_y1, pos_x2, pos_y2 = Circles[circle_1].pos_x, Circles[circle_1].pos_y, Circles[circle_2].pos_x, Circles[circle_2].pos_y
			vel_x1, vel_y1, vel_x2, vel_y2 = Circles[circle_1].x_vel, Circles[circle_1].y_vel, Circles[circle_2].x_vel, Circles[circle_2].y_vel
			sum_rad = Circles[circle_1].radius + Circles[circle_2].radius
			mass_1, mass_2 = Circles[circle_1].mass, Circles[circle_2].mass

			if dist(pos_x1, pos_y1, pos_x2, pos_y2) < sum_rad:
				basic_vec_1 = normalize_vec(pos_x2 - pos_x1, pos_y2 - pos_y1)
				basic_vec_2 = (-basic_vec_1[1], basic_vec_1[0])

				y_proj_coef_1 = scalar_prod(vel_x1, vel_y1, basic_vec_2[0], basic_vec_2[1])
				y_proj_1 = (-basic_vec_1[1] * y_proj_coef_1, basic_vec_1[0] * y_proj_coef_1)
				y_proj_coef_2 = scalar_prod(vel_x2, vel_y2, basic_vec_2[0], basic_vec_2[1])
				y_proj_2 = (-basic_vec_1[1] * y_proj_coef_2, basic_vec_1[0] * y_proj_coef_2)

				x_proj_coef_1 = scalar_prod(vel_x1, vel_y1, basic_vec_1[0], basic_vec_1[1])
				x_proj_coef_2 = scalar_prod(vel_x2, vel_y2, basic_vec_1[0], basic_vec_1[1])

				mass_coef_vel_1 = ((mass_1 - mass_2) * x_proj_coef_1 + 2 * mass_2 * x_proj_coef_2)/(mass_1 + mass_2)
				mass_coef_vel_2 = ((mass_2 - mass_1) * x_proj_coef_2 + 2 * mass_1 * x_proj_coef_1)/(mass_1 + mass_2)

				x_proj_1 = (basic_vec_1[0] * mass_coef_vel_1, basic_vec_1[1] * mass_coef_vel_1)
				x_proj_2 = (basic_vec_1[0] * mass_coef_vel_2, basic_vec_1[1] * mass_coef_vel_2)

				vel_circle_1 = (x_proj_1[0] + y_proj_1[0], x_proj_1[1] + y_proj_1[1])
				vel_circle_2 = (x_proj_2[0] + y_proj_2[0], x_proj_2[1] + y_proj_2[1])

				Circles[circle_1].set_vel(vel_circle_1[0], vel_circle_1[1])
				Circles[circle_2].set_pos(pos_x1 + basic_vec_1[0] * sum_rad, pos_y1 + basic_vec_1[1] * sum_rad)
				Circles[circle_2].set_vel(vel_circle_2[0], vel_circle_2[1])

def movement(Circles, FPF) -> None:
	for vel_iter in range(FPF):
		for circle in Circles:

			circle.set_pos(circle.pos_x + circle.x_vel / FPF, circle.pos_y + circle.y_vel/ FPF)
			circle.set_vel(circle.x_vel, circle.y_vel + GRAVITY_COEF / FPF)

			if circle.pos_x < circle.radius:
				circle.set_pos(circle.radius, circle.pos_y)
				circle.set_vel(-circle.x_vel * circle.recover_coef, circle.y_vel)

			if circle.pos_x > SCREEN_SIZE[0] - circle.radius:
				circle.set_pos(SCREEN_SIZE[0] - circle.radius, circle.pos_y)
				circle.set_vel(-circle.x_vel * circle.recover_coef, circle.y_vel)

			if circle.pos_y > SCREEN_SIZE[1] - circle.radius:
				circle.set_pos(circle.pos_x, SCREEN_SIZE[1] - circle.radius)
				circle.set_vel(circle.x_vel, -circle.y_vel * circle.recover_coef)

			if circle.pos_y < circle.radius:
				circle.set_pos(circle.pos_x, circle.radius)
				circle.set_vel(circle.x_vel, -circle.y_vel * circle.recover_coef)

		collision(Circles)

def update() -> None:
	win.fill(BACKGROUND_COLOR)

	movement(Circles, FPF)

	for circle in Circles:
		pygame.draw.circle(win, circle.color, (circle.pos_x, circle.pos_y), circle.radius)

	pygame.display.update()

RUN = True
GRAVITY_COEF = 0.1
FPF = 50

'''
Circles = [Circle(color = GREY, pos = (100, 100), y_vel = 1),
			Circle(color = GREY, pos = (100, 300), y_vel = -1), 
			Circle(color = GREY, pos = (200, 200), x_vel = -1)]
'''
Circles = []
for i in range(10):
	Circles += [Circle(color = COLORS[r(0, len(COLORS) - 1)], pos = (r(10, SCREEN_SIZE[0]) - 10, r(10, SCREEN_SIZE[1] - 10)), x_vel = r(-100, 100)/10, y_vel = r(-10, 10)/10)]

while RUN:
	pygame.time.delay(5)

	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_q: RUN = False
		if event.type == pygame.QUIT: RUN = False
		if event.type == pygame.VIDEORESIZE: SCREEN_SIZE = event.size
	update()

pygame.quit()