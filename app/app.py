from flask import Flask, jsonify

from boto.s3.connection import S3Connection
import os

import psycopg2

#import sql
 
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
        user=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD'])
    return print(conn)
