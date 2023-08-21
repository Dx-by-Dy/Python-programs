import pygame
import os

pygame.init()

win = pygame.display.set_mode((720, 720))
dsk = pygame.image.load("C:\\Users\\Alex\\Downloads\\chess_fig\\doska.png").convert()

white = [pygame.image.load("C:\\Users\\Alex\\Downloads\\chess_fig\\бкороль.png").convert(), 
pygame.image.load("C:\\Users\\Alex\\Downloads\\chess_fig\\бферзь.png").convert(),
pygame.image.load("C:\\Users\\Alex\\Downloads\\chess_fig\\бладья.png").convert(),
pygame.image.load("C:\\Users\\Alex\\Downloads\\chess_fig\\бслон.png").convert(),
pygame.image.load("C:\\Users\\Alex\\Downloads\\chess_fig\\бконь.png").convert(),
pygame.image.load("C:\\Users\\Alex\\Downloads\\chess_fig\\бпешка.png").convert(),
pygame.image.load("C:\\Users\\Alex\\Downloads\\chess_fig\\збпешка.png").convert(),
pygame.image.load("C:\\Users\\Alex\\Downloads\\chess_fig\\збконь.png").convert(),
pygame.image.load("C:\\Users\\Alex\\Downloads\\chess_fig\\збслон.png").convert(),
pygame.image.load("C:\\Users\\Alex\\Downloads\\chess_fig\\збладья.png").convert(),
pygame.image.load("C:\\Users\\Alex\\Downloads\\chess_fig\\збферзь.png").convert(),
pygame.image.load("C:\\Users\\Alex\\Downloads\\chess_fig\\збкороль.png").convert()]

black = [pygame.image.load("C:\\Users\\Alex\\Downloads\\chess_fig\\чкороль.png").convert(), 
pygame.image.load("C:\\Users\\Alex\\Downloads\\chess_fig\\чферзь.png").convert(),
pygame.image.load("C:\\Users\\Alex\\Downloads\\chess_fig\\чладья.png").convert(),
pygame.image.load("C:\\Users\\Alex\\Downloads\\chess_fig\\чслон.png").convert(),
pygame.image.load("C:\\Users\\Alex\\Downloads\\chess_fig\\чконь.png").convert(),
pygame.image.load("C:\\Users\\Alex\\Downloads\\chess_fig\\чпешка.png").convert(),
pygame.image.load("C:\\Users\\Alex\\Downloads\\chess_fig\\зчпешка.png").convert(),
pygame.image.load("C:\\Users\\Alex\\Downloads\\chess_fig\\зчконь.png").convert(),
pygame.image.load("C:\\Users\\Alex\\Downloads\\chess_fig\\зчслон.png").convert(),
pygame.image.load("C:\\Users\\Alex\\Downloads\\chess_fig\\зчладья.png").convert(),
pygame.image.load("C:\\Users\\Alex\\Downloads\\chess_fig\\зчферзь.png").convert(),
pygame.image.load("C:\\Users\\Alex\\Downloads\\chess_fig\\зчкороль.png").convert()]

pole = {'a1' : (0, 630, 90, 90), 'a2' : (0, 540, 90, 90), 'a3' : (0, 450, 90, 90), 'a4' : (0, 360, 90, 90), 'a5' : (0, 270, 90, 90), 'a6' : (0, 180, 90, 90), 'a7' : (0, 90, 90, 90), 'a8' : (0, 0, 90, 90),
'b1' : (90, 630, 90, 90), 'b2' : (90, 540, 90, 90), 'b3' : (90, 450, 90, 90), 'b4' : (90, 360, 90, 90), 'b5' : (90, 270, 90, 90), 'b6' : (90, 180, 90, 90), 'b7' : (90, 90, 90, 90), 'b8' : (90, 0, 90, 90),
'c1' : (180, 630, 90, 90), 'c2' : (180, 540, 90, 90), 'c3' : (180, 450, 90, 90), 'c4' : (180, 360, 90, 90), 'c5' : (180, 270, 90, 90), 'c6' : (180, 180, 90, 90), 'c7' : (180, 90, 90, 90), 'c8' : (180, 0, 90, 90),
'd1' : (270, 630, 90, 90), 'd2' : (270, 540, 90, 90), 'd3' : (270, 450, 90, 90), 'd4' : (270, 360, 90, 90), 'd5' : (270, 270, 90, 90), 'd6' : (270, 180, 90, 90), 'd7' : (270, 90, 90, 90), 'd8' : (270, 0, 90, 90),
'e1' : (360, 630, 90, 90), 'e2' : (360, 540, 90, 90), 'e3' : (360, 450, 90, 90), 'e4' : (360, 360, 90, 90), 'e5' : (360, 270, 90, 90), 'e6' : (360, 180, 90, 90), 'e7' : (360, 90, 90, 90), 'e8' : (360, 0, 90, 90),
'f1' : (450, 630, 90, 90), 'f2' : (450, 540, 90, 90), 'f3' : (450, 450, 90, 90), 'f4' : (450, 360, 90, 90), 'f5' : (450, 270, 90, 90), 'f6' : (450, 180, 90, 90), 'f7' : (450, 90, 90, 90), 'f8' : (450, 0, 90, 90),
'g1' : (540, 630, 90, 90), 'g2' : (540, 540, 90, 90), 'g3' : (540, 450, 90, 90), 'g4' : (540, 360, 90, 90), 'g5' : (540, 270, 90, 90), 'g6' : (540, 180, 90, 90), 'g7' : (540, 90, 90, 90), 'g8' : (540, 0, 90, 90),
'h1' : (630, 630, 90, 90), 'h2' : (630, 540, 90, 90), 'h3' : (630, 450, 90, 90), 'h4' : (630, 360, 90, 90), 'h5' : (630, 270, 90, 90), 'h6' : (630, 180, 90, 90), 'h7' : (630, 90, 90, 90), 'h8' : (630, 0, 90, 90)}

