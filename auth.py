from PyQt5.QtSql import QSqlTableModel, QSqlDatabase
from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QTableView
from PyQt5 import QtSql
from styles.auth_design import Ui_Dialog_Auth
from styles.reg_design import Ui_Dialog_Reg
from styles.profile_design import Ui_Profile_Dialog
from styles.add_post_design import Ui_AddPost_Dialog
from dbManager import Database


class AuthDialog(QDialog, Ui_Dialog_Auth):
    def __init__(self):
        super(AuthDialog, self).__init__()
        self.setupUi(self)
        self.regButton.clicked.connect(self.run)

    def run(self):
        self.reject()

    def getResults(self):
        if self.exec_() == QDialog.Accepted:
            login = self.loginEdit.text()
            password = self.passEdit.text()
            return login, password
        elif self.exec_() == QDialog.rejected:
            return False

    def close_dialog(self):
        self.close()


class RegDialog(QDialog, Ui_Dialog_Reg):
    def __init__(self):
        super(RegDialog, self).__init__()
        self.setupUi(self)

    def getResults(self):
        if self.exec_() == QDialog.Accepted:
            login = self.loginEdit.text()
            password1 = self.pass1Edit.text()
            password2 = self.pass2Edit.text()
            return login, password1, password2
        else:
            return False

    def close_dialog(self):
        self.close()


class AddPostDialog(QDialog, Ui_AddPost_Dialog):
    def __init__(self):
        super(AddPostDialog, self).__init__()
        self.setupUi(self)

    def getResults(self):
        if self.exec_() == QDialog.Accepted:
            quantity = self.amountLine.text()
            category = self.categoryLine.text()
            comment = self.commentText.toPlainText()
            return quantity, category, comment
        else:
            return False

    def close_dialog(self):
        self.close()


class ProfileDialog(QDialog, Ui_Profile_Dialog):
    def __init__(self):
        super(ProfileDialog, self).__init__()
        self.setupUi(self)
        self.__db = Database()

    def select_data(self, login):
        db = QSqlDatabase.addDatabase('SQLITE')
        db.setDatabaseName('users.sqlite')
        db.open()
        print(213123)
        model = QSqlTableModel(self, db)
        model.setTable('posts')
        model.select()
        self.tableView.setModel(model)

    def close_dialog(self):
        self.close()
