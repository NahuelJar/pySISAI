from unittest import result
from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from notifypy import Notify

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    port = 3306,
    password = "",
    database = "bdpython"
)
myCursor = mydb.cursor()

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("contenido.html")

@app.route('/layout', methods = ["GET", "POST"])
def layout():
    session.clear()
    return render_template("contenido.html")

@app.route('/login', methods = ["GET","POST"])
def login():
    notificacion = Notify()

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        myCursor.execute("SELECT * FROM usuarios WHERE email=%s",(email,))
        user = myCursor.fetchone()
        myCursor.close()

        if len(user)>0:
            if password == user["password"]:
                session['firstname'] = user['firstname']
                session['email'] = user['email']

                if session['tipo'] == 1:
                    return render_template("")
                elif session['tipo'] == 2:
                    return render_template("")
            else:
                notificacion.title = "Error de Acceso"
                notificacion.message="Correo o contraseña no valida"
                notificacion.send()
                return render_template("login.html")
        else:
            notificacion.title = "Error de Acceso"
            notificacion.message="No existe el usuario"
            notificacion.send()
            return render_template("login.html")
    else:
        return render_template("login.html")

@app.route('/register', methods = ["GET","POST"])
def register():
    notificacion = Notify()
    if request.method == 'GET':
        return render_template("register.html")
    
    if request.method == 'POST':
        dni = request.form['dni']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        password = request.form['password']
        query = f"INSERT INTO usuarios (dni, firstname, lastname, email, password) VALUES ({dni},'{firstname}','{lastname}','{email}','{password}')"
        myCursor.execute(query)
        mydb.commit()
        return render_template("register.html")
    else:
        return render_template("register.html")

if __name__ == '__main__':
    app.run(debug=True)