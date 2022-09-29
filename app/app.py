from types import NoneType
from flask import Flask, jsonify, request

from boto.s3.connection import S3Connection
import os

import psycopg2

from datetime import datetime
 
app = Flask(__name__)
 
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

@app.route("/drop-songs")
def drop_songs():
    return ''


class SQL:
    def __init__(self):
        self.conn = psycopg2.connect(
            host=os.environ['DB_HOST'],
            database=os.environ['DB_DATABASE'],
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASSWORD'])
        self.cur = self.conn.cursor()
        self.tables = {} # tablename : {val: type, val: type}
        self.dropTable('songs')
        self.createTable('songs', {'id': 'SERIAL PRIMARY KEY', 'name': 'TEXT NOT NULL'})
        
    def dropTable(self, name):
        self.cur.execute(f"""
            DROP TABLE IF EXISTS {name}
        """)
        self.conn.commit()

    def recreateTable(self, name):
        if not self.tables.get(name):
            return False
        text = ''
        for n, val in self.tables[name]:
            text += f'{n} {val}\n'
        self.cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {name} (
            {text});
        """)
        return True

    def createTable(self, name, columns: dict):
        text = ''
        for n, val in columns.items():
            text += f'{n} {val}\n'
        self.cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {name} (
            {text});
        """)
        self.tables.update({name: columns})
    
    def insert(self, table, columns: dict):
        # columns should be columnName: value
        colsList = list(columns)
        valsList = [f"'{i}',\n" if isinstance(i, str) else f"{i},\n" for i in columns.values()]
        self.cur.execute(f"""
        INSERT into {table} ({colsList})
        VALUES (
            {valsList}
        )
        """)
        self.conn.commit()

    def select(self, table, where):
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
            for (colname, cast), value in zip(self.tables[table].items(), s[:-1]):
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


