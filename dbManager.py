import sqlite3
from datetime import datetime

from extra.checkers import Checker
from extra.callbacks import *


class Database:
    def __init__(self):
        self.conn = sqlite3.connect("users.sqlite", timeout=10)
        self.cursor = self.conn.cursor()
        self.checker = Checker()
        self.help_dict_sub = {"expences": "subcategory_exp", "revenue": "subcategory_rev"}
        self.help_dict = {"expences": "category_exp", "revenue": "category_rev"}
        self.help_dict_general = {}
        self.help_dict_to_short = {"expences": "exp", "revenue": "rev"}

    def show_login_info(self, login):
        if not (self.checker.check_login_exists(login)):
            raise BadArgument("Польователя не существует!")
        query = f"""SELECT debt_cash, hand_cash, card_cash, bank_cash FROM accounts WHERE login = ?"""
        result = self.cursor.execute(query, (login,)).fetchall()
        return result

    def show_all_user_posts(self, login, database_type):
        if not (self.checker.check_login_exists(login)):
            raise BadArgument("Польователя не существует!")
        query = f"""SELECT amount, category, date, comment FROM ? WHERE login = ?"""
        result = self.cursor.execute(query, (database_type, login,)).fetchall()
        return result

    def add_post_to_db(self, database_type, login, argument, comment=""):
        try:
            if not (self.checker.check_login_exists(login)):
                raise BadArgument("Польователя не существует!")
            result_date, result_number, result_category, result_subcategory = self.checker.check_valid_post_argument(
                argument)
            query = f"""
            INSERT INTO {database_type}(date, amount, category, subcategory, comment, login) VALUES(?, ?, ?, ?, ?, ?)"""
            self.cursor.execute(query,
                                (result_date, result_number, result_category, result_subcategory, comment, login,))
            self.conn.commit()
            return True
        except sqlite3.Error as er:
            print(f"[SQLITE ERROR] {er}")

    def add_new_account_to_db(self, data):
        try:
            __login, __password_hash = self.checker.check_valid_reg_data(data)
            query = f"""
            INSERT INTO accounts(login, password, debt_cash, hand_cash, card_cash, bank_cash) VALUES(?, ?, ?, ?, ?, ?)
            """
            self.cursor.execute(query, (__login, __password_hash, 0, 0, 0, 0))
            self.conn.commit()
            return __login
        except sqlite3.Error as er:
            print(f"[SQLITE ERROR] {er}")

    def show_all_user_expenses(self, login):
        if not (self.checker.check_login_exists(login)):
            raise BadArgument("Польователя не существует!")
        query = f"""SELECT amount, category, date FROM expences WHERE (login = ?) AND (amount < 0)"""
        result = self.cursor.execute(query, (login,)).fetchall()
        return result

    def show_all_user_revenue(self, login):
        if not (self.checker.check_login_exists(login)):
            raise BadArgument("Польователя не существует!")
        query = f"""SELECT amount, category, date FROM revenue WHERE (login = ?) AND (amount > 0)"""
        result = self.cursor.execute(query, (login,)).fetchall()
        return result

    def show_user_post_during_period(self, login, sign, period):
        if sign == "+":
            user_data = self.show_all_user_revenue(login)
        elif sign == "-":
            user_data = self.show_all_user_expenses(login)
        today_date = datetime.now().date()
        visual_data = []
        if user_data:
            for i in user_data:
                if self.checker.check_valid_date_period(today_date, i[2], period):
                    visual_data.append(list(i))
        return visual_data

    def show_all_categories_and_subcategories(self, database_type):
        try:
            if database_type == "expences":
                query_cat = f"""SELECT name, subs FROM category_exp"""
                query_sub = f"""SELECT * FROM subcategory_exp"""
            else:
                query_cat = f"""SELECT name, subs FROM category_rev"""
                query_sub = f"""SELECT * FROM subcategory_rev"""
            result_cat = self.cursor.execute(query_cat).fetchall()
            result_sub = self.cursor.execute(query_sub).fetchall()
            result_sub = {i[0]: i[1] for i in result_sub}
            result_cat = [(i[0], str(i[1])) for i in result_cat]
            print(result_cat)
            print(result_sub)
            answer = {}
            for i in result_cat:
                temp = []
                if i[1] != "None" and len(i[1]) != 0:
                    if "_" in i[1]:
                        temp_sub = i[1].split("_")
                        for j in temp_sub:
                            temp.append(result_sub[int(j)])
                    else:
                        temp = [result_sub[int(i[1])]]
                answer[i[0]] = temp
            return answer
        except sqlite3.Error as er:
            print(f"[SQLITE ERROR] {er}")

    def add_category(self, name, database_type):
        try:
            self.checker.check_valid_category_name(name)
            database_name = self.help_dict[database_type]
            query = f"""INSERT INTO {database_name}(name) VALUES(?)"""
            self.cursor.execute(query, (name,))
            self.conn.commit()
        except sqlite3.Error as er:
            print(f"[SQLITE ERROR] {er}")

    def add_sub_category(self, category, name, database_type):
        try:
            print(database_type)
            self.checker.check_valid_category_name(name)
            database_name = self.help_dict_sub[database_type]
            database_name_short = self.help_dict_to_short[database_type]
            query_first = f"""INSERT INTO subcategory_{database_name_short}(name) VALUES(?)"""
            query_second = f"""SELECT id from subcategory_{database_name_short} WHERE name = ?"""
            query_third = f"""SELECT subs FROM category_{database_name_short} WHERE name = ?"""
            query_fourth = f"""UPDATE category_{database_name_short} SET subs = ? WHERE name = ?"""
            if len(list(self.cursor.execute(query_second, (name,)))) == 0:
                self.cursor.execute(query_first, (name,))
                self.conn.commit()
            sub_number = str(self.cursor.execute(query_second, (name,)).fetchall()[0][0])
            category_subs = str(self.cursor.execute(query_third, (category,)).fetchall()[0][0])
            print(type(category_subs), len(category_subs))
            if category_subs != "None" and len(category_subs) != 0:
                category_subs = category_subs.split("_")
                if sub_number in category_subs:
                    raise BadArgument("Подкатегория уже существует!")
                category_subs.append(sub_number)
                print(category_subs)
                new_subs = "_".join(category_subs)
            else:
                new_subs = str(sub_number)
            print(new_subs, type(new_subs))
            self.cursor.execute(query_fourth, (new_subs, category,))
            self.conn.commit()
        except sqlite3.Error as er:
            print(f"[SQLITE ERROR] {er}")

    def change_category_name(self, database_type, prev_name, new_name):
        try:
            print(database_type, prev_name, new_name)
            if not (self.checker.check_category_exists(database_type, prev_name)):
                raise BadArgument("Данной категории не существует!")

            prev_id = self.cursor.execute(f"""SELECT id FROM {database_type} WHERE name = ?""",
                                          (prev_name,)).fetchall()[0][0]
            query = f"""UPDATE {database_type} SET name = ? WHERE id = ?"""
            print(query)
            self.cursor.execute(query, (new_name, prev_id,))
            self.conn.commit()
        except sqlite3.Error as er:
            print(f"[SQLITE ERROR] {er}")

    def show_all_user_year_expences(self, login):
        current_year = str(datetime.now().date().year)
        query = f"""SELECT * FROM expences WHERE login = ? AND date like='{current_year}%'"""
        result = self.cursor.execute(query, (login, )).fetchall()
        print(result)
