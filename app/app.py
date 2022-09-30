import os
import secrets

from flask import Flask, request
from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.secret_key = os.environ['SECRET_KEY']

tables = {
    'accounts': {'id': 'SERIAL', 'username': 'TEXT NOT NULL', 'password': 'TEXT NOT NULL', 'auth': 'TEXT NOT NULL'},
    'songs': {'id': 'SERIAL', 'title': 'TEXT NOT NULL', 'artist': 'TEXT', 'image': 'TEXT', 'spotify': 'TEXT', 'itunes': 'TEXT', 'youtube': 'TEXT', 'tidal': 'TEXT', 'amazonMusic': 'TEXT', 'soundcloud': 'TEXT', 'youtubeMusic': 'TEXT'},
    'posts': {'id': 'SERIAL', 'userid': 'INTEGER', 'datetime': 'TEXT', 'songid': 'INTEGER', 'caption': 'TEXT', 'likes': 'INTEGER'},
    'friends': {'id': 'SERIAL', 'user': 'INTEGER NOT NULL', 'following': 'INTEGER NOT NULL'}
}

import app.sql as sqlClass

sql = sqlClass.SQL()
sqlClass.tables = tables

import app.accounts as accounts

accounts.sql = sql
accounts.bcrypt = Bcrypt(app)

import app.songs as songs

songs.sql = sql

import app.posts as posts

posts.sql = sql

@app.route("/add-song", methods=['POST'])
def add_song():
    return songs.add_song_request()

@app.route("/create-post", methods=['POST'])
def create_post():
    return posts.create_post_request()

@app.route("/follow", methods=['POST'])
def follow():
    return accounts.follow_request()

@app.route("/get-posts", methods=['POST'])
def get_posts():
    return posts.get_posts_request()

@app.route("/create-table", methods=['POST'])
def create_table():
    args = request.json
    name = args.get('name')
    if not name:
        return 'ERROR: Request needs name'
    return sql.createTable(name)

@app.route("/drop-table", methods=['POST'])
def drop_table():
    args = request.json
    name = args.get('name')
    if not name:
        return 'ERROR: Request needs name'
    return sql.dropTable(name)

@app.route("/get-table", methods=['POST'])
def get_table():
    args = request.json
    name = args.get('name')
    if not name:
        return 'ERROR: Request needs name'
    return sql.select(name)

@app.route("/login", methods=['POST'])
def login():
    return accounts.login()

@app.route("/signup", methods=['POST'])
def signup():
    return accounts.signup()

@app.route("/account-data", methods=['POST'])
def account_data():
    return accounts.account_data()
