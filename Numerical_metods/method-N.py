from mpmath import *
import matplotlib.pyplot as plt
from numpy import arange

accuracy = 1e-4 #задаем точность
mp.dps = abs(log(accuracy, 10)) + 1

def iterat(list_cnt, start_value : mpf, accuracy : mpf, func) -> mpf:  # функция метода Ньютона
	old_value = -inf
	new_value = start_value - func(start_value)/diff(func, start_value)
	cnt = 0
	while abs(new_value - old_value) > accuracy:
		old_value = new_value
		new_value = new_value - func(new_value)/diff(func, new_value)
		cnt += 1

	list_cnt += [cnt]

	return new_value

def grafics() -> None:

	ax = arange(0.5, 3, 0.01)  #задаем промежуток 
	func = lambda x: sin(x)*(x + log(x, 10) - 0.5) - 1.5  # исходная функция  sin(x)*(x + log(x, 10) - 0.5) - 1.5

	value_func = [func(x) for x in ax]  #считаем значения функции
	const_func = [0 for x in ax]
	diff1_func = [diff(func, x) for x in ax]  #считаем значения 1 производной функции
	diff2_func = [diff(func, x, 2) for x in ax]  #считаем значения 2 производной функции

	lst_iterat = []
	abs_start_point = []

	for i in range(100): # считаем количество итераций от расстояния
		if abs(diff(func, 1.7833 + 0.01*i)) > 1e-1: 
			iterat(lst_iterat, 1.7833 + 0.01*i, accuracy, func)   # 0.6723 1.7833
			abs_start_point += [0.01*i]

	plt.subplots(figsize=(15, 8))   #рисуем график

	plt.subplot(222)
	plt.plot(ax, diff1_func, "g", label = "1-я производная")
	plt.plot(ax, diff2_func, "b", label = "2-я производная")
	plt.plot(ax, const_func, "--r")
	plt.title("Значения 1-й и 2-й производной")
	plt.grid()
	plt.legend()

	plt.subplot(224)
	plt.plot(abs_start_point, lst_iterat, "g")
	plt.title("Количество итераций от расстояния")
	plt.xlabel("Расстояние до корня")
	plt.grid()

	plt.subplot(121)
	plt.plot(ax, value_func, "b", label = "f(x) = sin(x)(x + lg(x) - 0.5) - 1.5")
	plt.plot(ax, const_func, "--r")
	plt.title("Значения функции (корень ≈ " + str(mpf(iterat(lst_iterat, 2.5, accuracy, func))) + ")")
	plt.grid()
	plt.legend()

	plt.subplots_adjust(bottom=0.06, left=0.05, right=0.95, top=0.95)

	plt.show()

grafics()



