# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'choose_type_post.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Type_Post_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(302, 132)
        self.expButton = QtWidgets.QPushButton(Dialog)
        self.expButton.setGeometry(QtCore.QRect(40, 50, 101, 41))
        self.expButton.setObjectName("expButton")
        self.revButton = QtWidgets.QPushButton(Dialog)
        self.revButton.setGeometry(QtCore.QRect(160, 50, 101, 41))
        self.revButton.setObjectName("revButton")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.expButton.setText(_translate("Dialog", "Расход"))
        self.revButton.setText(_translate("Dialog", "Доход"))