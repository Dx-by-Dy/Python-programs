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


def norm(array : (list[mpf], tuple[mpf])) -> mpf:
	return pow(sum([elem ** 2 for elem in array]), 0.5)


def get_opt_step(start_x : mpf, end_x : mpf, start_list_y : tuple[mpf], epsilon : mpf, deg_err : int) -> mpf:
	delta = ( 1 / (max( abs(start_x), abs(end_x) )) ) ** (deg_err + 1) + \
				norm([func_ND(start_x, start_list_y, i + 1) for i in range(len(start_list_y))]) ** (deg_err + 1)
	return (epsilon / delta) ** (1 / (deg_err + 1))


def func_ND(arg_x : mpf, list_y : tuple[mpf], row : int) -> mpf:
	# для графиков
	global c_call_func
	c_call_func += 1
	# для графиков

	# многомерная функция правых частей
	if row == 1:
		return glA * list_y[1]
	else:
		return -glB * list_y[0]


#@lru_cache
def get_adjus_coef_ND(arg_x : mpf, list_y : tuple[mpf], arg_h : mpf, list_a : tuple[mpf], list_c : tuple[mpf], row : int, num : int) -> mpf:
	# рассчет поправок
	if num == 1: return arg_h * func_ND(arg_x, list_y, row)
	#if num == 2: return k2(arg_x, list_y, arg_h, list_a, list_c, row)
	#if num == 3: return k3(arg_x, list_y, arg_h, list_a, list_c, row)

	res_sum = list(list_y)
	
	for i in range(num - 1):
		for idx_y in range(len(list_y)):
			res_sum[idx_y] += list_a[num - 2][i] * get_adjus_coef_ND(arg_x, list_y, arg_h, list_a, list_c, idx_y + 1, i + 1)

	return arg_h * func_ND(arg_x + list_c[num - 2] * arg_h, res_sum, row)


'''
# явно выписанные поправки 1, 2, 3 ранга
def k1(arg_x : mpf, list_y : tuple[mpf], arg_h : mpf, row : int):
	return arg_h * func_ND(arg_x, list_y, row)

def k2(arg_x : mpf, list_y : tuple[mpf], arg_h : mpf, list_a : tuple[mpf], list_c : tuple[mpf], row : int):
	return arg_h * func_ND(arg_x + list_c[0] * arg_h, \
		(list_y[0] + list_a[0][0] * k1(arg_x, list_y, arg_h, row), list_y[1] + list_a[0][0] * k1(arg_x, list_y, arg_h, row)), row)

def k3(arg_x : mpf, list_y : tuple[mpf], arg_h : mpf, list_a : tuple[mpf], list_c : tuple[mpf], row : int):
	return arg_h * func_ND(arg_x + list_c[1] * arg_h, \
		(list_y[0] + list_a[1][0] * k1(arg_x, list_y, arg_h, row) + list_a[1][1] * k2(arg_x, list_y, arg_h, list_a, list_c, row), \
		 list_y[1] + list_a[1][0] * k1(arg_x, list_y, arg_h, row) + list_a[1][1] * k2(arg_x, list_y, arg_h, list_a, list_c, row)), row)
'''


def get_next_y(arg_x : mpf, list_y : tuple[mpf], arg_h : mpf, \
					list_a : tuple[mpf], list_b : tuple[mpf], list_c : tuple[mpf]) -> tuple[mpf]:
	# рассчет значения интегральной кривой в следующей точке
	res_y = list(list_y)
	for idx_y in range(len(list_y)):
		for idx_b in range(len(list_b)):
			res_y[idx_y] += list_b[idx_b] * get_adjus_coef_ND(arg_x, list_y, arg_h, list_a, list_c, idx_y + 1, idx_b + 1)

	return tuple(res_y)


def err_score_Runge(value_with_h : tuple[mpf], value_with_half_h : tuple[mpf], arg_h : mpf, epsilon : mpf, deg_err : int) -> (bool, ...):
	# оцениваем полную погрешность по методу Рунге
	norm_of_difference = norm([value_with_half_h[i] - value_with_h[i] for i in range(len(value_with_h))])

	R1, R2 = [], [] 
	for idx_y in range(len(value_with_h)):
		R1 += [abs((value_with_half_h[idx_y] - value_with_h[idx_y]) / (1 - 2 ** (-deg_err)))]
		R2 += [abs((value_with_half_h[idx_y] - value_with_h[idx_y]) / (2 ** deg_err - 1))]

	if norm(R1) < epsilon:
		return True, R2
	else:
		new_opt_h = (arg_h / 2) * (((2 ** deg_err - 1) * epsilon / norm_of_difference) ** (1 / deg_err))
		return False, new_opt_h


