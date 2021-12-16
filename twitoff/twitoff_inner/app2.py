from flask import Flask

app2 = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello World!"