pos = {pole['a1'] : white[-3], pole['h1'] : white[2], pole['b1'] : white[4], pole['g1'] : white[-5], pole['c1'] : white[-4], pole['f1'] : white[3], pole['d1'] : white[1], pole['e1'] : white[-1],
pole['a2'] : white[5], pole['h2'] : white[-6], pole['b2'] : white[-6], pole['g2'] : white[5], pole['c2'] : white[5], pole['f2'] : white[-6], pole['d2'] : white[-6], pole['e2'] : white[5],
pole['a3'] : None, pole['h3'] : None, pole['b3'] : None, pole['g3'] : None, pole['c3'] : None, pole['f3'] : None, pole['d3'] : None, pole['e3'] : None,
pole['a4'] : None, pole['h4'] : None, pole['b4'] : None, pole['g4'] : None, pole['c4'] : None, pole['f4'] : None, pole['d4'] : None, pole['e4'] : None,
pole['a5'] : None, pole['h5'] : None, pole['b5'] : None, pole['g5'] : None, pole['c5'] : None, pole['f5'] : None, pole['d5'] : None, pole['e5'] : None,
pole['a6'] : None, pole['h6'] : None, pole['b6'] : None, pole['g6'] : None, pole['c6'] : None, pole['f6'] : None, pole['d6'] : None, pole['e6'] : None,
pole['a7'] : black[-6], pole['h7'] : black[5], pole['b7'] : black[5], pole['g7'] : black[-6], pole['c7'] : black[-6], pole['f7'] : black[5], pole['d7'] : black[5], pole['e7'] : black[-6],
pole['a8'] : black[2], pole['h8'] : black[-3], pole['b8'] : black[-5], pole['g8'] : black[4], pole['c8'] : black[3], pole['f8'] : black[-4], pole['d8'] : black[-2], pole['e8'] : black[0]}

last_turn = []

def update():
	win.fill((0, 0, 0))
	win.blit(dsk, (0, 0, 720, 720))

	for i in ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'):
		for j in range(1, 9):
			if pos[pole[i + str(j)]] != None: win.blit(pos[pole[i + str(j)]], pole[i + str(j)])
	pygame.display.update()

