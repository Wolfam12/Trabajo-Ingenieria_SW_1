from flask import Flask, render_template, request, redirect, url_for, session
import os
import sqlite3

app = Flask(__name__)
app.secret_key = os.urandom(24)

users = {'wolfam': '123', 'raz': '1234'}  # Almacena los nombres de usuario y contraseñas en un diccionario (en la vida real, usarías una base de datos)

# Conexión a la base de datos SQLite
def conectar_bd():
    conn = sqlite3.connect('Bdd\BasesDatosRegistraduria.db')
    return conn

@app.route('/')
def home():
    if 'username' in session:
        # Recupera los datos de la base de datos
        connection = conectar_bd()
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM Personas')
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
        # Conecta a la base de datos
        connection = sqlite3.connect('BasesDatosRegistraduria.db')
        cursor = connection.cursor()

        # Ejecuta una consulta SQL para obtener los datos
        cursor.execute('SELECT * FROM Personas')
        datos = cursor.fetchall()

        # Cierra la conexión a la base de datos
        connection.close()

        return render_template('mostrar_datos.html', datos=datos)
   

if __name__ == '__main__':
    app.run(debug=True)
