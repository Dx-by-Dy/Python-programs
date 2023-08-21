from mpmath import *
from functools import lru_cache
import sys
import matplotlib.pyplot as plt
from numpy import arange

@lru_cache()
def my_pow(arg : mpf, st : int) -> mpf:		# функция подсчета натуральной степени любого аргумента
	if st < 0: return 1/my_pow(arg, -st)
	if arg == 1: return 1
	elif arg == -1:
		if st % 2 == 0: return 1
		else: return -1
	elif st == 0: return 1
	elif st == 1: return mpf(arg)
	elif st == 2: return mpf(arg)*mpf(arg)
	else: 
		if st % 2 == 0: return mpf(my_pow(arg, st//2))*mpf(my_pow(arg, st//2))
		else: return mpf(my_pow(arg, st//2))*mpf(my_pow(arg, st//2))*mpf(arg)

def sgn(arg : mpf) -> int:				# функция подсчета знака числа
	if arg > 0: return 1
	elif arg < 0: return -1
	else: return 0

@lru_cache()
def my_fact(arg : int) -> int:			# функция подсчета факториала
	if arg == 0 or arg == 1: return 1
	return arg*my_fact(arg-1)

def my_cos(arg : mpf, list_cnt_term = [], accuracy : mpf = 1e-6) -> mpf:  # функция подсчета cos(x) через ряд Тейлора

	arg = arg - int(arg/(2*PI))*2*PI
	sum_term = 0
	cnt_term = 0
	term = 0
	
	if abs(arg) <= PI/4:
		value_term = my_pow(-1, term)*my_pow(arg, 2*term)/my_fact(2*term)

		while abs(value_term) > accuracy:
			sum_term += value_term
			cnt_term += 1
			term += 1
			value_term = my_pow(-1, term)*my_pow(arg, 2*term)/my_fact(2*term)

		list_cnt_term += [cnt_term]

		return sum_term

	return my_sqrt(2)/2*(my_cos(arg - PI/4, list_cnt_term, accuracy) - my_sin(arg - PI/4, list_cnt_term, accuracy))

def my_sin(arg : mpf, list_cnt_term = [], accuracy : mpf = 1e-6) -> mpf:  # функция подсчета sin(x) через ряд Тейлора

	arg = arg - int(arg/(2*PI))*2*PI
	sum_term = 0
	cnt_term = 0
	term = 0

	if abs(arg) <= PI/4:
		value_term = my_pow(-1, term)*my_pow(arg, 2*term + 1)/my_fact(2*term + 1)

		while abs(value_term) > accuracy:
			sum_term += value_term
			cnt_term += 1
			term += 1
			value_term = my_pow(-1, term)*my_pow(arg, 2*term + 1)/my_fact(2*term + 1)

		list_cnt_term += [cnt_term]

		return sum_term

	return my_sqrt(2)/2*(my_sin(arg - PI/4, list_cnt_term, accuracy) + my_cos(arg - PI/4, list_cnt_term, accuracy))

def my_atan(arg : mpf, list_cnt_term = [], accuracy : mpf = 1e-6) -> mpf:  # функция подсчета atan(x) через ряд Тейлора
	cnt_term = 0
	term = 0

	if abs(arg) < 1: 
		sum_term = 0
		value_term = mpf(my_pow(-1, term)*my_pow(arg, 2*term + 1)/(2*term + 1))

		while abs(value_term) > accuracy:
			sum_term += value_term
			cnt_term += 1
			term += 1
			value_term = mpf(my_pow(-1, term)*my_pow(arg, 2*term + 1)/(2*term + 1))

		list_cnt_term += [cnt_term]

		return sum_term

	elif arg == 1: 
		list_cnt_term += [1]
		return PI/4
	elif arg == -1: 
		list_cnt_term += [1]
		return -PI/4

	else:
		sum_term = PI/2*sgn(arg)
		value_term = mpf(my_pow(-1, term)*my_pow(arg, -2*term - 1)/(2*term + 1))

		while abs(value_term) > accuracy:
			sum_term -= value_term
			cnt_term += 1
			term += 1
			value_term = mpf(my_pow(-1, term)*my_pow(arg, -2*term - 1)/(2*term + 1))

		list_cnt_term += [cnt_term]

		return sum_term

def my_exp(arg : mpf, list_cnt_term = [], accuracy : mpf = 1e-6) -> mpf: # функция подсчета exp(x) через ряд Тейлора
	sum_term = 0
	cnt_term = 0
	term = 0
	value_term = mpf(my_pow(arg, term)/my_fact(term))

	while abs(value_term) > accuracy:
		sum_term += value_term
		cnt_term += 1
		term += 1
		value_term = mpf(my_pow(arg, term)/my_fact(term))

	list_cnt_term += [cnt_term]

	return sum_term

def my_sqrt(arg : mpf, accuracy : mpf = 1e-6) -> mpf: # функция подсчета корня по формуле Герона
	if arg == 0: return 0
	iterat = 0.5*(max(1, arg) + arg/max(1, arg))
	last_iterat = -inf

	while abs(iterat - last_iterat) > accuracy:
		last_iterat = iterat
		iterat = mpf(0.5*(iterat + arg/iterat))

	return iterat

min_x = 0.1          # нижняя граница х
max_x = 0.2 		 # верхняя граница х
step = 0.01		     # шаг х
pwr = 6			     # степень погрешности
sys.setrecursionlimit(max(pwr*pwr, 10000))
accuracy = power(10, -pwr)
mp.dps = pwr + 5
PI = pi

def grafics():

	ax = [min_x + step*i for i in range(int((max_x - min_x) / step) + 1)]  # формируем массив точек

	abs_acc_eq_acc, abs_acc_eq_inf, abs_pwr_acc_eq_acc, abs_pwr_acc_eq_inf, ref_func_data, my_func_data_eq_acc, my_func_data_eq_inf = [], [], [], [], [], [], []
	cnt_func2_iterat_eq_acc, cnt_func2_iterat_eq_inf, cnt_func1_iterat_eq_acc, cnt_func1_iterat_eq_inf = [], [], [], []

	for x in ax:
		ref_func_data += [reference_func(x)]				# считаем данные 																		

		my_func_data_eq_acc += [my_func_eq_acc(x, cnt_func1_iterat_eq_acc, cnt_func2_iterat_eq_acc, accuracy)]
		my_func_data_eq_inf += [my_func_eq_inf(x, cnt_func1_iterat_eq_inf, cnt_func2_iterat_eq_inf, accuracy)]

		res_eq_acc = abs(ref_func_data[-1] - my_func_data_eq_acc[-1])
		res_eq_inf = abs(ref_func_data[-1] - my_func_data_eq_inf[-1])

		abs_acc_eq_acc += [res_eq_acc if res_eq_acc != 0 else accuracy*1e-10]
		abs_acc_eq_inf += [res_eq_inf if res_eq_inf != 0 else accuracy*1e-10]

		abs_pwr_acc_eq_acc += [log(res_eq_acc, 10)]
		abs_pwr_acc_eq_inf += [log(res_eq_inf, 10)]
		#nprint(res) n

	plt.subplots(figsize=(15, 8))    # рисуем графики

	plt.subplot(231)
	plt.plot(ax, ref_func_data, "g")
	plt.title("Эталонная функция")

	plt.subplot(232)
	plt.plot(ax, abs_acc_eq_acc, "r", label = "Равн. погрешности")
	plt.plot(ax, abs_acc_eq_inf, "--b", label = "Равн. влияния")
	plt.title("Абсолютная погрешность")
	plt.legend()

	plt.subplot(233)
	plt.plot(ax, cnt_func2_iterat_eq_acc, "r", label = "Равн. погрешности")
	plt.plot(ax, cnt_func2_iterat_eq_inf, "--b", label = "Равн. влияния")
	plt.title("Кол-во членов exp(2x + 1)")
	plt.legend()

	plt.subplot(234)
	plt.plot(ax, my_func_data_eq_acc, "r", label = "Равн. погрешности")
	plt.plot(ax, my_func_data_eq_inf, "--b", label = "Равн. влияния")
	plt.title("Приближенная функция")
	plt.legend()
 
	plt.subplot(235)
	plt.plot(ax, abs_pwr_acc_eq_acc, "r", label = "Равн. погрешности")
	plt.plot(ax, abs_pwr_acc_eq_inf, "--b", label = "Равн. влияния")
	plt.title("Степень погрешности")
	plt.legend()

	plt.subplot(236)
	plt.plot(ax, cnt_func1_iterat_eq_acc, "r", label = "Равн. погрешности")
	plt.plot(ax, cnt_func1_iterat_eq_inf, "--b", label = "Равн. влияния")
	plt.title("Кол-во членов atan(0.8x + 0.2)")
	plt.legend()

	plt.subplots_adjust(bottom=0.05, left=0.05, right=0.95, top=0.95)

	plt.show()

# разделение функции на 2 функции
func1 = lambda x: exp(2*x+1)
func2 = lambda x: 1+atan(0.8*x + 0.2)

# коэффициенты погрешности
c1 = max([abs(diff(lambda x, y = max([func1(i) for i in arange(min_x, max_x + step, step)]): sqrt(x)*y, func2(j))) for j in arange(min_x, max_x + step, step)])
c2 = max([abs(diff(lambda x, y = max([func2(i) for i in arange(min_x, max_x + step, step)]): sqrt(y)*x, func1(j))) for j in arange(min_x, max_x + step, step)])

# 2 вида подстчета погрешности и этелонная функция
my_func_eq_acc = lambda x, cnt_func1_term, cnt_func2_term, accuracy = 1e-6: my_sqrt(1+my_atan(0.8*x + 0.2, cnt_func1_term, accuracy/(c1+c2+1)), accuracy/(c1+c2+1))*my_exp(2*x+1, cnt_func2_term, accuracy/(c1+c2+1))
my_func_eq_inf = lambda x, cnt_func1_term, cnt_func2_term, accuracy = 1e-6: my_sqrt(1+my_atan(0.8*x + 0.2, cnt_func1_term, accuracy/(3*c1)), accuracy/3)*my_exp(2*x+1, cnt_func2_term, accuracy/(3*c2))
reference_func = lambda x: sqrt(1+atan(0.8*x + 0.2))*exp(2*x+1)

grafics()

"""func1 = lambda x: cos(7*x + 0.3)
func2 = lambda x: 1+atan(16.7*x + 0.1)

c1 = max([abs(diff(lambda x, y = min([func1(i) for i in arange(min_x, max_x + step, step)]): sqrt(x)/y, func2(j))) for j in arange(min_x, max_x + step, step)])
c2 = max([abs(diff(lambda x, y = max([func2(i) for i in arange(min_x, max_x + step, step)]): sqrt(y)/x, func1(j))) for j in arange(min_x, max_x + step, step)])

my_func_eq_acc = lambda x, cnt_func1_term, cnt_func2_term, accuracy = 1e-6: my_sqrt(1+my_atan(16.7*x + 0.1, cnt_func1_term, accuracy/(c1+c2+1)), accuracy/(c1+c2+1))/my_cos(7*x + 0.3, cnt_func2_term, accuracy/(c1+c2+1))
my_func_eq_inf = lambda x, cnt_func1_term, cnt_func2_term, accuracy = 1e-6: my_sqrt(1+my_atan(16.7*x + 0.1, cnt_func1_term, accuracy/(3*c1)), accuracy/3)/my_cos(7*x + 0.3, cnt_func2_term, accuracy/(3*c2))
reference_func = lambda x: sqrt(1+atan(16.7*x + 0.1))/cos(7*x + 0.3)

grafics()"""