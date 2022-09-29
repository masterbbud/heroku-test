from flask import Flask, jsonify

import sql
 
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
    return sql.s3
    