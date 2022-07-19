
import random
import psycopg2
from flask import Flask, render_template,request,redirect,session

#psql --host=10.17.10.70 --port=5432 --username=group_33  --password --dbname=group_33
#pass--BuHnPs9GNsUfQ
#set FLASK_ENV=development
app = Flask(__name__,template_folder='FRONT_END')
app.secret_key = "rrfghhthtgtrs"
def get_db_connection():
    con=psycopg2.connect(
        host="john.db.elephantsql.com",
        database="oxcbzzsv",
        user="oxcbzzsv",
        password="G0UGzkGcZ6X8OH_di8lpyT8REJ3nl6Qv"
    )
    return con



@app.route("/login")
def login():
    
    return render_template('login.html')

@app.route("/logout")
def logout():
    session.clear()
    return render_template('login.html')

@app.route("/history")
def history():
    if (session.get("spid") == None):
        return redirect('/login')
    con= get_db_connection()
    cur=con.cursor()
    q='select sold_items.add_id,profile.fname,brand.brand_name,model.model_name,sold_items.sold_at from sold_items,advertisements,brand,model,profile where sold_items.pid_buyer=%s and sold_items.add_id=advertisements.ad_id and advertisements.model_id=model.model_id and advertisements.brand_id=brand.brand_id; '
    data2=(session['spid'],)
    cur.execute(q,data2)
    l2=cur.fetchall()
    
    con.commit()
    return render_template('history.html',lst2=l2)

@app.route("/my_requests")
def my_requests():
    if (session.get("spid") == None):
        return redirect('/login')
    con= get_db_connection()
    cur=con.cursor()
    p='select sellers_requests.ad_id,profile.fname,brand.brand_name,model.model_name,sellers_requests.counter_offer from sellers_requests,advertisements,brand,model,profile where sellers_requests.pid_buyer=%s and sellers_requests.ad_id=advertisements.ad_id and advertisements.model_id=model.model_id and advertisements.brand_id=brand.brand_id; '
    data1=(session['spid'],)
    cur.execute(p,data1)
    l1=cur.fetchall()
    con.commit()
    return render_template('myrequests.html',lst1=l1)

@app.route("/signup")
def signup():
    s='gg'
    return render_template('signup.html',mssg=s)

@app.route("/seller_dashboard")
def seller_dashboard():
    return render_template('seller.html')

@app.route("/ad_remove/<int:sno>", methods=['GET', 'POST'])
def ad_remove(sno):
    con= get_db_connection()
    cur=con.cursor()
    p='delete from advertisements where ad_id=%s;'
    q='delete from seller_ads where pid=%s and add_id=%s;'  
    data1=(sno,)
    data2=(session['spid'],sno,) 
    cur.execute(p,data1)
    cur.execute(q,data2)
    con.commit()
    return redirect('/seller_vehicles')

@app.route("/accept_offer/<int:sno>/<int:pno>/<int:dno>", methods=['GET', 'POST'])
def accept_offer(sno,pno,dno):
    con= get_db_connection()
    cur=con.cursor()
    p='INSERT into sold_items(pid_seller,pid_buyer,add_id,sold_at) values(%s,%s,%s,%s)'
    q='delete from sellers_requests where pid_seller=%s and ad_id=%s;' 
    data1=(session['spid'],pno,sno,dno)
    data2=(session['spid'],sno,) 
    cur.execute(p,data1)
    cur.execute(q,data2)
    con.commit()
    return redirect('/buyers')

@app.route("/reject_offer/<int:sno>", methods=['GET', 'POST'])
def reject_offer(sno):
    con= get_db_connection()
    cur=con.cursor()
    q='delete from sellers_requests where pid_seller=%s and ad_id=%s;'  
    data2=(session['spid'],sno,) 
    cur.execute(q,data2)
    con.commit()
    return redirect('/buyers')


@app.route("/seller_vehicles")
def seller_vehicles():
    con= get_db_connection()
    cur=con.cursor()
    p='select seller_ads.add_id,brand.brand_name,model.model_name,advertisements.mileage,advertisements.person_capacity,advertisements.catalog_url from seller_ads,advertisements,model,brand where seller_ads.pid=%s and seller_ads.add_id=advertisements.ad_id and advertisements.model_id=model.model_id and advertisements.brand_id=brand.brand_id;'   
    data=(session['spid'],)
    cur.execute(p,data)
    k=cur.fetchall()
    n=len(k)
    print(k)
    con.commit()
    return render_template('seller_vehicles.html',lst=k)


@app.route("/add_vehicle")
def add_vehicles():
    return render_template('add_vehicle.html')
