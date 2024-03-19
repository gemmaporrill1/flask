from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hellos!</p>"


@app.route("/about")
def about_page():
    return "<h1>About Page</h1>"
