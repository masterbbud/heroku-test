from types import NoneType
from flask import Flask, jsonify, request

from boto.s3.connection import S3Connection
import os

import psycopg2

from datetime import datetime

from flask_bcrypt import Bcrypt

import secrets

# Something that will reset the cursor if you need to reconnect to the database
# tables just disappear sometimes. wtf

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.secret_key = os.environ['SECRET_KEY']

@app.route('/login', methods=['POST'])
def login():
    """
    POST with a username and password, returns the AUTH key for that account or a warning based on the failure
        of the account lookup.
    """
    args = request.json
    username = args.get('username')
    if not username:
        return 'ERROR: Request needs username'
    password = args.get('password')
    if not password:
        return 'ERROR: Request needs password'

    acc = sql.select('accounts', f"username = '{username}'")
    if not acc:
        return 'ERROR: No Account'

    if bcrypt.check_password_hash(acc[0]['password'], password):
        return acc[0]['auth']
    else:
        return 'ERROR: Incorrect Password'

@app.route('/signup', methods=['POST'])
def signup():
    """
    POST with a username and password, creates an account if able and returns the AUTH key for that account or
        a warning based on the failure of the account lookup.
    """
    args = request.json
    username = args.get('username')
    if not username:
        return 'ERROR: Request needs username'
    password = args.get('password')
    if not password:
        return 'ERROR: Request needs password'

    acc = sql.select('accounts', f"username = '{username}'")
    if acc:
        return 'ERROR: Username already exists'

    pw = bcrypt.generate_password_hash(password).decode('utf-8')

    auth = get_auth_token()
    while auth_token_used(auth):
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

@app.route("/sql-tables")
def sql_tables():
    return sql.tables

@app.route("/get-account-data", methods=['POST'])
def account_data():
    args = request.json
    token = args.get('token')
    if not token:
        return 'ERROR: Request needs token'
    if not auth_token_used(token):
        return 'ERROR: Invalid token'
    else:
        return user_data(token)

def get_auth_token():
    return secrets.token_urlsafe(20)

def auth_token_used(token):
        return True if sql.select('accounts', f"auth = '{token}'") else False
    
def user_data(token):
    return sql.select('accounts', f"auth = '{token}'")

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


