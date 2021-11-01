import sqlite3
from extra.checkers import Checker
from extra.callbacks import *


class Database:
    def __init__(self):
        self.conn = sqlite3.connect("users.sqlite")
        self.cursor = self.conn.cursor()
        self.checker = Checker()

    def show_all_user_posts(self, login):
        if not (self.checker.check_login_exists(login)):
            raise BadArgument("Польователя не существует!")
        query = f"""SELECT amount, category, date, comment FROM Data WHERE login = ?"""
        result = self.cursor.execute(query, (login,)).fetchall()
        return result

    def add_post_to_db(self, login, argument, comment=""):
        result_date, result_number, result_category = self.checker.check_valid_post_argument(argument)
        query = f"""INSERT INTO Data(date, amount, category, comment, login) VALUES(?, ?, ?, ?, ?)"""
        self.cursor.execute(query, (result_date, result_number, result_category, comment, login,))
        self.conn.commit()
        return True

    def add_new_account_to_db(self, data):
        __login, __password_hash = self.checker.check_valid_reg_data(data)
        print(1, __login, __password_hash)
        query = f"""INSERT INTO accounts(login, password) VALUES(?, ?)"""
        self.cursor.execute(query, (__login, __password_hash,))
        self.conn.commit()
        return __login
