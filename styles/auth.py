from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QTableView, QHeaderView
from PyQt5 import QtCore, Qt
from styles.auth_design import Ui_Dialog_Auth
from styles.reg_design import Ui_Dialog_Reg
from styles.profile_design import Ui_Profile_Dialog
from styles.add_post_design import Ui_AddPost_Dialog
from styles.statistic_design import Ui_Statistic_Dialog
from styles.create_category import Ui_Category_Dialog
from styles.create_subcategory import Ui_Subcategory_Dialog
from styles.choose_type_post import Ui_Type_Post_Dialog
from styles.change_cat_name import Ui_Cat_Change_Dialog
from styles.change_sub_cat_name import Ui_SubCat_Change_Dialog
from extra.checkers import Checker
from extra.callbacks import *
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
        self.__db = Database()
        self.setupUi(self)

    def select_data(self, database_type):
        self.data = self.__db.show_all_categories_and_subcategories(database_type)
        if self.data:
            self.categoryBox.addItems(list(self.data.keys()))
            self.subCategoryBox.addItems(list(self.data[list(self.data.keys())[0]]))
        self.categoryBox.currentTextChanged.connect(self.category_changed)
        self.want_to_create_category = False
        self.want_to_create_subcategory = False
        self.createCategoryButton.clicked.connect(self.run)
        self.createSubCategoryButton.clicked.connect(self.run)

    def run(self):
        button = self.sender()
        if button.text() == "Создать категорию":
            self.want_to_create_category = True
        elif button.text() == "Создать подкатегорию":
            self.want_to_create_subcategory = True
        self.reject()

    def category_changed(self, event):
        self.subCategoryBox.clear()
        self.subCategoryBox.addItems(self.data[self.categoryBox.currentText()])

    def getValue(self):
        amount = self.amountLine.text()
        category = self.categoryBox.currentText()
        subcategory = self.subCategoryBox.currentText()
        comment = self.commentText.toPlainText()
        return amount, category, subcategory, comment


class ProfileDialog(QDialog, Ui_Profile_Dialog):
    def __init__(self):
        super(ProfileDialog, self).__init__()
        self.setupUi(self)
        self.mainBalancePicture.setPixmap(QPixmap("img/main_balance.png"))
        self.debtPicture.setPixmap(QPixmap("img/debt_balance.png"))
        self.cashPicture.setPixmap(QPixmap("img/hand_cash.png"))
        self.cardPicture.setPixmap(QPixmap("img/cash_card.png"))
        self.bankPicture.setPixmap(QPixmap("img/cash_bank.png"))
        self.__db = Database()
        self.saveButton.clicked.connect(self.download_data)
        self.data = None
        self.login = None
        self.want_to_change_category = False
        self.want_to_change_sub_category = False
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.editCategory.clicked.connect(self.run_change_category)
        self.editSubCategory.clicked.connect(self.run_change_sub_category)

    def select_data(self, login):
        self.login = login
        result = self.__db.show_login_info(login)[0]
        debt_cash, hand_cash, card_cash, bank_cash = result[0], result[1], result[2], result[3]
        self.mainBalanceLabel.setText(str(debt_cash + hand_cash + card_cash + bank_cash) + "₽")
        self.debtLabel.setText(str(debt_cash) + "₽")
        self.cashhandLabel.setText(str(hand_cash) + "₽")
        self.cashcardLabel.setText(str(card_cash) + "₽")
        self.cashbankLabel.setText(str(bank_cash) + "₽")
        self.tableTypeBox.currentTextChanged.connect(self.text_changed)
        self.timePeriodBox.currentTextChanged.connect(self.text_changed)
        period, sign = self.spot_right_time_and_type(self.timePeriodBox.currentText(), self.tableTypeBox.currentText())
        print(period, sign)
        self.data = self.__db.show_user_post_during_period(self.login, sign, period)
        print(self.data)
        self.create_model()

    def text_changed(self, event):
        period, sign = self.spot_right_time_and_type(self.timePeriodBox.currentText(), self.tableTypeBox.currentText())
        self.data = self.__db.show_user_post_during_period(self.login, sign, period)
        self.create_model()

    def download_data(self):
        date = str(datetime.now()).replace(":", "-")
        self.data.to_csv(f"downloaded_files/{date}.csv", index=False, sep=";")

    def create_model(self):
        columns = ["Сумма", "Категория", "Время"]
        user_data = pd.DataFrame(self.data, columns=columns)
        print(user_data)
        model = PandasModel(user_data)
        self.tableView.setModel(model)

    def spot_right_time_and_type(self, time, table_type):
        if time == "Месяц":
            period = "m"
        elif time == "Неделя":
            period = "w"
        else:
            period = "d"
        if table_type == "Доходы":
            sign = "+"
        else:
            sign = "-"
        print(period, sign)
        return period, sign

    def run_change_category(self):
        self.want_to_change_category = True
        self.reject()

    def run_change_sub_category(self):
        self.want_to_change_sub_category = True
        self.reject()

    def getValue(self):
        return self.want_to_change_category, self.want_to_change_sub_category


