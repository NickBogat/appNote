import sys
import traceback
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QInputDialog

from styles.design import Ui_MainWindow
from extra.checkers import Checker
from dialogManager import *


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
        self.setWindowTitle("Главное окно")
        self.setWindowIcon(QIcon("img/logo_window.png"))

    def show_error_box(self, er):
        print(f"[ERROR] {er} - {traceback.format_exc()}")
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(str(er))
        msg.setWindowTitle("Error")
        msg.exec_()

    def choose_post_type(self):
        post_type = ChooseTypeDialog()
        returnCode_post_type = post_type.exec_()
        returned_value_post_type = post_type.getValue()
        if returnCode_post_type:
            if returned_value_post_type[0]:
                database_name = "expences"
            elif returned_value_post_type[1]:
                database_name = "revenue"
            return database_name
        return None

    def add_post(self):
        try:
            if self.authorized:
                database_type = self.choose_post_type()
                if database_type:
                    dlg_post = AddPostDialog()
                    dlg_post.select_data(database_type)
                    returnCode_post = dlg_post.exec_()
                    returned_value = dlg_post.getValue()
                    if returnCode_post:
                        receiver, ok_pressed = QInputDialog.getItem(
                            self, "Выберите куда пойдут деньги", "Получатель",
                            ("Наличные", "Кредитная карта", "Вклад в банке"), 1, False)
                        if ok_pressed:
                            money_arg = returned_value[0]
                            category_arg = returned_value[1]
                            subcategory_arg = returned_value[2]
                            comment_arg = returned_value[3]
                            argument = "%".join([money_arg, category_arg, subcategory_arg])
                            self.db.add_post_to_db(database_type, receiver, self.login, argument, comment_arg)
                            QMessageBox.about(self, "Info", "Вы успешно добавли запись!")
                    elif dlg_post.want_to_create_category:
                        self.create_category(database_type)
                    elif dlg_post.want_to_create_subcategory:
                        self.create_sub_category(database_type)
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

    def create_category(self, database_type):
        try:
            dlg = CreateCategoryDialog()
            returnCode = dlg.exec_()
            returned_value = dlg.getValue()
            if returnCode:
                self.db.add_category(returned_value, database_type)
                QMessageBox.about(self, "Info", f"Вы успешно создали категорию {returned_value.lower()}!")
        except (BadArgument, Exception) as er:
            self.show_error_box(er)

    def create_sub_category(self, database_type):
        try:
            dlg = CreateSubCategoryDialog()
            dlg.select_data(database_type)
            returnCode = dlg.exec_()
            returned_value = dlg.getValue()
            if returnCode:
                category, name = returned_value
                self.db.add_sub_category(category, str(name), database_type)
                QMessageBox.about(self, "Info",
                                  f"Вы успешно создали подкатегорию {returned_value[1].lower()} в {returned_value[0].lower()}!")
        except (BadArgument, Exception) as er:
            self.show_error_box(er)

    def show_profile(self):
        try:
            dlg = ProfileDialog()
            dlg.select_data(self.login)
            returned_value = dlg.getValue()
            returnCode = dlg.exec_()
            if dlg.want_to_change_category or dlg.want_to_change_sub_category:
                database_name = self.choose_post_type()
                if database_name:
                    database_type = database_name[:3]
                    if dlg.want_to_change_category:
                        dlg_change = ChangeCategoryName()
                        dlg_change.select_data(database_name)
                        returnCode_change = dlg_change.exec_()
                        returned_value_changed = dlg_change.getValue()
                        if returnCode_change:
                            self.db.change_category_name("category_" + database_type, returned_value_changed[0],
                                                         returned_value_changed[1])
                            QMessageBox.about(self, "Info",
                                              f"Вы успешно редактировали категорию {returned_value_changed[0].lower()}!")
                    elif dlg.want_to_change_sub_category:
                        dlg_change = ChangeSubCategoryName()
                        dlg_change.select_data(database_name)
                        returnCode_change = dlg_change.exec_()
                        returned_value_changed = dlg_change.getValue()
                        if returnCode_change:
                            self.db.change_category_name("subcategory_" + database_type, returned_value_changed[0],
                                                         returned_value_changed[1])
                            QMessageBox.about(self, "Info",
                                              f"Вы успешно редактировали под категорию {returned_value_changed[0].lower()}!")
            elif dlg.wand_to_exit:
                self.login = None
                self.authorized = False
                QMessageBox.about(self, "Info", f"Вы успешно вышли из аккаунта!")

        except Exception as er:
            self.show_error_box(er)

    def show_statistic(self):
        try:
            if self.login is None:
                raise BadEnterData("Вы не авторизованы!")
            statistic_type = ChooseTypeStatisticDialog()
            returnCode_statistic_type = statistic_type.exec_()
            if returnCode_statistic_type:
                if statistic_type.want_graph:
                    database_name = self.choose_post_type()
                    if database_name:
                        dlg_main = GraphStatisticDialog()
                        dlg_main.select_data(self.login, database_name)
                        returnCode_main_dlg = dlg_main.exec_()
                else:
                    dlg_main = FigureStatisticDialog()
                    dlg_main.select_data(self.login)
                    returnCode_main_dlg = dlg_main.exec_()
                    if returnCode_main_dlg:
                        if dlg_main.want_description:
                            database_name = self.choose_post_type()
                            if database_name:
                                dlg_desc = DescriptionFigureDialog()
                                dlg_desc.select_data(self.login, database_name)
                                returnCode_desc_dlg = dlg_desc.exec_()
                                if returnCode_desc_dlg:
                                    if dlg_desc.want_all_posts:
                                        dlg_all_posts = AllPostsDialog()
                                        dlg_all_posts.select_data(self.login, database_name)
                                        returnCode_all_posts = dlg_all_posts.exec_()
        except Exception as er:
            self.show_error_box(er)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    print(app.exec_())
    sys.exit(app.exec_())
