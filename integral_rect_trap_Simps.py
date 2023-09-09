from mpmath import *
import matplotlib.pyplot as plt
from numpy.linalg import solve
from numpy import array

def left_rect(a : mpf, b : mpf, count_of_separation : mpf) -> mpf:
	step = (b-a)/count_of_separation
	result = 0
	for iterat in range(count_of_separation):
		result += step*func(a + iterat*step)
	return result

def right_rect(a : mpf, b : mpf, count_of_separation : mpf) -> mpf:
	step = (b-a)/count_of_separation
	result = 0
	for iterat in range(count_of_separation):
		result += step*func(a + (iterat+1)*step)
	return result

def average_rect(a : mpf, b : mpf, count_of_separation : mpf) -> mpf:
	step = (b-a)/count_of_separation
	result = 0
	for iterat in range(count_of_separation):
		result += step*func(a + iterat*step + step/2)
	return result

def trapezoid(a : mpf, b : mpf, count_of_separation : mpf) -> mpf:
	step = (b-a)/count_of_separation
	result = 0
	for iterat in range(count_of_separation):
		result += step*(func(a + iterat*step) + func(a + (iterat+1)*step))/2
	return result

def Simpsons(a : mpf, b : mpf, count_of_separation : mpf) -> mpf:
	step = (b-a)/count_of_separation
	result = 0
	for iterat in range(count_of_separation):
		result += step*(func(a + iterat*step) + func(a + (iterat+1)*step) + 4*func(a + iterat*step + step/2))/6
	return result

def get_moments(local_a : mpf, local_b : mpf, count_of_nodes : mpf) -> matrix:
	local_step = (local_b-local_a)/(count_of_nodes-1)
	weight_moment = matrix([0]*count_of_nodes)

	for id_node in range(count_of_nodes):
		for j in range(id_node+1):
			weight_moment[id_node] += ((-1)**j) * binomial(id_node, j) * ((b-local_a)**(j+1-bbeta) - (b-local_b)**(j+1-bbeta)) * (b**(id_node-j)) / (j+1-bbeta)

		#weight_moment[id_node] = quad(lambda x: x**(id_node)*weight_func(x), [a, b])

	return weight_moment

def Newton_Cotes(a : mpf, b : mpf, count_of_separation : mpf, count_of_nodes : mpf) -> mpf:
	step = (b-a)/count_of_separation
	local_step = step/(count_of_nodes-1)
	result = 0

	for iterat in range(count_of_separation):
		points = [a + iterat*step + cnt*local_step for cnt in range(count_of_nodes)]
		matrix_A = matrix([[points[i]**j for i in range(count_of_nodes)] for j in range(count_of_nodes)])

		weight_moment = get_moments(points[0], points[-1], count_of_nodes)
		coefs_A = lu_solve(matrix_A, weight_moment)
		for id_coef_A in range(count_of_nodes):
			result += coefs_A[id_coef_A]*func(points[id_coef_A])

	return result

