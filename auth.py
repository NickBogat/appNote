from PyQt5.QtGui import QPixmap
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
import matplotlib.pyplot as plt
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

    def prepare_data(self, user_data, sign, period):
        today_date = datetime.now().date()
        visual_data = {}
        if user_data:
            for i in user_data:
                if self.__ch.check_valid_date_period(today_date, i[2], period):
                    visual_data.setdefault(i[1], 0)
                    visual_data[i[1]] += abs(i[0])
        sorted_tuple = sorted(visual_data.items(), key=lambda x: x[1], reverse=True)
        visual_data = dict(sorted_tuple)
        labels = list(visual_data.keys())
        amounts = list(visual_data.values())
        _sum = sum(amounts)
        _percent = 100
        if len(amounts) > 1:
            for i in range(len(amounts)):
                if _percent - (amounts[i] / _sum * 100) < 1:
                    amounts = amounts[:i] + [sum(amounts[i:])]
                    labels = labels[:i] + ["other"]
                    break
                _percent -= (amounts[i] / _sum * 100)
        fig, ax = plt.subplots()
        ax.pie(amounts, labels=labels, autopct='%1.1f%%', shadow=True,
               wedgeprops={'lw': 1, 'ls': '--', 'edgecolor': "k"}, rotatelabels=True)
        ax.axis("equal")
        name = sign + str(datetime.now()).replace(':', ' ')
        plt.savefig(f"img/{name}.png")
        return name, visual_data

    def select_data(self, login, period):
        user_expences = self.__db.show_all_user_expenses(login)
        user_revenue = self.__db.show_all_user_revenue(login)
        filename_expences, data_expences = self.prepare_data(user_expences, "-", period)
        filename_revenue, data_revenue = self.prepare_data(user_revenue, "+", period)
        if len(data_expences) == 0:
            self.expenceLabelPicture.setPixmap(QPixmap("img/nodata.png"))
            self.expenceLabelText.setText("Нет данных")
        else:
            self.expenceLabelPicture.setPixmap(QPixmap(f"img/{filename_expences}.png"))
            biggest_ex = (list(data_expences.keys())[0], sum(data_expences.values()))
            self.expenceLabelText.setText(
                f"Наиболее затратная категория - {biggest_ex[0]}. Всего потрачено: {biggest_ex[1]}")
        if len(data_revenue) == 0:
            self.revenueLabelPicture.setPixmap(QPixmap("img/nodata.png"))
            self.revenueLabelText.setText("Нет данных")
        else:

            self.revenueLabelPicture.setPixmap(QPixmap(f"img/{filename_revenue}.png"))
            biggest_rev = (list(data_revenue.keys())[0], sum(data_revenue.values()))
            self.revenueLabelText.setText(
                f"Наиболее доходная категория - {biggest_rev[0]}. Всего заработано: {biggest_rev[1]}")
