from mpmath import *
import matplotlib.pyplot as plt
from numpy import arange
from L_interpol import get_L_polinom
from SLAE import Gauss_method
from numpy import array

def get_lin_splain(points : list[mpf], value_func : list[mpf]) -> None:
	global lin_pols
	lin_pols = {}

	for i in range(len(points)-1):
		pol = get_L_polinom([points[j] for j in range(i, i + 2)], [value_func[j] for j in range(i, i + 2)])
		lin_pols[i] = pol

def get_sq_splain(points : list[mpf], value_func : list[mpf], diff_value_func : mpf) -> None:
	global sq_pols
	sq_pols = {}

	for i in range(len(points)-1):
		pol = get_L_polinom([points[j] for j in range(i, i + 2)], [value_func[j] for j in range(i, i + 2)])
		nodal_pol = get_nodal_polinom([points[j] for j in range(i, i + 2)])

		coef = (diff_value_func - value_polinom(diff_polinom(pol), points[i]))/value_polinom(diff_polinom(nodal_pol), points[i])

		for j in range(len(nodal_pol)):
			nodal_pol[j] = nodal_pol[j]*coef

		sq_pols[i] = sum_polinoms(pol, nodal_pol)
		diff_value_func = value_polinom(diff_polinom(sq_pols[i]), points[i + 1])

def get_cub_splain(points : list[mpf], value_func : list[mpf], diff_value_func : list[mpf]) -> None:
	global cub_pols
	cub_pols = {}

	for i in range(len(points)-1):
		pol = get_L_polinom([points[j] for j in range(i, i + 2)], [value_func[j] for j in range(i, i + 2)])
		nodal_pol_1 = get_nodal_polinom([points[j] for j in range(i, i + 2)])
		nodal_pol_2 = get_nodal_polinom([points[j] for j in range(i, i + 1)])

		coef1 = (diff_value_func[0] - value_polinom(diff_polinom(pol), points[i]))/value_polinom(diff_polinom(nodal_pol_1), points[i])
		coef2 = ((diff_value_func[1] - 2*coef1)/value_polinom(diff_polinom(diff_polinom(prod_polinoms(nodal_pol_1, nodal_pol_2))), points[i]))

		for j in range(len(nodal_pol_2)):
			nodal_pol_2[j] = nodal_pol_2[j]*coef2
		nodal_pol_2[-1] += coef1

		polin = prod_polinoms(nodal_pol_1, nodal_pol_2)
		cub_pols[i] = sum_polinoms(pol, polin)

		diff_value_func[0] = value_polinom(diff_polinom(cub_pols[i]), points[i+1])
		diff_value_func[1] = value_polinom(diff_polinom(diff_polinom(cub_pols[i])), points[i+1])

def get_natural_cub_splain(points : list[mpf], value_func : list[mpf]) -> None:
	global a, b

	step = mpf((b - a)/(count_points_cub_interp-1))

	A = array([[0 for i in range(count_points_cub_interp-2)] for j in range(count_points_cub_interp-2)], dtype = mpf)
	for i in range(count_points_cub_interp-2):
		for j in  range(count_points_cub_interp-2):
			if i == j: A[i, j] = 4*step
			if abs(i-j) == 1: A[i, j] = step

	gamma = array([[6*((value_func[i+1] - 2*value_func[i] + value_func[i-1])/step)] for i in range(1, count_points_cub_interp-1)], dtype = mpf)
	res = Gauss_method(A.copy(), gamma.copy())

	diff_value_func = (value_func[1] - value_func[0])/step - res[0, 0]*step/6
	get_cub_splain(points, value_func, [diff_value_func, 0])

def prod_polinoms(polinom1 : list[mpf], polinom2 : list[mpf]) -> list[mpf]:

	len_pol_1 = len(polinom1)
	len_pol_2 = len(polinom2)
	res_len = len_pol_2 + len_pol_1 - 1

	res = [0 for i in range(res_len)]

	for i in range(len_pol_1):
		pol = [0 for i in range(res_len)]
		for j in range(len_pol_2):
			pol[res_len - (len_pol_1-i-1) - (len_pol_2-j-1) - 1] += polinom1[i]*polinom2[j]
		res = sum_polinoms(res, pol)

	return res