def aut_err_score_Runge(value_with_h : tuple[mpf], value_with_half_h : tuple[mpf], arg_h : mpf, epsilon : mpf, deg_err : int) -> (bool, mpf, ...):
	# для графиков
	global loc_err
	# для графиков

	# оцениваем локальную погрешность по методу Рунге
	norm_of_difference = norm([value_with_half_h[i] - value_with_h[i] for i in range(len(value_with_h))])

	R1, R2 = [], [] 
	for idx_y in range(len(value_with_h)):
		R1 += [abs((value_with_half_h[idx_y] - value_with_h[idx_y]) / (1 - 2 ** (-deg_err)))]
		R2 += [abs((value_with_half_h[idx_y] - value_with_h[idx_y]) / (2 ** deg_err - 1))]

	nR1 = norm(R1)
	if nR1 > epsilon * 2 ** deg_err:
		return False, arg_h / 2, None

	elif nR1 > epsilon:
		loc_err += [[norm(R2)]]
		return True, arg_h / 2, tuple([value_with_half_h[i] + R2[i] for i in range(len(R2))])

	elif nR1 > epsilon * 2 ** (-(deg_err + 1)):
		loc_err += [[nR1]]
		return True, arg_h, tuple([value_with_h[i] + R1[i] for i in range(len(R1))])

	else:
		loc_err += [[nR1]]
		return True, 2 * arg_h, tuple([value_with_h[i] + R1[i] for i in range(len(R1))])


def ode_var_step(start_x : mpf, start_list_y : tuple[mpf], end_x : mpf, \
							list_a : tuple[mpf], list_b : tuple[mpf], list_c : tuple[mpf], \
							epsilon : mpf = 1e-4) -> tuple[mpf]:
	# для графиков
	global step_size, loc_err
	step_size, loc_err = [], []
	old_vel = start_list_y
	# для графиков

	# проводим вычисления до момента попадания в допустимую область погрешности
	
	deg_err = len(list_b)
	step_h = get_opt_step(start_x, end_x, start_y, epsilon, deg_err)

	res1, res2 = start_list_y, start_list_y
	near_end = False

	while True:
		res1 = get_next_y(start_x, res1, step_h, list_a, list_b, list_c)

		for _ in range(2):
			res2 = get_next_y(start_x, res2, step_h / 2, list_a, list_b, list_c)

		esc, new_step, new_res = aut_err_score_Runge(res1, res2, step_h, epsilon, deg_err)
		if esc:
			# для графиков
			step_size += [(step_h, start_x + step_h)]

			gen_sol = general_solution(start_x + step_h, start_x, old_vel)
			loc_err[-1] += [norm([gen_sol[0] - new_res[0], gen_sol[1] - new_res[1]]), start_x + step_h]

			old_vel = new_res
			# для графиков

			if near_end:
				return new_res, epsilon

			start_x += step_h
			res1 = res2 = new_res
			step_h = new_step

			if start_x + step_h > end_x:
				step_h = end_x - start_x
				near_end = True
		else:
			step_h = new_step


def ode_const_step(start_x : mpf, start_list_y : tuple[mpf], end_x : mpf, \
							list_a : tuple[mpf], list_b : tuple[mpf], list_c : tuple[mpf], \
							epsilon : mpf = 1e-6) -> tuple[mpf]:

	def value_ode(arg_h : mpf) -> tuple[mpf]:
		# для графиков
		global true_err
		true_err = []
		# для графиков

		# итеративный рассчет итогового значения интегральной кривой

		result = start_list_y
		point = start_x
		while True:
			if point + arg_h > end_x:
				result = get_next_y(point, result, end_x - point, list_a, list_b, list_c)

				# для графиков
				gen_sol = general_solution(end_x, start_x, start_y)
				true_err += [(log(norm([gen_sol[0] - result[0], gen_sol[1] - result[1]]), 10), end_x, arg_h)]
				# для графиков

				break
			else:
				result = get_next_y(point, result, arg_h, list_a, list_b, list_c)

			# для графиков
			gen_sol = general_solution(point + arg_h, start_x, start_y)
			true_err += [(log(norm([gen_sol[0] - result[0], gen_sol[1] - result[1]]), 10), point + arg_h, arg_h)]
			# для графиков

			point += arg_h

		return result

	# проводим вычисления до момента попадания в допустимую область погрешности
	
	deg_err = len(list_b)
	step_h = get_opt_step(start_x, end_x, start_y, epsilon, deg_err)

	while True:
		res1 = value_ode(step_h)
		res2 = value_ode(step_h / 2)

		esc, val = err_score_Runge(res1, res2, step_h, epsilon, deg_err)
		if esc:
			opt_res = tuple([res2[i] + val[i] for i in range(len(val))])
			return opt_res, epsilon
		else:
			step_h = val


