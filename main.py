import os
import sys

from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QErrorMessage

from design import Ui_MainWindow
from extra.checkers import Checker
from extra.callbacks import *
from dbManager import Database


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: white;")
        self.setupUi(self)
        self.plusButton.setIcon(QIcon("img/plus_post.png"))
        self.homeButton.setIcon(QIcon("img/home.png"))
        self.statButton.setIcon(QIcon("img/stat.png"))
        self.logoLabel.setPixmap(QPixmap("img/logo.png"))
        self.db = Database()
        self.Checker = Checker()
        self.plusButton.clicked.connect(self.add_post)

    def add_post(self):
        try:
            money_arg = self.amountLine.text()
            category_arg = self.categoryLine.text()
            comment_arg = self.commentText.toPlainText()
            argument = " ".join([money_arg, category_arg])
            self.db.add_post_to_db(argument, comment_arg)
        except (BadCategoryName, BadMoneyAmount, BadArgument) as er:
            print(er)
            error_dialog = QErrorMessage()
            error_dialog.showMessage(er)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
