import flask

from flask import Flask

import logging

logging.basicConfig(level=logging.DEBUG)

app = flask.Flask(__name__)

@app.route('/')
def main():
    return 'Hello'

if __name__ == "__main__":
    app.run()
