from Rational_numbers import RatNum as rn
from numpy import array, vstack

def get_min_row_coef_index(matrix : array, row_index : int, banned_clm : list = []):
	row = matrix[row_index, :]
	min_num = 0
	res_index = -1
	for id_clm in range(1, len(row)):
		if id_clm in banned_clm: continue
		if row[id_clm] < min_num:
			min_num = row[id_clm]
			res_index = id_clm
	return res_index

def get_colomn_elem_index(matrix : array, clm_index : int, offset : int = 1):
	colomn = matrix[:, clm_index]
	min_div = 100000000
	res_index = -1
	for id_num in range(offset, len(colomn)):
		if colomn[id_num] > 0 and matrix[id_num, 0] / colomn[id_num] < min_div:
			min_div = matrix[id_num, 0] / colomn[id_num]
			res_index = id_num
	return res_index

def transform_matrix(matrix : array, row : int, clm : int, offset : int):
	matrix[row, :] /= matrix[row, clm]

	for id_row in [i if i != row else None for i in range(offset, matrix.shape[0])]:
		if id_row == None: continue
		matrix[id_row, :] -= matrix[row, :] * matrix[id_row, clm]

def print_matrix(matrix : array):
	max_str_len = 0
	for row in range(matrix.shape[0]):
		for clm in range(matrix.shape[1]):
			max_str_len = max(max_str_len, len(str(matrix[row, clm])))

	for row in range(matrix.shape[0]):
		for clm in range(matrix.shape[1]):
			print(str(matrix[row, clm]) + " "*(max_str_len - len(str(matrix[row, clm])) + 2), end = '')
		print()
	print()

def input_matrix():
	size = int(input("Укажите количество строк матрицы: "))
	print("Вводите строки: ")
	
	lists = []
	rn_lambda = lambda x: rn(str_num = x)
	for i in range(size):
		lists += [list(map(rn_lambda, input(f"{i+1} строка: ").split(" ")))]
	lists = array(lists)

	index_basic_clm = []
	for i in range(1, lists.shape[0]):
		for j in range(1, lists.shape[1]):
			if lists[i, j] == 1:
				in_basic = True

				for k in range(len(lists[:, j])):
					if lists[k, j] != 0 and k != i:
						in_basic = False
						break

				if in_basic: 
					index_basic_clm += [j]
					break

	index_artif_clm = input("Введите номера искусственных переменных(Enter - пропуск): ").split(" ")
	if index_artif_clm[0] != '': index_artif_clm = list(map(int, index_artif_clm))
	else: index_artif_clm = []

	print()
	Distributor(lists, index_basic_clm, index_artif_clm)

def one_phase_simplex_method(matrix : array, index_basic_clm : list):

	print("------ Однофазный симплекс метод -------\n")
	print_matrix(matrix)

	while True:
		clm = get_min_row_coef_index(matrix, 0) 
			# находим в строке минимальный отрацательный элемент

		if clm == -1: 
			# если нет отрицательных элементов

			print("----------- Система оптимальна ---------")
			print("------- Значения базисного вектора -----\n")

			for i in range(len(index_basic_clm)):
				print(f"{index_basic_clm[i]} = {matrix[i + 1, 0]}")

			print()
			print(f"-------- Значение целевой функции: {matrix[0, 0]}")
			break
		else:
			# находим ведущий элемент
			row = get_colomn_elem_index(matrix, clm)

			if row == -1:
				# если нет положительных коэффициентов в столбце
				print("-------- Решение не ограничено --------")
				break

			else:
				# меняем базисный вектор
				print(f"<Вводим в базис {clm}. Выводим из базиса {index_basic_clm[row - 1]}>")
				index_basic_clm[row - 1] = clm

				# преобразуем матрицу
				transform_matrix(matrix, row, clm, 0)
				print_matrix(matrix)

def two_phase_simplex_method(matrix : array, index_basic_clm : list, index_artif_clm : list):

	# пересекаем все искусственные переменные и базисные
	artif_index_in_basic = []
	for j in index_artif_clm:
		if j in index_basic_clm: artif_index_in_basic += [j]

	# считаем строку новой целевой функции
	matrix = vstack([[-sum([matrix[index_basic_clm.index(j) + 1, i] for j in artif_index_in_basic]) \
		if i not in index_artif_clm else 0 for i in range(matrix.shape[1])], matrix])

	print("------ Двухфазный симплекс метод ------")
	print("--------------- I этап ----------------\n")
	print_matrix(matrix)

	offset_target = 0
	true_target = False

	while True:
		clm = get_min_row_coef_index(matrix, offset_target, index_artif_clm) 
			# находим в строке минимальный отрацательный элемент

		if clm == -1: 
			# если нет отрицательных элементов

			if true_target == False:

				# если оптимизировали первую целевую функцию
				if matrix[0, 0] != 0:
					# если не удалось оптимизировать
					print("-------- Нет допустимых решений --------")
					break

				# заменяем искусственные переменные, если они в базисе
				for i in index_artif_clm:
					if i in index_basic_clm:
						# если среди базисных есть искусственные переменные

						ind_row = index_basic_clm.index(i) + 2

						# ищем основную переменную для замены, если возможно заменяем
						for j in range(len(matrix[ind_row, :])):
							if matrix[ind_row, j] != 0 and j not in index_artif_clm:

								print(f"<Вводим в базис {j}. Выводим из базиса {index_basic_clm[ind_row - 2]}>")
								index_basic_clm[ind_row - 2] = j

								transform_matrix(matrix, ind_row, j, 0)
								print_matrix(matrix)
								break

				# начинаем оптимизировать вторую целевую функцию
				true_target = True
				offset_target = 1

				print("--------------- II этап ----------------\n")

			else:
				# если оптимизировали вторую целевую функцию
				print("----------- Система оптимальна ---------")
				print("------- Значения базисного вектора -----\n")

				for i in range(len(index_basic_clm)):
					print(f"{index_basic_clm[i]} = {matrix[i + 2, 0]}")

				print()
				print(f"-------- Значение целевой функции: {matrix[1, 0]}")
				break
		else:
			# находим ведущий элемент
			row = get_colomn_elem_index(matrix, clm, 2)

			if row == -1:
				# если нет положительных коэффициентов в столбце
				print("-------- Решение не ограничено --------")
				break
			else:
				# меняем базисный вектор
				print(f"<Вводим в базис {clm}. Выводим из базиса {index_basic_clm[row - 2]}>")
				index_basic_clm[row - 2] = clm

				# преобразуем матрицу
				transform_matrix(matrix, row, clm, offset_target)
				print_matrix(matrix)

def Distributor(matrix : array, index_basic_clm : list, index_artif_clm : list):
	
	if index_artif_clm != []: two_phase_simplex_method(matrix, index_basic_clm, index_artif_clm)
	else: one_phase_simplex_method(matrix, index_basic_clm)

input_matrix()