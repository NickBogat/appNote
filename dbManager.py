import sqlite3


class Database:
    def __init__(self):
        self.conn = sqlite3.connect("users.sqlite")
        self.cursor = self.conn.cursor()

    def add_post_to_db(self, date, amount, category, comment=""):
        temp_query = f"""INSERT INTO Data(date, amount, category, comment) VALUES(?, ?, ?, ?)"""
        self.cursor.execute(temp_query, (date, amount, category, comment, ))
        self.conn.commit()
