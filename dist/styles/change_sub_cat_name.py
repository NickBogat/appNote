# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'change_sub_cat_name.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SubCat_Change_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(350, 247)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(100, 210, 151, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(10, 0, 331, 181))
        font = QtGui.QFont()
        font.setFamily("MS Serif")
        font.setPointSize(11)
        self.groupBox.setFont(font)
        self.groupBox.setStyleSheet("QGroupBox {\n"
                                    "margin-top: 2ex;\n"
                                    "}\n"
                                    "QGroupBox:enabled {\n"
                                    "border: 1px solid black;\n"
                                    "border-radius: 5px;\n"
                                    "}\n"
                                    "QGroupBox::title {\n"
                                    "subcontrol-origin: margin;\n"
                                    " left: 3ex;\n"
                                    "}")
        self.groupBox.setObjectName("groupBox")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.groupBox)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(100, 30, 211, 131))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(30)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.catBox = QtWidgets.QComboBox(self.verticalLayoutWidget_2)
        self.catBox.setObjectName("catBox")
        self.verticalLayout_2.addWidget(self.catBox)
        self.nameEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.nameEdit.setObjectName("nameEdit")
        self.verticalLayout_2.addWidget(self.nameEdit)
        self.verticalLayoutWidget = QtWidgets.QWidget(self.groupBox)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(14, 30, 81, 131))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.groupBox.setTitle(_translate("Dialog", "Редактор"))
        self.label.setText(_translate("Dialog", "Подкатегория:"))
        self.label_2.setText(_translate("Dialog", "Название:"))
