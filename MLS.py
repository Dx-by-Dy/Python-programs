# метод наимешьших квадратов

from mpmath import *
import matplotlib.pyplot as plt
from numpy import arange

def get_pol_MLS(points : list[mpf], value_func : list[mpf], pow_pol_MLS : int) -> list[mpf]:

	q_pol = {0 : [mpf(1)], 1 : [mpf(1), mpf(-sum(points)/cnt_points)]}

	a0_0, a0_1, a1_0, a1_1 = mpf(0), mpf(0), mpf(0), mpf(0)
	for j in range(cnt_points):
		a0_0 += value_polinom(q_pol[0], points[j])*value_func[j]
		a1_0 += value_polinom(q_pol[1], points[j])*value_func[j]
		a0_1 += pow(value_polinom(q_pol[0], points[j]), 2)
		a1_1 += pow(value_polinom(q_pol[1], points[j]), 2)

	res = sum_polinoms(prod_polinoms([a0_0/a0_1], q_pol[0]), prod_polinoms([a1_0/a1_1], q_pol[1]))

	for i in range(2, pow_pol_MLS + 1):

		alpha1, alpha2 = 0, 0
		beta1, beta2 = 0, 0
		for j in range(cnt_points):
			alpha1 += points[j]*pow(value_polinom(q_pol[i-1], points[j]), 2)
			alpha2 += pow(value_polinom(q_pol[i-1], points[j]), 2)
			beta1 += points[j]*value_polinom(q_pol[i-1], points[j])*value_polinom(q_pol[i-2], points[j])
			beta2 += pow(value_polinom(q_pol[i-2], points[j]), 2)

		alpha = alpha1/alpha2
		beta = beta1/beta2

		q_pol[i] = sum_polinoms(prod_polinoms([1, -alpha], q_pol[i-1]), prod_polinoms([-beta], q_pol[i-2]))

		coef_a1, coef_a2 = 0, 0
		for j in range(cnt_points):
			coef_a1 += value_polinom(q_pol[i], points[j])*value_func[j]
			coef_a2 += pow(value_polinom(q_pol[i], points[j]), 2)

		res = sum_polinoms(res, prod_polinoms([coef_a1/coef_a2], q_pol[i]))

	return res

def value_polinom(polinom : list[mpf], arg : mpf) -> mpf:

	res = 0
	for i in range(len(polinom)):
		res += polinom[i] * power(arg, len(polinom) - i - 1)

	return res

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

def grafics() -> None:

	axis.clear()
	ax = arange(points[0] - 0.1, points[-1] + 0.1, 0.01)

	polinom = get_pol_MLS(points, value_func, pow_polinom)
	pol_value = [value_polinom(polinom, i) for i in ax]
	dod = sum([pow(value_func[i] - value_polinom(polinom, points[i]), 2) for i in range(cnt_points)])

	axis.plot(ax, list(map(func, ax)), "g", label = "Исходная функция 3x - cos(x) - 1")
	axis.plot(ax, pol_value, "--r", label = "Полином МКН (уклонение " + str(dod) + ")")
	axis.plot(points, list(map(func, points)), "ob", label = "Выбранные узлы (" + str(cnt_points) + ")")
	axis.set_title("Исходная функция и полином МНК степени " + str(pow_polinom))
	axis.set_ylim(-10, 10)
	axis.grid()
	axis.legend()

	plt.show()

def key_event(event) -> None:
	global cnt_points, points, value_func, pow_polinom

	key = getattr(event, 'key')

	if key == 'up': cnt_points += 1
	if key == 'down' and cnt_points > 2:
		if pow_polinom == cnt_points - 1: pow_polinom -= 1
		cnt_points -= 1
	if key == 'ctrl+up' and pow_polinom < cnt_points - 1: pow_polinom += 1
	if key == 'ctrl+down' and pow_polinom > 2: pow_polinom -= 1

	points = [a + i*(b-a)/(cnt_points - 1) for i in range(cnt_points)]
	value_func = [func(i) for i in points]

	grafics()

if __name__ == "__main__":

	func = lambda x: 3*x - cos(x) - 1
	#func = lambda x: (10*x + 3)/(1+25*power(x, 2))
	#func = lambda x: 1/(1+25*power(x, 2))

	a, b = mpf(-1), mpf(1)

	cnt_points = 5
	points = [a + i*(b-a)/(cnt_points - 1) for i in range(cnt_points)]
	value_func = [func(i) for i in points]
	pow_polinom = 2

	mp.dps = 16

	fg, axis = plt.subplots(1, 1, figsize=(15, 8))
	fg.subplots_adjust(bottom=0.06, left=0.05, right=0.95, top=0.95)
	fg.canvas.mpl_connect('key_release_event', key_event)

	grafics()