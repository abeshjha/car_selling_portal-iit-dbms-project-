from asyncio.windows_events import NULL
from flask import Flask, render_template,request,redirect
import psycopg2
import os


#def get_db_connection():
#    con=psycopg2.connect(
#        host="localhost",
#        database="ecom",
#        user="postgres",
#        password="neerajdb"
#    )
#    return con 


app = Flask(__name__,template_folder='FRONT_END')

@app.route("/")
def homepage():
    return render_template('index.html')


@app.route("/login")
def login():
    return render_template('login.html')

# @app.route("/signup")
# def signup():
#     s=NULL
#     return render_template('signup.html',mssg=s)

@app.route("/login_handle", methods=['GET', 'POST'])
def login_handle():
    if request.method=='POST':
        uname = request.form['Username']
        password = request.form['Password']
        option = request.form['chk1']
        print(uname,password,option)
        con= get_db_connection()
        cur=con.cursor()
        q='select * from profile where uname= %s and pword=%s and type=%s;'# Note: no quotes
        data = (uname,password,option, )
        cur.execute(q, data)
        drivers=cur.fetchall()
        n=len(drivers)
        if(n==1 and option=='seller'):
            return redirect("/seller_homepage")
        elif (n==1 and option=='customer'):
            return redirect("/customer_homepage")
        elif(n==0):
            s='incorrect details'
            return render_template('login.html',mssg=s)

if (__name__== "__main__"):
    app.run(debug=True)
    
