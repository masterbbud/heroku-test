import os
import secrets

from flask import Flask, request
from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.secret_key = os.environ['SECRET_KEY']

tables = {
    'accounts': {'id': 'SERIAL', 'username': 'TEXT NOT NULL', 'password': 'TEXT NOT NULL', 'auth': 'TEXT NOT NULL'}
}

import app.sql

sql = app.sql.SQL()
app.sql.tables = tables

import app.accounts

app.accounts.app = app
app.accounts.sql = sql
app.accounts.bcrypt = Bcrypt(app)

@app.route("/add-song")
def add_song():
    if request.args.get('name', None):
        sql.insert('songs', {'name': request.args.get('name')})
    return ''

@app.route("/get-songs")
def get_songs():
    return sql.select('songs')

@app.route("/get-accounts")
def get_accounts():
    return sql.select('accounts')

@app.route("/drop-songs")
def drop_songs():
    return ''

@app.route("/create-songs")
def create_songs():
    sql.createTable('songs', {'id': 'SERIAL', 'name': 'TEXT NOT NULL'})
    return 'Created Songs'

@app.route("/create-accounts")
def create_accounts():
    sql.createTable('accounts')
    return 'Created Accounts'

@app.route("/remove-songs")
def remove_songs():
    sql.dropTable('songs')
    return 'Removed Songs'

@app.route("/remove-accounts")
def remove_accounts():
    sql.dropTable('accounts')
    return 'Removed Accounts'

@app.route("/test-columns")
def test_columns():
    return [str(i) for i in sql.selectColumns('accounts')]