def sum_polinoms(polinom1 : list[mpf], polinom2 : list[mpf]) -> list[mpf]:

	len_pol_1 = len(polinom1)
	len_pol_2 = len(polinom2)
	max_len_pol = max(len_pol_1, len_pol_2)
	res = [0 for i in range(max_len_pol)]

	for i in range(max_len_pol):
		if i >= max_len_pol - len_pol_1: res[i] += polinom1[i - max_len_pol + len_pol_1]
		if i >= max_len_pol - len_pol_2: res[i] += polinom2[i - max_len_pol + len_pol_2]

	for i in range(max_len_pol):
		if res[i] != 0:
			res = res[i:max_len_pol]
			break

	return res

def get_nodal_polinom(points : list) -> list[mpf]:

	pol = [1, -points[0]]

	for i in range(1, len(points)):

		lst = pol + [0]
		for j in range(1, len(lst)):
			lst[j] += -points[i] * pol[j-1]

		pol = lst

	return pol

def diff_polinom(polinom) -> list[mpf]:
	lenght_pol = len(polinom)

	if lenght_pol == 1: return [0]
	res = []

	for i in range(lenght_pol-1):
		res += [polinom[i]*(lenght_pol-i-1)]

	return res

def value_polinom(polinom, arg : mpf) -> mpf:

	res = 0
	for i in range(len(polinom)):
		res += polinom[i] * power(arg, len(polinom) - i - 1)

	return res

