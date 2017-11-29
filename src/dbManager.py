from src.database import Database
from src.user import User
from src.bills import Bills
import bcrypt

# Database manager class
class DBManager():
    def __init__(self):
        self.database = Database()

    # adds user to the database after hashing the password
    # prevents an unsecured password from being entered in
    def add_user(self, first_name, last_name, email_address, password):
        hashedpw = self._hash_pw(password.encode('utf-8'))
        user = User(first_name, last_name, email_address, hashedpw)
        self.database._add_user(user)

    # adds a bill to the database from html
    def add_bill(self, date_added, electricity, gas, internet, city, total, due_date):
        bill = Bills(date_added, electricity, gas, internet, city, total, due_date)
        self.database._add_bill(bill)

    # validates the users password against their email
    # by retrieving the hashed password, then checking
    # the password entered by the user
    def auth_user(self, email, password):
        hashedpassword = self.database._validate_user_password(email)
        check = bcrypt.checkpw(password.encode('utf-8'), hashedpassword)
        if check is True:
            return True
        else:
            return False

    # hashes the users password using bcrypt
    def _hash_pw(self, password):
        hashedpw = bcrypt.hashpw(password, bcrypt.gensalt())
        return hashedpw