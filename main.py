'''импорты всего чего только можно'''
import os
import ui as design
from copy import deepcopy
import sys
from threading import Thread
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtWidgets import QInputDialog
from pyperclip import copy



def write_file(file):
	'''эта функция просто записывает последнюю папку в которую вы зашли чтобы при перезапуске приложения открытые папки сохранялись'''
	try:
		f = open('./settings.json', 'r')
		content = []
		for i in f:
			content.append(i)
		f.close()
		f = open('./settings.json', 'w')
		for i in content:
			if i.startswith('last_file: '):
				f.write('last_file: ' + "'" + file + "'")
			else:
				f.write(i)
	except:
		return 'не удалось записать файл'


data = {}

def get_comands():
	'''эта функция получает команды на открытие файлов и приложений
	пример:
	code ...
	открывает файл в Visual Studio Code
	'''
	f = open('./settings.json')
	global data
	try:
		for i in f:
			data[i[0 : i.index("'") - 2]] = i[i.index("'") + 1 : ].replace('\n', '')[ : -1]
	except:
		pass

get_comands()

def file_search(cwd):
	'''это функция поиска
	на вход принимает папку, содержимое которой необходимо узнать
	просто возвращает  список в виде [ [все папки], [все файлы]]
	'''
	try:
		results = [str(i)[ str(i).index("'")  + 1 : -2 ] for i in os.scandir(cwd)]
	except:
		print("it's an error")
		return []

	files = [ [], [] ]

	for i in results:
		if os.path.isfile(cwd) == False and cwd.endswith("/") == False:
			if os.path.isdir(cwd + "/" + i):
				files[0].append(i)
			else:
				files[1].append(i)
		else:
			if os.path.isdir(cwd + "/" + i):
				files[0].append(i)
			else:
				files[1].append(i)
	return files


array = ['hide_dirs', 'hide_files'] 

