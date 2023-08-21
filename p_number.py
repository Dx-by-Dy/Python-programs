from random import random as r
from random import randint
from numpy import *

def Virtual_disclosure(Table):
	while True:
		z = True
		for i in range(Size_table):
			for j in range(Size_table):
				if Table[i][j] >= 4:
					z = False
					if i - 1 >= 0: Table[i-1][j] = abs(Table[i-1][j]) + 1
					if j - 1 >= 0: Table[i][j-1] = abs(Table[i][j-1]) + 1
					if j + 1 < Size_table: Table[i][j+1] = abs(Table[i][j+1]) + 1
					if i + 1 < Size_table: Table[i+1][j] = abs(Table[i+1][j]) + 1
					Table[i][j] -= 4
					break
			if (z == False): break
		if z: break

	return Table

def Change_sign(Table):

	return Table * -1

def I_win(Table):
	win = True
	sign = 0
	for i in range(Size_table):
		for j in range(Size_table):
			if Table[i][j] != 0 and sign == 0: sign = Table[i][j]
			if Table[i][j] != 0 and Table[i][j] * sign < 0:
				win = False
				break
		if win == False: break
	return win

def Change(value):
	new_value = value + (r() / 10 - 0.05)
	if abs(new_value) <= 1: return new_value
	return value

class Neuron_network:

	def __init__(self, name, from_file):

		self.name = name
		self.Struct_network = array([Size_table**2, 10, 10, Size_table**2])
		self.First_turn = True

		if from_file == False:
			self.Weight_1 = random.random((self.Struct_network[0], self.Struct_network[1])) * 2 - 1
			self.Weight_2 = random.random((self.Struct_network[1], self.Struct_network[2])) * 2 - 1
			self.Weight_3 = random.random((self.Struct_network[2], self.Struct_network[3])) * 2 - 1
			self.Bias_1 = random.random((self.Struct_network[1])) * 2 - 1
			self.Bias_2 = random.random((self.Struct_network[2])) * 2 - 1
			self.Bias_3 = random.random((self.Struct_network[3])) * 2 - 1
		else:
			self.Weight_1 = loadtxt("C:\\Users\\Alex\\Desktop\\Network\\Weight_1", dtype = float)
			self.Weight_2 = loadtxt("C:\\Users\\Alex\\Desktop\\Network\\Weight_2", dtype = float)
			self.Weight_3 = loadtxt("C:\\Users\\Alex\\Desktop\\Network\\Weight_3", dtype = float)
			self.Bias_1 = loadtxt("C:\\Users\\Alex\\Desktop\\Network\\Bias_1", dtype = float)
			self.Bias_2 = loadtxt("C:\\Users\\Alex\\Desktop\\Network\\Bias_2", dtype = float)
			self.Bias_3 = loadtxt("C:\\Users\\Alex\\Desktop\\Network\\Bias_3", dtype = float)

	def Fill_network(self, Table):

		self.Input_neurons = Table.reshape((Size_table**2)) * 0.25
		self.Hidden_neurons_1 = zeros((10))
		self.Hidden_neurons_2 = zeros((10))
		self.Output_neurons = zeros((Size_table**2))

		self.Hidden_neurons_1 = Sigmoid(dot(self.Input_neurons, self.Weight_1) + self.Bias_1)
		self.Hidden_neurons_2 = Sigmoid(dot(self.Hidden_neurons_1, self.Weight_2) + self.Bias_2)
		self.Output_neurons = Sigmoid(dot(self.Hidden_neurons_2, self.Weight_3) + self.Bias_3)

		self.Output_neurons = self.Output_neurons.reshape((Size_table, Size_table))
		index_max = unravel_index(argmax(self.Output_neurons), self.Output_neurons.shape)

		if Table[index_max] <= 0:
			self.Weight_correction()
			return (-1, -1)

		return index_max

	def Weight_correction(self):
		self.Weight_1 = Small_change(self.Weight_1)
		self.Weight_2 = Small_change(self.Weight_2)
		self.Weight_3 = Small_change(self.Weight_3)
		self.Bias_1 = Small_change(self.Bias_1)
		self.Bias_2 = Small_change(self.Bias_2)
		self.Bias_3 = Small_change(self.Bias_3)

		if self.First_turn:
			for i in range(10):
				if Global_turn == 0:
					if self.Weight_1[54][i] + 0.2 < 1: self.Weight_1[54][i] += 0.2
					else: self.Weight_1[54][i] = 1
				else:
					if self.Weight_1[9][i] + 0.2 < 1: self.Weight_1[9][i] += 0.2
					else: self.Weight_1[9][i] = 1
			self.First_turn = False

	def Print_info(self):
		print(self.name, "\n")
		print(self.Weight_1, "\n")
		print(self.Weight_2, "\n")
		print(self.Weight_3, "\n")
		print(self.Bias_1, "\n")
		print(self.Bias_2, "\n")
		print(self.Bias_3, "\n")

	def Save_info(self):
		savetxt("C:\\Users\\Alex\\Desktop\\Network\\Weight_1", self.Weight_1, fmt='%f')
		savetxt("C:\\Users\\Alex\\Desktop\\Network\\Weight_2", self.Weight_2, fmt='%f')
		savetxt("C:\\Users\\Alex\\Desktop\\Network\\Weight_3", self.Weight_3, fmt='%f')
		savetxt("C:\\Users\\Alex\\Desktop\\Network\\Bias_1", self.Bias_1, fmt='%f')
		savetxt("C:\\Users\\Alex\\Desktop\\Network\\Bias_2", self.Bias_2, fmt='%f')
		savetxt("C:\\Users\\Alex\\Desktop\\Network\\Bias_3", self.Bias_3, fmt='%f')

	def Change_name(self, new_name):

		self.name = new_name

Size_table = 8

Sigmoid = vectorize(lambda value: 1/(1 + exp(-value)))
Small_change = vectorize(Change)

Count_games = 100

for i in range(Count_games):

	print(i)

	Table = zeros((Size_table, Size_table))
	Table[1][1], Table[6][6] = -3, 3

	Player_1 = Neuron_network("Player_1", True)
	Player_2 = Neuron_network("Player_2", True)
	Global_turn = 0

	while True:

		if Global_turn == 0: index = Player_1.Fill_network(Table)
		else: index = Player_2.Fill_network(Table)

		if index != (-1, -1): 
			Table[index] += 1
			Table = Virtual_disclosure(Table)
			Table = Change_sign(Table)
			Global_turn = (Global_turn + 1)%2

		if I_win(Table): break

	if (Global_turn + 1) % 2 == 0: Player_1.Save_info()
	else: Player_2.Save_info()

print(Change_sign(Table), "\n")