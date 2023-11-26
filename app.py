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
from werkzeug.security import check_password_hash


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        connection = conectar_bd()
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM Usuarios WHERE username=?', (username,))
        user = cursor.fetchone()
        connection.close()

        if user and check_password_hash(user[2], password):
            session['username'] = user[1]  # Cambié el índice para obtener el nombre de usuario
            return redirect(url_for('home'))
        else:
            return 'Credenciales incorrectas. Inténtalo de nuevo.'
    
    return render_template('login.html')

   
from werkzeug.security import generate_password_hash

@app.route('/register', methods=['GET', 'POST'])
def register():
     if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        identification = request.form['identification']
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        fuerza_publica = request.form['fuerza_publica']
        rango = request.form['rango']
        id_fuerza = request.form['id_fuerza']

        # Hash de la contraseña (usa funciones hash seguras en producción)
        hashed_password = generate_password_hash(password, method='sha256')

        connection = conectar_bd()
        cursor = connection.cursor()

        # Verifica si el usuario ya existe
        cursor.execute('SELECT * FROM Usuarios WHERE username=?', (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            return 'El nombre de usuario ya está en uso. Por favor, elige otro.'

        # Inserta el nuevo usuario en la base de datos con los nuevos campos
        cursor.execute('INSERT INTO Usuarios (username, password, email, identification, nombres, apellidos, fuerza_publica, rango, id_fuerza) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                       (username, hashed_password, email, identification, nombres, apellidos, fuerza_publica, rango, id_fuerza))
        connection.commit()
        connection.close()

        return redirect(url_for('login'))

     return render_template('register.html')
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

@app.route('/requeridos')
def requeridos():
    if 'username' in session:
        # Recupera los datos de la base de datos
         


        connection = conectar_bd()
        cursor = connection.cursor()
        cursor.execute("select * from Reporte where estado = 'Requerido'")
       
        datos = cursor.fetchall()
        connection.close()

        
         

        return render_template('requeridos.html', datos=datos)  # Pasa los datos a la plantilla
    return render_template('login.html')

@app.route('/norequeridos')
def norequeridos():
    if 'username' in session:
        # Recupera los datos de la base de datos
         


        connection = conectar_bd()
        cursor = connection.cursor()
        cursor.execute("select * from Reporte where estado = 'No Requerido'")
       
        datos = cursor.fetchall()
        connection.close()

        
         

        return render_template('norequeridos.html', datos=datos)  # Pasa los datos a la plantilla
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
