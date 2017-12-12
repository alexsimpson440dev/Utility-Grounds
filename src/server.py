from src.dbManager import DBManager
import os
from flask import Flask, render_template, redirect, request, session, flash

# sets manager class
MANAGER = DBManager()

# gets directories, sets a random app key
app = Flask(__name__, '/static', static_folder='../static', template_folder='../templates')
app.secret_key = os.urandom(24)

# calls index route
@app.route('/')
@app.route('/index')
@app.route('/index.html', methods=['get'])
def index():
    # if the session is empty, then it sends the user to the login page
    if session.get('email') is None:
        return redirect('login.html')
    # if the session is not empty, then the user can logout, check their bills, or manage the bills if its an admin
    else:
        if request.method == 'POST':
            sign_out()
        else:
            # gets email associated with the session and the user_level that is associated with user
            # (determines if admin or not
            email = session.get('email')
            user_level = MANAGER._get_user_level(email)
            if user_level > 1:
                return render_template('index.html', email=email, manage='')
            else:
                return render_template('index.html', email=email, manage='Manage Bills')

        return render_template('index.html')

# gets the signup route
@app.route('/signup', methods=['post', 'get'])
@app.route('/signup.html', methods=['get'])
def signup():
    # if the route is post, then the user clicked submit to add their user information
    # todo: add more validation
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
                sign_in(email_address)

            except RuntimeError as e:
                print('Run Time Error: ', e)
                return redirect('signup.html')

            return redirect('index.html')
        # if it is not available, a message will be displayed to the user
        # todo: fix how the message is displayed
        else:
            return render_template('signup.html', valid='Email is already in use!')
    else:
            return render_template('signup.html')

# logs a user in
@app.route('/login', methods=['post', 'get'])
@app.route('/login.html', methods=['get'])
def user_login():
    # gets users info from the html page
    # the server checks to see if the users credentials are correct
    # if auth is true the user will be signed in
    if request.method == 'POST':
        email_address = request.form.get('email_address')
        password = request.form.get('password')
        auth = MANAGER.auth_user(email_address, password)
        if auth is True:
            sign_in(email_address)
            return redirect("index.html")
        # if the credentials are wrong
        # the user will be redirected back to the sign in page
        else:
            flash('email or password is incorrect')
            return redirect("login.html")

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

        # tries to add a bill to the database
        # if it is a success, the bill will be added and the page will redirect back to the manage.html
        # this will then show an updated view of the bills
        try:
            MANAGER.add_bill(date_added, electricity, gas, internet, city, total, due_date)
            return redirect("manage.html")

        # if the add fails, this will catch the error and redirect the user back to the manage.html page
        except RuntimeError:
            print('cannot add bill')
            return redirect("manage.html")

    # if the request method is post, the server will get the bills and add them to the html table
    if request.method == 'GET':
        bills = MANAGER._get_bills()
        return render_template("manage.html", bills = bills)

# gets the view bills route
# pulls from the database and puts the bills into a table
# todo: divide by how many users are in the database, not including admins
# todo: maybe make a groups table for pulling correct bills?
@app.route('/viewbills.html', methods=['get'])
def view_bills():
    bills = MANAGER._get_bills()
    return render_template("viewbills.html", bills = bills)


# signs a user in based on the email address
# todo: add a time out
def sign_in(email_address):
    session['email'] = email_address

# if the user chooses to sign out or gets timed out
# the application will delete the session linked to the users email
@app.route('/logout', methods=['post'])
def sign_out():
    del session['email']
    return redirect('login.html')

# runs application from the app.py file
if __name__ == '__main__':
    app.run(port=9999, debug=True)