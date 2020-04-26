import sqlite3
import datetime
class Item:

    def __init__(self):
        self.connection = sqlite3.connect('accounts.db', check_same_thread=False)
        self.cur = self.connection.cursor()

    def add(self, name, description, weight,photo):
        sql = "insert into item (name,desc,weight,photo,created_date) \
                values (?,?,?,?,?)"
        response = self.cur.execute(sql,(name, description,weight,photo,datetime.datetime.now()))
        self.connection.commit()
        return response.lastrowid
        
    def get(self,id):
        sql = "select * from item where id = ?"
        result = self.cur.execute(sql,(id,))
        rows = result.fetchall()
        return rows

    def update(self,id, name, description, weight,photo):
        sql = "update item set name=?,desc=?,weight=? ,photo=? where id=?"
        try:
            result = self.cur.execute(sql,[name, description, weight,photo,id])
            self.connection.commit()
            return result
        except Exception as e:
            self.connection.rollback()
            print(e)

    def all_items(self,k='id',v='desc'):
        sql = "select * from item order by " + k + ' ' + v 
        result = self.cur.execute(sql)
        rows = result.fetchall()
        return rows
    def items(self,k='name',v='asc'):
        sql = "select * from item where stock>0 order by " + k + ' ' + v 
        result = self.cur.execute(sql)
        rows = result.fetchall()
        return rows
