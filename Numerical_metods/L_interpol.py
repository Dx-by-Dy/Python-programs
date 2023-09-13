from mpmath import *
import matplotlib.pyplot as plt
from numpy import arange

def get_L_polinom(points : list, value_func : list) -> list[mpf]:

	res = [0 for i in range(len(points))]

	for idx_point in range(len(points)):

		if idx_point != 0: start = 0
		else: start = 1

		li = [1, -points[start]]
		coef = points[idx_point] - points[start]

		for i in range(len(points)):

			if i != idx_point and i != start:

				lst = li + [0]
				for j in range(1, len(lst)):
					lst[j] += -points[i] * li[j-1]

				coef *= points[idx_point] - points[i]
				li = lst

		coef = value_func[idx_point]/coef

		for i in range(len(points)):
			res[i] += li[i]*coef

	return res

def get_nodal_polinom(points : list) -> list[mpf]:

	pol = [1, -points[0]]

	for i in range(1, len(points)):

		lst = pol + [0]
		for j in range(1, len(lst)):
			lst[j] += -points[i] * pol[j-1]

		pol = lst

	return pol

def value_polinom(polinom, arg : mpf) -> mpf:

	res = 0
	for i in range(len(polinom)):
		res += polinom[i] * power(arg, len(polinom) - i - 1)

	return res

def grafics(index : int) -> None:

	axis.clear()

	ax = arange(a - 0.1, b + 0.1, 0.01)

	points = [a + i*(b - a)/(count_points-1) for i in range(count_points)]
	points2 = [0.5*((b-a)*cos((2*i + 1)*pi/(2*count_points)) + b + a) for i in range(count_points)]

	if index == 0:

		value_func = list(map(func, points))
		polinom = get_L_polinom(points, value_func)
		nodal_pol = get_nodal_polinom(points)

		L_pol_value = [value_polinom(polinom, i) for i in ax]
		Nodal_pol_value = [value_polinom(nodal_pol, i) for i in ax]

		axis.plot(ax, list(map(func, ax)), "g", label = "Исходная функция 3x - cos(x) - 1" if index_func == 0 else "Исходная функция |x|(3x - cos(x) - 1)")
		axis.plot(ax, L_pol_value, "--r", label = "Полином Лагранжа")
		axis.plot(ax, Nodal_pol_value, "--k", label = "Узловой полином")
		axis.plot(points, list(map(func, points)), "ob", label = "Выбранные узлы (" + str(count_points) + ")")
		axis.set_title("Исходная функция и полином Лагранжа при равномерном распределении узлов")
		axis.grid()
		axis.legend()

	elif index == 1:

		value_func2 = list(map(func, points2))
		polinom2 = get_L_polinom(points2, value_func2)
		nodal_pol2 = get_nodal_polinom(points2)

		L_pol_value2 = [value_polinom(polinom2, i) for i in ax]
		Nodal_pol_value2 = [value_polinom(nodal_pol2, i) for i in ax]

		axis.plot(ax, list(map(func, ax)), "g", label = "Исходная функция 3x - cos(x) - 1" if index_func == 0 else "Исходная функция |x|(3x - cos(x) - 1)")
		axis.plot(ax, L_pol_value2, "--r", label = "Полином Лагранжа")
		axis.plot(ax, Nodal_pol_value2, "--k", label = "Узловой полином")
		axis.plot(points2, list(map(func, points2)), "ob", label = "Выбранные узлы (" + str(count_points) + ")")
		axis.set_title("Исходная функция и полином Лагранжа при распределении узлов на основе полинома Чебышева")
		axis.grid()
		axis.legend()

	elif index == 2:

		value_func = list(map(func, points))
		value_func2 = list(map(func, points2))

		polinom = get_L_polinom(points, value_func)
		polinom2 = get_L_polinom(points2, value_func2)

		if count_points >= 13: meshgrid = 1000
		else: meshgrid = 500

		ax2 = [a + i*(b - a)/(meshgrid-1) for i in range(meshgrid)]

		differ = [log(abs(func(i) - value_polinom(polinom, i)), 10) for i in ax2]
		differ2 = [log(abs(func(i) - value_polinom(polinom2, i)), 10) for i in ax2]

		max_value_diff_fuct = max([abs(diff(func, i, count_points)) for i in ax2])/factorial(count_points)

		grid_polinom = get_nodal_polinom(points)

		max_limit_acc_1 = log(max([abs(value_polinom(grid_polinom, i)) for i in ax2])*max_value_diff_fuct, 10)
		max_limit_acc_2 = log(max_value_diff_fuct*power(b-a,count_points)/power(2, 2*count_points - 1), 10)

		axis.plot(ax2, differ, "g", label = "Равномерное распределение")
		axis.plot(ax2, differ2, "r", label = "Распределении на основе полинома Чебышева")
		axis.plot(ax2, [max_limit_acc_1 for i in ax2], "--g", linewidth = 2, label = "Оценка погрешности для равномерного распределения")
		axis.plot(ax2, [max_limit_acc_2 for i in ax2], "--r", linewidth = 2, label = "Оценка погрешности для \"Чебышевского\" распределения")
		axis.set_title("Степень абсолютной погрешности при различном распределении узлов (" + str(count_points) + ")")
		axis.grid()
		axis.legend()

	plt.show()

def key_event(event) -> None:

	global index, index_func
	global count_points
	global func

	key = getattr(event, 'key')

	if key == 'right': index = (index + 1)%3
	elif key == 'left': index = (index - 1)%3
	elif key == 'up': count_points += 1
	elif key == 'down' and count_points > 2: count_points -= 1
	elif key == 'shift': 
		if index_func == 0: 
			func = lambda x: abs(x)*(3*x - cos(x) - 1)
			#func = lambda x: abs(x)/(1+25*power(x, 2))
		else: 
			func = lambda x: 3*x - cos(x) - 1
			#func = lambda x: 1/(1+25*power(x, 2))
		index_func = (index_func + 1)%2

	grafics(index)


if __name__ == "__main__":

	func = lambda x: 3*x - cos(x) - 1
	#func = lambda x: 1/(1+25*power(x, 2))
	index_func = 0
	index = 0

	a, b = -1, 1
	count_points = 5

	mp.dps = 20

	fg, axis = plt.subplots(1, 1, figsize=(15, 8))
	fg.subplots_adjust(bottom=0.06, left=0.05, right=0.95, top=0.95)
	fg.canvas.mpl_connect('key_release_event', key_event)

	grafics(index)

