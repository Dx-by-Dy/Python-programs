'''
inpt = open('input.txt', 'r')
f = open('output.txt', 'w+')

for i in inpt:
 	data = sum(map(int, i.split()))
f.write(str(data))
'''

a, b = input(), input()
cnt = 0
for i in b:
	if i in a: cnt += 1

print(cnt)

