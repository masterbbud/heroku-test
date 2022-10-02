import os
import secrets

from flask import Flask, request
from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.secret_key = os.environ['SECRET_KEY']

tableCols = {
    'accounts': {'id': 'SERIAL', 'username': 'TEXT NOT NULL', 'password': 'TEXT NOT NULL', 'auth': 'TEXT NOT NULL'},
    'songs': {'id': 'SERIAL', 'title': 'TEXT NOT NULL', 'artist': 'TEXT', 'image': 'TEXT', 'spotify': 'TEXT', 'itunes': 'TEXT', 'youtube': 'TEXT', 'tidal': 'TEXT', 'amazonMusic': 'TEXT', 'soundcloud': 'TEXT', 'youtubeMusic': 'TEXT'},
    'posts': {'id': 'SERIAL', 'userid': 'INTEGER', 'dt': 'TIMESTAMP', 'songid': 'INTEGER', 'caption': 'TEXT', 'likes': 'INTEGER'},
    #'friends': {'id': 'SERIAL', 'user': 'INTEGER', 'following': 'INTEGER'}
    'friends': {'id': 'SERIAL', 'userid': 'INTEGER', 'following': 'INTEGER'},
    'blocked': {'id': 'SERIAL', 'userid': 'INTEGER', 'blocked': 'INTEGER'}
}

import app.sql as sqlClass

sql = sqlClass.SQL()
sqlClass.tables = tableCols

import app.accounts as accounts

accounts.sql = sql
accounts.bcrypt = Bcrypt(app)

import app.songs as songs

songs.sql = sql

import app.posts as posts

posts.sql = sql

import app.tables as tables

tables.sql = sql

import app.utils as utils

utils.sql = sql

@app.route("/create-table", methods=['POST'])
def create_table(): return tables.create_table()

@app.route("/drop-table", methods=['POST'])
def drop_table(): return tables.drop_table()

@app.route("/get-table", methods=['POST'])
def get_table(): return tables.get_table()

@app.route("/get-song", methods=['POST'])
def get_song(): return songs.get_song_request()

@app.route("/add-song", methods=['POST'])
def add_song(): return songs.add_song_request()

@app.route("/create-post", methods=['POST'])
def create_post(): return posts.create_post()

@app.route("/follow", methods=['POST'])
def follow(): return accounts.follow_request()

@app.route("/unfollow", methods=['POST'])
def unfollow(): return accounts.unfollow_request()

@app.route("/block", methods=['POST'])
def block(): return accounts.block_request()

@app.route("/get-posts", methods=['POST'])
def get_posts(): return posts.get_posts()

@app.route("/login", methods=['POST'])
def login(): return accounts.login()

@app.route("/signup", methods=['POST'])
def signup(): return accounts.signup()

@app.route("/account-data", methods=['POST'])
def account_data(): return accounts.account_data()