class CreateCategoryDialog(QDialog, Ui_Category_Dialog):
    def __init__(self):
        super(CreateCategoryDialog, self).__init__()
        self.setupUi(self)

    def getValue(self):
        name = self.nameLine.text()
        return name


class CreateSubCategoryDialog(QDialog, Ui_Subcategory_Dialog):
    def __init__(self):
        super(CreateSubCategoryDialog, self).__init__()
        self.setupUi(self)
        self.__db = Database()

    def select_data(self, database_type):
        self.categories = list(self.__db.show_all_categories_and_subcategories(database_type).keys())
        self.categoryBox.addItems(self.categories)

    def getValue(self):
        category = self.categoryBox.currentText()
        name = self.nameLine.text()
        return category, name


class ChangeCategoryName(QDialog, Ui_Cat_Change_Dialog):
    def __init__(self):
        super(ChangeCategoryName, self).__init__()
        self.setupUi(self)
        self.__db = Database()
        self.catBox.currentTextChanged.connect(self.text_changed)

    def select_data(self, database_type):
        categories = []
        for i in self.__db.show_all_categories_and_subcategories(database_type).keys():
            categories.append(i)
        if len(categories) == 0:
            raise BadArgument("Нет данных о категориях!")
        print()
        self.catBox.addItems(categories)

    def text_changed(self, event):
        self.nameEdit.setText(self.catBox.currentText())

    def getValue(self):
        return self.catBox.currentText(), self.nameEdit.text()


class ChangeSubCategoryName(QDialog, Ui_SubCat_Change_Dialog):
    def __init__(self):
        super(ChangeSubCategoryName, self).__init__()
        self.setupUi(self)
        self.__db = Database()
        self.catBox.currentTextChanged.connect(self.text_changed)

    def select_data(self, database_type):
        sub_categories = []
        for i in self.__db.show_all_categories_and_subcategories(database_type).values():
            sub_categories += list(i)
        if len(sub_categories) == 0:
            raise BadArgument("Нет данных о подкатегориях!")
        self.catBox.addItems(sub_categories)

    def text_changed(self, event):
        self.nameEdit.setText(self.catBox.currentText())

    def getValue(self):
        return self.catBox.currentText(), self.nameEdit.text()


class ChooseTypeDialog(QDialog, Ui_Type_Post_Dialog):
    def __init__(self):
        super(ChooseTypeDialog, self).__init__()
        self.setupUi(self)
        self.expButton.clicked.connect(self.run)
        self.revButton.clicked.connect(self.run)
        self.want_to_exp = False
        self.want_to_rev = False

    def run(self):
        button = self.sender()
        if button.text() == "Расход":
            self.want_to_exp = True
        elif button.text() == "Доход":
            self.want_to_rev = True
        self.reject()

    def getValue(self):
        return self.want_to_exp, self.want_to_rev


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
            self.expenceLabelPicture.setPixmap(QPixmap("../img/nodata.png"))
            self.expenceLabelText.setText("Нет данных")
        else:
            self.expenceLabelPicture.setPixmap(QPixmap(f"img/{filename_expences}.png"))
            biggest_ex = (list(data_expences.keys())[0], sum(data_expences.values()))
            self.expenceLabelText.setText(
                f"Наиболее затратная категория - {biggest_ex[0]}. Всего потрачено: {biggest_ex[1]}")
        if len(data_revenue) == 0:
            self.revenueLabelPicture.setPixmap(QPixmap("../img/nodata.png"))
            self.revenueLabelText.setText("Нет данных")
        else:

            self.revenueLabelPicture.setPixmap(QPixmap(f"img/{filename_revenue}.png"))
            biggest_rev = (list(data_revenue.keys())[0], sum(data_revenue.values()))
            self.revenueLabelText.setText(
                f"Наиболее доходная категория - {biggest_rev[0]}. Всего заработано: {biggest_rev[1]}")
