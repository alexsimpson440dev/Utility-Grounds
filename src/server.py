from src.dbManager import DBManager
import os
import logging
import sys
from decimal import Decimal
from datetime import timedelta
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, render_template, redirect, request, session, flash, url_for

# sets manager class
MANAGER = DBManager()

# gets directories, sets a random app key
app = Flask(__name__, '/static', static_folder='../static', template_folder='../templates')
app.secret_key = os.environ['SECRET']

# sets logger for heroku
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

# calls index route
@app.route('/')
@app.route('/index')
@app.route('/index.html', methods=['get'])
def index():
    # if the session is empty, then it sends the user to the login page
    if 'email' not in session:
        return redirect(url_for('login'))

    # if the session is not empty, then the user can logout, check their bills, or manage the bills if its an admin
    else:
        if request.method == 'POST':
            if 'email' not in session:
                return redirect(url_for('login'))
            else:
                sign_out()
        else:
            # gets email associated with the session and the user_level that is associated with user
            # determines if admin or not
            email = session.get('email')
            user_name = MANAGER._get_name(email)
            user_level = MANAGER._get_user_level(email)
            if user_level > 1:
                return render_template('index.html', user_name=user_name, manage='')
            else:
                return render_template('index.html', user_name=user_name, manage='Manage Bills')

        return render_template(url_for('index'))

# gets the signup route
@app.route('/signup', methods=['post', 'get'])
@app.route('/signup.html', methods=['get'])
def signup():
    # if the route is post, then the user clicked submit to add their user information
    # todo: add more validation
    session['token'] = random.randint(100000, 999999)
    _send_email()
    print(session['token'])
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email_address = request.form.get('email_address')
        password = request.form.get('password')

        # checks if the email is in use
        # if nothing is returned, then the email is available
        check_email = MANAGER.check_email_availability(email_address)
        if check_email is None:
            try:
                MANAGER.add_user(first_name, last_name, email_address, password)
                session['email'] = email_address
                return redirect(url_for('index'))

            except RuntimeError as e:
                print('Run Time Error: ', e)
                return redirect(url_for('signup'))

        # if it is not available, a message will be displayed to the user
        # todo: fix how the message is displayed
        else:
            return render_template('signup.html', valid='Email is already in use!')
    else:
            return render_template(url_for('signup'))

# logs a user in
@app.route('/login', methods=['post', 'get'])
@app.route('/login.html', methods=['get'])
def login():
    # gets users info from the html page
    # the server checks to see if the users credentials are correct
    # if auth is true the user will be signed in
    if request.method == 'POST':
        email_address = request.form.get('email_address')
        password = request.form.get('password')
        auth = MANAGER.auth_user(email_address, password)
        if auth is True:
            session['email'] = email_address
            return redirect(url_for('index'))

        # if the credentials are wrong
        # the user will be redirected back to the sign in page
        else:
            flash('email or password is incorrect')
            return redirect(url_for('login'))

    else:
        return render_template(url_for('login'))

# adding bills
@app.route('/manage', methods=['post', 'get'])
@app.route('/manage.html', methods=['get'])
def add_bill():
    # checks to see if session is available
    if check_session() is False:
            return redirect(url_for('login'))
    else:
        # checks to see if the user is able to access the manager level
        user_level = MANAGER._get_user_level(session['email'])
        if user_level > 1:
            return redirect(url_for('index'))

        # creates a bills list for testing. will add to database
        # if post is requested, a bill will be added to the list
        # else the bills will be retrieved
        if request.method == 'POST':
            user_count = MANAGER._get_user_count()

            date_added = request.form.get('date_added')
            electricity = request.form.get('electricity')
            gas = request.form.get('gas')
            internet = request.form.get('internet')
            city = request.form.get('city')
            due_date = request.form.get('due_date')

            # reject a divide by zero error
            if user_count is 0:
                user_count = 1

            # sets the totals for bills
            total = Decimal(electricity) + Decimal(gas) + Decimal(internet) + Decimal(city)
            total_per_user = round(Decimal(total)/Decimal(user_count), 2)

            # tries to add a bill to the database
            # if it is a success, the bill will be added and the page will redirect back to the manage.html
            # this will then show an updated view of the bills
            try:
                MANAGER.add_bill(date_added, electricity, gas, internet, city, total_per_user, total, due_date)
                return redirect(url_for('add_bill'))

            # if the add fails, this will catch the error and redirect the user back to the manage.html page
            except RuntimeError:
                print('cannot add bill')
                return redirect(url_for('add_bill'))

        # if the request method is post, the server will get the bills and add them to the html table
        if request.method == 'GET':
            bills = MANAGER._get_bills()
            return render_template("manage.html", bills=bills)

# gets the view bills route
# pulls from the database and puts the bills into a table
# todo: maybe make a groups table for pulling correct bills?
@app.route('/viewbills.html', methods=['get'])
def view_bills():
    bills = MANAGER._get_bills()
    return render_template("viewbills.html", bills=bills)

#gets the pay bills route
#gets the information from clicked bill to display
@app.route('/paybill', methods=['get'])
@app.route('/paybill.html', methods=['get'])
def pay_bills():
    # checks user level, if it is 3 then it will display the bill
    # if it is not a 3, then the manager can edit the bill
    user_level = MANAGER._get_user_level(session['email'])
    print(user_level)
    bills = MANAGER._get_bills()
    bill_clicked = int(request.args.get('bill'))
    bill = bills[bill_clicked]

    DA = bill.pop(0)
    E = bill.pop(0)
    G = bill.pop(0)
    I = bill.pop(0)
    C = bill.pop(0)
    TPU = bill.pop(0)
    T = bill.pop(0)
    DD = bill.pop(0)

    if user_level == 1:
        return redirect(url_for('update_bill'))

    else:
        return render_template("paybill.html", DA=DA, E=E, G=G, I=I, C=C, TPU=TPU, T=T, DD=DD)

# opens update bill template
@app.route('/updatebill', methods=['get'])
@app.route('/updatebill.html', methods=['get'])
def update_bill():
    # checks if session is available. If not, the user will be redirected
    if check_session() is False:
        return redirect(url_for('login'))

    # if the session is available, see if the user has access. If so, go to update bill. If not, go back to index
    if MANAGER._get_user_level(session['email']) == 1:
        return render_template('updatebill.html')

    else:
        return redirect(url_for('index'))


# signs a user in based on the email address
# todo: add a time out

# def sign_in(email_address):
    #session['email'] = email_address

# if the user chooses to sign out or gets timed out
# the application will delete the session linked to the users email
@app.route('/logout', methods=['post'])
def sign_out():
    session.pop('email', None)
    return redirect(url_for('login'))

def check_session():
    if 'email' in session:
        return True
    else:
        return False

def _send_email():
    from_email = "alexsimpson440dev@gmail.com"
    to_email = "alexsimpson440@gmail.com"
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = "Utility-Grounds Manager Token"

    body = "Your new Manager Sign-Up token is, " + str(session['token'])
    msg.attach(MIMEText(body, 'plain'))

    email_server = smtplib.SMTP('smtp.gmail.com', 587)
    email_server.starttls()
    email_server.login(from_email, "apple440")
    text = msg.as_string()
    email_server.sendmail(from_email, to_email, text)
    email_server.quit()

# runs application from the app.py file
if __name__ == '__main__':
    app.run(port=9999, debug=True)