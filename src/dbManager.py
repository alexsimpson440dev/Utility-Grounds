from src.database import Database
from src.user import User
class DBManager():
    def __init__(self):
        self.database = Database()

    def add_user(self, first_name, last_name, email_address, password):
        user = User(first_name, last_name, email_address, password)
        self.database._add_user(user)
