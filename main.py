import sys

from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QErrorMessage, QMessageBox, QDialog, QInputDialog

from styles.design import Ui_MainWindow
from extra.checkers import Checker
from extra.callbacks import *
from dbManager import Database
from auth import AuthDialog, RegDialog, AddPostDialog, ProfileDialog, StatisticDialog


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setStyleSheet("background-color: white;")
        self.plusButton.setIcon(QIcon("img/plus_post.png"))
        self.homeButton.setIcon(QIcon("img/home.png"))
        self.statButton.setIcon(QIcon("img/stat.png"))
        self.logoLabel.setPixmap(QPixmap("img/logo.png"))
        self.db = Database()
        self.Checker = Checker()
        self.authorized = False
        self.login = None
        self.plusButton.clicked.connect(self.add_post)
        self.homeButton.clicked.connect(self.open_account)
        self.statButton.clicked.connect(self.show_statistic)

    def show_error_box(self, er):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(str(er))
        msg.setWindowTitle("Error")
        msg.exec_()

    def add_post(self):
        try:
            if self.authorized:
                dlg = AddPostDialog()
                returnCode = dlg.exec_()
                returned_value = dlg.getValue()
                print(f"Returned from adding post - {returned_value}")
                if returnCode:
                    money_arg = returned_value[0]
                    category_arg = returned_value[1]
                    comment_arg = returned_value[2]
                    argument = " ".join([money_arg, category_arg])
                    self.db.add_post_to_db(self.login, argument, comment_arg)
                    QMessageBox.about(self, "Info", "Вы успешно добавли запись!")
            else:
                print("Ошибка добавления записи")
                self.show_error_box("Вы не авторизваны!")
        except (BadCategoryName, BadMoneyAmount, BadArgument, Exception) as er:
            self.show_error_box(er)

    def open_account(self):
        try:
            if self.authorized:
                self.show_profile()
                return
            dlg = AuthDialog()
            returnCode = dlg.exec_()
            returned_value = dlg.getValue()
            print(f"Returned from entering account {returned_value}")
            if returnCode:
                result = self.Checker.check_valid_general_auth_data(returned_value)
                self.authorized = True
                self.login = result
                QMessageBox.about(self, "Info", "Вы успешно вошли в аккаунт!")
                print(self.login, self.authorized)
            elif dlg.want_to_reg:
                print("reff")
                self.create_account()
        except (BadArgument, BadEnterData, Exception) as er:
            self.show_error_box(er)

    def create_account(self):
        try:
            dlg = RegDialog()
            returnCode = dlg.exec_()
            returned_value = dlg.getValue()
            print(f"Returned from creating account {returned_value}")
            if returnCode:
                result = self.db.add_new_account_to_db(returned_value)
                self.authorized = True
                self.login = result
                QMessageBox.about(self, "Info", "Вы успешно вошли в аккаунт!")
        except (LoginAlreadyExists, BadEnterData, Exception) as er:
            self.show_error_box(er)

    def show_profile(self):
        try:
            dlg = ProfileDialog()
            dlg.select_data(self.login)
            returnCode = dlg.exec_()
        except Exception as er:
            self.show_error_box(er)

    def show_statistic(self):
        try:
            dlg = StatisticDialog()
            answer, ok_pressed = QInputDialog.getItem(
                self, "Выберите промежуток времени", "Какой период времени?",
                ("День", "Неделя", "Месяц"), 1, False)
            if ok_pressed:
                av = {
                    "День": "d",
                    "Неделя": "w",
                    "Месяц": "m",
                }
                answer_period = av[answer]
                dlg.select_data(self.login, answer_period)
        except Exception as er:
            self.show_error_box(er)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
