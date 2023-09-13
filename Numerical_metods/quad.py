from mpmath import *
import matplotlib.pyplot as plt

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

def Gauss(a : mpf, b : mpf, count_of_separation : mpf, count_of_nodes : mpf = 3) -> mpf:
	step = (b-a)/count_of_separation
	local_step = step/(count_of_nodes-1)
	result = 0

	for iterat in range(count_of_separation):
		points = [a + iterat*step + cnt*local_step for cnt in range(count_of_nodes)]
		weight_moment = get_moments(points[0], points[-1], 2*count_of_nodes)

		matrix_a = matrix([[weight_moment[i+j] for i in range(count_of_nodes)] for j in range(count_of_nodes)])
		free_vector = matrix([-weight_moment[count_of_nodes+i] for i in range(count_of_nodes)])

		coefs_nodes_polinoms = lu_solve(matrix_a, free_vector)

		q_coef = (2*coefs_nodes_polinoms[2]**3/27 - coefs_nodes_polinoms[2]*coefs_nodes_polinoms[1]/3 + coefs_nodes_polinoms[0])/2
		p_coef = (3*coefs_nodes_polinoms[1] - coefs_nodes_polinoms[2]**2)/9
		r_coef = abs(p_coef)**0.5*sign(q_coef)

		if q_coef != 0: 
			phi_coef = acos(q_coef/r_coef**3)
		else: 
			r_coef = abs(p_coef)**0.5
			phi_coef = acos(0)

		roots_of_nodes_polinoms = sorted([-2*r_coef*cos(phi_coef/3) - coefs_nodes_polinoms[2]/3, 2*r_coef*cos((pi-phi_coef)/3) - coefs_nodes_polinoms[2]/3, 2*r_coef*cos((pi+phi_coef)/3) - coefs_nodes_polinoms[2]/3])
		matrix_A = matrix([[roots_of_nodes_polinoms[i]**j for i in range(count_of_nodes)] for j in range(count_of_nodes)])

		coefs_A = lu_solve(matrix_A, weight_moment[:count_of_nodes])
		for id_coef_A in range(count_of_nodes):
			result += coefs_A[id_coef_A]*func(roots_of_nodes_polinoms[id_coef_A])

	return result

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

