import sqlite3
from datetime import datetime, date, timedelta

from PyQt5.QtGui import QIcon
from matplotlib import pyplot as plt
import matplotlib as mpl
from extra.checkers import Checker
from extra.callbacks import *


class Database:
    def __init__(self):
        self.conn = sqlite3.connect("users.sqlite", timeout=10)
        self.cursor = self.conn.cursor()
        self.checker = Checker()
        self.help_dict_sub = {"expences": "subcategory_exp", "revenue": "subcategory_rev"}
        self.help_dict = {"expences": "category_exp", "revenue": "category_rev"}
        self.help_dict_general = {"Наличные": "hand_cash", "Кредитная карта": "card_cash", "Вклад в банке": "bank_cash"}
        self.help_dict_to_short = {"expences": "exp", "revenue": "rev"}
        self.help_dict_download = {"expences": "расходов", "revenue": "доходов",
                                   "expences/revenue": "доходов и расходов"}

    def show_login_info(self, login):
        if not (self.checker.check_login_exists(login)):
            raise BadArgument("Польователя не существует!")
        query = f"""SELECT debt_cash, hand_cash, card_cash, bank_cash FROM accounts WHERE login = ?"""
        result = self.cursor.execute(query, (login,)).fetchall()
        return result

    def show_all_user_posts(self, login, database_type):
        if not (self.checker.check_login_exists(login)):
            raise BadArgument("Польователя не существует!")
        query = f"""SELECT amount, date, category, subcategory, comment FROM {database_type} WHERE login = ?"""
        result = self.cursor.execute(query, (login,)).fetchall()
        return result

    def add_post_to_db(self, database_type, receiver, login, argument, comment=""):
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
            sign = -1 if database_type == "expences" else 1
            receiver_name = self.help_dict_general[receiver]
            previous_balance = \
                self.cursor.execute(f"""SELECT {receiver_name} FROM accounts WHERE login = ?""", (login,)).fetchall()[
                    0][0]
            new_balance = previous_balance + sign * result_number
            query_to_accounts = f"""UPDATE accounts SET {receiver_name} = ?"""
            self.cursor.execute(query_to_accounts, (new_balance,))
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
        query = f"""SELECT amount, category, subcategory, comment, date FROM expences WHERE (login = ?)"""
        result = self.cursor.execute(query, (login,)).fetchall()
        return result

    def show_all_user_revenue(self, login):
        if not (self.checker.check_login_exists(login)):
            raise BadArgument("Польователя не существует!")
        query = f"""SELECT amount, category, subcategory, comment, date FROM revenue WHERE (login = ?)"""
        result = self.cursor.execute(query, (login,)).fetchall()
        return result

    def show_user_post_during_period(self, login, sign, period):
        if sign == "+":
            user_data = self.show_all_user_revenue(login)
        elif sign == "-":
            user_data = self.show_all_user_expenses(login)
        today_date = datetime.now().date()
        visual_data = []
        for i in user_data:
            if self.checker.check_valid_date_period(today_date, i[4], period):
                temp = list(i)[:-1] + [i[-1].split()[0]]
                visual_data.append(temp)
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
            if category_subs != "None" and len(category_subs) != 0:
                category_subs = category_subs.split("_")
                if sub_number in category_subs:
                    raise BadArgument("Подкатегория уже существует!")
                category_subs.append(sub_number)
                new_subs = "_".join(category_subs)
            else:
                new_subs = str(sub_number)
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
            self.cursor.execute(query, (new_name, prev_id,))
            self.conn.commit()
        except sqlite3.Error as er:
            print(f"[SQLITE ERROR] {er}")

    def show_all_user_months_posts_during_year(self, login, database_type):
        current_year = str(datetime.now().date().year)
        query = f"""SELECT * FROM {database_type} WHERE login = ? AND date like'{current_year}%'"""
        result = self.cursor.execute(query, (login,)).fetchall()
        answer = {i: {} for i in range(1, 13)}
        if result:
            for i in result:
                temp_date = i[1].split()[0]
                temp_month_number = int(temp_date.split("-")[1])
                temp_amount = i[2]
                temp_category = i[3]
                temp_sub_category = i[4]
                answer[temp_month_number].setdefault(temp_category, {"Остальное": 0})
                if temp_sub_category != "":
                    answer[temp_month_number][temp_category].setdefault(temp_sub_category, 0)
                if temp_sub_category == "":
                    answer[temp_month_number][temp_category]["Остальное"] += temp_amount
                else:
                    answer[temp_month_number][temp_category][temp_sub_category] += temp_amount
        return answer

    def show_all_user_days_posts_during_year(self, login, database_type):
        current_date = datetime.now().date()
        query = f"""SELECT * FROM {database_type} WHERE login = ? AND date like'{current_date.year}%'"""
        result = self.cursor.execute(query, (login,)).fetchall()
        answer = {}
        main = {}
        current_date = datetime.now().date()
        first_year_day = date(current_date.year, 1, 1)
        temp_date = first_year_day
        while temp_date.year < int(current_date.year) + 1:
            answer[str(temp_date)] = {}
            temp_date = temp_date + timedelta(days=1)
        for i in result:
            temp_date = i[1].split()[0]
            temp_amount = i[2]
            temp_category = i[3]
            temp_sub_category = i[4]
            answer[temp_date].setdefault(temp_category, {"Остальное": 0})
            if temp_sub_category != "":
                answer[temp_date][temp_category].setdefault(temp_sub_category, 0)
            if temp_sub_category == "":
                answer[temp_date][temp_category]["Остальное"] += temp_amount
            else:
                answer[temp_date][temp_category][temp_sub_category] += temp_amount
        for ind, val in enumerate(answer):
            main[ind + 1] = answer[val]
        return main

    def show_all_user_weeks_posts_during_year(self, login, database_type):
        current_year = datetime.now().date().year
        first_current_year_date = date(current_year, 1, 1)
        query = f"""SELECT * FROM {database_type} WHERE login = ? AND date like'{current_year}%'"""
        result = self.cursor.execute(query, (login,)).fetchall()
        normal_date_year = first_current_year_date + timedelta(days=7 - first_current_year_date.isoweekday())
        answer = {(first_current_year_date, normal_date_year): {}}
        start_day = normal_date_year + timedelta(days=1)
        while start_day <= date(current_year, 12, 31):
            if start_day + timedelta(days=6) <= date(current_year, 12, 31):
                answer[(start_day, start_day + timedelta(days=6))] = {}
                start_day += timedelta(days=7)
            else:
                break
        if list(answer.keys())[-1][1] != date(current_year, 12, 31):
            answer[(start_day, start_day + timedelta(date(current_year, 12, 31).weekday()))] = {}
        for post in result:
            temp_date = post[1].split()[0]
            year, month, day = map(int, temp_date.split("-"))
            new_date = date(year, month, day)
            temp_amount = post[2]
            temp_category = post[3]
            temp_sub_category = post[4]
            for day in answer:
                if day[0] <= new_date <= day[1]:
                    answer[day].setdefault(temp_category, {"Остальное": 0})
                    if temp_sub_category != "":
                        answer[day][temp_category].setdefault(temp_sub_category, 0)
                    if temp_sub_category == "":
                        answer[day][temp_category]["Остальное"] += temp_amount
                    else:
                        answer[day][temp_category][temp_sub_category] += temp_amount
        main = {ind: answer[val] for ind, val in enumerate(answer)}
        return main

    def show_general_posts_data_during_period(self, login, database_type, period):
        current_date = datetime.now().date()
        query = f"""SELECT * FROM {database_type} WHERE login = ? AND date like'{current_date.year}%'"""
        result = list(self.cursor.execute(query, (login,)).fetchall())
        prepared_data = []
        if period == 'Месяц':
            prepared_data = [i for i in result if i[1].split()[0][5:7] == str(current_date.month)]
        elif period == 'Неделя':
            first_day_week = current_date - timedelta(days=current_date.isoweekday())
            last_day_week = first_day_week + timedelta(days=6)
            for ind, val in enumerate(result):
                year, month, day = map(int, val[1].split()[0].split("-"))
                new_date = date(year, month, day)
                if first_day_week <= new_date <= last_day_week:
                    prepared_data.append(val)
        elif period == "День":
            prepared_data = [i for i in result if i[1].split()[0] == str(current_date)]
        else:
            prepared_data = result
        return prepared_data

    def prepare_category_and_subcategory_data(self, data):
        periods = list(set([i[3] for i in data]))
        visualise_data = {i: {} for i in periods}
        for val in data:
            if val[4] == '':
                visualise_data[val[3]].setdefault("Без подкатегории", 0)
                visualise_data[val[3]]["Без подкатегории"] += val[2]
            else:
                visualise_data[val[3]].setdefault(val[4], 0)
                visualise_data[val[3]][val[4]] += val[2]
        return visualise_data

    def download_data(self, amounts, labels, file_name, figure_short_name):
        figure_name = self.help_dict_download[figure_short_name]
        px = 1 / plt.rcParams['figure.dpi']
        fig = plt.figure(figsize=(690 * px, 590 * px))
        mpl.rcParams.update({'font.size': 9})
        plt.title(f'Диаграмма {figure_name} в %')
        plt.pie(
            amounts, autopct='%.1f', radius=1.1,
            explode=[0.15] + [0 for _ in range(len(labels) - 1)])
        plt.legend(
            bbox_to_anchor=(-0.16, 0.45, 0.25, 0.25),
            loc='lower left', labels=labels)
        fig.savefig(file_name)
