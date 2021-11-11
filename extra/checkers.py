import sqlite3

from extra.callbacks import *
from datetime import datetime, timedelta
import hashlib


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


class Checker:
    def __init__(self):
        self.__conn = sqlite3.connect("users.sqlite")
        self.__cursor = self.__conn.cursor()

    def check_valid_number(self, tender: str):
        if len(tender) < 1:
            raise BadMoneyAmount("Неверный формат суммы!")
        _available = "0123456789"
        if tender == "0":
            raise BadMoneyAmount("Неверный формат суммы!")
        for i in range(len(tender)):
            if tender[i] not in _available:
                raise BadMoneyAmount("Неверный формат суммы!")
        return True

    def check_valid_category(self, tender: str):
        if len(tender) < 3:
            raise BadCategoryName("Невеный формат категории!")
        if tender.isdigit():
            raise BadCategoryName("Невеный формат категории!")
        return True

    def check_login_exists(self, login):
        query = f"""SELECT id FROM accounts WHERE login = ?"""
        result = list(self.__cursor.execute(query, (login,)))
        return len(result) != 0

    def check_valid_post_argument(self, argument: str):
        __argument = argument.split("%")
        if len(__argument) < 2:
            raise BadMoneyAmount("Неверное количество аргуметов!")
        __number = __argument[0]
        __category = __argument[1]
        __subcategory = __argument[2]
        __current_date = datetime.now()
        self.check_valid_number(__number)
        self.check_valid_category(__category)
        self.check_valid_category(__subcategory)
        return str(__current_date), int(__number), __category, __subcategory

    def check_valid_enter_data(self, data):
        login = data[0]
        password = hash_password(data[1])
        print(f"Checking << {login} : {password}")
        query = f"""SELECT id FROM accounts WHERE login = ? AND password = ?"""
        result = list(self.__cursor.execute(query, (login, password,)))
        print(result)
        return len(result) == 1

    def check_valid_general_auth_data(self, returned_value):
        if returned_value is None:
            raise BadArgument("Ошибка авторизации!")
        if not returned_value:
            raise BadArgument("Ошибка авторизации!")
        if not (self.check_valid_enter_data(returned_value)):
            raise BadEnterData("Неправильный логин/пароль!")
        return returned_value[0]

    def check_valid_reg_data(self, data):
        __login = data[0]
        __password1 = data[1]
        __password2 = data[2]
        if len(__login) < 5:
            raise BadEnterData("Неверный формат логина!")
        if len(__password1) < 5:
            raise BadEnterData("Неверный формат пароля!")
        if self.check_login_exists(__login):
            raise LoginAlreadyExists("Пользователь уже существует!")
        if __password1 != __password2:
            raise BadEnterData("Не совпадают пароли!")
        return __login, hash_password(__password1)

    def check_valid_date_period(self, current_date, example, period):
        example = example.split()[0]
        if period == "d":
            return example == str(current_date)
        elif period == "w":
            dist = current_date.weekday()
            first_day_of_week = current_date - timedelta(days=dist)
            new_date = example.split("-")
            new_date = datetime(int(new_date[0]), int(new_date[1]), int(new_date[2])).date()
            return first_day_of_week <= new_date
        elif period == "m":
            return example[:-3] == str(current_date)[:-3]
        elif period == "y":
            return example[:4] == str(current_date)[:4]
        else:
            raise BadArgument("Неверный период вермени")

    def check_valid_category_name(self, name):
        if len(name) < 5:
            raise BadCategoryName("Недопустимое название категории!")
        if name.isdigit():
            raise BadCategoryName("Недопустимое название категории!")

    def check_category_exists(self, database_type, name):
        query = f"""SELECT id FROM {database_type} WHERE name = ?"""
        result = self.__cursor.execute(query, (name, )).fetchall()
        if result:
            return True
        return False
