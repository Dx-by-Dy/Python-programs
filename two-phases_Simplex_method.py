from Rational_numbers import RatNum as rn
from numpy import array, vstack, delete

def get_min_row_coef_index(matrix : array, index_artif_clm : list, offset : int):
	row = matrix[offset, :]
	min_num = 0
	min_index = -1
	for id_num in range(1, len(row)):
		if id_num in index_artif_clm: continue
		if row[id_num] < min_num:
			min_num = row[id_num]
			min_index = id_num
	return min_index

def get_colomn_elem_index(matrix : array, clm : int, offset : int):
	colomn = matrix[:, clm]
	min_div = 100000000
	index = -1
	for id_num in range(offset, len(colomn)):
		if colomn[id_num] > 0 and matrix[id_num, 0] / colomn[id_num] < min_div:
			min_div = matrix[id_num, 0] / colomn[id_num]
			index = id_num
	return index

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
	index_basic_clm = list(map(int, input("Введите номера базисных переменных: ").split(" ")))
	index_artif_clm = list(map(int, input("Введите номера искусственных переменных: ").split(" ")))
	print()
	Two_phase_simplex_method(array(lists), index_basic_clm, index_artif_clm)

def Two_phase_simplex_method(matrix : array, index_basic_clm : list, index_artif_clm : list):
	
	matrix = vstack([[-sum([matrix[index_basic_clm.index(j) + 1, i] for j in index_artif_clm]) if i not in index_artif_clm else 0 for i in range(matrix.shape[1])], matrix])
		# считаем строку новой целевой функции

	print("--------------- I этап ---------------- \n")
	print_matrix(matrix)

	offset_target = 2
	true_target = False

	while True:
		clm = get_min_row_coef_index(matrix, index_artif_clm, 2 - offset_target) 
			# находим в строке минимальный отрацательный элемент

		if clm == -1: 
			# если нет отрицательных элементов

			if true_target == False:
				# если оптимизировали первую целевую функцию
				if matrix[0, 0] != 0:
					print_matrix(matrix)
					print(matrix[0, 0] == 0)
					# если не удалось оптимизировать
					print("-------- Нет допустимых решений --------")
					break

				# заменяем искусственные переменные, если они в базисе
				for i in index_artif_clm:
					if i in index_basic_clm:
						ind_row = index_basic_clm.index(i) + 2
						for j in range(len(matrix[ind_row, :])):
							if matrix[ind_row, j] != 0:
								index_basic_clm[row - 2] = j
								transform_matrix(matrix, ind_row, j, 2 - offset_target)
								break

				# начинаем оптимизировать вторую целевую функцию
				true_target = True
				offset_target = 1

				print("--------------- II этап ----------------\n")
			else:
				# если оптимизировали вторую целевую функцию
				print("----------- Система оптимальна ---------")
				print("------- Значения базисного вектора -----")
				for i in index_basic_clm:
					print(f"{i} = {matrix[index_basic_clm.index(i) + 2, 0]}")
				print()
				print(f"-------- Значение целевой фукнции: {matrix[1, 0]}")
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
				index_basic_clm[row - 2] = clm

				# преобразуем матрицу
				transform_matrix(matrix, row, clm, 2 - offset_target)
				print_matrix(matrix)

input_matrix()