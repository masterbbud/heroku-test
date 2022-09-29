from flask import Flask
 
app = Flask(__name__)
 
@app.route("/")
def home_view():
    return "<h1>Welcome to Geeks for Geeks</h1>"

@app.route("/get-test")
def get_test():
    return "Get Response"