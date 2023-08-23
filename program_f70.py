from os import sys
import psycopg2
from openpyxl import load_workbook
from datetime import datetime
from PyQt6.QtCore import QSize, Qt, QRect
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QMainWindow, QPushButton, QVBoxLayout, \
							QFileDialog, QLineEdit, QDateEdit, QComboBox, QTextEdit
from PyQt6.QtGui import QPainter, QColor, QBrush, QFont

class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()

		self.font_arial_size7 = QFont("Arial", 7)
		self.font_arial_size8 = QFont("Arial", 8)
		self.font_arial_size10 = QFont("Arial", 10)
		self.font_arial_size15 = QFont("Arial", 15)

		self.setMouseTracking(True)

		self.lines_with_data = []
		self.menu_widgets = []
		self.y_coord_in_body = 255

		self.mode_menu = 'searching'

		self.russian_names_coloms = ["№ протокола", \
									"Дата выдачи", \
									"Фамилия", \
									"Имя", \
									"Отчество", \
									"Дата рождения", \
									"Адрес", \
									"Инвалидность", \
									"ОМС", \
									"№ карты", \
									"№ участка", \
									"Диагноз", \
									"Код", \
									"Фамилия врача", \
									"Тип ф.70", \
									]
		self.english_names_coloms = ["protocol_id", \
									"date_of_issue", \
									"second_name", \
									"first_name", \
									"surname", \
									"date_of_birth", \
									"address", \
									"disability", \
									"CHI", \
									"outpatient_card_id", \
									"site", \
									"diagnosis", \
									"code", \
									"doctor_second_name", \
									"type_f70", \
									]

		self.disability_items = ['-', 'инв I гр.', 'инв II гр.', 'инв III гр.', 'раб.', 'не раб.', 'реб. инв.']
		self.type_f70_items = ['-', 'органы дыхания', 'органы опор-дв. апп.', 'органы ССС', 'органы эндок. сист.', \
								'органы нерв. сист.', 'другое']

		self.x_len_labels = []
		for i in range(15):
			if i == 4: self.x_len_labels += [120] # +15
			elif i == 6: self.x_len_labels += [150] # 150
			elif i == 8: self.x_len_labels += [125]
			elif i == 9: self.x_len_labels += [80]
			elif i == 11: self.x_len_labels += [130]
			elif i == 12: self.x_len_labels += [60] # 60
			elif i == 14: self.x_len_labels += [130]
			else: self.x_len_labels += [100]

		self.setWindowTitle("Database")
		self.setFixedSize(QSize(1700, 800))
		self.setMinimumSize(800, 600)

		self.create_search_button()
		self.create_add_button()
		self.create_delete_button()
		self.create_labels()

		self.protocol_id_data = ''
		self.date_of_issue_data = ''
		self.first_name_data = ''
		self.second_name_data = ''
		self.surname_data = ''
		self.date_of_birth_data = ''
		self.address_data = ''
		self.disability_data = ''
		self.CHI_data = ''
		self.outpatient_card_id_data = ''
		self.site_data = ''
		self.diagnosis_data = ''
		self.code_data = ''
		self.doctor_second_name_data = ''
		self.type_f70_data = ''

		self.search_menu()

	def create_labels(self):
		x_coord = 20
		for i in range(15):
			body_label = QLabel(self.russian_names_coloms[i], self)
			body_label.setGeometry(QRect(x_coord, 225, self.x_len_labels[i], 20))
			body_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
			body_label.setFont(self.font_arial_size10)
			body_label.setStyleSheet("background-color:" + "#eeeeee; border: 1px solid black;")

			x_coord += self.x_len_labels[i] + 5

	def create_search_button(self):
		self.search_button = QPushButton(self)
		self.search_button.setCheckable(True)
		self.search_button.setGeometry(QRect(0, 0, 50, 20))
		self.search_button.setText("Поиск")
		self.search_button.clicked.connect(self.the_search_button_was_clicked)

	def create_add_button(self):
		self.add_button = QPushButton(self)
		self.add_button.setCheckable(True)
		self.add_button.setGeometry(QRect(50, 0, 65, 20))
		self.add_button.setText("Добавить")
		self.add_button.clicked.connect(self.the_add_button_was_clicked)

		#self.add_button_list = QComboBox(self)
		#self.add_button_list.addItems([''])

	def create_delete_button(self):
		self.delete_button = QPushButton(self)
		self.delete_button.setCheckable(True)
		self.delete_button.setGeometry(QRect(115, 0, 65, 20))
		self.delete_button.setText("Удалить")
		self.delete_button.clicked.connect(self.the_delete_button_was_clicked)

	def search_menu(self):

		x_coord = 20
		for i in range(15):

			if self.english_names_coloms[i] == 'disability':
				input_line = QComboBox(self)
				input_line.addItems(self.disability_items)
				input_line.activated.connect(getattr(self, 'get_' + self.english_names_coloms[i] + '_data'))
				input_line.setFont(self.font_arial_size10)

			elif self.english_names_coloms[i] == 'type_f70':
				input_line = QComboBox(self)
				input_line.addItems(self.type_f70_items)
				input_line.activated.connect(getattr(self, 'get_' + self.english_names_coloms[i] + '_data'))
				input_line.setFont(self.font_arial_size10)

			elif self.english_names_coloms[i] == 'second_name' or self.english_names_coloms[i] == 'first_name' \
				or self.english_names_coloms[i] == 'surname' or self.english_names_coloms[i] == 'address' \
				or self.english_names_coloms[i] == 'diagnosis':

				input_line = QTextEdit(self)
				self.menu_widgets += [input_line]
				input_line.textChanged.connect(getattr(self, 'get_' + self.english_names_coloms[i] + '_data'))
				input_line.setAlignment(Qt.AlignmentFlag.AlignCenter)
				input_line.setFont(self.font_arial_size8)
				#input_line.autoFormatting()

			else:
				input_line = QLineEdit(self)
				input_line.textEdited.connect(getattr(self, 'get_' + self.english_names_coloms[i] + '_data'))
				input_line.setAlignment(Qt.AlignmentFlag.AlignCenter)
				input_line.setFont(self.font_arial_size10)


			input_line.setGeometry(QRect(x_coord, 30, self.x_len_labels[i], 25))
			input_line.setStyleSheet("border: 2px solid black;")

			input_label = QLabel(self.russian_names_coloms[i], self)
			input_label.setGeometry(QRect(x_coord, 50, self.x_len_labels[i], 30))
			input_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
			input_label.setFont(self.font_arial_size8)

			x_coord += self.x_len_labels[i] + 5


		self.enter_search_button = QPushButton(self)
		self.enter_search_button.setCheckable(True)
		self.enter_search_button.setGeometry(QRect(self.size().width() - 145, 170, 130, 35))
		self.enter_search_button.setText("Искать")
		self.enter_search_button.clicked.connect(self.the_enter_search_button_was_clicked)
		self.enter_search_button.setFont(self.font_arial_size15)
		self.enter_search_button.setMouseTracking(True)
		self.enter_search_button.setStyleSheet("background-color: #009900; border-radius: 10px; \
												border: 1px solid black;")
		self.enter_search_button.setShortcut('Ctrl+Return')

		self.enter_add_button = QPushButton(self)
		self.enter_add_button.setCheckable(True)
		self.enter_add_button.setGeometry(QRect(self.size().width() - 145, 170, 130, 35))
		self.enter_add_button.setText("Добавить")
		self.enter_add_button.clicked.connect(self.the_enter_add_button_was_clicked)
		self.enter_add_button.setFont(self.font_arial_size15)
		self.enter_add_button.setMouseTracking(True)
		self.enter_add_button.setStyleSheet("background-color: #0000aa; border-radius: 10px; \
												border: 1px solid black;")
		self.enter_add_button.setShortcut('Ctrl+Return')
		self.enter_add_button.hide()

	def mouseMoveEvent(self, e):
		if self.mode_menu == 'searching':
			if e.position().toPoint() in QRect(self.size().width() - 145, 170, 130, 35):
				self.enter_search_button.setStyleSheet("background-color: #007700; border-radius: 10px; \
														border: 1px solid black;")
			elif e.position().toPoint() not in QRect(self.size().width() - 145, 170, 130, 35): 
				self.enter_search_button.setStyleSheet("background-color: #009900; border-radius: 10px; \
														border: 1px solid black;")
		elif self.mode_menu == 'adding':
			if e.position().toPoint() in QRect(self.size().width() - 145, 170, 130, 35):
				self.enter_add_button.setStyleSheet("background-color: #000099; border-radius: 10px; \
														border: 1px solid black;")
			elif e.position().toPoint() not in QRect(self.size().width() - 145, 170, 130, 35): 
				self.enter_add_button.setStyleSheet("background-color: #0000aa; border-radius: 10px; \
														border: 1px solid black;")


	def get_protocol_id_data(self, data):
		self.protocol_id_data = data

	def get_date_of_issue_data(self, data):
		try: self.date_of_issue_data = datetime.strptime(data, '%d.%m.%Y').date()
		except ValueError: self.date_of_issue_data = ''

	def get_second_name_data(self):
		self.second_name_data = self.menu_widgets[0].toPlainText()

	def get_first_name_data(self):
		self.first_name_data = self.menu_widgets[1].toPlainText()

	def get_surname_data(self):
		self.surname_data = self.menu_widgets[2].toPlainText()

	def get_date_of_birth_data(self, data):
		try: self.date_of_birth_data = datetime.strptime(data, '%d.%m.%Y').date()
		except ValueError: self.date_of_birth_data = ''

	def get_address_data(self):
		self.address_data = self.menu_widgets[3].toPlainText()

	def get_disability_data(self, data):
		if data == 0: self.disability_data = ''
		else: self.disability_data = self.disability_items[data]

	def get_CHI_data(self, data):
		self.CHI_data = data

	def get_outpatient_card_id_data(self, data):
		self.outpatient_card_id_data = data

	def get_site_data(self, data):
		self.site_data = data

	def get_diagnosis_data(self):
		self.diagnosis_data = self.menu_widgets[4].toPlainText()

	def get_code_data(self, data):
		self.code_data = data

	def get_doctor_second_name_data(self, data):
		self.doctor_second_name_data = data

	def get_type_f70_data(self, data):
		if data == 0: self.type_f70_data = ''
		else: self.type_f70_data = self.type_f70_items[data]


	def paintEvent(self, e):
		self.qp = QPainter()
		self.qp.begin(self)
		self.qp.setBrush(QColor(150, 150, 150))
		self.qp.drawRect(0, 20, self.size().width(), 200)

		self.qp.setBrush(QColor(200, 200, 200))
		self.qp.drawRect(0, 220, self.size().width(), self.size().height())

		self.qp.setBrush(QColor(0, 0, 0))
		self.qp.drawLine(0, 250, self.size().width(), 250)
		self.qp.end()

	def delete_body_data(self):
		for id_line in range(len(self.lines_with_data)):
			for wind in self.lines_with_data[id_line]:
				wind.hide()
		self.lines_with_data = []
		self.y_coord_in_body = 255

	def the_delete_button_was_clicked(self):
		self.delete_button.setChecked(False)

	def the_search_button_was_clicked(self):
		self.search_button.setChecked(False)

		self.delete_body_data()
		if self.mode_menu == 'adding':
			self.enter_add_button.hide()

		self.mode_menu = 'searching'

		self.enter_search_button.show()

	def add_one_line_in_body(self, data):

		x_coord = 20
		one_line_of_data = []

		for i in range(15):
			if i == 1 or i == 5: print_data_line = QTextEdit(data[i].strftime("%d.%m.%Y"), self)
			else: print_data_line = QTextEdit(data[i], self)

			print_data_line.setGeometry(QRect(x_coord, self.y_coord_in_body, self.x_len_labels[i], 25))
			print_data_line.setAlignment(Qt.AlignmentFlag.AlignCenter)

			if i in [2, 3, 4, 6, 8, 11]: print_data_line.setFont(self.font_arial_size8)
			else: print_data_line.setFont(self.font_arial_size10)

			print_data_line.setStyleSheet("border: 1px solid black; background-color:" + "#888888;")
			print_data_line.setReadOnly(True)

			one_line_of_data += [print_data_line]
			x_coord += self.x_len_labels[i] + 5

		self.lines_with_data += [one_line_of_data]
		self.y_coord_in_body += 30

	def add_data_from_db_in_body(self, data):

		for id_data_line in range(len(data)):
			self.add_one_line_in_body(data[id_data_line])

		self.print_all_data_in_body()

	def print_all_data_in_body(self):
		for id_line in range(len(self.lines_with_data)):
			for wind in self.lines_with_data[id_line]:
				wind.show()

	def print_new_line(self):
		for wind in self.lines_with_data[-1]:
			wind.show()

	def the_enter_search_button_was_clicked(self):
		self.enter_search_button.setChecked(False)

		self.delete_body_data()

		sql_request = "SELECT protocol_id, date_of_issue, second_name, first_name, \
								surname, date_of_birth, address, \
								disability, CHI, outpatient_card_id, site, diagnosis, \
								code, doctor_second_name, type_f70 FROM f70 "

		first_add = True
		data = []
		for i in range(15):
			if getattr(self, self.english_names_coloms[i] + '_data') != '': 
				if first_add:
					first_add = False
					sql_request += "WHERE " + self.english_names_coloms[i] + " = %s "
				else: sql_request += "and " +  self.english_names_coloms[i] + " = %s "
				data += [getattr(self, self.english_names_coloms[i] + '_data')]

		if not first_add: 
			cursor.execute(sql_request, data)
			self.add_data_from_db_in_body(cursor.fetchall())

	def the_enter_add_button_was_clicked(self):

		
		sql_request = "SELECT protocol_id, date_of_issue, second_name, first_name, \
								surname, date_of_birth, address, \
								disability, CHI, outpatient_card_id, site, diagnosis, \
								code, doctor_second_name, type_f70 FROM f70 "
		

		first_add = True
		data = []
		for i in range(15):
			if getattr(self, self.english_names_coloms[i] + '_data') != '': 
				if first_add:
					first_add = False
					sql_request += "WHERE " + self.english_names_coloms[i] + " = %s "
				else: sql_request += "and " +  self.english_names_coloms[i] + " = %s "
				data += [getattr(self, self.english_names_coloms[i] + '_data')]
			else: data += [None]

		sql_request = "INSERT INTO f70 (protocol_id, date_of_issue, second_name, first_name, \
								surname, date_of_birth, address, \
								disability, CHI, outpatient_card_id, site, diagnosis, \
								code, doctor_second_name, type_f70) VALUES \
								(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

		print(data)
		if not first_add: 
			cursor.execute(sql_request, data)
			self.add_one_line_in_body(data)
			self.print_new_line()

	def the_add_button_was_clicked(self):
		self.add_button.setChecked(False)

		self.delete_body_data()
		if self.mode_menu == 'searching':
			self.enter_search_button.hide()

		self.mode_menu = 'adding'
		self.enter_add_button.show()


		#self.get_file_name()

	def get_file_name(self):
		return QFileDialog.getOpenFileName(self, "Выбрать файл", ".", "Excel (*.xml *.xls *.xlsx)")
		# пример возвращения ('C:/Python programs/RL.xls', 'Excel (*.xml *.xls *.xlsx)')
		# если ничего не выбрал то ('', '')


if __name__ == "__main__":
	app = QApplication([])

	conn = psycopg2.connect(dbname="postgres", user="postgres", password="9", host="127.0.0.1")
	cursor = conn.cursor()

	conn.autocommit = True

	window = MainWindow()
	window.show()

	app.exec()

	cursor.close()
	conn.close()