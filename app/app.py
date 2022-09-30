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

@app.route("/get-songs")
def get_songs():
    return sql.select('songs')

@app.route("/get-accounts")
def get_accounts():
    return sql.select('accounts')

@app.route("/create-songs")
def create_songs():
    sql.createTable('songs')
    return 'Created Songs'

@app.route("/create-accounts")
def create_accounts():
    sql.createTable('accounts')
    return 'Created Accounts'

@app.route("/create-posts")
def create_posts():
    sql.createTable('posts')
    return 'Created Posts'

@app.route("/create-friends")
def create_friends():
    sql.createTable('friends')
    return 'Created Friends'

@app.route("/remove-songs")
def remove_songs():
    sql.dropTable('songs')
    return 'Removed Songs'

@app.route("/remove-accounts")
def remove_accounts():
    sql.dropTable('accounts')
    return 'Removed Accounts'
    
@app.route("/remove-posts")
def remove_posts():
    sql.dropTable('posts')
    return 'Removed Posts'

@app.route("/remove-friends")
def remove_friends():
    sql.dropTable('friends')
    return 'Removed Friends'

@app.route("/login", methods=['POST'])
def login():
    return accounts.login()

@app.route("/signup", methods=['POST'])
def signup():
    return accounts.signup()

@app.route("/account-data", methods=['POST'])
def account_data():
    return accounts.account_data()
