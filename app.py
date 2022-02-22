from flask import Flask
import psycopg2


conn = psycopg2.connect(
    host="localhost",
    database="suppliers",
    user="postgres",
    password="Abcd1234")

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p><center><h1>SECOND HAND CAR SELLING MARKETPLACE</h1></center></p>"