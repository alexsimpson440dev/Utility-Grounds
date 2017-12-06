from src.dbManager import DBManager
import os, datetime
from flask import Flask, render_template, redirect, request, session, url_for

MANAGER = DBManager()

app = Flask(__name__, '/static', static_folder='../static', template_folder='../templates')
app.secret_key = os.urandom(24)
bills = list()

@app.route('/')
@app.route('/index')
@app.route('/index.html', methods=['get'])
def index():
    if request.method == 'POST':
        sign_out()

    return render_template('index.html')

@app.route('/signup', methods=['post', 'get'])
@app.route('/signup.html', methods=['get'])
def signup():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email_address = request.form.get('email_address')
        password = request.form.get('password')

        try:
            MANAGER.add_user(first_name, last_name, email_address, password)
            sign_in(email_address)

        except RuntimeError as e:
            print('Run Time Error: ', e)
            return redirect('signup.html')

        return render_template('index.html')
    else:
        return render_template('signup.html')

@app.route('/login', methods=['post', 'get'])
@app.route('/login.html', methods=['get'])
def user_login():
    if request.method == 'POST':
        email_address = request.form.get('email_address')
        password = request.form.get('password')
        auth = MANAGER.auth_user(email_address, password)
        if auth is True:
            print("login success")
            sign_in(email_address)
            return redirect("index.html")
        else:
            print("email or password is incorrect")
            return render_template("login.html")

    else:
        return render_template("login.html")

# adding bills
@app.route('/manage', methods=['post', 'get'])
@app.route('/manage.html', methods=['get'])
def add_bill():
    # creates a bills list for testing. will add to database
    # if post is requested, a bill will be added to the list
    # else the bills will be retrieved
    if request.method == 'POST':
        date_added = request.form.get('date_added')
        electricity = request.form.get('electricity')
        gas = request.form.get('gas')
        internet = request.form.get('internet')
        city = request.form.get('city')
        total = float(electricity) + float(gas) + float(internet) + float(city)
        due_date = request.form.get('due_date')


        try:
            MANAGER.add_bill(date_added, electricity, gas, internet, city, total, due_date)
            bills = MANAGER._get_bills()
            for number in bills:
                bill = str(number)
                b_id,date_added,electricity,gas,internet,city,total,due_date = bill.split(',')
                return render_template("manage.html", date_added=date_added, electricity=electricity, gas=gas, internet=internet,
                                   city=city, total=total, due_date=due_date)

        except RuntimeError:
            print('cannot add bill')
            return redirect("manage.html")

    if request.method == 'GET':
        bills = MANAGER._get_bills()
        for value in bills:
            print(value)
        return render_template("manage.html", bills = bills)

def sign_in(email_address):
    session['email'] = email_address
    print('signing in: ' + session['email'])

@app.route('/logout', methods=['post', 'get'])
def sign_out():
    print('signing out: ' + session['email'])
    del session['email']
    return redirect('login.html')

if __name__ == '__main__':
    app.run(port=9999, debug=True)