# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/sergey/design_saves/my_vk_design.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets

f = open('/home/sergey/fm/settings.txt')

list_ = []

for i in f:
    list_.append(i)
f.close()

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        #создаем окошко
        #----------------------------------------------------------------- функция только для создателя (ну либо пишите свой адрес картинки)
        Dialog.setWindowIcon(QtGui.QIcon(list_[0][0 : -1] + 'explorer.ico'))
        #----------------------------------------------------------------- конец
        Dialog.setObjectName("not_Dialog")
        Dialog.title = "qwe"
        Dialog.resize(1920, 1080)

        #создаем первую строку ввода
        self.LineEdit = QtWidgets.QLineEdit(Dialog)
        self.LineEdit.setObjectName("LineEdit")
        self.LineEdit.setGeometry(61, 1, 1000, 30)
        self.LineEdit.setText('')
        # self.LineEdit.setStyleSheet('background-color:#333333')

        #создаем виджет который отображает результаты
        self.listWidget = QtWidgets.QListWidget(Dialog)
        self.listWidget.setGeometry(QtCore.QRect(0, 35, 1300, 1014))
        self.listWidget.setObjectName("listWidget")
        self.listWidget.addItem('чтобы увидеть файлы в нужной папке введите путь к папке')
        # self.listWidget.setStyleSheet('background-color:#333333')

        #создаем вторую строку ввода
        self.scripts_LineEdit = QtWidgets.QLineEdit(Dialog)
        self.scripts_LineEdit.setGeometry(QtCore.QRect(1305, 35, 443, 30))
        self.scripts_LineEdit.setObjectName("scripts_Lineedit")
        # self.scripts_LineEdit.setStyleSheet('background-color:#333333')

        self.finder_LineEdit = QtWidgets.QLineEdit(Dialog)
        self.finder_LineEdit.setGeometry(QtCore.QRect(1750, 35, 100, 30))
        self.finder_LineEdit.setObjectName('finder_LineEdit')
        # self.finder_LineEdit.setStyleSheet('background-color:#111111')

        #создаем второй виджет который отображает результаты после поиска из строки
        self.scripts_listWidget = QtWidgets.QListWidget(Dialog)
        self.scripts_listWidget.setObjectName("listwidget_scripts_list")
        self.scripts_listWidget.setGeometry(QtCore.QRect(1305, 69, 545, 780))
        self.scripts_listWidget.addItem('для поиска .py файлов введите в строку сверху путь')
        self.scripts_listWidget.addItem('нажмите Enter чтобы запустить файл с расширением .py')
        # self.scripts_listWidget.setStyleSheet('background-color:#333333')




        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "file dispatcher"))