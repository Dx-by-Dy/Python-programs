import numpy as np

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

	X1 = np.matmul(A, X) + np.matmul(B, U)
	P1 = np.matmul(np.matmul(A, P), np.transpose(A)) + R

	K = np.matmul(np.matmul(P1, np.transpose(C)), np.linalg.inv(np.matmul(np.matmul(C, P), np.transpose(C)) + Q))
	X = X1 + np.matmul(K, Z - X1)
	P = np.matmul(np.eye(dim, dim) - np.matmul(K, C), P1)

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

	P1 = np.matmul(np.matmul(G, P), np.transpose(G)) + R

	K = np.matmul(np.matmul(P1, np.transpose(H)), np.linalg.inv(np.matmul(np.matmul(H, P), np.transpose(H)) + Q))
	X = X1 + np.matmul(K, Z - h(X1))
	P = np.matmul(np.eye(dim, dim) - np.matmul(K, H), P1)

	return X, P