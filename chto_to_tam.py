import os
import chto_to_tam_design as design
import sys
from PyQt5 import QtWidgets
import sys

cwd = os.getcwd()

history = 0
history_array = []

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
				walk_resuls = [i for i in os.walk(self.LineEdit.text())][0]
			
				self.listWidget.addItem('-----------------------------------------------------dirs----------------------------------------------------------------------------------------------------')

				self.listWidget.addItems(walk_resuls[1])

				self.listWidget.addItem('-----------------------------------------------------files----------------------------------------------------------------------------------------------------')

				self.listWidget.addItems(walk_resuls[2])
			except:
				self.LineEdit.setText("а вот нет")

	def set_scripts_items(self):
		try:
			if self.scripts_LineEdit.text().endswith(".py"):
				os.system('python -u ' + '"' + self.scripts_LineEdit.text() + '"')
			else:
				for i in [j for j in os.walk(self.scripts_LineEdit.text())][0][2]:
					if i.endswith('.py'): self.scripts_listWidget.addItem(i)
		except:
			self.scripts_LineEdit.setText("а вот и нет")

	def function(self):
		print()
	
app = QtWidgets.QApplication(sys.argv)
window = ExampleApp()
window.show()
app.exec_()