class ExampleApp(QtWidgets.QDialog, design.Ui_Dialog):

	def __init__(self):
		super().__init__()

		# self.set_script("")


		self.setupUi(self)

		self.listWidget.setFont(QtGui.QFont("Fira Code Light", 11, QtGui.QFont.Bold))
		self.scripts_listWidget.setFont(QtGui.QFont("Fira Code Light", 11, QtGui.QFont.Bold))
		self.LineEdit.setFont(QtGui.QFont("Fira Code Light", 11, QtGui.QFont.Bold))
		self.scripts_LineEdit.setFont(QtGui.QFont("Fira Code Light", 11, QtGui.QFont.Bold))
		self.finder_LineEdit.setFont(QtGui.QFont("Fira Code Light", 11, QtGui.QFont.Bold))

		self.LineEdit.returnPressed.connect(self.set_items)

		self.scripts_LineEdit.returnPressed.connect(self.set_scripts_items)

		self.finder_LineEdit.returnPressed.connect(self.set_scripts_items)

		self.listWidget.itemDoubleClicked.connect(self.new_search)

		self.listWidget.itemClicked.connect(self.selectionChanged)

		self.scripts_listWidget.itemDoubleClicked.connect(self.start_program_on_python)




	def new_search(self, item):
		'''функция которая ищет содержимое файла и сразу заполняет им нужный список
		ну и еще открывает файлы при нажатии на них
		кстати открывает-то в отдельном потоке, а все приложение все равно виснет'''
		dir_now = self.LineEdit.text() + item.text()
		if os.path.isdir(dir_now) and not dir_now.endswith('/'):
			dir_now += '/'
			self.LineEdit.setText(self.LineEdit.text() + '/')
			write_file(dir_now)
		if os.path.isdir(dir_now):
			write_file(dir_now)
			self.listWidget.clear()
			os.system('cd ' + dir_now)
			result = file_search(dir_now)
			self.LineEdit.setText(dir_now)
			self.listWidget.clear()
			self.listWidget.addItem(f'|>	{len(result[0])}				папок---------------------------------------------------------------------------------')
			if len(result[0]) != 0:
				if len(result[0]) >= 16:
					self.listWidget.addItems(result[0][ : 15] + ['d---->'])
					array[0] = 'hide_dirs'
				else:
					self.listWidget.addItems(result[0])
					array[0] = 'full_dirs'
			else:
				self.listWidget.addItem('в этой папке нет вложенных папок')
			self.listWidget.addItem(f'|>	{len(result[1])}				файлов--------------------------------------------------------------------------------')
			if len(result[1]) != 0:
				if len(result[1]) >= 16:
					self.listWidget.addItems(result[1][ : 15] + ['f---->'])
					array[0] = 'hide_files'
				else:
					self.listWidget.addItems(result[1])
					array[1] = 'full_dirs'
			else:
				self.listWidget.addItem('нет файлов в этой папке')
		#____________________________________________________
		elif os.path.isfile(dir_now) and (dir_now.endswith('.jpg') or dir_now.endswith('.ico') or dir_now.endswith('.png')) and data['images_show_comand'] != '':
			t1 = Thread(name='pictures', target=os.system(data['images_show_comand'] +  dir_now))
			t1.start()
			t1.join()
		#____________________________________________________
		elif os.path.isfile(dir_now) and (dir_now.endswith('.json') or dir_now.endswith('.py')):
			if data['files_open_comand'] != '':
				t2 = Thread(name='pictures', target=os.system(data['files_open_comand'] + dir_now))
				t2.start()
				t2.join()
			else:
				self.terminal.setText('')
				for i in open(dir_now):
					self.terminal.setText(self.terminal.toPlainText() + i)
		

	def run(self, item):
		'''функция которая просто запускает питонвский файл (ну это же типа программируемый менеджер)'''
		if os.path.isfile(self.scripts_LineEdit.text() + item.text()) and item.text().endswith('.py'):
			os.system("python -u " + '"' + self.scripts_LineEdit.text() + item.text() + '"')

	def start_program_on_python(self, item):
		'''функция которая в отдельном потоке запускает предыдущую функцию (в отдельном потоке для того чтобы менеджер не зависал пока выполняется файл)'''
		t = Thread(name='python file exec', target=self.run(item))
		t.start()
		t.join()

	def selectionChanged(self, item):
		'''а вот и та функция для которой нужен был список перед классом
		это функция которая обрабатывает нажатия на кнопки
		например если вы нажмете 'd--->' она выдвинет весь список папок и так далее'''
		text = deepcopy(item.text())
		if item.text() == 'd---->':
			self.set_items(arg='full_dirs', arg2=array[1])
		elif item.text() == 'f---->':
			self.set_items(arg=array[0], arg2='full_files')
		elif item.text() == '    delete':
			if os.path.isdir(self.LineEdit.text() + self.listWidget.item(self.listWidget.currentRow() - 1).text()):
				os.rmdir(self.LineEdit.text() + self.listWidget.item(self.listWidget.currentRow() - 1).text())
			elif os.path.isfile(self.LineEdit.text() + self.listWidget.item(self.listWidget.currentRow() - 1).text()):
				os.remove(self.LineEdit.text() + self.listWidget.item(self.listWidget.currentRow() - 1).text())
			self.set_items()
		elif item.text() == '    rename':
			text_dialog, ok = QInputDialog.getText(self, 'input dialog', 'enter the file name')
			if ok:
				os.rename(self.LineEdit.text() + self.listWidget.item(self.listWidget.currentRow() - 2).text(), self.LineEdit.text() + text_dialog)
			self.set_items(arg='full_dirs', arg2='full_files')
		elif item.text() == '    copy':
			copy(self.LineEdit.text() + self.listWidget.item(self.listWidget.currentRow() - 3).text())
			'''я успел реализовать копирование пока это писал
			а вот функцию вставки пока не реализовал, хах'''
		elif item.text() == '    replace':
			text_dialog, ok = QInputDialog.getText(self, 'input dialog', 'enter the file name')
			if ok:
				os.rename(self.LineEdit.text() + self.listWidget.item(self.listWidget.currentRow() - 4).text(), text_dialog + self.listWidget.item(self.listWidget.currentRow() - 4).text())
		

		else:
			'''вот тут она что-то делает  если вы кликаете не по кнопкам, а по папке или файлу
			она вам высвечивает список кнопочек'''
			if os.path.isdir(self.LineEdit.text() + item.text()):

				result = file_search(self.LineEdit.text())
				self.listWidget.clear()
				




				self.listWidget.addItem(f'|>	{len(result[0])}				папок---------------------------------------------------------------------------------')
				if len(result[0]) != 0:
					self.listWidget.addItems(result[0][ : result[0].index(text) + 1] + ['    delete', '    rename', '    copy', '    replace', '    paste'] + result[0][result[0].index(text) + 1: ])
				else:
					self.listWidget.addItem('в этой папке нет вложенных папок')
				self.listWidget.addItem(f'|>	{len(result[1])}				файлов--------------------------------------------------------------------------------')
				if len(result[1]) != 0:
					if len(result[1]) >= 16:
						self.listWidget.addItems(result[1][ : 15] + ['f---->'])
					else:
						self.listWidget.addItems(result[1])
				else:
					self.listWidget.addItem('нет файлов в этой папке')





			elif os.path.isfile(self.LineEdit.text() + text):
				result = file_search(self.LineEdit.text())
				self.listWidget.clear()


				self.listWidget.addItem(f'|>	{len(result[0])}				папок---------------------------------------------------------------------------------')
				if len(result[0]) != 0:
					if len(result[0]) >= 16:
						self.listWidget.addItems(result[0][ : 15] + ['d---->'])
					else:
						self.listWidget.addItems(result[0])
				else:
					self.listWidget.addItem('в этой папке нет вложенных папок')
				self.listWidget.addItem(f'|>	{len(result[1])}				файлов--------------------------------------------------------------------------------')
				if len(result[1]) != 0:
					self.listWidget.addItems(result[1][ : result[1].index(text) + 1] + ['    delete', '    rename', '    copy', '    replace'] + result[1][result[1].index(text) + 1: ])
				else:
					self.listWidget.addItem('нет файлов в этой папке')




	def set_items(self, arg='hide_dirs', arg2='hide_files'):
		'''очередная блин функция для поиска, причем я удивляюсь тому что они все разные
		и тут опять же нужен список перед классом'''
		if self.LineEdit.text() != "":
			if self.LineEdit.text().startswith("|>"):
				try:
					exec(self.LineEdit.text()[3 : ])
				except Exception as e:
					print(e)
				self.LineEdit.setText("|> ")
			elif self.LineEdit.text().startswith("||>"):
				try:
					os.system(self.LineEdit.text()[4 : ])
				except Exception as e:
					print(e)
				self.LineEdit.setText("||> ")

			else:
				write_file(self.LineEdit.text())
				result = file_search(self.LineEdit.text())
				self.listWidget.clear()
				try:
					self.listWidget.clear()
					self.listWidget.addItem(f'|>	{len(result[0])}				папок---------------------------------------------------------------------------------')
					if len(result[0]) != 0:
						if len(result[0]) >= 16 and arg == 'hide_dirs':
							self.listWidget.addItems(result[0][ : 15] + ['d---->'])
							array[0] = 'hide_dirs'
						else:
							self.listWidget.addItems(result[0])
							array[0] = 'full_dirs'
					else:
						self.listWidget.addItem('в этой папке нет вложенных папок')
					self.listWidget.addItem(f'|>	{len(result[1])}				файлов--------------------------------------------------------------------------------')
					if len(result[1]) != 0:
						if len(result[1]) >= 16 and arg2 == 'hide_files':
							self.listWidget.addItems(result[1][ : 15] + ['f---->'])
							array[0] = 'hide_files'
						else:
							self.listWidget.addItems(result[1])
							array[1] = 'full_dirs'
					else:
						self.listWidget.addItem('нет файлов в этой папке')
					return
				except Exception as e:
					print(e)

	def set_scripts_items(self):
		'''вот тут я собираю значения в список поиска файлов с каким-то расширением и если кликнуть на элемент и он .py файл то оно его запустит, 
		используя функцию '''
		try:
			if os.path.isfile(self.scripts_LineEdit.text()) and self.scripts_LineEdit.text().endswith('.py'):
				self.start_program_on_python(self.scripts_LineEdit.text())
				return None	
			result = file_search(self.scripts_LineEdit.text())

			'''и опять же функция поиска, но уже чтобы искать файлы с данными расширениями'''

			fiile = []

			for files in result[1]:
				if files.endswith(self.finder_LineEdit.text()):
					fiile.append(files)
			
			if len(fiile) == 0:
				self.scripts_listWidget.clear()
				self.scripts_listWidget.addItem(f'файлов с расширением {self.finder_LineEdit.text()} в данной папке нет')
				self.scripts_listWidget.addItem('какая жалость, поищите в другой папке')
			else:
				self.scripts_listWidget.clear()
				self.scripts_listWidget.addItems(fiile)
		except Exception as e:
			print(e)			



'''запуск всего этого'''
if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	window = ExampleApp()
	window.show()
	app.exec_()
