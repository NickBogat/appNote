# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'create_category.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Category_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(382, 193)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(110, 160, 161, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(20, 20, 341, 111))
        font = QtGui.QFont()
        font.setFamily("MS Serif")
        font.setPointSize(11)
        self.groupBox.setFont(font)
        self.groupBox.setStyleSheet("QGroupBox {\n"
                                    "margin-top: 2ex;\n"
                                    "}\n"
                                    "QGroupBox:enabled {\n"
                                    "border: 2px solid black;\n"
                                    "border-radius: 5px;\n"
                                    "}\n"
                                    "QGroupBox::title {\n"
                                    "subcontrol-origin: margin;\n"
                                    " left: 3ex;\n"
                                    " }")
        self.groupBox.setObjectName("groupBox")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(10, 40, 81, 31))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.nameLine = QtWidgets.QLineEdit(self.groupBox)
        self.nameLine.setGeometry(QtCore.QRect(100, 45, 201, 20))
        self.nameLine.setObjectName("nameLine")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.groupBox.setTitle(_translate("Dialog", "Создание категории"))
        self.label_2.setText(_translate("Dialog", "Введите имя:"))