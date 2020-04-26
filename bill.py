import sqlite3
import datetime
class Bill:

    def __init__(self):
        self.connection = sqlite3.connect('accounts.db', check_same_thread=False)
        self.cur = self.connection.cursor()

    def add(self, customer_id,item_id, qty, unit_price,discount,total_price):
        sql = "insert into bill (customer_id,item_id, qty, unit_price, discount,total_price,created_date) \
                values (?,?,?,?,?,?,?)"
        response = self.cur.execute(sql,[customer_id,item_id, qty, unit_price, discount,total_price,datetime.datetime.now()])
        self.connection.commit()
        return response.lastrowid
        
    def get(self,id):
        sql = "select * from bill where id = ?"
        result = self.cur.execute(sql,(id,))
        rows = result.fetchall()
        return rows

    def update(self,id, customer_id,item_id, weight, unit_price,discount,total_price):
        sql = "update bill set customer_id=?, item_id=?, qty=?, unit_price=?, discount=?,total_price=? where id=?"
        try:
            result = self.cur.execute(sql,[customer_id,item_id, weight, unit_price, discount,total_price,id])
            self.connection.commit()
            return result
        except Exception as e:
            print(e)

    def bills(self,k='id',v='desc'):
        sql = "select * from bill order by " + k + ' ' + v 
        result = self.cur.execute(sql)
        rows = result.fetchall()
        return rows

    def get_bills_for_customer(self,customer_id):
        sql = "select * from bill where customer_id = ? order by id desc" 
        result = self.cur.execute(sql,(customer_id,))
        rows = result.fetchall()
        return rows
