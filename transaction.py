import sqlite3
import datetime
class Transaction:

    def __init__(self):
        self.connection = sqlite3.connect('accounts.db', check_same_thread=False)
        self.dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def add(self, customer_id, unit_price, cart, tax, misc,final_price):
        sql = "insert into trans (customer_id, unit_price, tax, misc, final_price,create_date) values (?,?,?,?,?,?)"
        tx_id = self.connection.cursor().execute(sql,(customer_id, unit_price, tax, misc,final_price,self.dt))
        for item in cart:
            sql = "insert into transaction_items (tx_id, item_id, qty, discount) values (?,?,?,?)"
            response = self.connection.cursor().execute(sql,(tx_id.lastrowid,item[0], item[1],item[2]))
            
            sql = "update item set stock=stock-? where id = ?"
            response = self.connection.cursor().execute(sql,(item[1],item[0],))

        self.connection.commit()
        return response.lastrowid
    def cancel(self, id):
        sql = "update trans set status=?, cancel_date=? where id =?"
        self.connection.cursor().execute(sql,[ id,self.dt,id])
        items = self.get_items_for_transaction(id)
        for item in items:
            print(item)
            sql = "update item set stock = stock + ? where id=?"
            self.connection.cursor().execute(sql,[item[3],item[0]])

        self.connection.commit()
        
    def update(self, id,bill_id, payment_method, amount, details):
        sql = "update payment set payment_type=?, amount=?, payment_details=?, payment_date=? where id =?"
        response = self.connection.cursor().execute(sql,[ payment_method,amount,details,self.dt,id])
        self.connection.commit()
        return response.lastrowid
    def get_transactions(self):
        sql = "select * from trans order by id desc"
        result = self.connection.cursor().execute(sql)
        rows = result.fetchall()
        return rows
    def get_customer_for_transaction(self,tx_id):
        sql = "select customer_id from trans where id = ? order by id desc"
        result = self.connection.cursor().execute(sql,[tx_id])
        rows = result.fetchall()[0][0]
        return rows
    def get_transactions_for_customer(self,id):
        sql = "select * from trans where customer_id = ? order by id desc"
        result = self.connection.cursor().execute(sql,[id])
        rows = result.fetchall()
        transactions=[]
        for row in rows:
            items=[]
            payments=[]
            y = self.payments(row[0])
            for i in y:
                payments += [{'id':i[0],'payment_method':i[1],'amount':i[2],
                    'payment_details':i[3],'payment_date':i[4]}]
            x = self.get_items_for_transaction(row[0])
            for i in x:
                items += [{'id':i[0],'tx_id':i[1],'item_id':i[2],'qty':i[3],
                    'discount':i[4],'item_name':i[6],'item_desc':i[7],'weight':i[8] }]
            transactions += [{'id':row[0],'customer_id':row[1],'unit_price':row[2],
                'tax':row[3],'misc':row[4],'created_date':row[5],'final_price':row[6],
                'status':row[7],'items':items,'payments':payments}]
            
        return {'transactions':transactions}

    def get_items_for_transaction(self,ids):
        sql = "select * from transaction_items a, item b where a.tx_id = ? \
             and a.item_id = b.id order by tx_id desc"
        result = self.connection.cursor().execute(sql,[ids])
        rows = result.fetchall()
        return rows
    def all_payments(self):
        sql = "select * from payment order by id desc" 
        result = self.connection.cursor().execute(sql)
        rows = result.fetchall()
        return rows
    def payments(self, bill_id):
        sql = "select id,payment_type,amount,payment_details,payment_date from payment where tx_id = ? order by id desc" 
        result = self.connection.cursor().execute(sql,(bill_id,))
        rows = result.fetchall()
        return rows
