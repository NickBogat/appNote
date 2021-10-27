import sqlite3

from extra.callbacks import *
from datetime import datetime
import hashlib


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


class Checker:
    def __init__(self):
        self.__conn = sqlite3.connect("users.sqlite")
        self.__cursor = self.__conn.cursor()

    def check_valid_number(self, tender: str):
        if len(tender) < 2 or tender[0] not in ("+", "-"):
            raise BadMoneyAmount("Неверный формат суммы!")
        _available = "0123456789"
        sign = tender[0]
        tender = tender[1:]
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
        __argument = argument.split()
        if len(__argument) < 2:
            raise BadMoneyAmount("Неверное количество аргуметов!")
        __number = __argument[0]
        __category = " ".join(__argument[1:])
        __current_date = datetime.now()
        self.check_valid_number(__number)
        self.check_valid_category(__category)
        return str(__current_date), int(__number), __category

    def check_valid_enter_data(self, data):
        login = data[0]
        password = hash_password(data[1])
        print(f"Checking << {login} : {password}")
        query = f"""SELECT id FROM accounts WHERE login = ? AND password = ?"""
        result = list(self.__cursor.execute(query, (login, password,)))
        return len(result) == 1

    def check_valid_general_auth_data(self, returned_value):
        if returned_value is None:
            raise BadArgument("Ошибка авторизации!")
        if not returned_value:
            return False
        if not (self.check_valid_enter_data(returned_value)):
            raise BadEnterData("Неправильный логин/пароль!")
        return True

    def check_valid_reg_data(self, data):
        __login = data[0]
        __password1 = data[1]
        __password2 = data[2]
        if self.check_login_exists(__login):
            raise LoginAlreadyExists("Пользователь уже существует!")
        if __password1 != __password2:
            raise BadEnterData("Не совпадают пароли!")
        return __login, hash_password(__password1)
