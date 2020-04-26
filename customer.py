import sqlite3
import datetime
class Customer:

    def __init__(self):
        self.connection = sqlite3.connect('accounts.db', check_same_thread=False)
        self.cur = self.connection.cursor()

    def add(self, name, mob1, mob2, address, city, aadhar_card, photo):
        sql = "insert into customer (name,mob1,mob2,address,city,aadhar_card, photo,created_date) \
                values (?,?,?,?,?,?,?,?)"
        response = self.cur.execute(sql,(name, mob1, mob2, address, city, aadhar_card, photo,datetime.datetime.now()))
        self.connection.commit()
        return response.lastrowid
        
    def get(self,id):
        sql = "select * from customer where id = ?"
        result = self.cur.execute(sql,(id,))
        rows = result.fetchall()
        return rows

    def update(self,id, name, mob1, mob2, address, city, aadhar_card, photo):
        sql = "update customer set name=?,mob1=?,mob2=?,address=?,city=?,aadhar_card=?,photo=? where id=?"
        try:
            result = self.cur.execute(sql,[name, mob1, mob2, address, city, aadhar_card, photo,id])
            self.connection.commit()
            return result
        except Exception as e:
            self.connection.rollback()
            print(e)

    def customers(self,k='id',v='desc'):
        sql = "select * from customer order by " + k + ' ' + v 
        result = self.cur.execute(sql)
        rows = result.fetchall()
        return rows

    def getBillsForCustomer(self,customer_id):
        sql = "select * from bill where customer_id=? order by id desc"
        result = self.cur.execute(sql ,(customer_id,))
        rows = result.fetchall()
        return rows
