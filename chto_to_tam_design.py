# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/sergey/design_saves/my_vk_design.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("not_Dialog")
        Dialog.title = "qwe"
        Dialog.resize(1920, 1080)

        self.LineEdit = QtWidgets.QLineEdit(Dialog)
        self.LineEdit.setObjectName("LineEdit")
        self.LineEdit.setGeometry(61, 1, 1000, 30)

        self.listWidget = QtWidgets.QListWidget(Dialog)
        self.listWidget.setGeometry(QtCore.QRect(0, 35, 1300, 1015))
        self.listWidget.setObjectName("listWidget")

        self.scripts_LineEdit = QtWidgets.QLineEdit(Dialog)
        self.scripts_LineEdit.setGeometry(QtCore.QRect(1305, 35, 545, 30))
        self.scripts_LineEdit.setObjectName("scripts_Lineedit")

        self.scripts_listWidget = QtWidgets.QListWidget(Dialog)
        self.scripts_listWidget.setObjectName("listwidget_scripts_list")
        self.scripts_listWidget.setGeometry(QtCore.QRect(1305, 69, 545, 980))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "file dispetcher"))