def grafics(index : int) -> None:
	global c_call_func

	plt.ion()
	axis.clear()

	if index == 0:
		gen_sol = general_solution(pi, start_x, start_y)

		res2 = ode_const_step(start_x, start_y, pi, tuple_a_2, tuple_b_2, tuple_c_2, epsilon)
		true_err2 = true_err.copy()
		res2 = norm([gen_sol[0] - res2[0][0], gen_sol[1] - res2[0][1]]) < epsilon

		res3 = ode_const_step(start_x, start_y, pi, tuple_a_3_1, tuple_b_3_1, tuple_c_3_1, epsilon)
		true_err3 = true_err.copy()
		res3 = norm([gen_sol[0] - res3[0][0], gen_sol[1] - res3[0][1]]) < epsilon

		res4 = ode_const_step(start_x, start_y, pi, tuple_a_4_1, tuple_b_4_1, tuple_c_4_1, epsilon)
		true_err4 = true_err.copy()
		res4 = norm([gen_sol[0] - res4[0][0], gen_sol[1] - res4[0][1]]) < epsilon

		axis.plot([i[1] for i in true_err2], [i[0] for i in true_err2], "r", \
			label = f"Двухэтапный метод (h = {round(true_err2[0][2], 3)}, {res2})", marker = 'X')
		axis.plot([i[1] for i in true_err3], [i[0] for i in true_err3], "b", \
			label = f"Трехэтапный метод (h = {round(true_err3[0][2], 3)}, {res3})", marker = 'X')
		axis.plot([i[1] for i in true_err4], [i[0] for i in true_err4], "g", \
			label = f"Четырехэтапный метод (h = {round(true_err4[0][2], 3)}, {res4})", marker = 'X')
		axis.set_title("Степень зависимости нормы истинной погрешности \n двухэтапного, трехэтапного и четырехэтапного метода" + \
			" с постоянным шагом от значения х $(\\epsilon = 10^{" + str(int(log(epsilon/2, 10))) + "})$")
		axis.set_xlabel("Значение х")
		axis.grid()
		axis.legend()


	if index == 1:
		gen_sol = general_solution(pi, start_x, start_y)

		res2 = ode_var_step(start_x, start_y, pi, tuple_a_2, tuple_b_2, tuple_c_2, epsilon)
		step_size2 = step_size.copy()
		res2 = norm([gen_sol[0] - res2[0][0], gen_sol[1] - res2[0][1]]) < epsilon

		res3 = ode_var_step(start_x, start_y, pi, tuple_a_3_1, tuple_b_3_1, tuple_c_3_1, epsilon)
		step_size3 = step_size.copy()
		res3 = norm([gen_sol[0] - res3[0][0], gen_sol[1] - res3[0][1]]) < epsilon

		res4 = ode_var_step(start_x, start_y, pi, tuple_a_4_1, tuple_b_4_1, tuple_c_4_1, epsilon)
		step_size4 = step_size.copy()
		res4 = norm([gen_sol[0] - res4[0][0], gen_sol[1] - res4[0][1]]) < epsilon

		axis.plot([i[1] for i in step_size2], [i[0] for i in step_size2], "r", label = f"Двухэтапный метод ({res2})", marker = 'X')
		axis.plot([i[1] for i in step_size3], [i[0] for i in step_size3], "b", label = f"Трехэтапный метод ({res3})", marker = 'X')
		axis.plot([i[1] for i in step_size4], [i[0] for i in step_size4], "g", label = f"Четырехэтапный метод ({res4})", marker = 'X')
		axis.set_title("Зависимость шага двухэтапного, трехэтапного и четырехэтапного метода \n " +\
			"с автоматическим шагом от значения х $(\\epsilon = 10^{" + str(int(log(epsilon/2, 10))) + "})$")
		axis.set_xlabel("Значение х")
		axis.grid()
		axis.legend()


	if index == 2:
		gen_sol = general_solution(pi, start_x, start_y)

		res2 = ode_var_step(start_x, start_y, pi, tuple_a_2, tuple_b_2, tuple_c_2, epsilon)
		loc_err2 = loc_err.copy()
		res2 = norm([gen_sol[0] - res2[0][0], gen_sol[1] - res2[0][1]]) < epsilon

		res3 = ode_var_step(start_x, start_y, pi, tuple_a_3_1, tuple_b_3_1, tuple_c_3_1, epsilon)
		loc_err3 = loc_err.copy()
		res3 = norm([gen_sol[0] - res3[0][0], gen_sol[1] - res3[0][1]]) < epsilon

		res4 = ode_var_step(start_x, start_y, pi, tuple_a_4_1, tuple_b_4_1, tuple_c_4_1, epsilon)
		loc_err4 = loc_err.copy()
		res4 = norm([gen_sol[0] - res4[0][0], gen_sol[1] - res4[0][1]]) < epsilon

		axis.plot([i[2] for i in loc_err2], [i[1] / i[0] for i in loc_err2], "r", label = f"Двухэтапный метод ({res2})", marker = 'X')
		axis.plot([i[2] for i in loc_err3], [i[1] / i[0] for i in loc_err3], "b", label = f"Трехэтапный метод ({res3})", marker = 'X')
		axis.plot([i[2] for i in loc_err4], [i[1] / i[0] for i in loc_err4], "g", label = f"Четырехэтапный метод ({res4})", marker = 'X')
		axis.set_title("Зависимость отношения истинной локальной погрешности к полученной оценке \n" + \
			"для двухэтапного, трехэтапного и четырехэтапного метода " + \
			"с автоматическим шагом от значения х $(\\epsilon = 10^{" + str(int(log(epsilon/2, 10))) + "})$")
		axis.set_xlabel("Значение х")
		axis.grid()
		axis.legend()


	if index == 3:

		ax = [i for i in range(5, 13)]
		c_call_func2, c_call_func3, c_call_func4, c_call_func_c2, c_call_func_c3, c_call_func_c4 = [], [], [], [], [], []
		c_call_func = 0

		for i in range(5, 13):
			ode_var_step(start_x, start_y, pi, tuple_a_2, tuple_b_2, tuple_c_2, 10**(-i))
			c_call_func2 += [c_call_func]
			c_call_func = 0

			'''
			ode_const_step(start_x, start_y, pi, tuple_a_2, tuple_b_2, tuple_c_2, 10**(-i))
			c_call_func_c2 += [c_call_func]
			c_call_func = 0
			'''

			ode_var_step(start_x, start_y, pi, tuple_a_3_1, tuple_b_3_1, tuple_c_3_1, 10**(-i))
			c_call_func3 += [c_call_func]
			c_call_func = 0

			'''
			ode_const_step(start_x, start_y, pi, tuple_a_3_1, tuple_b_3_1, tuple_c_3_1, 10**(-i))
			c_call_func_c3 += [c_call_func]
			c_call_func = 0
			'''

			ode_var_step(start_x, start_y, pi, tuple_a_4_1, tuple_b_4_1, tuple_c_4_1, 10**(-i))
			c_call_func4 += [c_call_func]
			c_call_func = 0

			'''
			ode_const_step(start_x, start_y, pi, tuple_a_4_1, tuple_b_4_1, tuple_c_4_1, 10**(-i))
			c_call_func_c4 += [c_call_func]
			c_call_func = 0
			'''


		axis.plot(ax, c_call_func2, "r", label = "Двухэтапный метод (автоматический шаг)")
		#axis.plot(ax, c_call_func_c2, "r--", label = "Двухэтапный метод (постоянный шаг)")
		axis.plot(ax, c_call_func3, "b", label = "Трехэтапный метод (автоматический шаг)")
		#axis.plot(ax, c_call_func_c3, "b--", label = "Трехэтапный метод (постоянный шаг)")
		axis.plot(ax, c_call_func4, "g", label = "Четырехэтапный метод (автоматический шаг)")
		#axis.plot(ax, c_call_func_c4, "g--", label = "Четырехэтапный метод (постоянный шаг)")
		axis.set_title("Зависимость количества вызовов функции \n" + \
			"для двухэтапного, трехэтапного и четырехэтапного метода с автоматическим шагом от значения $ \\epsilon $")
		axis.set_xlabel("Значение $ \\epsilon $")
		axis.set_ylim(0, 5000)
		axis.set_xticks(ax, ["$10^{" + str(-i) + "}$" for i in ax])
		axis.grid()
		axis.legend()


	plt.draw()
	plt.ioff()


