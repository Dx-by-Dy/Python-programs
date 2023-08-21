from mpmath import *
import matplotlib.pyplot as plt
from numpy import arange

def get_PP(start : int, end : int, points : list[mpf], value_func : list[mpf]) -> list[mpf]:
	global PP

	if str(start) + ':' + str(end) in PP.keys(): return PP[str(start) + ':' + str(end)]
	if end - start == 1: 
		PP[str(start) + ':' + str(end)] = (value_func[end] - value_func[start])/(points[end] - points[start])
		return PP[str(start) + ':' + str(end)]

	PP[str(start) + ':' + str(end)] = (get_PP(start + 1, end, points, value_func) - get_PP(start, end - 1, points, value_func))/(points[end] - points[start])

	return PP[str(start) + ':' + str(end)]

def get_H_polinom(points : list, value_func : list) -> list[mpf]:
	global H_polinoms

	if len(points) in H_polinoms.keys(): return H_polinoms[len(points)]

	nd_pol = get_nodal_polinom(points[0:-1])

	for j in range(len(nd_pol)):
		nd_pol[j] = PP['0:' + str(len(points)-1)]*nd_pol[j]
		if j >= len(nd_pol) - len(H_polinoms[list(H_polinoms.keys())[-1]]):
			nd_pol[j] += H_polinoms[list(H_polinoms.keys())[-1]][j - (len(nd_pol) - len(H_polinoms[list(H_polinoms.keys())[-1]]))]

	H_polinoms[len(points)] = nd_pol

	return H_polinoms[len(points)]

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

	ax = arange(points[0] - 0.1, points[-1] + 0.1, 0.01)

	if index == 0:

		value_func = list(map(func, points))
		polinom = get_H_polinom(points, value_func)
		nodal_pol = get_nodal_polinom(points)

		H_pol_value = [value_polinom(polinom, i) for i in ax]
		Nodal_pol_value = [value_polinom(nodal_pol, i) for i in ax]

		axis.plot(ax, list(map(func, ax)), "g", label = "Исходная функция 3x - cos(x) - 1" if index_func == 0 else "Исходная функция |x|(3x - cos(x) - 1)")
		axis.plot(ax, H_pol_value, "--r", label = "Полином Ньютона")
		axis.plot(ax, Nodal_pol_value, "--k", label = "Узловой полином")
		axis.plot(points, list(map(func, points)), "ob", label = "Выбранные узлы (" + str(len(points)) + ")")
		axis.set_title("Исходная функция и полином Ньютона при равномерном распределении узлов")
		axis.grid()
		axis.legend()

	elif index == 1:

		value_func = list(map(func, points))
		polinom = get_H_polinom(points, value_func)

		meshgrid = 500

		ax2 = [points[0] + i*(points[-1] - points[0])/(meshgrid-1) for i in range(meshgrid)]

		differ = [log(abs(func(i) - value_polinom(polinom, i)), 10) for i in ax2]

		max_value_diff_fuct = max([abs(diff(func, i, len(points))) for i in ax2])/factorial(len(points))
		grid_polinom = get_nodal_polinom(points)
		max_limit_acc = log(max([abs(value_polinom(grid_polinom, i)) for i in ax2])*max_value_diff_fuct, 10)

		axis.plot(ax2, differ, "g", label = "Равномерное распределение")
		axis.plot(ax2, [max_limit_acc for i in ax2], "--g", linewidth = 2, label = "Оценка погрешности для равномерного распределения")
		axis.set_title("Степень абсолютной погрешности при равномерном распределении узлов (" + str(len(points)) + ")")
		axis.grid()
		axis.legend()

	plt.show()

def key_event(event) -> None:

	global index, index_func, PP
	global points, value_func, H_polinoms
	global func

	key = getattr(event, 'key')

	if key == 'right': index = (index + 1)%2
	elif key == 'left': index = (index - 1)%2
	elif key == 'up': 
		points += [points[-1] + step]
		value_func += [func(points[-1])]
		get_PP(0, len(points)-1, points, value_func)

	elif key == 'down' and len(points) > 2: 
		points = points[0:-1]
		value_func = value_func[0:-1]
		get_PP(0, len(points), points, value_func)

	elif key == 'shift': 
		if index_func == 0: 
			func = lambda x: abs(x)*(3*x - cos(x) - 1)
			#func = lambda x: abs(x)/(1+25*power(x, 2))

			points = [a + i*step for i in range(2)]
			value_func = [func(i) for i in points]

			PP = {}
			get_PP(0, len(points)-1, points, value_func)
			H_polinoms = {1 : [value_func[0]]}

		else: 
			func = lambda x: 3*x - cos(x) - 1
			#func = lambda x: 1/(1+25*power(x, 2))

			points = [a + i*step for i in range(2)]
			value_func = [func(i) for i in points]

			PP = {}
			get_PP(0, len(points)-1, points, value_func)
			H_polinoms = {1 : [value_func[0]]}

		index_func = (index_func + 1)%2

	grafics(index)


if __name__ == "__main__":

	func = lambda x: 3*x - cos(x) - 1
	#func = lambda x: 1/(1+25*power(x, 2))
	index_func = 0
	index = 0

	a, b = mpf(-1), mpf(1)
	step = mpf(0.25)

	points = [a + i*step for i in range(2)]
	value_func = [func(i) for i in points]

	PP = {}
	get_PP(0, len(points)-1, points, value_func)
	H_polinoms = {1 : [value_func[0]]}

	mp.dps = 20

	fg, axis = plt.subplots(1, 1, figsize=(15, 8))
	fg.subplots_adjust(bottom=0.06, left=0.05, right=0.95, top=0.95)
	fg.canvas.mpl_connect('key_release_event', key_event)

	grafics(index)
	'''

	func = lambda x: 3*x - cos(x) - 1

	a, b = -1, 1
	step = 0.25

	points = [a + i*step for i in range(2)]
	value_func = [func(i) for i in points]

	PP = {}
	get_PP(0, len(points)-1, points, value_func)
	H_polinoms = {1 : [value_func[0]]}

	for i in range(3):

		points += [points[-1] + step]
		value_func += [func(points[-1])]
		get_PP(0, len(points)-1, points, value_func)

		print(get_H_polinom(points, value_func))
	'''
