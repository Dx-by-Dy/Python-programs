class Group():
	
	def __init__(self, body, number):
		self.number = number
		self.body = body
		self.size = len(body)
		self.delete_me = False

	def check_size_number(self) -> bool:
		if self.size == self.number:
			for cell in self.body:
				pass
				#update(3, cell, bombs_defuse, true_bombs_defuse, 1)
			self.delete_me = True
		if self.number == 0:
			for cell in self.body:
				pass
				#update(1, cell, bombs_defuse, true_bombs_defuse, 1)
			self.delete_me = True

	def substraction(self, another_group) -> None:
		for cell in another_group.body:
			if cell in self.body: self.body.remove(cell)
		self.number -= another_group.number
		self.check_size_number()

	def contains(self, body_another_group) -> bool:
		for cell in body_another_group:
			if cell not in self.body: return False
		return True

	def intersect(self, body_another_group) -> bool:
		for cell in body_another_group:
			if cell in self.body: return True
		return False

	def intersect_body(self, body_another_group) -> list:
		inter_body = []
		for cell in body_another_group:
			if cell in self.body: inter_body += [cell]
		return inter_body

	def print_me(self):
		print(self.body, self.number)


Groups = [Group([(1, 2)], 1), Group([(1, 1), (1, 2)], 1)]
new_groups = []
for id_first_group in range(len(Groups)):
	if Groups[id_first_group].delete_me: continue
	for id_second_group in range(id_first_group + 1, len(Groups)):
		if Groups[id_second_group].delete_me: continue
		if Groups[id_first_group].size < Groups[id_second_group].size: id_first_group, id_second_group = id_second_group, id_first_group
		if Groups[id_first_group].intersect(Groups[id_second_group].body):
			if Groups[id_first_group].contains(Groups[id_second_group].body):
				Groups[id_first_group].substraction(Groups[id_second_group])
			else:
				new_body = Groups[id_first_group].intersect_body(Groups[id_second_group].body)
				if Groups[id_first_group].number > Groups[id_second_group].number:
					new_number = Groups[id_first_group].number - Groups[id_second_group].size + len(Groups[id_second_group].intersect_body(new_body))
				else:
					new_number = Groups[id_second_group].number - Groups[id_first_group].size + len(Groups[id_first_group].intersect_body(new_body))
				new_groups += [Group(new_body, new_number)]
				Groups[id_first_group].substraction(new_groups[-1])
				Groups[id_second_group].substraction(new_groups[-1])

for i in new_groups:
	i.print_me()
print()
for i in Groups:
	i.print_me()