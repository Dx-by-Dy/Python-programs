from os import sys
from PyQt6.QtCore import QSize, Qt, QRect
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QMainWindow, QPushButton, QVBoxLayout, QFileDialog

app = QApplication([])

class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()

		self.setWindowTitle("Database")
		self.resize(QSize(1200, 800))
		self.setMinimumSize(800, 600)

		self.create_search_button()
		self.create_add_button()
		self.create_delete_button()

	def create_search_button(self):
		self.search_button = QPushButton(self)
		self.search_button.setCheckable(True)
		self.search_button.setGeometry(QRect(0, 0, 50, 20))
		self.search_button.setText("Поиск")
		self.search_button.clicked.connect(self.the_search_button_was_clicked)
		#self.search_button.setShortcut('Ctrl+D')  # установить шорткат

	def create_add_button(self):
		self.add_button = QPushButton(self)
		self.add_button.setCheckable(True)
		self.add_button.setGeometry(QRect(50, 0, 65, 20))
		self.add_button.setText("Добавить")
		self.add_button.clicked.connect(self.the_add_button_was_clicked)

	def create_delete_button(self):
		self.delete_button = QPushButton(self)
		self.delete_button.setCheckable(True)
		self.delete_button.setGeometry(QRect(115, 0, 65, 20))
		self.delete_button.setText("Удалить")
		self.delete_button.clicked.connect(self.the_delete_button_was_clicked)

	def the_delete_button_was_clicked(self):
		self.delete_button.setChecked(False)

	def the_search_button_was_clicked(self):
		self.search_button.setChecked(False)

	def the_add_button_was_clicked(self):
		self.add_button.setChecked(False)
		self.get_file_name()

	def get_file_name(self):
		return QFileDialog.getOpenFileName(self, "Выбрать файл", ".", "Excel (*.xml *.xls *.xlsx)")
		# пример возвращения ('C:/Python programs/RL.xls', 'Excel (*.xml *.xls *.xlsx)')
		# если ничего не выбрал то ('', '')

window = MainWindow()
window.show()

sys.exit(app.exec())