def grafics(index : int) -> None:

	axis.clear()
	ax = [a-0.1 + mpf(i*(b-a+0.2)/(499)) for i in range(500)]

	if index == 0:

		points = [a + mpf(i*(b - a)/(count_points_lin_interp-1)) for i in range(count_points_lin_interp)]
		value_func = list(map(func, points))
		get_lin_splain(points, value_func)

		pol_value = []
		for i in ax:

			idx_pol = count_points_lin_interp - 2
			for j in range(count_points_lin_interp - 1):
				if points[j + 1] > i:
					idx_pol = j
					break

			pol_value += [value_polinom(lin_pols[idx_pol], i)]

		axis.plot(ax, list(map(func, ax)), "g", label = "Исходная функция 3x - cos(x) - 1" if index_func == 0 else "Исходная функция |x|(3x - cos(x) - 1)")
		axis.plot(ax, pol_value, "--r", label = "Линейный сплайн")
		axis.plot(points, list(map(func, points)), "ob", label = "Выбранные узлы (" + str(count_points_lin_interp) + ")")
		axis.set_title("Исходная функция и линейный сплайн при равномерном распределении узлов")
		axis.grid()
		axis.legend()

	elif index == 1:

		points = [a + mpf(i*(b - a)/(count_points_sq_interp-1)) for i in range(count_points_sq_interp)]
		value_func = list(map(func, points))
		get_sq_splain(points, value_func, diff(func, points[0]))

		pol_value = []
		diff_pol_value = []
		diff_value_func_graf = []
		for i in ax:

			idx_pol = count_points_sq_interp - 2
			for j in range(count_points_sq_interp - 1):
				if points[j + 1] > i:
					idx_pol = j
					break

			pol_value += [value_polinom(sq_pols[idx_pol], i)]
			diff_pol_value += [value_polinom(diff_polinom(sq_pols[idx_pol]), i)]
			diff_value_func_graf += [diff(func, i)]

		axis.plot(ax, list(map(func, ax)), "g", label = "Исходная функция 3x - cos(x) - 1" if index_func == 0 else "Исходная функция |x|(3x - cos(x) - 1)")
		axis.plot(ax, pol_value, "--r", label = "Квадратичный сплайн")
		axis.plot(ax, diff_value_func_graf, "m", label = "Первая производная исходной функции")
		axis.plot(ax, diff_pol_value, "--b", label = "Первая производная квадратичного сплайна")
		axis.plot(points, list(map(func, points)), "ob", label = "Выбранные узлы (" + str(count_points_sq_interp) + ")")
		axis.set_title("Исходная функция и квадратичный сплайн при равномерном распределении узлов")
		axis.grid()
		axis.set_ylim(-10, 10)
		axis.legend()

	elif index == 2:

		points = [a + mpf(i*(b - a)/(count_points_cub_interp-1)) for i in range(count_points_cub_interp)]
		value_func = list(map(func, points))
		#get_cub_splain(points, value_func, [diff(func, points[0]), diff(func, points[0], 2)])
		get_natural_cub_splain(points, value_func)

		pol_value = []
		diff_pol_value = []
		diff_value_func_graf = []
		diff2_pol_value = []
		diff2_value_func_graf = []
		for i in ax:

			idx_pol = count_points_cub_interp - 2
			for j in range(count_points_cub_interp - 1):
				if points[j + 1] > i:
					idx_pol = j
					break

			pol_value += [value_polinom(cub_pols[idx_pol], i)]
			diff_pol_value += [value_polinom(diff_polinom(cub_pols[idx_pol]), i)]
			diff2_pol_value += [value_polinom(diff_polinom(diff_polinom(cub_pols[idx_pol])), i)]
			diff_value_func_graf += [diff(func, i)]
			diff2_value_func_graf += [diff(func, i, 2)]

		axis.plot(ax, list(map(func, ax)), "g", label = "Исходная функция 3x - cos(x) - 1" if index_func == 0 else "Исходная функция |x|(3x - cos(x) - 1)")
		axis.plot(ax, pol_value, "--r", label = "Естественный кубический сплайн")
		axis.plot(ax, diff_value_func_graf, "m", label = "Первая производная исходной функции")
		axis.plot(ax, diff_pol_value, "--b", label = "Первая производная кубического сплайна")
		axis.plot(ax, diff2_value_func_graf, "c", label = "Вторая производная исходной функции")
		axis.plot(ax, diff2_pol_value, "--y", label = "Вторая производная кубического сплайна")
		axis.plot(points, list(map(func, points)), "ob", label = "Выбранные узлы (" + str(count_points_cub_interp) + ")")
		axis.set_title("Исходная функция и естественный кубический сплайн при равномерном распределении узлов")
		axis.set_ylim(-10, 10)
		axis.grid()
		axis.legend()

	elif index == 3:

		points = [a + mpf(i*(b - a)/(count_points_lin_interp-1)) for i in range(count_points_lin_interp)]
		value_func = list(map(func, points))

		if count_points_lin_interp >= 13: meshgrid = 1000
		else: meshgrid = 500
		ax2 = [a + i*(b - a)/(meshgrid-1) for i in range(meshgrid)]

		get_lin_splain(points, value_func)
		pol_value = []
		for i in ax2:

			idx_pol = count_points_lin_interp - 2
			for j in range(count_points_lin_interp - 1):
				if points[j + 1] > i:
					idx_pol = j
					break

			pol_value += [value_polinom(lin_pols[idx_pol], i)]

		differ = [log(abs(func(ax2[i]) - pol_value[i]), 10) for i in range(meshgrid)]

		max_value_acc = log(max([abs(diff(func, i)) for i in ax2])*((b - a)/(count_points_lin_interp-1))*(7/4), 10)

		axis.plot(ax2, differ, "g", label = "Степень абсолютной погрешности")
		axis.plot(ax2, [max_value_acc for i in ax2], "--k", linewidth = 2, label = "Оценка погрешности")
		axis.set_title("Степень абсолютной погрешности линейного сплайна при равномерном распределении узлов (" + str(count_points_lin_interp) + ")")
		axis.grid()
		axis.legend()

	elif index == 4:

		points = [a + mpf(i*(b - a)/(count_points_sq_interp-1)) for i in range(count_points_sq_interp)]
		value_func = list(map(func, points))

		if count_points_lin_interp >= 13: meshgrid = 1000
		else: meshgrid = 500
		ax2 = [a + mpf(i*(b - a)/(meshgrid-1)) for i in range(meshgrid)]

		get_sq_splain(points, value_func, diff(func, points[0]))
		diff_differ = []
		differ = []
		max_value_acc = []
		max_diff_value = -inf

		for i in ax2:

			idx_pol = count_points_sq_interp - 2
			for j in range(count_points_sq_interp - 1):
				if points[j + 1] > i:
					idx_pol = j
					break

			pol_value = value_polinom(sq_pols[idx_pol], i)
			differ += [log(abs(func(i) - pol_value), 10)]

			diff_value_func_graf = diff(func, i)
			diff_pol_value = value_polinom(diff_polinom(sq_pols[idx_pol]), i)
			diff_differ += [log(abs(diff_value_func_graf - diff_pol_value), 10)]

			max_diff_value = max(max_diff_value, abs(diff_value_func_graf))

		max_value_acc = log(max_diff_value*((b - a)/(count_points_sq_interp-1))*(7/4), 10)

		axis.plot(ax2, differ, "g", label = "Степень абсолютной погрешности")
		axis.plot(ax2, diff_differ, "r", label = "Степень абсолютной погрешности производной")
		axis.plot(ax2, [max_value_acc for i in ax2], "--k", linewidth = 2, label = "Оценка погрешности")
		axis.set_title("Степень абсолютной погрешности квадратичного сплайна и его производной при равномерном распределении узлов (" + str(count_points_sq_interp) + ")")
		axis.grid()
		axis.legend()

	elif index == 5:

		points = [a + mpf(i*(b - a)/(count_points_cub_interp-1)) for i in range(count_points_cub_interp)]
		value_func = list(map(func, points))

		if count_points_lin_interp >= 13: meshgrid = 1000
		else: meshgrid = 500
		ax2 = [a + i*(b - a)/(meshgrid-1) for i in range(meshgrid)]

		#get_cub_splain(points, value_func, [diff(func, points[0]), diff(func, points[0], 2)])
		get_natural_cub_splain(points, value_func)
		diff_differ = []
		diff2_differ = []
		differ = []
		max_value_acc = []
		max_diff_value = -inf

		for i in ax2:

			idx_pol = count_points_cub_interp - 2
			for j in range(count_points_cub_interp - 1):
				if points[j + 1] > i:
					idx_pol = j
					break

			pol_value = value_polinom(cub_pols[idx_pol], i)
			differ += [log(abs(func(i) - pol_value), 10)]

			diff_value_func_graf = diff(func, i)
			diff_pol_value = value_polinom(diff_polinom(cub_pols[idx_pol]), i)
			diff_differ += [log(abs(diff_value_func_graf - diff_pol_value), 10)]

			diff2_value_func_graf = diff(func, i, 2)
			diff2_pol_value = value_polinom(diff_polinom(diff_polinom(cub_pols[idx_pol])), i)
			diff2_differ += [log(abs(diff2_value_func_graf - diff_pol_value), 10)]

			max_diff_value = max(max_diff_value, abs(diff_value_func_graf))

		max_value_acc = log(max_diff_value*((b - a)/(count_points_cub_interp-1))*(7/4), 10)

		axis.plot(ax2, differ, "g", label = "Степень абсолютной погрешности")
		axis.plot(ax2, diff_differ, "r", label = "Степень абсолютной погрешности первой производной")
		axis.plot(ax2, diff2_differ, "m", label = "Степень абсолютной погрешности второй производной")
		axis.plot(ax2, [max_value_acc for i in ax2], "--k", linewidth = 2, label = "Оценка погрешности")
		axis.set_title("Степень абсолютной погрешности естественного кубического сплайна и его первой и второй производной при равномерном распределении узлов (" + str(count_points_cub_interp) + ")")
		axis.grid()
		axis.legend()

	plt.show()

