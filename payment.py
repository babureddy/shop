import sqlite3
import datetime
class Payment:

    def __init__(self):
        self.connection = sqlite3.connect('accounts.db', check_same_thread=False)
        self.cur = self.connection.cursor()
        self.dt = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")

    def add(self, bill_id, amount, payment_type,payment_details):
        sql = "insert into payment (tx_id, amount, payment_type, payment_details, payment_date) \
                values (?,?,?,?,?)"
        response = self.cur.execute(sql,[bill_id, amount, payment_type,payment_details,self.dt])
        self.connection.commit()
        return response.lastrowid
        
    def update(self, id,bill_id, payment_method, amount, details):
        sql = "update payment set payment_type=?, amount=?, payment_details=?, payment_date=? where id =?"
        response = self.cur.execute(sql,[ payment_method,amount,details,self.dt,id])
        self.connection.commit()
        return response.lastrowid

    def get(self,id):
        sql = "select * from payment where id = ?"
        result = self.cur.execute(sql,[','.join([str(i) for i in id])])
        rows = result.fetchall()
        return rows

    def all_payments(self):
        sql = "select * from payment order by id desc" 
        result = self.cur.execute(sql)
        rows = result.fetchall()
        return rows
    def payments(self, bill_id):
        sql = "select * from payment where bill_id = ? order by id desc" 
        result = self.cur.execute(sql,(bill_id,))
        rows = result.fetchall()
        return rows
Payment().get([1,2,3])