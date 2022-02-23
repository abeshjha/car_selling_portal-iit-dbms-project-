from flask import Flask, render_template
import psycopg2




app = Flask(__name__,template_folder='FRONT_END')

@app.route("/")
def homepage():
    return render_template('index.html')


@app.route("/login")
def login():
    return render_template('login.html')

    