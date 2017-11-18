from src.database import Database
from src.user import User
import bcrypt

class DBManager():
    def __init__(self):
        self.database = Database()

    def add_user(self, first_name, last_name, email_address, password):
        hashedpw = self._hash_pw(password)
        user = User(first_name, last_name, email_address, hashedpw)
        self.database._add_user(user)

    def auth_user(self, email, password):
        user = self.database._validate_user_login(email, password)
        print(str(user[1]))
        hashedpw = user[1]
        check = self._check_pw_hash(password, hashedpw)
        user = user[0] + user[1]
        if check is True:
            return user
        else:
            return "Password is not correct"

    def _hash_pw(self, password):
        hashedpw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
        return hashedpw

    def _check_pw_hash(self, password, hashedpw):
        if bcrypt.checkpw(password, hashedpw):
            return True
        else:
            return False