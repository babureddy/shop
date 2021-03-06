import sqlite3
import datetime
class Customer:

    def __init__(self):
        self.connection = sqlite3.connect('accounts.db', check_same_thread=False)
        self.dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def add(self, name, mob1, mob2, address, city, aadhar_card, photo, email):
        if photo is None:
            photo = '/uploads/no_photo.png'
        sql = "insert into customer (name,mob1,mob2,address,city,aadhar_card, photo,email,created_date) \
                values (?,?,?,?,?,?,?,?,?)"
        response = self.connection.cursor().execute(sql,(name, mob1, mob2, address, city, aadhar_card, photo,email,self.dt))
        self.connection.commit()
        return response.lastrowid
        
    def get(self,id):
        sql = "select * from customer where id = ?"
        result = self.connection.cursor().execute(sql,(id,))
        rows = result.fetchall()
        return rows

    def update(self,id, name, mob1, mob2, address, city, aadhar_card, photo,email):
        print(id, name, mob1, mob2, address, city, aadhar_card, photo,email)
        sql = "update customer set name=?,mob1=?,mob2=?,address=?,city=?,aadhar_card=?,photo=?,email=? where id=?"
        result = self.connection.cursor().execute(sql,[name, mob1, mob2, address, city, aadhar_card, photo,email,id])
        self.connection.commit()
        return result

    def customers(self,k='id',v='desc'):
        sql = "select * from customer order by " + k + ' ' + v 
        result = self.connection.cursor().execute(sql)
        rows = result.fetchall()
        return rows

    def getBillsForCustomer(self,customer_id):
        sql = "select * from trans where customer_id=? order by id desc"
        result = self.connection.cursor().execute(sql ,(customer_id,))
        rows = result.fetchall()
        return rows
