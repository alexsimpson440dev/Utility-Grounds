import sqlite3
from src.user import User
from src.bills import Bills
from sqlalchemy import Table, MetaData, Column, Integer, Float, String, Date, ForeignKey, create_engine
from sqlalchemy.orm import mapper, sessionmaker, relationship
METADATA = MetaData()

# Database Class
class Database():
    # constructor, declares connection string within
    # sets sql_file, users, and engine
    def __init__(self, connection_string="sqlite:///groundsDB.sqlite3"):
        self.sql_file = connection_string
        self.users = self._map_user()
        self.bills = self._map_bills()
        self.engine = self._get_connection()
        METADATA.create_all(bind=self.engine)

    # maps users table
    def _map_user(self):
        users = Table('Users', METADATA,
                     Column('user_id', Integer, primary_key=True),
                     Column('first_name', String),
                     Column('last_name', String),
                     Column('email_address', String),
                     Column('password', String)
                     )
        mapper(User, users)
        return users

    def _map_bills(self):
        bills = Table('Bills', METADATA,
                      Column('bill_id', Integer, primary_key=True),
                      Column('date_added', String),
                      Column('electricity', Float),
                      Column('gas', Float),
                      Column('internet', Float),
                      Column('city', Float),
                      Column('total', Float),
                      Column('due_date', String)
                      )
        mapper(Bills, bills)
        return bills

    # gets connection through sqlalchemy with the sql_file connection string
    def _get_connection(self):
        engine = create_engine(self.sql_file)
        return engine

    # gets the session with the session maker
    def _get_session(self):
        session = sessionmaker(bind=self.engine)
        return session()

    # adds a new user to the database
    def _add_user(self, user):
        session = self._get_session()
        session.add(user)
        session.commit()

    # adds a new bill to the database
    def _add_bill(self, bill):
        session = self._get_session()
        session.add(bill)
        session.commit()

    # queries for the users email
    def _validate_user_email(self, email):
        session = self._get_session()
        for user in session.query(User)\
                .filter(User.email_address == email):
            session.commit()
            return user.email_address

    # queries for the users password
    def _validate_user_password(self, email):
        session = self._get_session()
        for user in session.query(User)\
                .filter(User.email_address == email):
            session.commit()
            return user.password

    def _get_bills(self):
        bill_list = list()
        session = self._get_session()
        for bills in session.query(Bills).all():
            bill_list.append(bills)
        return bill_list

