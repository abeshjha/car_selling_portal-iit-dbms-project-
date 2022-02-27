from asyncio.windows_events import NULL
from flask import Flask, render_template,request,redirect
import psycopg2
import os

#set FLASK_ENV=development
#psql --host=john.db.elephantsql.com --port=5432 --username=oxcbzzsv  --password --dbname=oxcbzzsv
#G0UGzkGcZ6X8OH_di8lpyT8REJ3nl6Qv

def get_db_connection():
    con=psycopg2.connect(
        host="john.db.elephantsql.com",
        database="oxcbzzsv",
        user="oxcbzzsv",
        password="G0UGzkGcZ6X8OH_di8lpyT8REJ3nl6Qv"
    )
    return con

app = Flask(__name__,template_folder='FRONT_END')

@app.route("/")
def homepage():
    advertisement_query = "select * from advertisements ORDER BY random() LIMIT 3"
    brand_query = "select * from brand ORDER BY random() LIMIT 3"
    model_query = "select * from model ORDER BY random() LIMIT 3"
    con= get_db_connection()
    cursor=con.cursor()

    cursor.execute(advertisement_query)
    advertisements = cursor.fetchall()

    cursor.execute(brand_query)
    brands = cursor.fetchall()
    
    cursor.execute(model_query)
    models = cursor.fetchall()
    
    print(models)
    print(brands)
    return render_template('index.html',advertisements=advertisements,models=models,brands=brands)

@app.route("/models")
def models():
    postgreSQL_select_Query = "select * from model"
    con= get_db_connection()
    cursor=con.cursor()
    cursor.execute(postgreSQL_select_Query)
    print("Selecting all models ")
    models = cursor.fetchall()

    print("Print each row and it's columns values")
    return render_template('models.html',models=models)

@app.route("/advertisement")
def advertisement():
    postgreSQL_select_Query = "select * from advertisements LIMIT 100"
    con= get_db_connection()
    cursor=con.cursor()
    cursor.execute(postgreSQL_select_Query)
    print("Selecting all brands ")
    items = cursor.fetchall()
    print("Print each row and it's columns values")
    return render_template('advertisement.html',items=items)

@app.route("/brands")
def brands():
    postgreSQL_select_Query = "select * from brand"
    con= get_db_connection()
    cursor=con.cursor()
    cursor.execute(postgreSQL_select_Query)
    print("Selecting all brands ")
    brands = cursor.fetchall()
    print("Print each row and it's columns values")
    return render_template('brands.html',brands=brands)

@app.route("/search/<string:name>")
def search(name):
    postgreSQL_select_Query = "select * from advertisements where brand_id IN (select brand_id from brand where brand_name LIKE '%{}%') ;".format(name.upper())
    print(postgreSQL_select_Query)
    con= get_db_connection()
    cursor=con.cursor()
    cursor.execute(postgreSQL_select_Query)
    items = cursor.fetchall()
    return render_template('search.html',items=items)

@app.route("/filter/<int:id>/<string:name>")
def filter(id,name):
    postgreSQL_select_Query = "select * from advertisements where {} = {};".format(name,id)
    print(postgreSQL_select_Query)
    con= get_db_connection()
    cursor=con.cursor()
    cursor.execute(postgreSQL_select_Query)
    items = cursor.fetchall()
    return render_template('search.html',items=items)

@app.route("/single/<int:id>")
def single(id):
    postgreSQL_select_Query = "select * from advertisements where ad_id = {};".format(id)
    con= get_db_connection()
    cursor=con.cursor()
    cursor.execute(postgreSQL_select_Query)
    ad = cursor.fetchall()
    print(ad)
    return render_template('single.html',ad=ad)
   

@app.route("/test")
def test():
    postgreSQL_select_Query = "select * from advertisements LIMIT 3"
    con= get_db_connection()
    cursor=con.cursor()
    cursor.execute(postgreSQL_select_Query)
    print("Selecting rows from mobile table using cursor.fetchall ")
    models = cursor.fetchall()
    print("Print each row and it's columns values")
    return render_template('test.html',models=models)
   
        
@app.route("/login")
def login():
    return render_template('login.html')


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
    
