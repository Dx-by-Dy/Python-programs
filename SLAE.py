from numpy import *
from mpmath import *
import matplotlib.pyplot as plt

mp.dps = 50

def norm_inf(A : array) -> mpf: # Норма бесконечность матрицы
	dim = len(A)

	max_value = -inf
	for i in range(dim):
		sm = 0
		for j in range(dim):
			sm += abs(A[i, j])
		max_value = max(max_value, sm)

	return max_value

def norm_inf_vec(x : array) -> mpf: # Норма бесконечность вектора 
	max_value = -inf
	for i in x:
		max_value = max(max_value, abs(i[0]))

	return max_value

def Gauss_method(A : array, b : array) -> array: # Метод Жордана-Гаусса
	dim = len(A)
	x = array([[0] for j in range(dim)], dtype = mpf)

	for i in range(dim):

		if A[i, i] == 0:
			for k in range(i+1, dim):
				if A[k, i] != 0:
					row = array(A[i, :])
					A[i, :] = A[k, :]
					A[k, :] = row
					b[k, 0], b[i, 0] = b[i, 0], b[k, 0]
					break

		for j in range(dim):
			if i != j:
				b[j, 0] -= mpf(A[j, i]/A[i, i])*b[i, 0]
				A[j, :] -= mpf(A[j, i]/A[i, i])*A[i, :]

	for i in range(dim):
		x[i, 0] = b[i, 0]/A[i, i]

	return x

def print_vec(arg : array) -> None:
	print("[")
	for i in range(len(arg)):
		nprint(mpf(arg[i][0]))
		#if i != len(arg) - 1: print(", ", end="")
	print("]\n")

def easy_iterat_method(accuracy: mpf, A : array, b : array) -> array: # Метод простых итераций
	#global lst_cnt 

	dim = len(A)
	u_coef = mpf(1/norm_inf(A))
	cnt = 0

	B = array([[0 for i in range(dim)] for j in range(dim)], dtype = mpf)
	for i in range(dim):
		B[i, i] = 1

	B -= u_coef*A
	c = u_coef*b
	new_x = c
	old_x = array([[-inf] for j in range(dim)], dtype = mpf)

	b_coef = mpf(norm_inf(B)/(1 - norm_inf(B)))
	print(norm_inf(B))

	while abs(b_coef*norm_inf_vec(new_x - old_x)) > accuracy:
		old_x = new_x
		new_x = dot(B, new_x) + c
		#cnt += 1

	#lst_cnt += [cnt]
	return new_x

if __name__ == "__main__":

	A = array([[0 for i in range(3)] for j in range(3)], dtype = mpf)
	b = array([[12], [14], [16]], dtype = mpf)
		
	for i in range(3):
		for j in range(3):
			if i != j: A[i, j] = 1
			else: A[i, j] = 8 + (i+1)*2

	print_vec(Gauss_method(A.copy(), b.copy()))
	print_vec(easy_iterat_method(1e-10, A.copy(), b.copy()))

	#ax, lst_cnt = [], []

	#for i in range(3, 21):
		#ax += [i]
		#print_vec(easy_iterat_method(10**(-i), A.copy(), b.copy()))

	dim = 10
	epsilon = 8*1e-4
	A = array([[0 for i in range(dim)] for j in range(dim)], dtype = mpf)
	b = array([[-1] for i in range(dim)], dtype = mpf)
	b[-1] = [1]

	for i in range(dim):
		for j in range(dim):
			if i == j: A[i, j] = 1 + epsilon
			elif j > i: A[i, j] = -1 - epsilon
			else: A[i, j] = epsilon

	#b = dot(transpose(A), b)
	#A = dot(transpose(A), A)

	print_vec(Gauss_method(A.copy(), b.copy()))
	print_vec(easy_iterat_method(1e-10, A.copy(), b.copy()))

	#for i in range(21, 21):
		#ax += [i]
		#print_vec(easy_iterat_method(10**(-i), A.copy(), b.copy()))

	"""
	plt.subplot(111)
	plt.plot(ax, lst_cnt, "r")
	plt.title("Количество итераций от требуемой точности")
	plt.xlabel("Требуемоая точность")
	plt.ylabel("Количество итераций")

	plt.subplots_adjust(bottom=0.05, left=0.05, right=0.95, top=0.95)

	plt.show()
	"""