def key_event(event) -> None:
	global index, epsilon

	key = getattr(event, 'key')

	if key == 'right': index = (index + 1) % 4
	elif key == 'left': index = (index - 1) % 4
	elif key == 'up': epsilon = min(epsilon * 10, 1e-1)
	elif key == 'down': epsilon = max(epsilon / 10, 1e-10)

	grafics(index)


if __name__ == "__main__":

	mp.dps = 20

	glA = mpf(1/20)
	glB = mpf(1/25)
	xi = mpf(1/19)

	tuple_a_2 = ( ( xi, ), )
	tuple_b_2 = ( 1 - 1 / (2 * xi), 1 / (2 * xi) )
	tuple_c_2 = ( xi, )

	o = mpf(1)

	tuple_a_3_1 = ( ( o/2, ), ( -1, 2 ) )
	tuple_b_3_1 = ( o/6, o/6*4, o/6 )
	tuple_c_3_1 = ( o/2, o )

	tuple_a_3_2 = ( ( o/3, ), ( 0, o/3*2 ) )
	tuple_b_3_2 = ( o/4, 0, o/4*3 )
	tuple_c_3_2 = ( o/3, o/3*2 )

	tuple_a_4_1 = ( ( o/2, ), ( 0, o/2 ), ( mpf(0), mpf(0), o ) )
	tuple_b_4_1 = ( o/6, o/6*2, o/6*2, o/6 )
	tuple_c_4_1 = ( o/2, o/2, o )

	start_x = mpf(0)
	start_y = ( glB * pi, glA * pi )
	epsilon = 1e-4


	fg, axis = plt.subplots(nrows= 1, ncols= 1, figsize=(15, 8))
	fg.subplots_adjust(bottom=0.1, left=0.06, right=0.98, top=0.92, hspace=0.3)
	fg.canvas.mpl_connect('key_release_event', key_event)

	true_err, step_size, loc_err, c_call_func = [], [], [], 0

	index = 0
	grafics(index)

	plt.show()

	'''
	gen_sol = general_solution(pi, start_x, start_y)
	print(gen_sol)

	for i in range(8):
		if i == 0:
			res = ode_const_step(start_x, start_y, pi, tuple_a_2, tuple_b_2, tuple_c_2, epsilon)
		elif i == 1:
			res = ode_const_step(start_x, start_y, pi, tuple_a_3_1, tuple_b_3_1, tuple_c_3_1, epsilon)
		elif i == 2:
			res = ode_const_step(start_x, start_y, pi, tuple_a_3_2, tuple_b_3_2, tuple_c_3_2, epsilon)
		elif i == 3:
			res = ode_const_step(start_x, start_y, pi, tuple_a_4_1, tuple_b_4_1, tuple_c_4_1, epsilon)
		elif i == 4:
			print()
			res = ode_var_step(start_x, start_y, pi, tuple_a_2, tuple_b_2, tuple_c_2, epsilon)
		elif i == 5:
			res = ode_var_step(start_x, start_y, pi, tuple_a_3_1, tuple_b_3_1, tuple_c_3_1, epsilon)
		elif i == 6:
			res = ode_var_step(start_x, start_y, pi, tuple_a_3_2, tuple_b_3_2, tuple_c_3_2, epsilon)
		elif i == 7:
			res = ode_var_step(start_x, start_y, pi, tuple_a_4_1, tuple_b_4_1, tuple_c_4_1, epsilon)

		print(res, norm([gen_sol[0] - res[0][0], gen_sol[1] - res[0][1]]) < epsilon)
	'''
