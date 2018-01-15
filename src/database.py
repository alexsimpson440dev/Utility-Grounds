# import sqlite3
# todo: go to - https://www.pgadmin.org - for a postgres manager

import os
from src.user import User
from src.bills import Bills
from sqlalchemy import Table, MetaData, Column, Integer, Float, String, Date, ForeignKey, create_engine
from sqlalchemy.orm import mapper, sessionmaker, relationship

METADATA = MetaData()
DATABASE_URI = os.environ['DATABASE_URL']

# todo: check to see if tables already exist before creating
# Database Class
class Database():
    # constructor, declares connection string within
    # sets sql_file, users, and engine
    def __init__(self, connection_string=DATABASE_URI):
        self.sql_file = connection_string
        self.users = self._map_user()
        self.bills = self._map_bills()
        self.engine = self._get_connection()
        METADATA.create_all(bind=self.engine)

    # maps users table for sqlalchemy to its data model
    def _map_user(self):
        users = Table('Users', METADATA,
                     Column('user_id', Integer, primary_key=True),
                     Column('first_name', String),
                     Column('last_name', String),
                     Column('email_address', String),
                     Column('password', String),
                     Column('user_level', Integer)
                     )
        mapper(User, users)
        return users

    # maps bills table for sqlalchemy to its data model
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

    # queries for the users email, used to check for already existing email
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

    # gets the bills in the bills table
    # takes the bills and places them in a list
    # the list is then placed into a dictionary with a key that starts at one.
    def _get_bills(self):
        counter = 1
        bills_dict = dict()
        session = self._get_session()
        for bid, da, e, g, i, c, t, dd in session.query(Bills.bill_id, Bills.date_added, Bills.electricity, Bills.gas, Bills.internet,
                                   Bills.city, Bills.total, Bills.due_date):
            loop_list = [da, e, g, i, c, t, dd]
            for items in loop_list:
                bills_dict.setdefault(counter, []).append(items)
            counter+=1

        # returns the bills dictionary
        return bills_dict

    # query that checks the users level based off of the email provided
    def _check_user_level(self, email):
        session = self._get_session()
        for user in session.query(User.user_level)\
                .filter(User.email_address == email):
            return user.user_level

    # query that retrieves the users Names
    def _get_users_name(self, email):
        session = self._get_session()
        for name in session.query(User.first_name, User.last_name)\
                .filter(User.email_address == email):
            usersName = name.first_name + ' ' + name.last_name
            return usersName


