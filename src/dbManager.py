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
    def add_bill(self, date_added, electricity, gas, internet, city, total_per_user, total, due_date):
        bill = Bills(date_added, electricity, gas, internet, city, total_per_user, total, due_date)
        self.database._add_bill(bill)

    def check_email_availability(self, email):
        email = self.database._validate_user_email(email)
        return email

    # validates the users password against their email
    # by retrieving the hashed password, then checking
    # the password entered by the user
    def auth_user(self, email, password):
        try:
            hashedpassword = self.database._validate_user_password(email)
            check = bcrypt.checkpw(password.encode('utf-8'), hashedpassword.encode('utf-8'))
            if check is True:
                return True
            else:
                return False
        except AttributeError:
            return False

    # hashes the users password using bcrypt
    def _hash_pw(self, password):
        hashedpw = bcrypt.hashpw(password, bcrypt.gensalt())
        hashedpw = hashedpw.decode('utf-8')
        return hashedpw

    # retrieves bills from the database
    def _get_bills(self):
        bills = self.database._get_bills()
        return bills

    # retrieves billID from database
    def _get_billID(self, date_added):
        billID = self.database._get_billID(date_added)
        return billID

    # gets the users level from the database
    def _get_user_level(self, email):
        user_level = self.database._check_user_level(email)
        return user_level

    # gets users name
    def _get_name(self, email):
        user_name = self.database._get_users_name(email)
        return user_name

    def _get_user_count(self):
        count = self.database._count_users()
        return count