def grafics(index : int) -> None:
	global err_rate_left_rect, err_rate_right_rect, err_rate_average_rect, err_rate_trapezoid, err_rate_Simpsons

	plt.ion()
	axis[0].clear()
	axis[1].clear()

	if index == 0:

		log_func = lambda x: log(x, 10)
		ax = [i+1 for i in range(max_count_of_separation_for_index_0)]

		axis[0].plot(ax, err_rate_left_rect, "g", markersize = 7, marker ="X", label = "Левый прямоугольник")
		axis[0].plot(ax, err_rate_right_rect, "r", markersize = 7, marker ="o", label = "Правый прямоугольник")
		axis[0].plot(ax, err_rate_average_rect, "k", markersize = 7, marker ="s", label = "Средний прямоугольник")
		axis[0].set_title("Абсолютная погрешность левого, правого и среднего прямоульных формул от эталонных формул")
		axis[0].set_xlabel("Количество разбиений")
		axis[0].set_ylabel("Абсолютная погрешность")
		axis[0].set_xticks(ax, ax)
		axis[0].grid()
		axis[0].legend()

		axis[1].plot(ax, list(map(log_func, err_rate_left_rect)), "g", markersize = 7, marker ="X", label = "Левый прямоугольник")
		axis[1].plot(ax, list(map(log_func, err_rate_right_rect)), "r", markersize = 7, marker ="o", label = "Правый прямоугольник")
		axis[1].plot(ax, list(map(log_func, err_rate_average_rect)), "k", markersize = 7, marker ="s", label = "Средний прямоугольник")
		axis[1].set_title("Степень погрешности левого, правого и среднего прямоульных формул от эталонных формул")
		axis[1].set_xlabel("Количество разбиений")
		axis[1].set_ylabel("Степень погрешности")
		axis[1].set_xticks(ax, ax)
		axis[1].grid()
		axis[1].legend()

	elif index == 1:

		log_func = lambda x: log(x, 10)
		ax = [i+1 for i in range(max_count_of_separation_for_index_1)]

		axis[0].plot(ax, err_rate_trapezoid, "g", markersize = 7, marker ="X", label = "Формула трапеции")
		axis[0].plot(ax, err_rate_Simpsons, "r", markersize = 7, marker ="o", label = "Формула Симпсона")
		axis[0].set_title("Абсолютная погрешность формулы трапеции и формулы Симпсона от эталонных формул")
		axis[0].set_xlabel("Количество разбиений")
		axis[0].set_ylabel("Абсолютная погрешность")
		axis[0].set_xticks(ax, ax)
		axis[0].grid()
		axis[0].legend()

		axis[1].plot(ax, list(map(log_func, err_rate_trapezoid)), "g", markersize = 7, marker ="X", label = "Формула трапеции")
		axis[1].plot(ax, list(map(log_func, err_rate_Simpsons)), "r", markersize = 7, marker ="o", label = "Формула Симпсона")
		axis[1].set_title("Степень погрешности формулы трапеции и формулы Симпсона от эталонных формул")
		axis[1].set_xlabel("Количество разбиений")
		axis[1].set_ylabel("Степень погрешности")
		axis[1].set_xticks(ax, ax)
		axis[1].grid()
		axis[1].legend()

	elif index == 2:

		log_func = lambda x: log(x, 10)
		ax = [i+1 for i in range(max_count_of_separation_for_index_2)]

		axis[0].plot(ax, err_rate_Newton_Cotes, "g", markersize = 7, marker ="X", label = "Формула Ньютона-Котеса")
		#axis[0].plot(ax, err_rate_Simpsons, "r", markersize = 7, marker ="o", label = "Формула Симпсона")
		axis[0].set_title("Абсолютная погрешность формулы Ньютона-Котеса от эталонных формул")
		axis[0].set_xlabel("Количество разбиений")
		axis[0].set_ylabel("Абсолютная погрешность")
		axis[0].set_xticks(ax, ax)
		axis[0].grid()
		axis[0].legend()

		axis[1].plot(ax, list(map(log_func, err_rate_Newton_Cotes)), "g", markersize = 7, marker ="X", label = "Формула Ньютона-Котеса")
		#axis[1].plot(ax, list(map(log_func, err_rate_Simpsons)), "r", markersize = 7, marker ="o", label = "Формула Симпсона")
		axis[1].set_title("Степень погрешности формулы Ньютона-Котеса от эталонных формул")
		axis[1].set_xlabel("Количество разбиений")
		axis[1].set_ylabel("Степень погрешности")
		axis[1].set_xticks(ax, ax)
		axis[1].grid()
		axis[1].legend()

	plt.draw()
	plt.ioff()

