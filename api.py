from flask import request, redirect, Flask, flash, render_template, send_from_directory, url_for, jsonify #pip install flask
from werkzeug.utils import secure_filename
import os
from customer import Customer 
from bill import Bill 
from item import Item 
from payment import Payment
from transaction import Transaction
trans = Transaction()
payment = Payment()
bill = Bill()
item = Item()
app = Flask(__name__)
customer = Customer()
UPLOAD_FOLDER = 'C:\\Users\\babur\\Google Drive\\tutorial\\python\\shop\\uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
@app.route('/')
def home():
    return render_template("home.html")

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
    photo = request.form.get('customer_photo')
    print(id,name,mob1,mob2,address,city,aadhar_card,photo)
    customer.add(name.title(), mob1, mob2, address, city, aadhar_card, photo)
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
    photo = request.form.get('customer_photo')
    customer.update(id,name.title(), mob1, mob2, address, city, aadhar_card, photo)
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

@app.route('/bills/<id>/')
def get_bill(id):
    result = bill.get(id)
    return render_template("bill_edit.html", bills = result)  
@app.route('/bill/<id>/', methods=['POST'])
def update_bill(id):
    customer_id = request.form.get('customer_id')
    item_id = request.form.get('item_id')
    unit_price = request.form.get('unit_price')
    weight = request.form.get('item_weight')
    discount = request.form.get('discount')
    total_price = request.form.get('total_price')
    bill.update(id,customer_id,item_id,weight,unit_price,discount,total_price)
    return redirect('/bills')
@app.route('/transactions/<id>/')
def transactions(id):
    c = customer.get(id)
    items = item.items()
    return render_template("transactions.html",customer=c,items=items)  
@app.route('/showtransactions/<id>/')
def show_transactions(id):
    c = customer.get(id)
    transactions = trans.get_transactions_for_customer(id)
    # print(transactions)
    return render_template("transaction.html",customer=c,transactions=transactions)  
@app.route('/transaction/<id>/', methods=['POST'])
def add_transaction(id):
    data = request.form
    print(data)
    cart=[]
    for d in data:
        if 'qty' in d:
            itemid=d[3:]
            if int(request.form[d]) == 0: continue
            cart += [(itemid,request.form[d], request.form['discount'+str(itemid)])]
    trans.add(id,data['unit_price'],cart,data['tax'],data['misc'],data['grand_total'])
    return redirect('/customers/')

@app.route('/bill/', methods=['POST'])
def add_bill():
    customer_id = request.form.get('customer_id')
    item_id = request.form.get('item_id')
    unit_price = request.form.get('unit_price')
    weight = request.form.get('item_weight')
    discount = request.form.get('discount')
    total_price = request.form.get('total_price')
    bill.add(customer_id,item_id,weight,unit_price,discount,total_price)
    return redirect('/bills/'+str(customer_id))

@app.route('/bills/')
@app.route('/bills/<k>/<v>/')
def bills(k='id',v='desc'):
    result = bill.bills(k,v)
    return render_template("bill.html", bills = result)  

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
        filename = file.filename
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
        filename = file.filename
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
    return render_template("payment.html", tx_id = tx_id,customer_id=customer_id)  
@app.route('/payment/<tx_id>/<customer_id>/', methods=['POST'])
def add_payment(tx_id,customer_id):
    payment_method = request.form.get('payment_method')
    amount = request.form.get('amount')
    payment_details = request.form.get('payment_details')
    print(tx_id, payment_method,amount,payment_details)
    id = payment.add(tx_id, payment_method,amount,payment_details)
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

if __name__ == '__main__':
 app.debug = True
 app.run()