@app.route("/buyers", methods=['GET', 'POST'])
def buyers():
    con= get_db_connection()
    cur=con.cursor()
    p='select sellers_requests.ad_id,profile.uname,brand.brand_name,model.model_name,sellers_requests.counter_offer,sellers_requests.pid_buyer from sellers_requests,model,brand,advertisements,profile where profile.pid=sellers_requests.pid_buyer and sellers_requests.pid_seller=%s and sellers_requests.ad_id=advertisements.ad_id and advertisements.model_id=model.model_id and advertisements.brand_id=brand.brand_id;'   
    data=(session['spid'],)
    cur.execute(p,data)
    k=cur.fetchall()
    n=len(k)
    print(n)
    for x in k:
        print(x)
    con.commit()
    return render_template('buyers.html',lst=k)
@app.route('/xyz')
def xyz():
    print("gg",session['spid'])
    return redirect('/login')
@app.route("/signup_handle", methods=['GET', 'POST'])
def signup_handle():
    if request.method=='POST':
        fname = request.form['fname']
        lname = request.form['lname']
        uname = request.form['uname']
        pas = request.form['password']
        rpas= request.form['rpassword']
        contact=request.form['contact']
        age=int(request.form['age'])
        address=request.form['address']
        option = request.form['chk1']
        print(fname,lname,uname,pas,rpas,contact,age,address,option)
        con= get_db_connection()
        cur=con.cursor()
        if(pas!=rpas):
            s='repeat password doesnot match'
            return render_template('signup.html',mssg=s)
        p='select * from profile'   
        # q='INSERT INTO profile (fname,lname,uname,pword,address,contact,age,type) VALUES ('neeraj','kumar','nkumar','12345','jaipur,rajasthan','8202021232',24,'seller');'
        q='INSERT INTO profile (fname,lname,uname,pword,address,contact,age,type) VALUES (%s,%s,%s,%s,%s,%s,%s,%s);'# Note: no quotes
        data = (fname,lname,uname,pas,address,contact,age,option,)
        cur.execute(q, data)
        con.commit()
        q='select pid from profile where uname=%s and pword=%s;'
        data=(uname,pas,)
        cur.execute(q, data)
        k=cur.fetchall()
        nn= len(k)
        print(nn)
        for x in k:
            session['spid']=x[0]
        print(session['spid'])
        if(option=='seller'):
            return redirect("/seller_dashboard")
        elif (option=='customer'):
            return redirect("/")

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
        k=cur.fetchall()
        n=len(k)
        print(n,option)
        if(n==1 and option=='seller'):
            session['spid']=k[0][0]
            return redirect("/seller_dashboard")
        elif (n==1 and option=='customer'):
            session['spid']=k[0][0]
            return redirect("/")
        else:
            s='incorrect details'
            return render_template('login.html',mssg=s)

@app.route("/add_vehicle_handle", methods=['GET', 'POST'])
def add_vehicle_handle():
    if request.method=='POST':
        production = request.form['production']
        mileage = request.form['mileage']
        person_capacity=request.form['person_capacity']
        region_id=request.form['region_id']
        num_pictures=request.form['num_pictures']
        pro_seller=request.form['pro_seller']
        adoldness=request.form['adoldness']
        postal_code=request.form['postal_code']
        clime_id=request.form['clime_id']
        shifter=request.form['shifter']
        doorsnumber=request.form['doorsnumber']
        documentvalid=request.form['documentvalid']
        postal_code=request.form['postal_code']
        color=request.form['color']
        brand_id=request.form['brand_id']
        model_id=request.form['model_id']
        ccm=request.form['ccm']
        catalog_url=request.form['catalog_url']
        category_id = request.form['category_id']
        start_production = request.form['start_production']
        end_production= request.form['end_production']
        msrp=request.form['msrp']
        car_type_id=request.form['car_type_id']
        weight=request.form['weight']
        fuel_tank=request.form['fuel_tank']
        boot_capacity=request.form['boot_capacity']
        fuel=request.form['fuel']
        environmental_id=request.form['environmental_id']
        cylinder_layout=request.form['cylinder_layout']
        cylinder=request.form['cylinder']
        drive_id=request.form['drive_id']
        clime_id=request.form['clime_id']
        consump_city=request.form['consump_city']
        consump_highway=request.form['consump_highway']
        consump_mixed=request.form['consump_mixed']
        top_speed=request.form['top_speed']
        acceleration=request.form['acceleration']
        torque=request.form['torque']
        power=request.form['power']
        con= get_db_connection()
        cur=con.cursor()  
        qn=random.randint(0,500000)
        q='INSERT INTO advertisements (ad_id,region_id,numpictures,proseller,adoldness,postalcode,production,mileage,clime_id,shifter,person_capacity,doorsnumber,documentvalid,color,brand_id,model_id,ccm,catalog_url) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'# Note: no quotes
        data = (qn,region_id,num_pictures,pro_seller,adoldness,postal_code,production,mileage,clime_id,shifter,person_capacity,doorsnumber,documentvalid,color,brand_id,model_id,ccm,catalog_url,)
        cur.execute(q, data)
        q='INSERT INTO catalogs (catalog_url,category_id,start_production,end_production,msrp,car_type_id,doorsnumber,person_capacity,weight,fuel_tank,boot_capacity,fuel,environmental_id,cylinder_layout,cylinders,drive_id,ccm,consump_city,consump_highway,consump_mixed,top_speed,acceleration,torque,power) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'# Note: no quotes
        data=(catalog_url,category_id,start_production,end_production,msrp,car_type_id,doorsnumber,person_capacity,weight,fuel_tank,boot_capacity,fuel,environmental_id,cylinder_layout,cylinder,drive_id,ccm,consump_city,consump_highway,consump_mixed,top_speed,acceleration,torque,power,)
        cur.execute(q, data)
        q='INSERT INTO seller_ads (pid,add_id) values(%s,%s);'
        print(session['spid'],qn)
        data=(session['spid'],qn,)
        cur.execute(q, data)
        con.commit()
        return redirect("/seller_vehicles")

