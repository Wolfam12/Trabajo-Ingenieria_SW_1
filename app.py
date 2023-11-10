from flask import Flask, render_template, request, redirect, url_for, session
import os
import sqlite3
import random

app = Flask(__name__)
app.secret_key = os.urandom(24)

users = {'wolfam': '123', 'raz': '1234'}  # Almacena los nombres de usuario y contraseñas en un diccionario (en la vida real, usarías una base de datos)

# Conexión a la base de datos SQLite
def conectar_bd():
    conn = sqlite3.connect('Bdd\BasesDatosRegistraduria.db')
    return conn

def conectar_bd1():
    conn = sqlite3.connect('Bdd\BasesDatosRegistraduria.db')
    return conn
@app.route('/')
def home():
    if 'username' in session:
        # Recupera los datos de la base de datos
        connection = conectar_bd()
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM Personass')
        datos = cursor.fetchall()
        connection.close()

        return render_template('home.html', datos=datos)  # Pasa los datos a la plantilla
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return 'Credenciales incorrectas. Inténtalo de nuevo.'
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))
@app.route('/mostrar_datos')
def otra_pagina():
    if 'username' in session:
        # Recupera los datos de la base de datos
         

        numero_aleatorio = random.randint(1, 30)
        frase = "SELECT * FROM Personass where id = "
        frase_concatenada = frase + " " + str(numero_aleatorio)
        frease1 = "INSERT INTO Reporte (Nombres, Apellidos, Identificacion, FechaNacimiento, LugarNacimiento, FechaExpedicion, LugarExpedicion, RH, Estatura, Estado) SELECT Nombres, Apellidos, Identificacion, FechaNacimiento, LugarNacimiento, FechaExpedicion, LugarExpedicion, RH, Estatura, Estado FROM Personass WHERE ID = "
        frase_concatenada1 = frease1 + " " + str(numero_aleatorio)
   

        connection = conectar_bd()
        cursor = connection.cursor()
       
        cursor.execute(frase_concatenada1)
        connection.commit()
        cursor.execute(frase_concatenada)
        datos = cursor.fetchall()
        connection.close()

        
         

        return render_template('mostrar_datos.html', datos=datos)  # Pasa los datos a la plantilla
    return render_template('login.html')
@app.route('/reportes')
def reportes():
    if 'username' in session:
        # Recupera los datos de la base de datos
         


        connection = conectar_bd()
        cursor = connection.cursor()
        cursor.execute("select * from Reporte")
       
        datos = cursor.fetchall()
        connection.close()

        
         

        return render_template('reportes.html', datos=datos)  # Pasa los datos a la plantilla
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
