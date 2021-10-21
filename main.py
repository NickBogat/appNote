import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from design import Ui_MainWindow
from extra.checkers import Checker
from extra.callbacks import *
from dbManager import Database


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        self.Checker = Checker()
        super().__init__()
        self.setupUi(self)
        #self.add_post_button.clicked.connect(self.add_post)
        self.db = Database()

    def add_post(self):
        argument = self.post_field.toPlainText()
        result_date, result_number, result_category = self.Checker.check_valid_post_argument(argument)
        self.db.add_post_to_db(result_date, result_number, result_category)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
