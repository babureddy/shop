import sqlite3
import datetime
class Reports:

    def __init__(self):
        self.connection = sqlite3.connect('accounts.db', check_same_thread=False)
        self.dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def customersCount(self):
        sql = "select count(*) from customer"
        result = self.connection.cursor().execute(sql)
        rows = result.fetchall()
        return rows[0][0]
        
    def itemsCount(self):
        sql = "select count(*) from item"
        result = self.connection.cursor().execute(sql)
        rows = result.fetchall()
        return rows[0][0]

    def transactionsCount(self):
        sql = "select count(*) from trans"
        result = self.connection.cursor().execute(sql)
        rows = result.fetchall()
        return rows[0][0]

    def salesTotal(self):
        sql = "select sum(final_price) from trans"
        result = self.connection.cursor().execute(sql)
        rows = result.fetchall()
        return rows[0][0]
    def balanceTotal(self):
        sql = "select sum(balance) from trans"
        result = self.connection.cursor().execute(sql)
        rows = result.fetchall()
        return rows[0][0]

    def sales(self):
        sql = "select final_price, create_date from trans order by create_date desc"
        result = self.connection.cursor().execute(sql)
        rows = result.fetchall()
        return rows
