import sqlite3
import datetime
class Item:

    def __init__(self):
        self.connection = sqlite3.connect('accounts.db', check_same_thread=False)
        self.dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def add(self, name, description, weight,photo,stock=1):
        sql = "insert into item (name,desc,weight,photo,stock,created_date) \
                values (?,?,?,?,?,?)"
        print(sql,name, description,weight,photo,stock,self.dt)
        response = self.connection.cursor().execute(sql,[name, description,weight,photo,stock,self.dt])
        self.connection.commit()
        return response.lastrowid
        
    def get(self,id):
        sql = "select * from item where id = ?"
        result = self.connection.cursor().execute(sql,(id,))
        rows = result.fetchall()
        return rows

    def update(self,id, name, description, weight,photo,stock):
        sql = "update item set name=?,desc=?,weight=? ,photo=?,stock=? where id=?"
        try:
            result = self.connection.cursor().execute(sql,[name, description, weight,photo,stock,id])
            self.connection.commit()
            return result
        except Exception as e:
            self.connection.rollback()
            print(e)

    def all_items(self,k='id',v='desc'):
        sql = "select * from item order by " + k + ' ' + v 
        result = self.connection.cursor().execute(sql)
        rows = result.fetchall()
        return rows
    def items(self,k='name',v='asc'):
        sql = "select * from item where stock>0 order by " + k + ' ' + v 
        result = self.connection.cursor().execute(sql)
        rows = result.fetchall()
        return rows
