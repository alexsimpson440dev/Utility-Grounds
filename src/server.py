from src.dbManager import DBManager
from flask import Flask, render_template, redirect, request, session

MANAGER = DBManager()

app = Flask(__name__, '/static', static_folder='../static', template_folder='../templates')
app.secret_key = 'the moo goes cow'

@app.route('/')
@app.route('/index')
@app.route('/index.html', methods=['get'])
def index():
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
        auth = str(MANAGER.auth_user(email_address, password))
        print(auth)
        if auth == email_address + password:
            print("login success")
            sign_in(email_address)
            return redirect("index.html")
        else:
            return render_template("signup.html")

    else:
        return render_template("login.html")

def sign_in(email_address):
    session['email'] = email_address

def sign_out():
    del session['email']
if __name__ == '__main__':
    app.run(port=9999, debug=True)