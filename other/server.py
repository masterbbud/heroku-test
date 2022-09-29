import flask

from flask import Flask

import logging

logging.basicConfig(level=logging.DEBUG)

app = flask.Flask(__name__)

@app.route('/main')
def main():
    return 'Hello'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