def instan1(a, b, x, y, rec):
	global last_turn, turn, pos, prev, drkrw, krkrw, drkrb, krkrb, lwr, rwr, lbr, rbr
	buk = {'a' : '1', 'b' : '2', 'c' : '3', 'd' : '4', 'e' : '5', 'f' : '6', 'g' : '7', 'h' : '8', '1' : 'a', '2' : 'b', '3' : 'c', '4' : 'd', '5' : 'e', '6' : 'f', '7' : 'g', '8' : 'h'}

	if pos[pole[a + b]] == white[5] or pos[pole[a + b]] == white[-6]:
		pown, proh, recf, recfe = [], False, pos[pole[a + b]], pos[pole[x + y]]
		
		if not rec:
			for i in ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'):
				for j in range(1, 9):
					if pos[pole[i + str(j)]] == white[0] or pos[pole[i + str(j)]] == white[-1]: xk, yk = i, str(j)

			pos[pole[x + y]] = pos[pole[a + b]]
			pos[pole[a + b]] = None

			for i in ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'):
				for j in range(1, 9):
					dobr = False
					if pos[pole[i + str(j)]] in black: dobr = instan1(i, str(j), xk, yk, True)
					if dobr:
						pos[pole[x + y]] = recfe
						pos[pole[a + b]] = recf
						return False
			pos[pole[x + y]] = recfe
			pos[pole[a + b]] = recf

		if y == '8' and not rec:
			p = True
			while p:
				for event in pygame.event.get():
					if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_q:
							if a != x:
								if white.index(pos[pole[a + b]]) < 6: pos[pole[x + y]] = white[1]
								else: pos[pole[x + y]] = white[-2]
							else:
								if white.index(pos[pole[a + b]]) < 6: pos[pole[x + y]] = white[-2]
								else: pos[pole[x + y]] = white[1]
							p = False

						elif event.key == pygame.K_r:
							if a != x:
								if white.index(pos[pole[a + b]]) < 6: pos[pole[x + y]] = white[2]
								else: pos[pole[x + y]] = white[-3]
							else:
								if white.index(pos[pole[a + b]]) < 6: pos[pole[x + y]] = white[-3]
								else: pos[pole[x + y]] = white[2]
							p = False

						elif event.key == pygame.K_n:
							if a != x:
								if white.index(pos[pole[a + b]]) < 6: pos[pole[x + y]] = white[4]
								else: pos[pole[x + y]] = white[-5]
							else:
								if white.index(pos[pole[a + b]]) < 6: pos[pole[x + y]] = white[-5]
								else: pos[pole[x + y]] = white[4]
							p = False

						elif event.key == pygame.K_b:
							if a != x:
								if white.index(pos[pole[a + b]]) < 6: pos[pole[x + y]] = white[3]
								else: pos[pole[x + y]] = white[-4]
							else:
								if white.index(pos[pole[a + b]]) < 6: pos[pole[x + y]] = white[-4]
								else: pos[pole[x + y]] = white[3]
							p = False
			last_turn[0], last_turn[1], last_turn[2], last_turn[3], last_turn[4] = 'p', a, b, x, y
			prev = True
			return True

		if pos[pole[a + str(int(b) + 1)]] == None and not rec: pown.append(a + str(int(b) + 1))
		if b == '2' and pos[pole[a + str(int(b) + 2)]] == None and not rec: pown.append(a + str(int(b) + 2))
		if a != 'h' and pos[pole[buk[str(int(buk[a]) + 1)] + str(int(b) + 1)]] in black: pown.append(buk[str(int(buk[a]) + 1)] + str(int(b) + 1))
		elif a != 'h' and rec: pown.append(buk[str(int(buk[a]) + 1)] + str(int(b) + 1))
		if a != 'a' and pos[pole[buk[str(int(buk[a]) - 1)] + str(int(b) + 1)]] in black: pown.append(buk[str(int(buk[a]) - 1)] + str(int(b) + 1))
		elif a != 'a' and rec: pown.append(buk[str(int(buk[a]) - 1)] + str(int(b) + 1))
		if b == '5' and last_turn[0] == 'p' and last_turn[2] == '7' and last_turn[4] == '5':
			if a != 'h' and buk[str(int(buk[a]) + 1)] == last_turn[3]: 
				pown.append(buk[str(int(buk[a]) + 1)] + str(int(b) + 1))
				if x + y == buk[str(int(buk[a]) + 1)] + str(int(b) + 1): proh = True
			if a != 'a' and buk[str(int(buk[a]) - 1)] == last_turn[3]: 
				pown.append(buk[str(int(buk[a]) - 1)] + str(int(b) + 1))
				if x + y == buk[str(int(buk[a]) - 1)] + str(int(b) + 1): proh = True

		if x + y in pown: 
			if rec: return True
			if int(y) - int(b) == 1 and a == x:  
				if pos[pole[a + b]] == white[5]: pos[pole[a + b]] = white[-6]
				else: pos[pole[a + b]] = white[5]
			if proh: pos[pole[x + str(int(y) - 1)]] = None
			if turn == 1:
				last_turn.append('p')
				last_turn.append(a)
				last_turn.append(b)
				last_turn.append(x)
				last_turn.append(y)
			elif not rec: last_turn[0], last_turn[1], last_turn[2], last_turn[3], last_turn[4] = 'p', a, b, x, y
			return True
		else: return False

	if pos[pole[a + b]] == black[5] or pos[pole[a + b]] == black[-6]:
		pown, proh, recf, recfe = [], False, pos[pole[a + b]], pos[pole[x + y]] 

		if not rec:
			for i in ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'):
				for j in range(1, 9):
					if pos[pole[i + str(j)]] == black[0] or pos[pole[i + str(j)]] == black[-1]: xk, yk = i, str(j)

			pos[pole[x + y]] = pos[pole[a + b]]
			pos[pole[a + b]] = None

			for i in ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'):
				for j in range(1, 9):
					dobr = False
					if pos[pole[i + str(j)]] in white: dobr = instan1(i, str(j), xk, yk, True)
					if dobr:
						pos[pole[x + y]] = recfe
						pos[pole[a + b]] = recf
						return False
			pos[pole[x + y]] = recfe
			pos[pole[a + b]] = recf

		if y == '1' and not rec:
			p = True
			while p:
				for event in pygame.event.get():
					if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_q:
							if a != x:
								if black.index(pos[pole[a + b]]) < 6: pos[pole[x + y]] = black[1]
								else: pos[pole[x + y]] = black[-2]
							else:
								if black.index(pos[pole[a + b]]) < 6: pos[pole[x + y]] = black[-2]
								else: pos[pole[x + y]] = black[1]
							pos[pole[a + b]] = None
							p = False

						elif event.key == pygame.K_r:
							if a != x:
								if black.index(pos[pole[a + b]]) < 6: pos[pole[x + y]] = black[2]
								else: pos[pole[x + y]] = black[-3]
							else:
								if black.index(pos[pole[a + b]]) < 6: pos[pole[x + y]] = black[-3]
								else: pos[pole[x + y]] = black[2]
							pos[pole[a + b]] = None
							p = False

						elif event.key == pygame.K_n:
							if a != x:
								if black.index(pos[pole[a + b]]) < 6: pos[pole[x + y]] = black[4]
								else: pos[pole[x + y]] = black[-5]
							else:
								if black.index(pos[pole[a + b]]) < 6: pos[pole[x + y]] = black[-5]
								else: pos[pole[x + y]] = black[4]
							pos[pole[a + b]] = None
							p = False

						elif event.key == pygame.K_b:
							if a != x:
								if black.index(pos[pole[a + b]]) < 6: pos[pole[x + y]] = black[3]
								else: pos[pole[x + y]] = black[-4]
							else:
								if black.index(pos[pole[a + b]]) < 6: pos[pole[x + y]] = black[-4]
								else: pos[pole[x + y]] = black[3]
							pos[pole[a + b]] = None
							p = False
			turn += 1
			if not rec: last_turn[0], last_turn[1], last_turn[2], last_turn[3], last_turn[4] = 'p', a, b, x, y
			return False

		if pos[pole[a + str(int(b) - 1)]] == None and not rec: pown.append(a + str(int(b) - 1))
		if b == '7' and pos[pole[a + str(int(b) - 2)]] == None and not rec: pown.append(a + str(int(b) - 2))
		if a != 'h' and pos[pole[buk[str(int(buk[a]) + 1)] + str(int(b) - 1)]] in white: pown.append(buk[str(int(buk[a]) + 1)] + str(int(b) - 1))
		elif a != 'h' and rec: pown.append(buk[str(int(buk[a]) + 1)] + str(int(b) - 1))
		if a != 'a' and pos[pole[buk[str(int(buk[a]) - 1)] + str(int(b) - 1)]] in white: pown.append(buk[str(int(buk[a]) - 1)] + str(int(b) - 1))
		elif a != 'a' and rec: pown.append(buk[str(int(buk[a]) - 1)] + str(int(b) - 1))
		if b == '4' and last_turn[0] == 'p' and last_turn[2] == '2' and last_turn[4] == '4':
			if a != 'h' and buk[str(int(buk[a]) + 1)] == last_turn[3]: 
				pown.append(buk[str(int(buk[a]) + 1)] + str(int(b) - 1))
				if x + y == buk[str(int(buk[a]) + 1)] + str(int(b) - 1): proh = True
			if a != 'a' and buk[str(int(buk[a]) - 1)] == last_turn[3]: 
				pown.append(buk[str(int(buk[a]) - 1)] + str(int(b) - 1))
				if x + y == buk[str(int(buk[a]) - 1)] + str(int(b) - 1): proh = True

		if x + y in pown:
			if rec: return True
			if int(b) - int(y) == 1 and a == x:  
				if pos[pole[a + b]] == black[5]: pos[pole[a + b]] = black[-6]
				else: pos[pole[a + b]] = black[5]
			if proh: pos[pole[x + str(int(y) + 1)]] = None
			if turn == 1:
				last_turn.append('p')
				last_turn.append(a)
				last_turn.append(b)
				last_turn.append(x)
				last_turn.append(y)
			else: last_turn[0], last_turn[1], last_turn[2], last_turn[3], last_turn[4] = 'p', a, b, x, y
			return True
		else: return False

	if pos[pole[a + b]] == white[2] or pos[pole[a + b]] == white[-3]:
		rock, recf, recfe = [], pos[pole[a + b]], pos[pole[x + y]]
		L, U, R, D = True, True, True, True

		if not rec:
			for i in ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'):
				for j in range(1, 9):
					if pos[pole[i + str(j)]] == white[0] or pos[pole[i + str(j)]] == white[-1]: xk, yk = i, str(j)

			pos[pole[x + y]] = pos[pole[a + b]]
			pos[pole[a + b]] = None

			for i in ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'):
				for j in range(1, 9):
					dobr = False
					if pos[pole[i + str(j)]] in black: dobr = instan1(i, str(j), xk, yk, True)
					if dobr:
						pos[pole[x + y]] = recfe
						pos[pole[a + b]] = recf
						return False
			pos[pole[x + y]] = recfe
			pos[pole[a + b]] = recf

		for i in range(1, 8):
			if int(buk[a]) - i > 0 and L:
				if pos[pole[buk[str(int(buk[a]) - i)] + b]] in black: L = False
				if pos[pole[buk[str(int(buk[a]) - i)] + b]] in white: L = False
				else: rock.append(buk[str(int(buk[a]) - i)] + b)
			if int(buk[a]) + i < 9 and R:
				if pos[pole[buk[str(int(buk[a]) + i)] + b]] in black: R = False
				if pos[pole[buk[str(int(buk[a]) + i)] + b]] in white: R = False
				else: rock.append(buk[str(int(buk[a]) + i)] + b)
			if int(b) + i < 9 and U:
				if pos[pole[a + str(int(b) + i)]] in black: U = False
				if pos[pole[a + str(int(b) + i)]] in white: U = False
				else: rock.append(a + str(int(b) + i))
			if int(b) - i > 0 and D:
				if pos[pole[a + str(int(b) - i)]] in black: D = False
				if pos[pole[a + str(int(b) - i)]] in white: D = False
				else: rock.append(a + str(int(b) - i))
		if x + y in rock:
			if rec: return True
			if abs(int(b) - int(y)) % 2 == 1 or abs(int(buk[a]) - int(buk[x])) % 2 == 1:  
				if pos[pole[a + b]] == white[2]: pos[pole[a + b]] = white[-3]
				else: pos[pole[a + b]] = white[2]
			if a + b == 'a1': lwr = False
			if a + b == 'h1': rwr = False
			return True
		else: return False

	if pos[pole[a + b]] == black[2] or pos[pole[a + b]] == black[-3]:
		rock, recf, recfe = [], pos[pole[a + b]], pos[pole[x + y]]
		L, U, R, D = True, True, True, True 

		if not rec:
			for i in ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'):
				for j in range(1, 9):
					if pos[pole[i + str(j)]] == black[0] or pos[pole[i + str(j)]] == black[-1]: xk, yk = i, str(j)

			pos[pole[x + y]] = pos[pole[a + b]]
			pos[pole[a + b]] = None

			for i in ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'):
				for j in range(1, 9):
					dobr = False
					if pos[pole[i + str(j)]] in white: dobr = instan1(i, str(j), xk, yk, True)
					if dobr:
						pos[pole[x + y]] = recfe
						pos[pole[a + b]] = recf
						return False
			pos[pole[x + y]] = recfe
			pos[pole[a + b]] = recf

		for i in range(1, 8):
			if int(buk[a]) - i > 0 and L:
				if pos[pole[buk[str(int(buk[a]) - i)] + b]] in white: L = False
				if pos[pole[buk[str(int(buk[a]) - i)] + b]] in black: L = False
				else: rock.append(buk[str(int(buk[a]) - i)] + b)
			if int(buk[a]) + i < 9 and R:
				if pos[pole[buk[str(int(buk[a]) + i)] + b]] in white: R = False
				if pos[pole[buk[str(int(buk[a]) + i)] + b]] in black: R = False
				else: rock.append(buk[str(int(buk[a]) + i)] + b)
			if int(b) + i < 9 and U:
				if pos[pole[a + str(int(b) + i)]] in white: U = False
				if pos[pole[a + str(int(b) + i)]] in black: U = False
				else: rock.append(a + str(int(b) + i))
			if int(b) - i > 0 and D:
				if pos[pole[a + str(int(b) - i)]] in white: D = False
				if pos[pole[a + str(int(b) - i)]] in black: D = False
				else: rock.append(a + str(int(b) - i))
		if x + y in rock:
			if rec: return True
			if abs(int(b) - int(y)) % 2 == 1 or abs(int(buk[a]) - int(buk[x])) % 2 == 1:  
				if pos[pole[a + b]] == black[2]: pos[pole[a + b]] = black[-3]
				else: pos[pole[a + b]] = black[2]
			if a + b == 'a8': lbr = False
			if a + b == 'h8': rbr = False
			return True
		else: return False

	if pos[pole[a + b]] == white[4] or pos[pole[a + b]] == white[-5]:
		knife, recf, recfe = [], pos[pole[a + b]], pos[pole[x + y]]

		if not rec:
			for i in ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'):
				for j in range(1, 9):
					if pos[pole[i + str(j)]] == white[0] or pos[pole[i + str(j)]] == white[-1]: xk, yk = i, str(j)

			pos[pole[x + y]] = pos[pole[a + b]]
			pos[pole[a + b]] = None

			for i in ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'):
				for j in range(1, 9):
					dobr = False
					if pos[pole[i + str(j)]] in black: dobr = instan1(i, str(j), xk, yk, True)
					if dobr:
						pos[pole[x + y]] = recfe
						pos[pole[a + b]] = recf
						return False
			pos[pole[x + y]] = recfe
			pos[pole[a + b]] = recf

		if int(buk[a]) - 1 > 0 and int(b) - 2 > 0 and (pos[pole[buk[str(int(buk[a]) - 1)] + str(int(b) - 2)]] == None or pos[pole[buk[str(int(buk[a]) - 1)] + str(int(b) - 2)]] in black): knife.append(buk[str(int(buk[a]) - 1)] + str(int(b) - 2))
		if int(buk[a]) - 1 > 0 and int(b) + 2 < 9 and (pos[pole[buk[str(int(buk[a]) - 1)] + str(int(b) + 2)]] == None or pos[pole[buk[str(int(buk[a]) - 1)] + str(int(b) + 2)]] in black): knife.append(buk[str(int(buk[a]) - 1)] + str(int(b) + 2))
		if int(buk[a]) - 2 > 0 and int(b) - 1 > 0 and (pos[pole[buk[str(int(buk[a]) - 2)] + str(int(b) - 1)]] == None or pos[pole[buk[str(int(buk[a]) - 2)] + str(int(b) - 1)]] in black): knife.append(buk[str(int(buk[a]) - 2)] + str(int(b) - 1))
		if int(buk[a]) - 2 > 0 and int(b) + 1 < 9 and (pos[pole[buk[str(int(buk[a]) - 2)] + str(int(b) + 1)]] == None or pos[pole[buk[str(int(buk[a]) - 2)] + str(int(b) + 1)]] in black): knife.append(buk[str(int(buk[a]) - 2)] + str(int(b) + 1))
		if int(buk[a]) + 1 < 9 and int(b) - 2 > 0 and (pos[pole[buk[str(int(buk[a]) + 1)] + str(int(b) - 2)]] == None or pos[pole[buk[str(int(buk[a]) + 1)] + str(int(b) - 2)]] in black): knife.append(buk[str(int(buk[a]) + 1)] + str(int(b) - 2))
		if int(buk[a]) + 1 < 9 and int(b) + 2 < 9 and (pos[pole[buk[str(int(buk[a]) + 1)] + str(int(b) + 2)]] == None or pos[pole[buk[str(int(buk[a]) + 1)] + str(int(b) + 2)]] in black): knife.append(buk[str(int(buk[a]) + 1)] + str(int(b) + 2))
		if int(buk[a]) + 2 < 9 and int(b) - 1 > 0 and (pos[pole[buk[str(int(buk[a]) + 2)] + str(int(b) - 1)]] == None or pos[pole[buk[str(int(buk[a]) + 2)] + str(int(b) - 1)]] in black): knife.append(buk[str(int(buk[a]) + 2)] + str(int(b) - 1))
		if int(buk[a]) + 2 < 9 and int(b) + 1 < 9 and (pos[pole[buk[str(int(buk[a]) + 2)] + str(int(b) + 1)]] == None or pos[pole[buk[str(int(buk[a]) + 2)] + str(int(b) + 1)]] in black): knife.append(buk[str(int(buk[a]) + 2)] + str(int(b) + 1))

		if x + y in knife: 
			if not rec:
				if pos[pole[a + b]] == white[4]: pos[pole[a + b]] = white[-5]
				else: pos[pole[a + b]] = white[4]
			return True
		else: return False

	if pos[pole[a + b]] == black[4] or pos[pole[a + b]] == black[-5]:
		knife, recf, recfe = [], pos[pole[a + b]], pos[pole[x + y]]

		if not rec:
			for i in ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'):
				for j in range(1, 9):
					if pos[pole[i + str(j)]] == black[0] or pos[pole[i + str(j)]] == black[-1]: xk, yk = i, str(j)

			pos[pole[x + y]] = pos[pole[a + b]]
			pos[pole[a + b]] = None

			for i in ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'):
				for j in range(1, 9):
					dobr = False
					if pos[pole[i + str(j)]] in white: dobr = instan1(i, str(j), xk, yk, True)
					if dobr:
						pos[pole[x + y]] = recfe
						pos[pole[a + b]] = recf
						return False
			pos[pole[x + y]] = recfe
			pos[pole[a + b]] = recf

		if int(buk[a]) - 1 > 0 and int(b) - 2 > 0 and (pos[pole[buk[str(int(buk[a]) - 1)] + str(int(b) - 2)]] == None or pos[pole[buk[str(int(buk[a]) - 1)] + str(int(b) - 2)]] in white): knife.append(buk[str(int(buk[a]) - 1)] + str(int(b) - 2))
		if int(buk[a]) - 1 > 0 and int(b) + 2 < 9 and (pos[pole[buk[str(int(buk[a]) - 1)] + str(int(b) + 2)]] == None or pos[pole[buk[str(int(buk[a]) - 1)] + str(int(b) + 2)]] in white): knife.append(buk[str(int(buk[a]) - 1)] + str(int(b) + 2))
		if int(buk[a]) - 2 > 0 and int(b) - 1 > 0 and (pos[pole[buk[str(int(buk[a]) - 2)] + str(int(b) - 1)]] == None or pos[pole[buk[str(int(buk[a]) - 2)] + str(int(b) - 1)]] in white): knife.append(buk[str(int(buk[a]) - 2)] + str(int(b) - 1))
		if int(buk[a]) - 2 > 0 and int(b) + 1 < 9 and (pos[pole[buk[str(int(buk[a]) - 2)] + str(int(b) + 1)]] == None or pos[pole[buk[str(int(buk[a]) - 2)] + str(int(b) + 1)]] in white): knife.append(buk[str(int(buk[a]) - 2)] + str(int(b) + 1))
		if int(buk[a]) + 1 < 9 and int(b) - 2 > 0 and (pos[pole[buk[str(int(buk[a]) + 1)] + str(int(b) - 2)]] == None or pos[pole[buk[str(int(buk[a]) + 1)] + str(int(b) - 2)]] in white): knife.append(buk[str(int(buk[a]) + 1)] + str(int(b) - 2))
		if int(buk[a]) + 1 < 9 and int(b) + 2 < 9 and (pos[pole[buk[str(int(buk[a]) + 1)] + str(int(b) + 2)]] == None or pos[pole[buk[str(int(buk[a]) + 1)] + str(int(b) + 2)]] in white): knife.append(buk[str(int(buk[a]) + 1)] + str(int(b) + 2))
		if int(buk[a]) + 2 < 9 and int(b) - 1 > 0 and (pos[pole[buk[str(int(buk[a]) + 2)] + str(int(b) - 1)]] == None or pos[pole[buk[str(int(buk[a]) + 2)] + str(int(b) - 1)]] in white): knife.append(buk[str(int(buk[a]) + 2)] + str(int(b) - 1))
		if int(buk[a]) + 2 < 9 and int(b) + 1 < 9 and (pos[pole[buk[str(int(buk[a]) + 2)] + str(int(b) + 1)]] == None or pos[pole[buk[str(int(buk[a]) + 2)] + str(int(b) + 1)]] in white): knife.append(buk[str(int(buk[a]) + 2)] + str(int(b) + 1))

		if x + y in knife:
			if not rec:
				if pos[pole[a + b]] == black[4]: pos[pole[a + b]] = black[-5]
				else: pos[pole[a + b]] = black[4]
			return True
		else: return False

	if pos[pole[a + b]] == white[3] or pos[pole[a + b]] == white[-4]:
		bishop, recf, recfe = [], pos[pole[a + b]], pos[pole[x + y]]
		L, U, R, D = True, True, True, True

		if not rec:
			for i in ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'):
				for j in range(1, 9):
					if pos[pole[i + str(j)]] == white[0] or pos[pole[i + str(j)]] == white[-1]: xk, yk = i, str(j)

			pos[pole[x + y]] = pos[pole[a + b]]
			pos[pole[a + b]] = None

			for i in ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'):
				for j in range(1, 9):
					dobr = False
					if pos[pole[i + str(j)]] in black: dobr = instan1(i, str(j), xk, yk, True)
					if dobr:
						pos[pole[x + y]] = recfe
						pos[pole[a + b]] = recf
						return False
			pos[pole[x + y]] = recfe
			pos[pole[a + b]] = recf

		for i in range(1, 8):
			if int(buk[a]) + i < 9 and int(b) + i < 9 and U:
				if pos[pole[buk[str(int(buk[a]) + i)] + str(int(b) + i)]] in black: U = False
				if pos[pole[buk[str(int(buk[a]) + i)] + str(int(b) + i)]] in white: U = False
				else: bishop.append(buk[str(int(buk[a]) + i)] + str(int(b) + i))

			if int(buk[a]) + i < 9 and int(b) - i > 0 and R:
				if pos[pole[buk[str(int(buk[a]) + i)] + str(int(b) - i)]] in black: R = False
				if pos[pole[buk[str(int(buk[a]) + i)] + str(int(b) - i)]] in white: R = False
				else: bishop.append(buk[str(int(buk[a]) + i)] + str(int(b) - i))

			if int(buk[a]) - i > 0 and int(b) + i < 9 and L:
				if pos[pole[buk[str(int(buk[a]) - i)] + str(int(b) + i)]] in black: L = False
				if pos[pole[buk[str(int(buk[a]) - i)] + str(int(b) + i)]] in white: L = False
				else: bishop.append(buk[str(int(buk[a]) - i)] + str(int(b) + i))

			if int(buk[a]) - i > 0 and int(b) - i > 0 and D:
				if pos[pole[buk[str(int(buk[a]) - i)] + str(int(b) - i)]] in black: D = False
				if pos[pole[buk[str(int(buk[a]) - i)] + str(int(b) - i)]] in white: D = False
				else: bishop.append(buk[str(int(buk[a]) - i)] + str(int(b) - i))

		if x + y in bishop: return True
		else: return False

	if pos[pole[a + b]] == black[3] or pos[pole[a + b]] == black[-4]:
		bishop, recf, recfe = [], pos[pole[a + b]], pos[pole[x + y]]
		L, U, R, D = True, True, True, True

		if not rec:
			for i in ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'):
				for j in range(1, 9):
					if pos[pole[i + str(j)]] == black[0] or pos[pole[i + str(j)]] == black[-1]: xk, yk = i, str(j)

			pos[pole[x + y]] = pos[pole[a + b]]
			pos[pole[a + b]] = None

			for i in ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'):
				for j in range(1, 9):
					dobr = False
					if pos[pole[i + str(j)]] in white: dobr = instan1(i, str(j), xk, yk, True)
					if dobr:
						pos[pole[x + y]] = recfe
						pos[pole[a + b]] = recf
						return False
			pos[pole[x + y]] = recfe
			pos[pole[a + b]] = recf

		for i in range(1, 8):
			if int(buk[a]) + i < 9 and int(b) + i < 9 and U:
				if pos[pole[buk[str(int(buk[a]) + i)] + str(int(b) + i)]] in white: U = False
				if pos[pole[buk[str(int(buk[a]) + i)] + str(int(b) + i)]] in black: U = False
				else: bishop.append(buk[str(int(buk[a]) + i)] + str(int(b) + i))

			if int(buk[a]) + i < 9 and int(b) - i > 0 and R:
				if pos[pole[buk[str(int(buk[a]) + i)] + str(int(b) - i)]] in white: R = False
				if pos[pole[buk[str(int(buk[a]) + i)] + str(int(b) - i)]] in black: R = False
				else: bishop.append(buk[str(int(buk[a]) + i)] + str(int(b) - i))

			if int(buk[a]) - i > 0 and int(b) + i < 9 and L:
				if pos[pole[buk[str(int(buk[a]) - i)] + str(int(b) + i)]] in white: L = False
				if pos[pole[buk[str(int(buk[a]) - i)] + str(int(b) + i)]] in black: L = False
				else: bishop.append(buk[str(int(buk[a]) - i)] + str(int(b) + i))

			if int(buk[a]) - i > 0 and int(b) - i > 0 and D:
				if pos[pole[buk[str(int(buk[a]) - i)] + str(int(b) - i)]] in white: D = False
				if pos[pole[buk[str(int(buk[a]) - i)] + str(int(b) - i)]] in black: D = False
				else: bishop.append(buk[str(int(buk[a]) - i)] + str(int(b) - i))

		if x + y in bishop: return True
		else: return False

	if pos[pole[a + b]] == white[1] or pos[pole[a + b]] == white[-2]:
		queen1, queen2, recf, recfe = [], [], pos[pole[a + b]], pos[pole[x + y]]
		L, U, R, D = True, True, True, True

		if not rec:
			for i in ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'):
				for j in range(1, 9):
					if pos[pole[i + str(j)]] == white[0] or pos[pole[i + str(j)]] == white[-1]: xk, yk = i, str(j)

			pos[pole[x + y]] = pos[pole[a + b]]
			pos[pole[a + b]] = None

			for i in ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'):
				for j in range(1, 9):
					dobr = False
					if pos[pole[i + str(j)]] in black: dobr = instan1(i, str(j), xk, yk, True)
					if dobr:
						pos[pole[x + y]] = recfe
						pos[pole[a + b]] = recf
						return False
			pos[pole[x + y]] = recfe
			pos[pole[a + b]] = recf

		for i in range(1, 8):
			if int(buk[a]) - i > 0 and L:
				if pos[pole[buk[str(int(buk[a]) - i)] + b]] in black: L = False
				if pos[pole[buk[str(int(buk[a]) - i)] + b]] in white: L = False
				else: queen1.append(buk[str(int(buk[a]) - i)] + b)
			if int(buk[a]) + i < 9 and R:
				if pos[pole[buk[str(int(buk[a]) + i)] + b]] in black: R = False
				if pos[pole[buk[str(int(buk[a]) + i)] + b]] in white: R = False
				else: queen1.append(buk[str(int(buk[a]) + i)] + b)
			if int(b) + i < 9 and U:
				if pos[pole[a + str(int(b) + i)]] in black: U = False
				if pos[pole[a + str(int(b) + i)]] in white: U = False
				else: queen1.append(a + str(int(b) + i))
			if int(b) - i > 0 and D:
				if pos[pole[a + str(int(b) - i)]] in black: D = False
				if pos[pole[a + str(int(b) - i)]] in white: D = False
				else: queen1.append(a + str(int(b) - i))

		L, U, R, D = True, True, True, True	
		for i in range(1, 8):
			if int(buk[a]) + i < 9 and int(b) + i < 9 and U:
				if pos[pole[buk[str(int(buk[a]) + i)] + str(int(b) + i)]] in black: U = False
				if pos[pole[buk[str(int(buk[a]) + i)] + str(int(b) + i)]] in white: U = False
				else: queen2.append(buk[str(int(buk[a]) + i)] + str(int(b) + i))

			if int(buk[a]) + i < 9 and int(b) - i > 0 and R:
				if pos[pole[buk[str(int(buk[a]) + i)] + str(int(b) - i)]] in black: R = False
				if pos[pole[buk[str(int(buk[a]) + i)] + str(int(b) - i)]] in white: R = False
				else: queen2.append(buk[str(int(buk[a]) + i)] + str(int(b) - i))

			if int(buk[a]) - i > 0 and int(b) + i < 9 and L:
				if pos[pole[buk[str(int(buk[a]) - i)] + str(int(b) + i)]] in black: L = False
				if pos[pole[buk[str(int(buk[a]) - i)] + str(int(b) + i)]] in white: L = False
				else: queen2.append(buk[str(int(buk[a]) - i)] + str(int(b) + i))

			if int(buk[a]) - i > 0 and int(b) - i > 0 and D:
				if pos[pole[buk[str(int(buk[a]) - i)] + str(int(b) - i)]] in black: D = False
				if pos[pole[buk[str(int(buk[a]) - i)] + str(int(b) - i)]] in white: D = False
				else: queen2.append(buk[str(int(buk[a]) - i)] + str(int(b) - i))

		if x + y in queen2: return True
		elif x + y in queen1:
			if rec: return True
			if abs(int(b) - int(y)) % 2 == 1 or abs(int(buk[a]) - int(buk[x])) % 2 == 1:  
				if pos[pole[a + b]] == white[1]: pos[pole[a + b]] = white[-2]
				else: pos[pole[a + b]] = white[1]
			return True
		else: return False

	if pos[pole[a + b]] == black[1] or pos[pole[a + b]] == black[-2]:
		queen1, queen2, recf, recfe = [], [], pos[pole[a + b]], pos[pole[x + y]]
		L, U, R, D = True, True, True, True

		if not rec:
			for i in ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'):
				for j in range(1, 9):
					if pos[pole[i + str(j)]] == black[0] or pos[pole[i + str(j)]] == black[-1]: xk, yk = i, str(j)

			pos[pole[x + y]] = pos[pole[a + b]]
			pos[pole[a + b]] = None

			for i in ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'):
				for j in range(1, 9):
					dobr = False
					if pos[pole[i + str(j)]] in white: dobr = instan1(i, str(j), xk, yk, True)
					if dobr:
						pos[pole[x + y]] = recfe
						pos[pole[a + b]] = recf
						return False
			pos[pole[x + y]] = recfe
			pos[pole[a + b]] = recf

		for i in range(1, 8):
			if int(buk[a]) - i > 0 and L:
				if pos[pole[buk[str(int(buk[a]) - i)] + b]] in white: L = False
				if pos[pole[buk[str(int(buk[a]) - i)] + b]] in black: L = False
				else: queen1.append(buk[str(int(buk[a]) - i)] + b)
			if int(buk[a]) + i < 9 and R:
				if pos[pole[buk[str(int(buk[a]) + i)] + b]] in white: R = False
				if pos[pole[buk[str(int(buk[a]) + i)] + b]] in black: R = False
				else: queen1.append(buk[str(int(buk[a]) + i)] + b)
			if int(b) + i < 9 and U:
				if pos[pole[a + str(int(b) + i)]] in white: U = False
				if pos[pole[a + str(int(b) + i)]] in black: U = False
				else: queen1.append(a + str(int(b) + i))
			if int(b) - i > 0 and D:
				if pos[pole[a + str(int(b) - i)]] in white: D = False
				if pos[pole[a + str(int(b) - i)]] in black: D = False
				else: queen1.append(a + str(int(b) - i))

		L, U, R, D = True, True, True, True	
		for i in range(1, 8):
			if int(buk[a]) + i < 9 and int(b) + i < 9 and U:
				if pos[pole[buk[str(int(buk[a]) + i)] + str(int(b) + i)]] in white: U = False
				if pos[pole[buk[str(int(buk[a]) + i)] + str(int(b) + i)]] in black: U = False
				else: queen2.append(buk[str(int(buk[a]) + i)] + str(int(b) + i))

			if int(buk[a]) + i < 9 and int(b) - i > 0 and R:
				if pos[pole[buk[str(int(buk[a]) + i)] + str(int(b) - i)]] in white: R = False
				if pos[pole[buk[str(int(buk[a]) + i)] + str(int(b) - i)]] in black: R = False
				else: queen2.append(buk[str(int(buk[a]) + i)] + str(int(b) - i))

			if int(buk[a]) - i > 0 and int(b) + i < 9 and L:
				if pos[pole[buk[str(int(buk[a]) - i)] + str(int(b) + i)]] in white: L = False
				if pos[pole[buk[str(int(buk[a]) - i)] + str(int(b) + i)]] in black: L = False
				else: queen2.append(buk[str(int(buk[a]) - i)] + str(int(b) + i))

			if int(buk[a]) - i > 0 and int(b) - i > 0 and D:
				if pos[pole[buk[str(int(buk[a]) - i)] + str(int(b) - i)]] in white: D = False
				if pos[pole[buk[str(int(buk[a]) - i)] + str(int(b) - i)]] in black: D = False
				else: queen2.append(buk[str(int(buk[a]) - i)] + str(int(b) - i))

		if x + y in queen2: return True
		elif x + y in queen1:
			if rec: return True
			if abs(int(b) - int(y)) % 2 == 1 or abs(int(buk[a]) - int(buk[x])) % 2 == 1:  
				if pos[pole[a + b]] == black[1]: pos[pole[a + b]] = black[-2]
				else: pos[pole[a + b]] = black[1]
			return True
		else: return False

	if pos[pole[a + b]] == white[0] or pos[pole[a + b]] == white[-1]:

		if (a == x and b == y) or pos[pole[x + y]] in white: return False
		for i in ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'):
				for j in range(1, 9):
					if pos[pole[i + str(j)]] == black[0] or pos[pole[i + str(j)]] == black[-1]: xk, yk = i, str(j)
		if (abs(int(buk[x]) - int(buk[xk])) == 1 or int(buk[x]) - int(buk[xk]) == 0) and (abs(int(y) - int(yk)) == 1 or int(y) - int(yk) == 0) and (int(buk[x]) - int(buk[xk]) == 0 and int(y) - int(yk) == 0): return False
		if int(buk[a]) - int(buk[x]) == 2 and b == y and drkrw and pos[pole[buk[str(int(buk[a]) - 1)] + b]] == None and pos[pole[buk[str(int(buk[a]) - 2)] + b]] == None and pos[pole[buk[str(int(buk[a]) - 3)] + b]] == None and lwr and not rec:
			for i in ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'):
				for j in range(1, 9):
					dobr, dobr1, dobr2 = False, False, False
					if pos[pole[i + str(j)]] in black: 
						dobr = instan1(i, str(j), buk[str(int(buk[a]) - 1)], y, True)
						dobr1 = instan1(i, str(j), buk[str(int(buk[a]) - 2)], y, True)
						dobr2 = instan1(i, str(j), buk[str(int(buk[a]) - 2)], y, True)
					if dobr or dobr1 or dobr2: return False
			drkrw, krkrw = False, False
			pos[pole['a1']], pos[pole['d1']] = None, white[2]
			return True
		elif int(buk[a]) - int(buk[x]) == -2 and b == y and krkrw and pos[pole[buk[str(int(buk[a]) + 1)] + b]] == None  and pos[pole[buk[str(int(buk[a]) + 2)] + b]] == None and rwr and not rec:
			for i in ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'):
				for j in range(1, 9):
					dobr, dobr1 = False, False
					if pos[pole[i + str(j)]] in black: 
						dobr = instan1(i, str(j), buk[str(int(buk[a]) + 1)], y, True)
						dobr1 = instan1(i, str(j), buk[str(int(buk[a]) + 2)], y, True)
					if dobr or dobr1: return False
			drkrw, krkrw = False, False
			pos[pole['h1']], pos[pole['f1']] = None, white[2]
			return True
		elif (abs(int(buk[a]) - int(buk[x])) == 1 or abs(int(buk[a]) - int(buk[x])) == 0) and (abs(int(b) - int(y)) == 1 or abs(int(b) - int(y)) == 0) and not rec:
			for i in ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'):
				for j in range(1, 9):
					dobr = False
					if pos[pole[i + str(j)]] in black: dobr = instan1(i, str(j), x, y, True)
					if dobr: return False
			drkrw, krkrw = False, False
			if (abs(int(buk[a]) - int(buk[x])) == 1 and abs(int(b) - int(y)) == 0) or (abs(int(buk[a]) - int(buk[x])) == 0 and abs(int(b) - int(y)) == 1): 
				if pos[pole[a + b]] == white[0]: pos[pole[a + b]] = white[-1]
				else: pos[pole[a + b]] = white[0]
			return True

	if pos[pole[a + b]] == black[0] or pos[pole[a + b]] == black[-1]:

		if (a == x and b == y) or pos[pole[x + y]] in black: return False
		for i in ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'):
				for j in range(1, 9):
					if pos[pole[i + str(j)]] == white[0] or pos[pole[i + str(j)]] == white[-1]: xk, yk = i, str(j)
		if (abs(int(buk[x]) - int(buk[xk])) == 1 or int(buk[x]) - int(buk[xk]) == 0) and (abs(int(y) - int(yk)) == 1 or int(y) - int(yk) == 0) and (int(buk[x]) - int(buk[xk]) == 0 and int(y) - int(yk) == 0): return False
		if int(buk[a]) - int(buk[x]) == 2 and b == y and drkrb and pos[pole[buk[str(int(buk[a]) - 1)] + b]] == None and pos[pole[buk[str(int(buk[a]) - 2)] + b]] == None and pos[pole[buk[str(int(buk[a]) - 3)] + b]] == None and lbr and not rec:
			for i in ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'):
				for j in range(1, 9):
					dobr, dobr1, dobr2 = False, False, False
					if pos[pole[i + str(j)]] in white: 
						dobr = instan1(i, str(j), buk[str(int(buk[a]) - 1)], y, True)
						dobr1 = instan1(i, str(j), buk[str(int(buk[a]) - 2)], y, True)
						dobr2 = instan1(i, str(j), buk[str(int(buk[a]) - 2)], y, True)
					if dobr or dobr1 or dobr2: return False
			drkrb, krkrb = False, False
			pos[pole['a8']], pos[pole['d8']] = None, black[-3]
			return True
		elif int(buk[a]) - int(buk[x]) == -2 and b == y and krkrb and pos[pole[buk[str(int(buk[a]) + 1)] + b]] == None  and pos[pole[buk[str(int(buk[a]) + 2)] + b]] == None and rbr and not rec:
			for i in ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'):
				for j in range(1, 9): 
					dobr, dobr1 = False, False
					if pos[pole[i + str(j)]] in white: 
						dobr = instan1(i, str(j), buk[str(int(buk[a]) + 1)], y, True)
						dobr1 = instan1(i, str(j), buk[str(int(buk[a]) + 2)], y, True)
					if dobr or dobr1: return False
			drkrb, krkrb = False, False
			pos[pole['h8']], pos[pole['f8']] = None, black[-3]
			return True
		elif (abs(int(buk[a]) - int(buk[x])) == 1 or abs(int(buk[a]) - int(buk[x])) == 0) and (abs(int(b) - int(y)) == 1 or abs(int(b) - int(y)) == 0) and not rec:
			for i in ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'):
				for j in range(1, 9):
					dobr = False
					if pos[pole[i + str(j)]] in white: dobr = instan1(i, str(j), x, y, True)
					if dobr: return False
			drkrb, krkrb = False, False
			if (abs(int(buk[a]) - int(buk[x])) == 1 and abs(int(b) - int(y)) == 0) or (abs(int(buk[a]) - int(buk[x])) == 0 and abs(int(b) - int(y)) == 1): 
				if pos[pole[a + b]] == black[0]: pos[pole[a + b]] = black[-1]
				else: pos[pole[a + b]] = black[0]
			return True

	return False

