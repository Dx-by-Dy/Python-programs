from numpy import matmul, transpose, eye
from numpy.linalg import inv

def Kalman_filter(X, U, Z, P, A, B, C, R, Q):
	"""
	X - Вектор состояния с прошлого шага
	U - Вектор управления
	Z - Вектор измерений
	P - Матрица погрешности с прошлого шага
	A - Матрица системы
	В - Матрица управления
	С - Матрица измерений
	R - Матрица ковариации модели
	Q - Матрица ковариации системы измерений
	"""

	dim = P.shape[0]

	X1 = matmul(A, X) + matmul(B, U)
	P1 = matmul(matmul(A, P), transpose(A)) + R

	K = matmul(matmul(P1, transpose(C)), inv(matmul(matmul(C, P1), transpose(C)) + Q))
	X = X1 + matmul(K, Z - X1)
	P = matmul(eye(dim, dim) - matmul(K, C), P1)

	return X, P

def Extended_Kalman_filter(X, U, Z, P, R, Q, g, h, grad_g, grad_h):
	"""
	X - Вектор состояния с прошлого шага
	U - Вектор управления
	Z - Вектор измерений
	P - Матрица погрешности с прошлого шага
	R - Матрица ковариации модели
	Q - Матрица ковариации системы измерений
	g - Функция системы
	h - Функция измерений
	grad_g - Функция, возвращающая матрицу Якоби фукнции g в точке
	grad_h - Функция, возвращающая матрицу Якоби фукнции h в точке
	"""

	dim = P.shape[0]

	X1 = g(X, U)

	G = grad_g(X1)
	H = grad_h(X1)

	P1 = matmul(matmul(G, P), transpose(G)) + R

	K = matmul(matmul(P1, transpose(H)), inv(matmul(matmul(H, P1), transpose(H)) + Q))
	X = X1 + matmul(K, Z - h(X1))
	P = matmul(eye(dim, dim) - matmul(K, H), P1)

	return X, P