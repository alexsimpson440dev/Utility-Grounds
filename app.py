#from src.server import app
import os
import psycopg2
from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, '/static', static_folder='../static', template_folder='../templates')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL',"postgresql://postgres:password/grounds")
db = SQLAlchemy(app)

if __name__=='__main__':
    app.run()