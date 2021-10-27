import sqlite3
from extra.checkers import Checker


class Database:
    def __init__(self):
        self.conn = sqlite3.connect("users.sqlite")
        self.cursor = self.conn.cursor()
        self.checker = Checker()

    def add_post_to_db(self, argument, comment=""):
        result_date, result_number, result_category = self.checker.check_valid_post_argument(argument)
        query = f"""INSERT INTO Data(date, amount, category, comment) VALUES(?, ?, ?, ?)"""
        self.cursor.execute(query, (result_date, result_number, result_category, comment,))
        self.conn.commit()

    def add_new_account_to_db(self, data):
        __login, __password_hash = self.checker.check_valid_reg_data(data)
        print(1)
        query = f"""INSERT INTO accounts VALUES(?, ?)"""
        self.cursor.execute(query, (__login, __password_hash, ))
        self.conn.commit()