def key_event(event) -> None:
	global index, max_count_of_separation_for_index_0, max_count_of_separation_for_index_1, max_count_of_separation_for_index_2, \
		err_rate_left_rect, err_rate_right_rect, err_rate_average_rect, err_rate_trapezoid, err_rate_Simpsons, err_rate_Newton_Cotes


	key = getattr(event, 'key')

	if key == 'right': index = (index + 1)%3
	elif key == 'left': index = (index - 1)%3
	elif key == 'up': 
		if index == 0: 
			max_count_of_separation_for_index_0 += 1
			err_rate_left_rect += [abs(quad(func, [a, b]) - left_rect(a, b, max_count_of_separation_for_index_0))]
			err_rate_right_rect += [abs(quad(func, [a, b]) - right_rect(a, b, max_count_of_separation_for_index_0))]
			err_rate_average_rect += [abs(quad(func, [a, b]) - average_rect(a, b, max_count_of_separation_for_index_0))]
		elif index == 1: 
			max_count_of_separation_for_index_1 += 1
			err_rate_trapezoid += [abs(quad(func, [a, b]) - trapezoid(a, b, max_count_of_separation_for_index_1))]
			err_rate_Simpsons += [abs(quad(func, [a, b]) - Simpsons(a, b, max_count_of_separation_for_index_1))]
		elif index == 2:
			max_count_of_separation_for_index_2 += 1
			err_rate_Newton_Cotes += [abs(quad(full_func, [a, b]) - Newton_Cotes(a, b, max_count_of_separation_for_index_2, 3))]
	elif key == 'down': 
		if index == 0 and max_count_of_separation_for_index_0 > 1: 
			max_count_of_separation_for_index_0 -= 1
			err_rate_left_rect = err_rate_left_rect[:-1]
			err_rate_right_rect = err_rate_right_rect[:-1]
			err_rate_average_rect = err_rate_average_rect[:-1]
		elif index == 1 and max_count_of_separation_for_index_1 > 1: 
			max_count_of_separation_for_index_1 -= 1
			err_rate_trapezoid = err_rate_trapezoid[:-1]
			err_rate_Simpsons = err_rate_Simpsons[:-1]
		elif index == 2 and max_count_of_separation_for_index_2 > 1:
			max_count_of_separation_for_index_2 -= 1
			err_rate_Newton_Cotes = err_rate_Newton_Cotes[:-1] 


	grafics(index)

if __name__ == "__main__":

	func = lambda x: 3*cos(0.5*x)*exp(x/4) + 5*sin(2.5*x)*exp(-x/3) + 2*x
	#func = lambda x: x**2
	func_pol_0 = lambda x: 1
	func_pol_1 = lambda x: x+2
	func_pol_2 = lambda x: 2*x**2+x-1
	func_pol_3 = lambda x: x**3-3*x**2+2*x+5

	mp.dps = 20
	a, b = mpf(1), mpf(2)
	alpha, bbeta = mpf(0), mpf(0.25)
	max_count_of_separation_for_index_0 = 10
	max_count_of_separation_for_index_1 = 10
	max_count_of_separation_for_index_2 = 10
	index = 0

	weight_func = lambda x: 1/((b-x)**bbeta)
	full_func = lambda x: func(x)*weight_func(x)

	int_value_for_func = quad(func, [a, b])
	int_value_for_full_func = quad(full_func, [a, b])
	err_rate_left_rect = [abs(int_value_for_func - left_rect(a, b, i+1)) for i in range(max_count_of_separation_for_index_0)]
	err_rate_right_rect = [abs(int_value_for_func - right_rect(a, b, i+1)) for i in range(max_count_of_separation_for_index_0)]
	err_rate_average_rect = [abs(int_value_for_func - average_rect(a, b, i+1)) for i in range(max_count_of_separation_for_index_0)]
	err_rate_trapezoid = [abs(int_value_for_func - trapezoid(a, b, i+1)) for i in range(max_count_of_separation_for_index_1)]
	err_rate_Simpsons = [abs(int_value_for_func - Simpsons(a, b, i+1)) for i in range(max_count_of_separation_for_index_1)]
	err_rate_Newton_Cotes = [abs(int_value_for_full_func - Newton_Cotes(a, b, i+1, 3)) for i in range(max_count_of_separation_for_index_2)]

	fg, axis = plt.subplots(nrows= 2, ncols= 1, figsize=(15, 8))
	fg.subplots_adjust(bottom=0.1, left=0.06, right=0.98, top=0.95, hspace=0.3)
	fg.canvas.mpl_connect('key_release_event', key_event)

	grafics(index)

	plt.show()