def key_event(event) -> None:

	global index, index_func
	global count_points_lin_interp, count_points_sq_interp, count_points_cub_interp
	global func

	key = getattr(event, 'key')

	if key == 'right': index = (index + 1)%6
	elif key == 'left': index = (index - 1)%6
	elif key == 'up':
		if index == 0 or index == 3: count_points_lin_interp += 1
		if index == 1 or index == 4: count_points_sq_interp += 1
		if index == 2 or index == 5: count_points_cub_interp += 1
	elif key == 'down': 
		if (index == 0 or index == 3) and count_points_lin_interp > 2: count_points_lin_interp -= 1
		if (index == 1 or index == 4) and count_points_sq_interp > 2: count_points_sq_interp -= 1
		if (index == 2 or index == 5) and count_points_cub_interp > 2: count_points_cub_interp -= 1
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
	func = lambda x: sin(exp(x))
	index_func = 0
	index = 0

	mp.dps = 20

	a, b = mpf(-1), mpf(1)
	count_points_lin_interp = 5
	count_points_sq_interp = 5
	count_points_cub_interp = 5

	lin_pols = {}
	sq_pols = {}
	cub_pols = {}

	fg, axis = plt.subplots(1, 1, figsize=(15, 8))
	fg.subplots_adjust(bottom=0.06, left=0.05, right=0.95, top=0.95)
	fg.canvas.mpl_connect('key_release_event', key_event)

	grafics(index)