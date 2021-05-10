from flask import Flask,render_template,redirect,url_for,request,flash,session

import mysql.connector
import os
 
app=Flask(__name__)
app.secret_key=os.urandom(24)

conn=mysql.connector.connect(host="localhost",user="root",passwd="",database='flaskproject')
cursor=conn.cursor()

@app.route('/')
def login():
    return render_template("login.html")

@app.route('/register')
def about():
    return render_template("register.html")

@app.route('/addnewproduct')
def addnewproduct():
    return render_template("addnewproduct.html")

@app.route('/home')
def home():
    if 'user_id' in session:
        cursor.execute("SELECT * FROM products_list")
        productlist = cursor.fetchall()
        print(productlist)
        return render_template("home.html",data = productlist)
    else:
        return redirect('/')    

@app.route('/login_validation', methods=['POST'])
def login_validaion():
    email=request.form.get('email')
    password=request.form.get('password')

    cursor.execute("SELECT * FROM users WHERE email LIKE '{}' AND password LIKE '{}' ".format(email,password))
    users=cursor.fetchall()
    # print(users)
    if len(users)>0:
        session['user_id']=users[0][0]
        return redirect('/home')
    else:
        return redirect('/')   

@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.form.get('uname')
    email = request.form.get('uemail')
    password = request.form.get('upassword') 

    cursor.execute("INSERT INTO users(user_id,name,email,password) VALUES(NULL,'{}','{}','{}')".format(name,email,password))
    conn.commit()

    cursor.execute("SELECT * FROM users WHERE email LIKE '{}' ".format(email))
    myuser=cursor.fetchall()
    session['user_id']=myuser[0][0]
    return redirect('/home')

@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')




@app.route('/add_product', methods=['POST'])
def add_product():
    productname = request.form.get('productname')
    mfdate = request.form.get('mfdate')
    serialno = request.form.get('serialno') 

    cursor.execute("INSERT INTO products_list(product_id,productname,mfdate,serialno) VALUES(NULL,'{}','{}','{}')".format(productname,mfdate,serialno))
    conn.commit()

    # cursor.execute("SELECT * FROM users WHERE email LIKE '{}' ".format(email))
    # myuser=cursor.fetchall()
    # session['user_id']=myuser[0][0]
    return redirect('/home')

if __name__=="__main__":
    app.run(debug=True)