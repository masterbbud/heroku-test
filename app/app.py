from flask import Flask, jsonify, request

from boto.s3.connection import S3Connection
import os

import psycopg2
 
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
    return rows + sql.testvar

@app.route("/add-song")
def add_song():
    args = {x:y for x,y in request.args}
    sql.addSong(args['name'])
    return ''

@app.route("/get-songs")
def get_songs():
    return sql.getSongs()

@app.route("/drop-songs")
def drop_songs():
    return sql.dropTable()


class SQL:
    def __init__(self):
        self.conn = psycopg2.connect(
            host=os.environ['DB_HOST'],
            database=os.environ['DB_DATABASE'],
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASSWORD'])
        self.cur = self.conn.cursor()
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS songs (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL
        );
        """)
        
    def addSong(self, name):
        self.cur.execute(f"""
            INSERT into songs (name)
            VALUES (
                '{name}'
            )
        """)
        self.conn.commit()
    
    def getSongs(self):
        self.cur.execute(f"""
            SELECT * from songs
        """)
        retList = []
        for s in self.cur.fetchall():
            retList.append({
                'id': s[0],
                'name': s[1]
            })
        return retList

    def dropTable(self):
        self.cur.execute(f"""
            DROP TABLE IF EXISTS songs
        """)
        self.conn.commit()

sql = SQL()


