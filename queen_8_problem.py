from time import time

def myprint(table):
	global cnt

	cnt += 1

	for i in range(8):
		print(table[i])
	print(cnt, "\n")

def fill_table(row : int, clm : int, table):
	for i in range(1, 8):
		if row + i < 8: 
			table[row + i][clm] = 0
			if clm + i < 8: table[row + i][clm + i] = 0
			if clm - i >= 0: table[row + i][clm - i] = 0
		if row - i >= 0: 
			table[row - i][clm] = 0
			if clm + i < 8: table[row - i][clm + i] = 0
			if clm - i >= 0: table[row - i][clm - i] = 0
		if clm + i < 8: table[row][clm + i] = 0
		if clm - i >= 0: table[row][clm - i] = 0

	return table

def queen_problem(rec : int, table):

	for i in range(8):

		ftable = []
		for k in range(8):
			ftable += [[]]
			for l in range(8):
				ftable[k] += [table[k][l]]

		if table[rec][i] == -1:
			ftable[rec][i] = 1
			if rec != 7: queen_problem(rec + 1, fill_table(rec, i, ftable))
			else: myprint(ftable)

begin = time()

table = [[-1 for i in range(8)] for j in range(8)]
cnt = 0
queen_problem(0, table)

print(time() - begin)