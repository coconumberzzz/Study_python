#DB
#동적 uri
from flask import Flask, render_template,request
import pymysql

app=Flask(__name__)
app.debug=True

@app.route ("/login")
def login():
    return render_template("login.html")

@app.route("/login_up",methods=["POST","GET"])
def login_up():
    if request.method =="POST":
        email=request.form["email"]
        pw=request.form["pw"]

        db = pymysql.connect(host='127.0.0.1',
                port=3306,
                user='admin',
                passwd='0507',
                db='attendance',
                charset='utf8')

        cursor = db.cursor()
        query = "SELECT name FROM tutor_info WHERE email=%s AND pw=%s;"
        value =(email,pw)

        cursor.execute(query,value)
        data=(cursor.fetchall())

        cursor.close()
        db.close()

        for row in data:
            data=row[0]
        if data:
            return 'login success!!!!'
        else:
            return 'None Data!!!!!!!!!'

    else :
        email=request.args.get("email")
        pw=request.args.get("pw")
        return "login \n email is %s \n pw is %s"%(email, pw)