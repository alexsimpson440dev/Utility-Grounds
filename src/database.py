import sqlite3
from src.user import User
from sqlalchemy import Table, MetaData, Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import mapper, sessionmaker, relationship
METADATA = MetaData()

class Database():
    def __init__(self, connection_string="sqlite:///groundsDB.sqlite3"):
        self.sql_file = connection_string
        self.users = self._map_user()
        self.engine = self._get_connection()
        METADATA.create_all(self.engine)

    def _map_user(self):
        users = Table('Users', METADATA,
                     Column('user_id', Integer, primary_key=True),
                     Column('first_name', String(30)),
                     Column('last_name', String(30)),
                     Column('email_address', String(50)),
                     Column('password', String(15))
                     )
        mapper(User, users)
        return users

    def _get_connection(self):
        engine = create_engine(self.sql_file)
        return engine

    def _get_session(self):
        session = sessionmaker(bind=self.engine)
        return session()

    def _add_user(self, user):
        session = self._get_session()
        session.add(user)
        session.commit()
