from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QTableView, QHeaderView
from PyQt5 import QtCore, Qt
from styles.auth_design import Ui_Dialog_Auth
from styles.reg_design import Ui_Dialog_Reg
from styles.profile_design import Ui_Profile_Dialog
from styles.add_post_design import Ui_AddPost_Dialog
from styles.statistic_design import Ui_Statistic_Dialog
from extra.checkers import Checker
from dbManager import Database
import pandas as pd
import matplotlib as plt
from datetime import datetime


class PandasModel(QtCore.QAbstractTableModel):
    def __init__(self, data, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self._data = data

    def rowCount(self, parent=None):
        return len(self._data.values)

    def columnCount(self, parent=None):
        return self._data.columns.size

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if index.isValid():
            if role == QtCore.Qt.DisplayRole:
                return QtCore.QVariant(str(
                    self._data.values[index.row()][index.column()]))
        return QtCore.QVariant()


class AuthDialog(QDialog, Ui_Dialog_Auth):
    def __init__(self):
        super(AuthDialog, self).__init__()
        self.setupUi(self)
        self.want_to_reg = False
        self.regButton.clicked.connect(self.run)

    def getValue(self):
        login = self.loginEdit.text()
        password = self.passEdit.text()
        return login, password

    def run(self):
        self.want_to_reg = True
        self.reject()


class RegDialog(QDialog, Ui_Dialog_Reg):
    def __init__(self):
        super(RegDialog, self).__init__()
        self.setupUi(self)

    def getValue(self):
        login = self.loginEdit.text()
        password1 = self.pass1Edit.text()
        password2 = self.pass2Edit.text()
        return login, password1, password2


class AddPostDialog(QDialog, Ui_AddPost_Dialog):
    def __init__(self):
        super(AddPostDialog, self).__init__()
        self.setupUi(self)

    def getValue(self):
        quantity = self.amountLine.text()
        category = self.categoryLine.text()
        comment = self.commentText.toPlainText()
        return quantity, category, comment


class ProfileDialog(QDialog, Ui_Profile_Dialog):
    def __init__(self):
        super(ProfileDialog, self).__init__()
        self.setupUi(self)
        self.__db = Database()
        self.pushButton.clicked.connect(self.download_data)
        self.data = None
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def select_data(self, login):
        user_data = self.__db.show_all_user_posts(login)
        columns = ["Сумма", "Категория", "Время", "Комментарий"]
        self.data = pd.DataFrame(user_data)
        model = PandasModel(self.data)
        for i in range(len(columns)):
            model.setHeaderData(i, QtCore.Qt.Horizontal, columns[i])
        self.tableView.setModel(model)

    def download_data(self):
        date = str(datetime.now()).replace(":", "-")
        self.data.to_csv(f"downloaded_files/{date}.csv", index=False, sep=";")


class StatisticDialog(QDialog, Ui_Statistic_Dialog):
    def __init__(self):
        super(StatisticDialog, self).__init__()
        self.setupUi(self)
        self.__db = Database()
        self.__ch = Checker()

    def select_data(self, login, period):
        user_data = self.__db.show_all_user_expenses(login)
        today_date = datetime.now().date()
        visual_data = {}
        if user_data:
            for i in user_data:
                if self.__ch.check_valid_date_period(today_date, i[2], period):
                    visual_data.setdefault(i[1], 0)
                    visual_data[i[1]] += abs(i[0])
        print(visual_data)




        # fig, ax = plt.subplots()
        # ax.pie(values, labels=labels, autopct='%1.1f%%', shadow=True,
        #        wedgeprops={'lw': 1, 'ls': '--', 'edgecolor': "k"}, rotatelabels=True)
        # ax.axis("equal")