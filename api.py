from flask import request, redirect, Flask, flash, render_template, send_from_directory, url_for, jsonify #pip install flask
from werkzeug.utils import secure_filename
import os,datetime,math
from customer import Customer 
from item import Item 
from payment import Payment
from transaction import Transaction
from goldprice import getTodaysGoldPrice
from reports import Reports

# from util import encrypt
reports = Reports()
trans = Transaction()
payment = Payment()
item = Item()
app = Flask(__name__)
users = {'babureddy1969@gmail.com': {'password': 'secret'}}
app.secret_key = 'super secret string'
customer = Customer()
UPLOAD_FOLDER = os.curdir+'\\uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

@app.route('/')
def home():
    return render_template("home.html",reports=get_reports())

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
@app.route('/customer/', methods=['POST'])
def add_customer():
    name = request.form.get('customer_name')
    mob1 = request.form.get('customer_mob1')
    mob2 = request.form.get('customer_mob2')
    address = request.form.get('customer_address')
    city = request.form.get('customer_city')
    aadhar_card = request.form.get('customer_aadhar')
    email = request.form.get('customer_email')
    photo = request.form.get('customer_photo')
    file = request.files['file']
    if file:
        filename = datetime.datetime.now().strftime('%Y%m%d%H%M%S')+file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        photo = '/uploads/'+filename

    customer.add(name.title(), mob1, mob2, address, city, aadhar_card, photo,email)
    return redirect('/customers/')

@app.route('/customer/<id>/', methods=['POST'])
def update_customer(id):
    name = request.form.get('customer_name')
    id = request.form.get('customer_id')
    mob1 = request.form.get('customer_mob1')
    mob2 = request.form.get('customer_mob2')
    address = request.form.get('customer_address')
    city = request.form.get('customer_city')
    aadhar_card = request.form.get('customer_aadhar')
    email = request.form.get('customer_email')
    photo = request.form.get('customer_photo')
    file = request.files['file']
    if file:
        filename = datetime.datetime.now().strftime('%Y%m%d%H%M%S')+file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        photo = '/uploads/'+filename
    customer.update(id,name.title(), mob1, mob2, address, city, aadhar_card, photo,email)
    return redirect('/customers/')

@app.route('/customers/<id>/')
def get_customer(id):
    result = customer.get(id)
    bills = customer.getBillsForCustomer(id)
    return render_template("customer_edit.html", customers = result, bills = bills)  

@app.route('/customers/')
@app.route('/customers/<k>/<v>/')
def customers(k='id',v='desc'):
    result = customer.customers(k,v)
    return render_template("customer.html", customers = result)  

@app.route('/alltransactions/')
def all_transactions():
    transactions = trans.get_transactions()
    return render_template("all_transactions.html",transactions=transactions)  
@app.route('/cancel/<id>/')
def cancel_transaction(id):
    trans.cancel(id)
    customer_id = trans.get_customer_for_transaction(id)
    return redirect('/showtransactions/'+str(customer_id) + '/')
@app.route('/transactions/<id>/')
def transactions(id):
    c = customer.get(id)
    items = item.items()
    todays_gold_price=getTodaysGoldPrice()
    # print(todays_gold_price)
    return render_template("transactions.html",customer=c,items=items, todays_gold_price=todays_gold_price)  
@app.route('/showtransactions/<id>/')
def show_transactions(id):
    c = customer.get(id)
    transactions = trans.get_transactions_for_customer(id)
    # print(transactions)
    return render_template("transaction.html",customer=c,transactions=transactions)  
@app.route('/transaction/<id>/', methods=['POST'])
def add_transaction(id):
    data = request.form
    # print(data)
    cart=[]
    for d in data:
        if 'qty' in d:
            itemid=d[3:]
            if int(request.form[d]) == 0: continue
            cart += [(itemid,request.form[d], request.form['discount'+str(itemid)])]
    trans.add(id,data['unit_price'],cart,data['tax'],data['misc'],data['grand_total'])
    return redirect('/customers/')

@app.route('/items/')
@app.route('/items/<k>/<v>/')
def get_items(k='id',v='desc'):
    result = item.all_items(k,v)
    return render_template("item.html", items = result)  
@app.route('/item/', methods=['POST'])
def add_item():
    name = request.form.get('item_name')
    desc = request.form.get('item_desc')
    weight = request.form.get('item_weight')
    photo = request.form.get('item_photo')
    stock = request.form.get('item_stock')
    file = request.files['file']
    if file:
        filename = datetime.datetime.now().strftime('%Y%m%d%H%M%S')+file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        photo = '/uploads/'+filename
    id = item.add(name.title(), desc,weight,photo,stock)
    return redirect('/items/')
@app.route('/items/<id>/')
def get_item(id):
    result = item.get(id)
    return render_template("item_edit.html", items = result)  
@app.route('/item/<id>/', methods=['POST'])
def update_item(id):
    name = request.form.get('item_name')
    desc = request.form.get('item_desc')
    weight = request.form.get('item_weight')
    photo = request.form.get('item_photo')
    stock = request.form.get('item_stock')
    file = request.files['file']
    if file:
        filename = datetime.datetime.now().strftime('%Y%m%d%H%M%S')+file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        photo = '/uploads/'+filename
    item.update(id,name.title(), desc,weight,photo,stock)
    return redirect('/items/')
@app.route('/payments/<customer_id>')
def get_payments(transaction_id):
    result = payment.payments(transaction_id)
    return render_template("payment.html", payments = result)  
@app.route('/newpayment/<tx_id>/<customer_id>/')
def new_payment(tx_id,customer_id):
    tx = trans.get_transaction(tx_id)
    return render_template("payment.html", tx_id = tx_id,customer_id=customer_id,amount=tx[0][9])  
@app.route('/payment/<tx_id>/<customer_id>/', methods=['POST'])
def add_payment(tx_id,customer_id):
    payment_method = request.form.get('payment_method')
    amount = request.form.get('amount')
    payment_details = request.form.get('payment_details')
    # print(tx_id, payment_method,amount,payment_details)
    id = payment.add(tx_id, amount,payment_method,payment_details)
    trans.update_balance(tx_id)
    return redirect('/showtransactions/'+str(customer_id))
@app.route('/payment/<id>/', methods=['POST'])
def update_payment(id):
    bill_id = request.form.get('tx_id')
    payment_method = request.form.get('payment_type')
    amount = request.form.get('amount')
    details = request.form.get('payment_details')
    payment.update(id,bill_id, payment_method, amount, details)
    return redirect('/payments/')
@app.route('/payments/<id>/')
def get_payment(id):
    result = payment.get(id)
    return render_template("payment_edit.html", payment = result)  

def get_reports():
    customers_count = reports.customersCount()
    items_count = reports.itemsCount()
    transactions_count = reports.transactionsCount()
    total_sales = reports.salesTotal()
    total_balance = reports.balanceTotal()
    sales = reports.sales()
    x={}
    for sale in sales:
        if sale[1][:10] not in x.keys() :
            x[sale[1][:10]] = 0
        if sale[0] != None :
            x[sale[1][:10]] +=  sale[0]  
    rows=[]
    for k in x.keys(): 
        rows += [{'date':k,'amount':x[k]}]
    return {'customers_count':customers_count,
                'items_count':items_count,'transactions_count':transactions_count,
                'total_sales':total_sales, 'total_balance':total_balance,  'daily_sales':rows}

if __name__ == '__main__':
 app.debug = True
#  app.run(host='0.0.0.0:80')
 app.run()
