from flask import Flask,render_template,request,url_for,redirect,flash
from flask_mysqldb import  MySQL

app=Flask(__name__)

app.config["MYSQL_HOST"]= "localhost"
app.config["MYSQL_USER"]='root'
app.config["MYSQL_PASSWORD"]='root'
app.config["MYSQL_DB"]='automation_db'
app.config["MYSQL_DATABASE_PORT"]="3306"
app.config["MYSQL_CURSORCLASS"]='DictCursor'

mysql = MySQL(app)

@app.route("/")
@app.route("/home")
def homepage():
    con=mysql.connection.cursor()
    sql="Select * from users;"
    con.execute(sql)
    res=con.fetchall()
    return  render_template('home.html',datas=res)

@app.route("/addUsers",methods=['GET','POST'])
def addUsers():
    if request.method=='POST':
        name=request.form['name']
        city=request.form['city']
        age=request.form['age']
        con=mysql.connection.cursor()
        sql="insert into users(NAME,CITY,AGE) value(%s,%s,%s);"
        con.execute(sql,[name,city,age])
        mysql.connection.commit()
        con.close()
        flash("User Details Added")
        return redirect(url_for("homepage"))
    return render_template("addUsers.html")

@app.route('/editUser/<string:id>',methods=['GET','POST'])
def editUser(id):
    con=mysql.connection.cursor()
    if request.method=='POST':
        name=request.form['name']
        city=request.form['city']
        age=request.form['age']
        sql="update users set NAME=%s,CITY=%s,AGE=%s where ID=%s"
        con.execute(sql,[name,city,age,id])
        mysql.connection.commit()
        con.close()
        flash("User Details Updated")
        return redirect(url_for("homepage"))
        con=mysql.connection.cursor()

    sql="select * from users where ID=%s"
    con.execute(sql,[id])
    res=con.fetchone()
    return render_template("editUser.html",datas=res)

@app.route('/deleteUser/<string:id>',methods=['GET','POST'])
def deleteUser(id): 
    con=mysql.connection.cursor()
    sql="delete from users where ID=%s"
    con.execute(sql,[id])
    mysql.connection.commit()
    con.close()
    flash("User Details Deleted")
    return redirect(url_for("homepage"))

if (__name__ == '__main__'):
    app.secret_key='abc123'
    app.run(debug=True)