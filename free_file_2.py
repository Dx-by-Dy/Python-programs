import numpy as np
import matplotlib.pyplot as plt

def Kalmal_filter(X, P):
	global K_data

	dim = P.shape[0]

	X1 = np.matmul(A, X)
	P1 = np.matmul(np.matmul(A, P), np.transpose(A)) + R

	K = np.matmul(np.matmul(P1, np.transpose(C)), np.linalg.inv(np.matmul(np.matmul(C, P), np.transpose(C)) + Q))
	K_data += [np.linalg.norm(K)]

	X = X1 + np.matmul(K, Z - X1)
	P = np.matmul(np.eye(dim, dim) - np.matmul(K, C), P1)

	return X, P

sigma1, sigma2 = 0.2, 1
A = np.array([[1, 1], [0, 1]])
B = np.array([[0, 0], [0, 0]])
C = np.array([[1, 0], [0, 1]])

R = np.array([[0, 0], [0, sigma1]])
Q = np.array([[sigma2, 0], [0, sigma2]])

P = np.array([[0, 0], [0, 0]])

X = np.array([[0], [1]])
X_true = np.array([[0], [1]])

ax, data = [], []
K_data, P_data = [], []

for i in range(100):

	'''
	#Пример резкого сдвига шума и реагирования на него
	sigma2 = 0.7 if i < 50 else 0.4
	Q = np.array([[sigma2, 0], [0, sigma2]])
	'''

	'''
	#Пример резкого изменения шума и реагирования на него
	sigma2 = 0.7 if i != 30 else 5
	Q = np.array([[sigma2, 0], [0, sigma2]])
	'''

	'''
	#Пример не постоянных матриц корреляций
	sigma2 = 0.7 + 0.3 * (-1) ** i
	Q = np.array([[sigma2, 0], [0, sigma2]])

	sigma1 = 0.3 + 0.2 * (-1) ** (i+1)
	R = np.array([[0, 0], [0, sigma1]])
	'''

	Z = np.matmul(C, X_true) + np.array([[np.random.normal(scale = sigma2)], [np.random.normal(scale = sigma2)]])
	
	X, P = Kalmal_filter(X, P)

	ax += [i+1]
	data += [np.linalg.norm(X_true - X)]
	P_data += [np.linalg.norm(P)]

	'''
	Пример резкого удара и реагирования на него
	if i == 50:
		X_true = np.matmul(A, X_true) + np.array([[0], [np.random.normal(scale = sigma1)]]) + np.array([[-100], [100]])
	else:
		X_true = np.matmul(A, X_true) + np.array([[0], [np.random.normal(scale = sigma1)]])
	'''

	X_true = np.matmul(A, X_true) + np.array([[0], [np.random.normal(scale = sigma1)]])

	print(np.linalg.norm(X_true))

def grafics() -> None:

	plt.ion()

	axis.plot(ax, K_data, 'm', alpha = 0.8,  label = "$||K_k||$")
	axis.plot(ax, P_data, 'k', alpha = 0.8,  label = "$||P_k||$")
	axis.plot(ax, data, 'r', label = "$||X_{true}^k - X^k||$")
	axis.legend()
	axis.set_xlabel("Номер шага")
	axis.set_xticks([i for i in range(0, 101, 5)], [i for i in range(0, 101, 5)])

	plt.draw()
	plt.ioff()


fg, axis = plt.subplots(nrows= 1, ncols= 1, figsize=(15, 8))
fg.subplots_adjust(bottom=0.1, left=0.06, right=0.98, top=0.95, hspace=0.3)

grafics()

plt.show()