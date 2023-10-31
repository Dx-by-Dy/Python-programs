from mpmath import *
from functools import lru_cache
import matplotlib.pyplot as plt


'''
# одномерный случай, поглощенный многомерным
def func(arg_x : mpf, arg_y : mpf) -> mpf:
	return arg_x + arg_y


def get_adjus_coef(arg_x : mpf, arg_y : mpf, arg_h : mpf, list_a : list[mpf], list_c : list[mpf], num : int):
	if num == 1: return arg_h * func(arg_x, arg_y)

	res_sum = arg_y
	for i in range(num - 1):
		res_sum += list_a[num - 2][i] * get_adjus_coef(arg_x, arg_y, arg_h, list_a, list_c, i + 1)

	return arg_h * func(arg_x + list_c[num - 2] * arg_h, res_sum)
'''


def general_solution(arg_x : mpf, arg_x0 : mpf, list_y0 : tuple[mpf]) -> tuple[mpf]:
	# рассчет эталонной функции
	coef1 = (glA * glB) ** 0.5
	coef2 = (glA / glB) ** 0.5
	res1 = list_y0[0] * cos(coef1 * (arg_x - arg_x0)) + list_y0[1] * coef2 * sin(coef1 * (arg_x - arg_x0))
	res2 = list_y0[1] * cos(coef1 * (arg_x - arg_x0)) - list_y0[0] * (1 / coef2) * sin(coef1 * (arg_x - arg_x0))
	return (res1, res2)


def meshgrid(start : mpf, end : mpf, count_of_partition : mpf) -> tuple[mpf]:
	# просчет расположения точек
	step = (end - start) / count_of_partition
	return tuple([start + i * step for i in range(count_of_partition)])


def norm(array : (list[mpf], tuple[mpf])) -> mpf:
	return pow(sum([elem ** 2 for elem in array]), 0.5)


def get_opt_step(start_x : mpf, end_x : mpf, start_list_y : tuple[mpf], epsilon : mpf, deg_err : int) -> mpf:
	delta = ( 1 / (max( abs(start_x), abs(end_x) )) ) ** (deg_err + 1) + \
				norm([func_ND(start_x, start_list_y, 1), func_ND(start_x, start_list_y, 2)]) ** (deg_err + 1)
	return (epsilon / delta) ** (1 / (deg_err + 1))


def func_ND(arg_x : mpf, list_y : tuple[mpf], row : int) -> mpf:
	# многомерная функция правых частей
	if row == 1:
		return glA * list_y[1]
	else:
		return -glB * list_y[0]


@lru_cache
def get_adjus_coef_ND(arg_x : mpf, list_y : tuple[mpf], arg_h : mpf, list_a : tuple[mpf], list_c : tuple[mpf], row : int, num : int) -> mpf:
	# рассчет поправок
	if num == 1: return arg_h * func_ND(arg_x, list_y, row)

	res_sum = list(list_y)
	for i in range(num - 1):
		for idx_y in range(len(list_y)):
			res_sum[idx_y] += list_a[num - 2][i] * get_adjus_coef_ND(arg_x, list_y, arg_h, list_a, list_c, idx_y + 1, i + 1)

	return arg_h * func_ND(arg_x + list_c[num - 2] * arg_h, res_sum, row)


'''
# явно выписанные поправки 1 и 2 ранга
def k1(arg_x : mpf, list_y : tuple[mpf], arg_h : mpf, row : int):
	return arg_h * func_ND(arg_x, list_y, row)

def k2(arg_x : mpf, list_y : tuple[mpf], arg_h : mpf, list_a : tuple[mpf], list_c : tuple[mpf], row : int):
	return arg_h * func_ND(arg_x + list_c[0] * arg_h, \
		(list_y[0] + list_a[0][0] * k1(arg_x, list_y, arg_h, row), list_y[1] + list_a[0][0] * k1(arg_x, list_y, arg_h, row)), row)
'''


def get_next_y(arg_x : mpf, list_y : tuple[mpf], arg_h : mpf, list_a : tuple[mpf], list_b : tuple[mpf], list_c : tuple[mpf]) -> tuple[mpf]:
	# рассчет значения интегральной кривой в следующей точке
	res_y = list(list_y)
	for idx_y in range(len(list_y)):
		for idx_b in range(len(list_b)):
			res_y[idx_y] += list_b[idx_b] * get_adjus_coef_ND(arg_x, list_y, arg_h, list_a, list_c, idx_y + 1, idx_b + 1)

	return tuple(res_y)


def err_score_Runge(value_with_h : tuple[mpf], value_with_half_h : tuple[mpf], arg_h : mpf, epsilon : mpf, deg_err : int) -> (bool, ...):
	# оцениваем погрешность по методу Рунге
	norm_of_difference = norm([value_with_half_h[i] - value_with_h[i] for i in range(len(value_with_h))])

	R1, R2 = [], [] 
	for idx_y in range(len(value_with_h)):
		R1 += [abs((value_with_half_h[idx_y] - value_with_h[idx_y]) / (1 - 2 ** (-deg_err)))]
		R2 += [abs((value_with_half_h[idx_y] - value_with_h[idx_y]) / (2 ** deg_err - 1))]

	if norm(R2) < epsilon:
		return True, R2
	else:
		new_opt_h = arg_h / 2 * ((2 ** deg_err - 1) * epsilon / norm_of_difference) ** deg_err
		return False, new_opt_h


def ode2_const_step_and_score_err(start_x : mpf, start_list_y : tuple[mpf], end_x : mpf, \
										list_a : tuple[mpf], list_b : tuple[mpf], list_c : tuple[mpf]) -> tuple[mpf]:

	def ode2_const_step(arg_h : mpf) -> tuple[mpf]:

		# итеративный рассчет итогового значения интегральной кривой
		points = meshgrid(start_x, end_x, int((end_x - start_x) / arg_h))

		result = start_list_y
		for point in points:
			result = get_next_y(point, result, arg_h, tuple_a, tuple_b, tuple_c)

		return result

	# проводим вычисления до момента попадания в допустимую область погрешности
	step_h = get_opt_step(start_x, end_x, start_y, epsilon, deg_err)

	while True:
		res1 = ode2_const_step(step_h)
		res2 = ode2_const_step(step_h / 2)

		esc, val = err_score_Runge(res1, res2, step_h, epsilon, deg_err)
		if esc:
			opt_res = tuple([res2[i] + val[i] for i in range(len(val))])
			return opt_res, norm(val)
		else:
			step_h = val


if __name__ == "__main__":

	mp.dps = 30

	glA = mpf(1/20)
	glB = mpf(1/25)
	xi = mpf(1/19)

	epsilon = mpf(1e-6)
	deg_err = 2

	tuple_a = ( ( xi, ), )
	tuple_b = ( 1 - 1 / (2 * xi), 1 / (2 * xi) )
	tuple_c = ( xi, )

	start_x = mpf(0)
	start_y = ( glB * pi, glA * pi )


	print(ode2_const_step_and_score_err(start_x, start_y, pi, tuple_a, tuple_b, tuple_c))
	#print(ode2_const_step_and_score_err(start_x, start_y, pi, step_h, tuple_a, tuple_b, tuple_c))
	print(general_solution(pi, start_x, start_y))