drkrw, krkrw, drkrb, krkrb, lwr, rwr, lbr, rbr = True, True, True, True, True, True, True, True
a, b, x, y = 0, 0, 0, 0
run = True
turn = 1
while run:
	pygame.time.delay(10)
	prev = False
	for event in pygame.event.get():
		if event.type == pygame.QUIT: run = False
		elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			pm = pygame.mouse.get_pos()

			if x != 0: a, b = x, y

			if pm[0] <= 90: x = 'a'
			elif pm[0] > 90 and pm[0] <= 180: x = 'b'
			elif pm[0] > 180 and pm[0] <= 270: x = 'c'
			elif pm[0] > 270 and pm[0] <= 360: x = 'd'
			elif pm[0] > 360 and pm[0] <= 450: x = 'e'
			elif pm[0] > 450 and pm[0] <= 540: x = 'f'
			elif pm[0] > 540 and pm[0] <= 630: x = 'g'
			elif pm[0] > 630 and pm[0] <= 720: x = 'h'

			if pm[1] <= 90: y = '8'
			elif pm[1] > 90 and pm[1] <= 180: y = '7'
			elif pm[1] > 180 and pm[1] <= 270: y = '6'
			elif pm[1] > 270 and pm[1] <= 360: y = '5'
			elif pm[1] > 360 and pm[1] <= 450: y = '4'
			elif pm[1] > 450 and pm[1] <= 540: y = '3'
			elif pm[1] > 540 and pm[1] <= 630: y = '2'
			elif pm[1] > 630 and pm[1] <= 720: y = '1'

			if a == 0 and b == 0 and pos[pole[x + y]] == None: a, b, x, y = 0, 0, 0, 0

			if a != 0:
				dob = False
				if pos[pole[a + b]] in white and turn % 2 == 1: dob = instan1(a, b, x, y, False)
				elif pos[pole[a + b]] in black and turn % 2 == 0: dob = instan1(a, b, x, y, False)
				if dob:
					if not prev: pos[pole[x + y]] = pos[pole[a + b]]
					pos[pole[a + b]] = None
					turn += 1
				a, b, x, y = 0, 0, 0, 0
	
	update()
pygame.quit()