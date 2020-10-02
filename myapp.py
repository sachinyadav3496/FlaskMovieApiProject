#!/usr/bin/python3
import requests
from flask import Flask, redirect, render_template, url_for, request, session
import json
import smtplib,ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import socket
import pymysql as sql

app = Flask(__name__)
app.secret_key = "ouehrouhoehouoejndjnoji[o[pkpjoioijow[p12345678"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login/")
def login():
    if request.cookies.get("islogin"):
        return render_template("one.html")
    return render_template("login.html")

@app.route("/signup/")
def signup():
    return render_template("signup.html")

@app.route("/aftersignup/",methods=["POST","GET"])
def aftersignup():
    if request.method == "POST":
        firstname = request.form.get("fname")
        lastname = request.form.get("lname","Null")
        email = request.form.get("email")
        password = request.form.get("passwd")
        cpassword = request.form.get("cpasswd")
        gender = request.form.get("gender")  #request.form["gender"]
        if password == cpassword:
            try:
                db = sql.connect(host="localhost", port=3306, user="root",password="redhat",database="batch9am")
            except:
                return "\n Connectivity Issue......"
            else:
                cur = db.cursor()
                cmd = "select email from user where email='{}'".format(email)
                cur.execute(cmd)
                data = cur.fetchone()  #if theree is no such email then the query will return empty set and after fetching it will return None
                #if there is data then it will return me that data
                if data:
                    error = "Email already exist.....Enter new email"
                    return render_template("signup.html",error=error)
                else:
                    cmd = "insert into user values('{}','{}','{}',\
                            '{}','{}')".format(firstname, lastname, email, password, gender)
                    cur.execute(cmd)
                    db.commit()
                    return render_template("login.html")
                #return "login.html"
        else:
            error =  "Password does not match please try again....."
            return render_template("signup.html",error=error)
    else:
        return render_template("signup.html")

    
@app.route("/afterlogin/",methods=["GET","POST"])
def afterlogin():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("passwd")  #form data
        try:
            db = sql.connect(host="localhost",port=3306,user="root",password="redhat",database="batch9am")
        except Exception as e:
            return e
        else:
            cmd = "select * from user where email='{}'".format(email)
            cur = db.cursor()
            cur.execute(cmd)
            data = cur.fetchone()
            if data:
                #print(data)
                if password == data[3]:
                    #resp = make_response(render_template("one.html"))
                    #resp.set_cookie("email",email)
                    #resp.set_cookie("islogin","true")
                    #return resp
                    session["email"] = email
                    session["islogin"] = "true"
                    return render_template("afterlogin.html")
                    #return render_template("one.html")
                else:
                    error = "Invalid password!!!!!"
                    return render_template("login.html",error=error)
            else:
                #email does not exist
                error = "Invalid email"
                return render_template("login.html",error=error)
    else:
        return render_template("login.html")


@app.route("/logout/")
def logout():
    #resp = make_response(render_template("login.html"))
    #resp.delete_cookie("email")
    #resp.delete_cookie("islogin")
    del session["email"]
    del session["islogin"]
    #return resp
    return render_template("login.html")

#{"fname":"simran","lname":"grover","email":"simran@gmail.com","passwd":"adminadmin"}
#session and cookies, api
#project
#store password in encrypted form!!!!
#cookies and session is used to store data (user information)
# session --> for 2 mins and after every 2 mins session should be deleted and login
#page should be given to user
#if session.get("email"):
    #pass
#return
#passlib.hash 

@app.route("/getmovie/",methods=["GET","POST"])
def get_movie():
    if request.method == "POST":
        title = request.form.get("title")
        key = "e22bdd41"
        url = "http://www.omdbapi.com/?apikey={}&t={}".format(key, title)
        page = requests.get(url)
        if page.status_code == 200:
            data = json.loads(page.text)
            lists = ["Year","Released","Genre","Language","Actors","Plot","Awards","imdbRating"]
            d = {}
            for i in lists:
                d[i] = data[i]
            poster = data["Poster"]
            return render_template("showmovie.html",data=d,poster=poster)
        else:
            return render_template("afterlogin.html",error="Invalid Details")
    else:
        return redirect(url_for("login"))  #url_for(fun_name)
    

@app.route("/forgot_password/")
def forgot_password():
    from_email = "simrangrover5@gmail.com"
    to_email = "simrangrover5@gmail.com"
    password = "7742524047sima"

    message = MIMEMultipart("alternative")
    message["Subject"] = "Mail through Python script"
    message["To"] = to_email
    message["From"] = from_email

    html = """
    <label style='color:#123456;font-size:30px'>This is mail from your intelligent Student <i><b>Simran Grover</b></i></label><br>

    <a href='localhost/login/'>Link to google you can search anything there like your plots and dataset</a>

    <p style='color:red;font-style:italoc;font-family:sans serif;font-size:30px'>This is decorative email send</p>

    <img src = 'https://www.success.com/wp-content/uploads/legacy/sites/default/files/10_16.jpg'> 
    """

    m = MIMEText(html,"html")

    message.attach(m)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com",465,context=context) as server:
        server.login(from_email,password)
        server.sendmail(from_email,to_email,message.as_string())
    


#app.run()
