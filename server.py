import flask

from flask import Flask

from waitress import serve

import logging

logging.basicConfig(level=logging.DEBUG)

app = flask.Flask(__name__)

@app.route('/')
def main():
    return 'Hello'

if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=8080)
