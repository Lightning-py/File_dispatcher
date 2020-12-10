import os
import chto_to_tam_design as design
import sys
from PyQt5 import QtWidgets
import sys

cwd = os.getcwd()

history = 0
history_array = []

def file_search(cwd):
		results = [str(i)[ str(i).index("'")  + 1 : -2 ] for i in os.scandir(cwd)]

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

class ExampleApp(QtWidgets.QDialog, design.Ui_Dialog):

	def __init__(self):
		super().__init__()
		self.setupUi(self)
		self.LineEdit.returnPressed.connect(self.set_items)
		self.scripts_LineEdit.returnPressed.connect(self.set_scripts_items)
		self.scripts_listWidget.itemPressed.connect(self.function)

	def set_items(self):
		if self.LineEdit.text() != "":
			self.listWidget.clear()


			try:
				result = file_search(self.LineEdit.text())

				self.listWidget.clear()
				self.listWidget.addItem('=>					папки---------------------------------------------------------------------------------')
				if len(result[0]) != 0:self.listWidget.addItems(result[0])
				else:self.listWidget.addItem('в этой папке нет вложенных папок')

				self.listWidget.addItem('=>					файлы---------------------------------------------------------------------------------')
				if len(result[1]) != 0:self.listWidget.addItems(result[1])
				else:self.listWidget.addItem('нет файлов в этой папке')
			except Exception as e:
				self.LineEdit.setText(str(e))

	def set_scripts_items(self):
		try:
			if os.path.isfile(self.scripts_LineEdit.text()) and self.scripts_LineEdit.text().endswith('.py'):
				os.system("python -u " + '"' + self.scripts_LineEdit.text() + '"')
				return None	
			result = file_search(self.scripts_LineEdit.text())

			fiile = []

			for files in result[1]:
				if files.endswith('.py'):
					fiile.append(files)
			
			if len(fiile) == 0:
				self.scripts_listWidget.clear()
				self.scripts_listWidget.addItem('файлов с расширением .py в данной папке нет')
				self.scripts_listWidget.addItem('какая жалость, поищите в другой папке')
			else:
				self.scripts_listWidget.clear()
				self.scripts_listWidget.addItems(fiile)
		except Exception as e:
			self.scripts_LineEdit.setText(str(e))			

	def function(self):
		print()
	
app = QtWidgets.QApplication(sys.argv)
window = ExampleApp()
window.show()
app.exec_()