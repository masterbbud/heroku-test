from types import NoneType
from flask import Flask, jsonify, request

from boto.s3.connection import S3Connection
import os

import psycopg2

from datetime import datetime

from flask_login import LoginManager, login_user, current_user

from flask_bcrypt import Bcrypt

import secrets

# Something that will reset the cursor if you need to reconnect to the database

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.secret_key = os.environ['SECRET_KEY']
 
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.get(id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    user = User.find(request.args.get('username'), request.args.get('password'))
    if user:
        login_user(user, remember=True)
        return 'Logged in!'
    else:
        return 'Incorrect Login Credentials'
    

@app.route('/signupAAA', methods=['GET', 'POST'])
def signupAAA():
    user = User.create(request.args.get('username'), request.args.get('password'))
    if user:
        login_user(user, remember=True)
        return 'Signed up and Logged in!'
    else:
        return 'Account already exists with that username'

@app.route('/signup', methods=['POST'])
def signup():
    args = request.json
    username = args.get('username')
    if not username:
        return 'Failed to create account: no username provided'
    password = args.get('password')
    if not password:
        return 'Failed to create account: no password provided'

    acc = sql.select('accounts', f"username = '{username}'")
    if acc:
        return 'Failed to create account: account with that username already exists'
    # then, add username and hashed password to sql

    pw = bcrypt.generate_password_hash(password).decode('utf-8')

    auth = get_auth_token()
    while User.auth_token_used(auth):
        auth = get_auth_token()
    
    sql.insert('accounts', {'username': username, 'password': pw, 'auth': auth})
    return auth

@app.route("/")
def home_view():
    return "<h1>Welcome to Geeks for Geeks</h1>"

@app.route("/get-test")
def get_test():
    retDict = {
        'users': [
            {
                'id': 1,
                'name': 'brandon'
            },
            {
                'id': 6,
                'name': 'leah'
            }
        ]
    }
    return jsonify(retDict)

@app.route("/sql-test")
def sql_test():
    conn = psycopg2.connect(
        host=os.environ['DB_HOST'],
        database=os.environ['DB_DATABASE'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD'])
    cur = conn.cursor()

    sql.addSong('testsong')
    cur.execute("""
    SELECT * from newtable
    """)
    rows = cur.fetchall()
    return rows

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
    sql.createTable('accounts', {'id': 'SERIAL', 'username': 'TEXT NOT NULL', 'password': 'TEXT NOT NULL', 'auth': 'TEXT NOT NULL'})
    return 'Created Accounts'

@app.route("/remove-songs")
def remove_songs():
    sql.dropTable('songs')
    return 'Removed Songs'

@app.route("/remove-accounts")
def remove_accounts():
    sql.dropTable('accounts')
    return 'Removed Accounts'

@app.route("/test-login")
def test_login():
    if current_user.is_authenticated:
        return 'authenticated' + str(current_user)
    else:
        return 'not authenticated' + str(current_user)

@app.route("/sql-tables")
def sql_tables():
    return sql.tables

def get_auth_token():
    return secrets.token_urlsafe(20)

class User:

    users = {}

    def __init__(self, id):
        self.id = id
        User.users.update({id: self})

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return self.is_active

    @property
    def is_anonymouse(self):
        return False
    
    def get_id(self):
        return self.id
    
    def set_id(self, id):
        self.id = id
    
    @staticmethod
    def get(id):
        return User.users.get(id)

    @staticmethod
    def find(username, password):
        # takes a username and password as input and tries to find the account associated
        # if none, returns None
        acc = sql.select('accounts', f"username = '{username}'")
        if not acc:
            return None
        pw = acc[0]['password']
        if bcrypt.check_password_hash(pw, password):
            return User(acc[0]['id'])

    @staticmethod
    def create(username, password):
        # takes a username and password and creates an account

        # first, check if account already exists:
        acc = sql.select('accounts', f"username = '{username}'")
        if acc:
            return None
        # then, add username and hashed password to sql

        pw = bcrypt.generate_password_hash(password).decode('utf-8')

        auth = get_auth_token()
        while User.auth_token_used(auth):
            auth = get_auth_token()
        
        sql.insert('accounts', {'username': username, 'password': pw, 'auth': auth})
        return User.find(username, password)
    
    @staticmethod
    def auth_token_used(token):
        return True if sql.select('accounts', f"auth = '{token}'") else False

class SQL:
    def __init__(self):
        self.conn = psycopg2.connect(
            host=os.environ['DB_HOST'],
            database=os.environ['DB_DATABASE'],
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASSWORD'])
        self.cur = self.conn.cursor()
        self.tables = {} # tablename : {val: type, val: type}
        #self.dropTable('songs')
        #self.createTable('songs', {'id': 'SERIAL', 'name': 'TEXT NOT NULL'})
        #self.dropTable('accounts')
        #self.createTable('accounts', {'id': 'SERIAL', 'username': 'TEXT NOT NULL', 'password': 'TEXT NOT NULL'})
        
    def dropTable(self, name):
        self.cur.execute(f"""
            ALTER TABLE {name}
                DROP CONSTRAINT {name}_id_seq
            DROP TABLE IF EXISTS {name}
        """)
        self.conn.commit()

    def recreateTable(self, name):
        if not self.tables.get(name):
            return False
        text = []
        for n, val in self.tables[name]:
            text.append(f'{n} {val}')
        text = ',\n'.join(text)
        self.cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {name} (
            {text});
        """)
        self.conn.commit()
        return True

    def createTable(self, name, columns: dict):
        self.tables[name] = columns
        text = []
        for n, val in columns.items():
            text.append(f'{n} {val}')
        text = ',\n'.join(text)
        self.cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {name} (
            {text});
        """)
        self.conn.commit()
    
    def insert(self, table, columns: dict):
        # columns should be columnName: value
        colsList = ', '.join(list(columns))
        valsList = [f"'{i}'" if isinstance(i, str) else f"{i}" for i in columns.values()]
        valsText = ',\n'.join(valsList)
        self.cur.execute(f"""
        INSERT into {table} ({colsList})
        VALUES (
            {valsText}
        )
        """)
        self.conn.commit()

    def select(self, table, where=None):
        if where:
            self.cur.execute(f"""
                SELECT * from {table} where {where}
            """)
        else:
            self.cur.execute(f"""
                SELECT * from {table}
            """)
        retList = []
        for s in self.cur.fetchall():
            row = {}
            for (colname, cast), value in zip(self.tables.get(table).items(), s):
                row.update({colname: self.typeCast(value, cast)[0]})
            retList.append(row)
        return retList

    def typeCast(self, val, typeString):
        # returns a value, typecast via typeString, and also the type
        if 'TEXT' in typeString:
            return str(val), str
        elif 'INTEGER' in typeString or 'SERIAL' in typeString:
            return int(val), int
        elif 'BOOLEAN' in typeString:
            return bool(val), bool
        elif 'TIMESTAMP' in typeString:
            return datetime(val), datetime
        return val, NoneType


sql = SQL()


