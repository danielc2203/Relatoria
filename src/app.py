from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required

from config import config

# Modelos
from models.ModelUser import ModelUser

# Entidades
from models.entities.User import User

# Creamos la Aplicación
app = Flask(__name__)

csrf=CSRFProtect()

#Variable de la Base de Datos
db = MySQL(app)
login_manager_app=LoginManager(app)

@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)

# Ruta Raiz que nos redirige al login
@app.route('/')
def index():
    return redirect(url_for('login'))

#Creamos una ruta para ver contenido
@app.route('/login', methods=['GET', 'POST'])
def login(): # Defino el nombre de una vista
    if request.method == 'POST':
        #print(request.form['username'])
        #print(request.form['password'])
        user = User(0, request.form['username'], request.form['password'])
        logged_user = ModelUser.login(db, user)
        if logged_user != None:
            if logged_user.password:
                login_user(logged_user)
                return redirect(url_for('home'))
            else:
                flash("Password Incorrecto...")
                return render_template('auth/login.html')
                
        else:
            flash("Usuario no encontrado...")
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html') # Retornamos la ruta a llamar

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))
    
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/protected')
@login_required
def protected():
    return "<h1>Estas en un area para solo administradores</h1>"

def status_401(error):
    return redirect(url_for('login'))

def status_404(error):
    return "<h1>Esta pagina no existe ... </h1>", 404
               

if __name__=='__main__':
    # Linea para poder utilizar la configuración de config
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run()