# /////////////////////////

@app.route("/")
def homepage():
    advertisement_query = ("""WITH 
                            f1 as (SELECT  * from advertisements ORDER BY random() LIMIT 3),
                            f3 as (SELECT ad_id,ad_price,model_name,brand_name from brand,model,f1 where  f1.model_id = model.model_id 
                                    AND f1.brand_id = brand.brand_id )
                             SELECT * from f3;""")
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
    
    print(advertisements)
    name=None
    if (session.get("spid") != None):
        q= 'select fname from profile where pid=%s limit 1;'
        data = (session['spid'],)
        cursor.execute(q, data)
        j=cursor.fetchall()
        name=j[0][0]
        session['name']=name
    return render_template('index.html',advertisements=advertisements,models=models,brands=brands,name=name)


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
    postgreSQL_select_Query = ("""WITH 
                            f1 as (SELECT  * from advertisements ORDER BY random() LIMIT 100),
                            f3 as (SELECT ad_id,ad_price,model_name,brand_name from brand,model,f1 where  f1.model_id = model.model_id 
                                    AND f1.brand_id = brand.brand_id )
                             SELECT * from f3;""")
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
    postgreSQL_select_Query = ("""WITH 
                            f1 as (SELECT  * from advertisements where {} = {}),
                            f3 as (SELECT ad_id,ad_price,model_name,brand_name from brand,model,f1 where  f1.model_id = model.model_id 
                                    AND f1.brand_id = brand.brand_id )
                             SELECT * from f3;""").format(name,id)
    print(postgreSQL_select_Query)
    con= get_db_connection()
    cursor=con.cursor()
    cursor.execute(postgreSQL_select_Query)
    items = cursor.fetchall()
    return render_template('search.html',items=items)

@app.route("/single/<int:id>")
def single(id):
    if (session.get("spid") == None):
        return redirect('/login')
    print(session.get("spid"))
    print("spid")
    postgreSQL_select_Query = ("""WITH 
                            f1 as (SELECT  * from advertisements where ad_id = {}),
                            f2 as (SELECT ad_id,ad_price,model_name,brand_name,mileage,clime_name,gas_name,shifter,
                                    person_capacity ,doorsnumber ,documentvalid ,color ,upload_date,
                                    advertisement_url,catalog_url,download_date,sales_update_date,postalcode,
                                    region_name
                                    from brand,model,f1,clime,region,gas
                                    where  f1.model_id = model.model_id 
                                    AND f1.region_id = region.region_id
                                    AND f1.brand_id = brand.brand_id
                                    AND f1.gas_id = gas.gas_id
                                    AND f1.clime_id = clime.clime_id )
                             SELECT * from f2;""").format(id)
    con= get_db_connection()
    cursor=con.cursor()
    cursor.execute(postgreSQL_select_Query)
    ads = cursor.fetchall()
    print(ads)
    return render_template('single.html',ads=ads)
   

@app.route("/order/<int:id>/<int:price>")
def order(id,price):
    
    return render_template('order.html',price=price,id=id)

@app.route("/test")
def test():
    postgreSQL_select_Query = "update table gas set gas_name = 'disel' where gas_id = -1"
    con= get_db_connection()
    cursor=con.cursor()
    cursor.execute(postgreSQL_select_Query)
    con.commit()
    print("executed")

    return render_template('test.html')
   
        
@app.route("/confirm_payment", methods=['GET', 'POST'])
def confirm_payment():
    if request.method=='POST':
        ad_id = request.form.get('ad_id')
        price = request.form.get('price')
        con= get_db_connection()
        cur=con.cursor()
        q='select pid from seller_ads where add_id=%s limit 1;'# Note: no quotes
        data = (ad_id, )
        cur.execute(q, data)
        k=cur.fetchall()
        bid=random.randint(0,500000)
        for x in k:
            bid=x[0]
        q='INSERT into sellers_requests(pid_seller,pid_buyer,ad_id,counter_offer) values (%s,%s,%s,%s);'# Note: no quotes
        data = (bid,session['spid'],ad_id,price,)
        cur.execute(q, data)
        print(ad_id)
        print(price)
        print('helooooooo')
        con.commit()
        print('ggggg')
        return redirect('/') 


if (__name__== "__main__"):
    app.run(debug=True)
