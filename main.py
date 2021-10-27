import sys

from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QErrorMessage, QMessageBox

from styles.design import Ui_MainWindow
from extra.checkers import Checker
from extra.callbacks import *
from dbManager import Database
from auth import AuthDialog, RegDialog
import settings


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

    def add_post(self):
        try:
            money_arg = self.amountLine.text()
            category_arg = self.categoryLine.text()
            comment_arg = self.commentText.toPlainText()
            argument = " ".join([money_arg, category_arg])
            self.db.add_post_to_db(argument, comment_arg)
        except (BadCategoryName, BadMoneyAmount, BadArgument) as er:
            show_error_box(er)

    def open_account(self):
        dlg = AuthDialog()
        returned_value = dlg.getResults()
        if not returned_value:
            self.create_account()
            return
        QMessageBox.about(self, "Info", "Вы успешно вошли в аккаунт!")

    def create_account(self):
        try:
            dlg = RegDialog()
            returned_value = dlg.getResults()
            print(returned_value)
            if returned_value:
                self.db.add_new_account_to_db(returned_value)
        except (LoginAlreadyExists, BadEnterData) as er:
            show_error_box(er)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
