import os
import secrets

from flask import Flask, request
from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.secret_key = os.environ['SECRET_KEY']

tables = {
    'accounts': {'id': 'SERIAL', 'username': 'TEXT NOT NULL', 'password': 'TEXT NOT NULL', 'auth': 'TEXT NOT NULL'},
    'songs': {'id': 'SERIAL', 'title': 'TEXT NOT NULL', 'artist': 'TEXT', 'image': 'TEXT', 'spotify': 'TEXT', 'itunes': 'TEXT', 'youtube': 'TEXT', 'tidal': 'TEXT', 'amazonMusic': 'TEXT', 'soundcloud': 'TEXT', 'youtubeMusic': 'TEXT'}
}

import app.sql as sqlClass

sql = sqlClass.SQL()
sqlClass.tables = tables

import app.accounts as accounts

accounts.sql = sql
accounts.bcrypt = Bcrypt(app)

import app.songs as songs

songs.sql = sql

@app.route("/add-song", methods=['POST'])
def add_song():
    return songs.add_song_request()

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

@app.route("/login", methods=['POST'])
def login():
    return accounts.login()

@app.route("/signup", methods=['POST'])
def signup():
    return accounts.signup()

@app.route("/account-data", methods=['POST'])
def account_data():
    return accounts.account_data()

@app.route("/reset-cursor", requests=['POST'])
def reset_cursor():
    sql.resetCursor()
    return 'Reset Cursor'
    