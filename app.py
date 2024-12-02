from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///alumnos.db'
db = SQLAlchemy(app)

# Modelo de la base de datos
class Alumno(db.Model):
    numero_de_cuenta = db.Column(db.String(20), primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    grupo = db.Column(db.String(10), nullable=False)
    grado = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Alumno {self.nombre}>'

@app.route('/')
def index():
    alumnos = Alumno.query.all()
    return render_template('index.html', alumnos=alumnos)

@app.route('/agregar', methods=['POST'])
def agregar():
    if request.method == 'POST':
        numero_de_cuenta = request.form['numero_de_cuenta']
        nombre = request.form['nombre']
        grupo = request.form['grupo']
        grado = request.form['grado']
        email = request.form['email']
        
        nuevo_alumno = Alumno(
            numero_de_cuenta=numero_de_cuenta, 
            nombre=nombre, 
            grupo=grupo, 
            grado=grado, 
            email=email
        )
        db.session.add(nuevo_alumno)
        db.session.commit()
        return redirect(url_for('index'))

@app.route('/eliminar/<numero_de_cuenta>', methods=['POST'])
def eliminar(numero_de_cuenta):
    alumno = Alumno.query.get(numero_de_cuenta)
    if alumno:
        db.session.delete(alumno)
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  
    app.run(debug=True)
