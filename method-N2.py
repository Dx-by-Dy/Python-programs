from mpmath import *
import matplotlib.pyplot as plt
from numpy import arange, array, linalg
from random import vonmisesvariate
from SLAE import Gauss_method

accuracy = 1e-5
mp.dps = abs(log(accuracy, 10)) + 1

def iterat(start_value, accuracy, list_num_steps = []):

	point = start_value
	old_point = [-inf, -inf]

	diff_func1_x = lambda p0, p1: mpf(diff(lambda x: 5*cos(p1+0.5)+x-0.8, p0))
	diff_func1_y = lambda p0, p1: mpf(diff(lambda y: 5*cos(y+0.5)+p0-0.8, p1))
	diff_func2_x = lambda p0, p1: mpf(diff(lambda x: 5*sin(x)-2*p1-1.6, p0))
	diff_func2_y = lambda p0, p1: mpf(diff(lambda y: 5*sin(p0)-2*y-1.6, p1))

	cnt_steps = 0

	while sqrt(power(point[0] - old_point[0], 2) + power(point[1] - old_point[1], 2)) > accuracy:

		A = array([[diff_func1_x(point[0], point[1]), diff_func1_y(point[0], point[1])], [diff_func2_x(point[0], point[1]), diff_func2_y(point[0], point[1])]], dtype=mpf)
		b = array([[-fun1(point[0], point[1])], [-fun2(point[0], point[1])]], dtype=mpf)

		try: res = Gauss_method(A, b)
		except ZeroDivisionError: pass

		del_x, del_y = res[0][0], res[1][0]
		old_point = point
		point = [point[0] + del_x, point[1] + del_y]
		cnt_steps += 1

		if cnt_steps > 100:
			return [None, None]

	list_num_steps += [cnt_steps]

	return [mpf(point[0]), mpf(point[1])]

def fun1(x, y):
	return 5*cos(y + 0.5) + x - 0.8

def fun2(x, y):
	return 5*sin(x) - 2*y - 1.6

def grafics() -> None:

	ax = arange(-6, 6, 0.01)
	ay = arange(-6, 6, 0.01)

	func1 = lambda y: 0.8 - 5*cos(y + 0.5)
	func2 = lambda x: 5*sin(x)/2 - 0.8

	value_func1 = [func1(y) for y in ay]
	value_func2 = [func2(x) for x in ax]
	Ox = [0 for x in ax]
	Oy = [0 for y in ay]

	start_x, start_y = -0.13, -0.86
	list_num_steps = []
	coord_root_x, coord_root_y = [0.85, -0.42, 5.10, 2.11, 4.05, -3.48, -2.97], [1.08, -1.82, -3.10, 1.33, -2.77, 0.04, -1.21]
	coord_x, coord_y = [], []
	color = []
	
	for i in range(21):
		for j in range(21):
			res = iterat([-5 + i*0.5, -5 + j*0.5], accuracy, list_num_steps)
			if res != [None, None]:
				for k in range(7):
					if abs(coord_root_x[k] - res[0]) + abs(coord_root_y[k] - res[1]) < 0.1: 
						color += [k]
						break
			else: 
				color += [-1] 

			coord_x += [-5 + i*0.5]
			coord_y += [-5 + j*0.5]

		#rnd = vonmisesvariate(0, 0)
		#start_x = -0.13 + i*0.01*cos(rnd)
		#start_y = -0.86 + i*0.01*sin(rnd)
		#nprint(res)

	plt.subplots(figsize=(8, 8))

	plt.subplot(111)
	#plt.plot(value_func1, ay, "b", label = "5cos(y + 0.5) + x - 0.8 = 0")
	#plt.plot(ax, value_func2, "r", label = "5sin(x) - 2y - 1.6 = 0")
	plt.plot(ax, Ox, "--r")
	plt.plot(Oy, ay, "--r")


	for i in range(7):
		if i == 0: plt.plot(coord_root_x[i], coord_root_y[i], "Xg")
		if i == 1: plt.plot(coord_root_x[i], coord_root_y[i], "X", color = "sienna")
		if i == 2: plt.plot(coord_root_x[i], coord_root_y[i], "Xy")
		if i == 3: plt.plot(coord_root_x[i], coord_root_y[i], "Xc")
		if i == 4: plt.plot(coord_root_x[i], coord_root_y[i], "Xm")
		if i == 5: plt.plot(coord_root_x[i], coord_root_y[i], "Xk")
		if i == 6: plt.plot(coord_root_x[i], coord_root_y[i], "X", color = "lime")

	
	for i in range(len(color)):
		if color[i] == -1: plt.plot(coord_x[i], coord_y[i], "or", alpha=0.3)
		elif color[i] == 0: plt.plot(coord_x[i], coord_y[i], "og", alpha=0.8) 
		elif color[i] == 1: plt.plot(coord_x[i], coord_y[i], "o", color = "sienna", alpha=0.8) 
		elif color[i] == 2: plt.plot(coord_x[i], coord_y[i], "oy", alpha=0.8) 
		elif color[i] == 3: plt.plot(coord_x[i], coord_y[i], "oc", alpha=0.8) 
		elif color[i] == 4: plt.plot(coord_x[i], coord_y[i], "om", alpha=0.8) 
		elif color[i] == 5: plt.plot(coord_x[i], coord_y[i], "ok", alpha=0.6) 
		elif color[i] == 6: plt.plot(coord_x[i], coord_y[i], "o", color = "lime", alpha=0.6)
	
	
	plt.plot([], [], "X", color = "grey", label = "Корни")
	plt.plot([], [], "o", color = "grey", label = "Начальные точки")
	plt.title("Зависимость схождения к корню от начальной точки")
	plt.grid()
	plt.legend()
	

	"""plt.subplot(122)
	plt.plot(sorted([sqrt(power(-0.13 - coord_x[i], 2) + power(-0.86 - coord_y[i], 2)) for i in range(len(list_num_steps))]), list_num_steps)
	plt.title("Зависимость количества шагов от выбора начальной точки")
	plt.xlabel("Расстояние до решения")"""

	plt.subplots_adjust(bottom=0.1, left=0.05, right=0.95, top=0.90)
	plt.show()

grafics()