def Aitken_process(coef_of_splitting : mpf, type_method : str) -> int:
	coef_of_splitting = coef_of_splitting - coef_of_splitting%4

	if type_method == 'Newton_Cotes':
		value_int_3 = Newton_Cotes(a, b, coef_of_splitting, 3)
		value_int_2 = Newton_Cotes(a, b, coef_of_splitting//2, 3)
		value_int_1 = Newton_Cotes(a, b, coef_of_splitting//4, 3)

	elif type_method == 'Gauss':
		value_int_3 = Gauss(a, b, coef_of_splitting)
		value_int_2 = Gauss(a, b, coef_of_splitting//2)
		value_int_1 = Gauss(a, b, coef_of_splitting//4)

	return -log(abs((value_int_3 - value_int_2)/(value_int_2 - value_int_1)))/log(2)

def get_optimal_step(ADA : mpf, best_err_rate : mpf, count_of_separation : mpf) -> mpf:
	step = (b-a)/count_of_separation
	return step*(epsilon/best_err_rate)**(1/ADA)

def get_result_with_optimal_step(optimal_step : mpf, type_method : str) -> mpf:

	if optimal_step < 0.01: return None

	count_of_separation = int((b-a)/optimal_step) + 4 - int((b-a)/optimal_step)%4
	value_integr = []

	for i in range(3):
		if type_method == 'Newton_Cotes': value_integr += [Newton_Cotes(a, b, count_of_separation, 3)]
		if type_method == 'Gauss': value_integr += [Gauss(a, b, count_of_separation)]
		count_of_separation *= 2

	while True:
		score_rate = score_err_rate(value_integr, Aitken_process(count_of_separation, type_method), type_method)

		for i in range(len(score_rate)):
			if score_rate[i] < epsilon:
				return ((b-a)/ (count_of_separation//(2**(len(score_rate)-i))) )

		if type_method == 'Newton_Cotes': value_integr += [Newton_Cotes(a, b, count_of_separation, 3)]
		if type_method == 'Gauss': value_integr += [Gauss(a, b, count_of_separation)]

def score_err_rate(list_of_value_integr : list[mpf], ADA : mpf, type_method : str, offset_h : mpf = 0) -> list[mpf]:
	global verified_value_of_int_func, verified_value_of_int_full_func, step_epsilon_Newton_Cotes, step_epsilon_Gauss, \
		cnt_epsilon_Newton_Cotes, cnt_epsilon_Gauss

	cnt_value = len(list_of_value_integr)
	err_rate = [0]*cnt_value

	if cnt_value >= 5 and cnt_value%5 == 0:

		deg_system = 5
		for iterat in range(cnt_value//deg_system):
			matrix_A = matrix([[((b-a)/(offset_h+j+1))**(ADA+i) if i != deg_system-1 else -1 for i in range(deg_system)] for j in range(deg_system*iterat, deg_system*(iterat+1))])
			b_vector = matrix([-list_of_value_integr[i] for i in range(deg_system*iterat, deg_system*(iterat+1))])

			err_rate_coef = lu_solve(matrix_A, b_vector)

			for i in range(deg_system):
				for j in range(deg_system-1):
					err_rate[deg_system*iterat + i] += err_rate_coef[j]*matrix_A[i, j]
				err_rate[deg_system*iterat + i] = abs(err_rate[deg_system*iterat + i])

				if type_method in ['trapezoid', 'Simpsons']: verified_value_of_int_func = err_rate[deg_system*iterat + i] + list_of_value_integr[deg_system*iterat + i]
				else: 
					verified_value_of_int_full_func = err_rate[deg_system*iterat + i] + list_of_value_integr[deg_system*iterat + i]
					if type_method == 'Newton_Cotes' and err_rate[deg_system*iterat + i] < epsilon and step_epsilon_Newton_Cotes == None: 
						step_epsilon_Newton_Cotes = (b-a)/(offset_h + deg_system*iterat + i + 1)
						cnt_epsilon_Newton_Cotes = offset_h + deg_system*iterat + i + 1
					elif type_method == 'Gauss' and err_rate[deg_system*iterat + i] < epsilon and step_epsilon_Gauss == None: 
						step_epsilon_Gauss = (b-a)/(offset_h + deg_system*iterat + i + 1)
						cnt_epsilon_Gauss = offset_h + deg_system*iterat + i + 1

				#err_rate[5*iterat + i] = abs(err_rate_coef[4] - list_of_value_integr[5*iterat + i])

	else:

		deg_system = cnt_value
		matrix_A = matrix([[((b-a)/(offset_h+j+1))**(ADA+i) if i != deg_system-1 else -1 for i in range(deg_system)] for j in range(0, deg_system)])
		b_vector = matrix([-list_of_value_integr[i] for i in range(0, deg_system)])

		err_rate_coef = lu_solve(matrix_A, b_vector)

		for i in range(deg_system):
			for j in range(deg_system-1):
				err_rate[i] += err_rate_coef[j]*matrix_A[i, j]
			err_rate[i] = abs(err_rate[i])

	return err_rate

def grafics(index : int) -> None:
	global err_rate_left_rect, err_rate_right_rect, err_rate_average_rect, err_rate_trapezoid, err_rate_Simpsons

	plt.ion()
	axis.clear()

	if index == 0:

		log_func = lambda x: log(x, 10)
		ax = [i+1 for i in range(max_count_of_separation_for_index_0)]
		x_ax = [1] + [10*(i+1) for i in range(max_count_of_separation_for_index_0//10)]

		axis.plot(ax, list(map(log_func, err_rate_left_rect)), "g", label = "Левый прямоугольник")
		axis.plot(ax, list(map(log_func, err_rate_right_rect)), "r", label = "Правый прямоугольник")
		axis.plot(ax, list(map(log_func, err_rate_average_rect)), "k", label = "Средний прямоугольник")
		axis.set_title("Степень погрешности левого, правого и среднего прямоульных формул от эталонных формул")
		axis.set_xlabel("Количество разбиений")
		axis.set_ylabel("Степень погрешности")
		axis.set_xticks(x_ax, x_ax)
		axis.grid()
		axis.legend()

	elif index == 1:

		log_func = lambda x: log(x, 10)
		ax = [i+1 for i in range(max_count_of_separation_for_index_1)]
		x_ax = [1] + [10*(i+1) for i in range(max_count_of_separation_for_index_1//10)]

		axis.plot(ax, list(map(log_func, err_rate_trapezoid)), "g", label = "Степень погрешности формулы трапеции от эталонной")
		#axis.plot(ax, list(map(log_func, score_err_rate_for_trapezoid)), "--k", label = "Степень погрешности формулы трапеции по Ричардсону")
		axis.plot(ax, list(map(log_func, err_rate_Simpsons)), "r", label = "Степень погрешности формула Симпсона от эталонной")
		#axis.plot(ax, list(map(log_func, score_err_rate_for_Simpsons)), "--b", label = "Степень погрешности формулы Симпсона по Ричардсону")
		#axis.plot(ax, [log(abs(quad(func, [a, b]) - verified_value_of_int_func), 10)]*max_count_of_separation_for_index_1, 'k', label = 'Степень погрешности уточненного значения интеграла от эталонного')
		axis.set_title("Степень погрешности формулы трапеции и формулы Симпсона от эталонных формул и оценка погрешности")
		axis.set_xlabel("Количество разбиений")
		axis.set_ylabel("Степень погрешности")
		axis.set_xticks(x_ax, x_ax)
		axis.grid()
		axis.legend()

	elif index == 2:

		log_func = lambda x: log(x, 10)
		ax = [i+1 for i in range(max_count_of_separation_for_index_2)]
		x_ax = [1] + [10*(i+1) for i in range(max_count_of_separation_for_index_2//10)]
		if cnt_epsilon_Newton_Cotes != None: x_ax = sorted(x_ax + [cnt_epsilon_Newton_Cotes])
		if cnt_epsilon_Gauss != None: x_ax = sorted(x_ax + [cnt_epsilon_Gauss])

		optimal_step_Newton_Cotes = get_optimal_step(Aitken_process(max_count_of_separation_for_index_2, 'Newton_Cotes'), score_err_rate_for_Newton_Cotes[-1], max_count_of_separation_for_index_2)
		optimal_step_Gauss = get_optimal_step(Aitken_process(max_count_of_separation_for_index_2, 'Gauss'), score_err_rate_for_Gauss[-1], max_count_of_separation_for_index_2)
		new_optimal_step_Newton_Cotes = get_result_with_optimal_step(optimal_step_Newton_Cotes, 'Newton_Cotes')
		new_optimal_step_Gauss = get_result_with_optimal_step(optimal_step_Gauss, 'Gauss')

		#new_optimal_step_Newton_Cotes = 0
		#new_optimal_step_Gauss = 0

		axis.plot(ax, list(map(log_func, err_rate_Newton_Cotes)), "g", label = "Степень погрешности формулы Ньютона-Котеса от эталонной")
		axis.plot(ax, list(map(log_func, score_err_rate_for_Newton_Cotes)), "--k", label = "Степень погрешности формулы Ньютона-Котеса по Ричардсону")
		axis.plot(ax, list(map(log_func, err_rate_Gauss)), "r", label = "Степень погрешности формулы Гаусса от эталонной")
		axis.plot(ax, list(map(log_func, score_err_rate_for_Gauss)), "--b", label = "Степень погрешности формулы Гаусса по Ричардсону")
		axis.plot(ax, [log(abs(quad(full_func, [a, b]) - verified_value_of_int_full_func), 10)]*max_count_of_separation_for_index_2, 'k', label = 'Степень погрешности уточненного значения интеграла от эталонного')
		axis.plot(ax, list(map(log_func, [epsilon]*max_count_of_separation_for_index_2)), "m", label = "Требуемая степень точности ($\\epsilon = { 10}^{" + str(int(log(epsilon, 10))) +"}, h_{ opt}^{ N-C} ≈ " + nstr(optimal_step_Newton_Cotes, 3) +" \\rightarrow h_{ \\epsilon \\_ opt}^{ N-C} ≈ " + nstr(new_optimal_step_Newton_Cotes, 3) + ", h_{ opt}^{ G} ≈ " + nstr(optimal_step_Gauss, 3) + "\\rightarrow h_{ \\epsilon \\_ opt}^{ G} ≈ " + nstr(new_optimal_step_Gauss, 3) + "$)")
		axis.set_title("Степень погрешности формулы Ньютона-Котеса(ПП ≈ " + nstr(Aitken_process(max_count_of_separation_for_index_2, 'Newton_Cotes'), 3) + ", $h_\\epsilon$ = " + nstr(step_epsilon_Newton_Cotes, 3) + ") и формулы Гаусса(ПП ≈ " + nstr(Aitken_process(max_count_of_separation_for_index_2, 'Gauss'), 3) + ", $h_\\epsilon$ = " + nstr(step_epsilon_Gauss, 3) + ") от эталонных формул и оценка погрешности")
		axis.set_xlabel("Количество разбиений")
		axis.set_ylabel("Степень погрешности")
		axis.set_xticks(x_ax, x_ax)
		axis.grid()
		axis.legend()

	plt.draw()
	plt.ioff()

def key_event(event) -> None:
	global index, max_count_of_separation_for_index_0, max_count_of_separation_for_index_1, \
		max_count_of_separation_for_index_2, err_rate_left_rect, err_rate_right_rect, err_rate_average_rect, \
		err_rate_trapezoid, err_rate_Simpsons, err_rate_Newton_Cotes, err_rate_Gauss, \
		value_int_with_left_rect, value_int_with_right_rect, value_int_with_average_rect, value_int_with_trapezoid, \
		value_int_with_Simpsons, value_int_with_Newton_Cotes, value_int_with_Gauss, score_err_rate_for_trapezoid, \
		score_err_rate_for_Simpsons, score_err_rate_for_Newton_Cotes, score_err_rate_for_Gauss

	key = getattr(event, 'key')

	if key == 'right': index = (index + 1)%3
	elif key == 'left': index = (index - 1)%3
	elif key == 'up': 
		if index == 0: 
			value_int_with_left_rect += [left_rect(a, b, max_count_of_separation_for_index_0+i+1) for i in range(10)]
			value_int_with_right_rect += [right_rect(a, b, max_count_of_separation_for_index_0+i+1) for i in range(10)]
			value_int_with_average_rect += [average_rect(a, b, max_count_of_separation_for_index_0+i+1) for i in range(10)]

			err_rate_left_rect += [abs(int_value_for_func - value_int_with_left_rect[max_count_of_separation_for_index_0 + i]) for i in range(10)]
			err_rate_right_rect += [abs(int_value_for_func - value_int_with_right_rect[max_count_of_separation_for_index_0 + i]) for i in range(10)]
			err_rate_average_rect += [abs(int_value_for_func - value_int_with_average_rect[max_count_of_separation_for_index_0 + i]) for i in range(10)]
			max_count_of_separation_for_index_0 += 10
		elif index == 1: 
			value_int_with_trapezoid += [trapezoid(a, b, max_count_of_separation_for_index_1+i+1) for i in range(10)]
			value_int_with_Simpsons += [Simpsons(a, b, max_count_of_separation_for_index_1+i+1) for i in range(10)]

			#score_err_rate_for_trapezoid += score_err_rate(value_int_with_trapezoid[max_count_of_separation_for_index_1:], 2, 'trapezoid', max_count_of_separation_for_index_1)
			#score_err_rate_for_Simpsons += score_err_rate(value_int_with_Simpsons[max_count_of_separation_for_index_1:], 3, 'Simpsons', max_count_of_separation_for_index_1)

			err_rate_trapezoid += [abs(int_value_for_func - value_int_with_trapezoid[max_count_of_separation_for_index_1 + i]) for i in range(10)]
			err_rate_Simpsons += [abs(int_value_for_func - value_int_with_Simpsons[max_count_of_separation_for_index_1 + i]) for i in range(10)]
			max_count_of_separation_for_index_1 += 10
		elif index == 2:
			value_int_with_Newton_Cotes += [Newton_Cotes(a, b, max_count_of_separation_for_index_2+i+1, 3) for i in range(10)]
			value_int_with_Gauss += [Gauss(a, b, max_count_of_separation_for_index_2+i+1) for i in range(10)]

			score_err_rate_for_Newton_Cotes += score_err_rate(value_int_with_Newton_Cotes[max_count_of_separation_for_index_2:], Aitken_process(max_count_of_separation_for_index_2, 'Newton_Cotes'), 'Newton_Cotes', max_count_of_separation_for_index_2)
			score_err_rate_for_Gauss += score_err_rate(value_int_with_Gauss[max_count_of_separation_for_index_2:], Aitken_process(max_count_of_separation_for_index_2, 'Gauss'), 'Gauss', max_count_of_separation_for_index_2)

			err_rate_Newton_Cotes += [abs(int_value_for_full_func - value_int_with_Newton_Cotes[max_count_of_separation_for_index_2 + i]) for i in range(10)]
			err_rate_Gauss += [abs(int_value_for_full_func - value_int_with_Gauss[max_count_of_separation_for_index_2 + i]) for i in range(10)]
			max_count_of_separation_for_index_2 += 10

	grafics(index)

if __name__ == "__main__":

	func = lambda x: 3*cos(0.5*x)*exp(x/4) + 5*sin(2.5*x)*exp(-x/3) + 2*x
	#func = lambda x: 2 * cos(2.5 * x) * exp(x / 3) + 4 * sin(3.5 * x) * exp(-3 * x) + x

	mp.dps = 30
	a, b = mpf(1), mpf(4)
	alpha, bbeta = mpf(0), mpf(0.25)
	max_count_of_separation_for_index_0 = 10
	max_count_of_separation_for_index_1 = 10
	max_count_of_separation_for_index_2 = 10
	index = 0

	weight_func = lambda x: 1/((b-x)**bbeta)
	full_func = lambda x: func(x)*weight_func(x)

	int_value_for_func = quad(func, [a, b])
	int_value_for_full_func = quad(full_func, [a, b])
	verified_value_of_int_func = None
	verified_value_of_int_full_func = None
	epsilon = 1e-6

	step_epsilon_Newton_Cotes = None
	step_epsilon_Gauss = None
	cnt_epsilon_Newton_Cotes = None
	cnt_epsilon_Gauss = None
	#print(quad(full_func, [a, b], error = True))

	value_int_with_left_rect = [left_rect(a, b, i+1) for i in range(max_count_of_separation_for_index_0)]
	value_int_with_right_rect = [right_rect(a, b, i+1) for i in range(max_count_of_separation_for_index_0)]
	value_int_with_average_rect = [average_rect(a, b, i+1) for i in range(max_count_of_separation_for_index_0)]
	value_int_with_trapezoid = [trapezoid(a, b, i+1) for i in range(max_count_of_separation_for_index_1)]
	value_int_with_Simpsons = [Simpsons(a, b, i+1) for i in range(max_count_of_separation_for_index_1)]
	value_int_with_Newton_Cotes = [Newton_Cotes(a, b, i+1, 3) for i in range(max_count_of_separation_for_index_2)]
	value_int_with_Gauss = [Gauss(a, b, i+1) for i in range(max_count_of_separation_for_index_2)]

	#score_err_rate_for_trapezoid = score_err_rate(value_int_with_trapezoid, 2, 'trapezoid')
	#score_err_rate_for_Simpsons = score_err_rate(value_int_with_Simpsons, 3, 'Simpsons')
	score_err_rate_for_Newton_Cotes = score_err_rate(value_int_with_Newton_Cotes, Aitken_process(max_count_of_separation_for_index_2, 'Newton_Cotes'), 'Newton_Cotes')
	score_err_rate_for_Gauss = score_err_rate(value_int_with_Gauss, Aitken_process(max_count_of_separation_for_index_2, 'Gauss'), 'Gauss')

	err_rate_left_rect = [abs(int_value_for_func - value_int_with_left_rect[i]) for i in range(max_count_of_separation_for_index_0)]
	err_rate_right_rect = [abs(int_value_for_func - value_int_with_right_rect[i]) for i in range(max_count_of_separation_for_index_0)]
	err_rate_average_rect = [abs(int_value_for_func - value_int_with_average_rect[i]) for i in range(max_count_of_separation_for_index_0)]
	err_rate_trapezoid = [abs(int_value_for_func - value_int_with_trapezoid[i]) for i in range(max_count_of_separation_for_index_1)]
	err_rate_Simpsons = [abs(int_value_for_func - value_int_with_Simpsons[i]) for i in range(max_count_of_separation_for_index_1)]
	err_rate_Newton_Cotes = [abs(int_value_for_full_func - value_int_with_Newton_Cotes[i]) for i in range(max_count_of_separation_for_index_2)]
	err_rate_Gauss = [abs(int_value_for_full_func - value_int_with_Gauss[i]) for i in range(max_count_of_separation_for_index_2)]

	fg, axis = plt.subplots(nrows= 1, ncols= 1, figsize=(15, 8))
	fg.subplots_adjust(bottom=0.1, left=0.06, right=0.98, top=0.95, hspace=0.3)
	fg.canvas.mpl_connect('key_release_event', key_event)

	grafics(index)

	plt.show()