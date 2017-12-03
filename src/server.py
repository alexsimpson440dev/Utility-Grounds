from src.dbManager import DBManager
import os
from flask import Flask, render_template, redirect, request, session

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
@app.route('/manage/<bill>', methods=['post', 'get'])
@app.route('/manage.html', methods=['get'])
def add_bill(bill=None):
    # creates a bills list for testing. will add to database
    # if post is requested, a bill will be added to the list
    # else the bills will be retrieved
    if request.method == 'POST':
        count = len(bills) + 1
        bills.append('Bill' + str(count))
        print(bills)
        return render_template("manage.html", bill=bills)
    else:
        print(bills)
        return render_template("manage.html")

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