import sqlite3
from extra.checkers import Checker


class Database:
    def __init__(self):
        self.conn = sqlite3.connect("users.sqlite")
        self.cursor = self.conn.cursor()
        self.checker = Checker()

    def add_post_to_db(self, argument, comment=""):
        result_date, result_number, result_category = self.checker.check_valid_post_argument(argument)
        temp_query = f"""INSERT INTO Data(date, amount, category, comment) VALUES(?, ?, ?, ?)"""
        self.cursor.execute(temp_query, (result_date, result_number, result_category, comment, ))
        self.conn.commit()
