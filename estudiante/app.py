from flask import Flask, request, jsonify
from models import db, Estudiante
import os

app = Flask(__name__)

# Configurar la base de datos desde la variable de entorno
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://admin:admin@localhost:5432/microservicios')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar la base de datos
db.init_app(app)

# Crear las tablas al iniciar la app (solo una vez)
with app.app_context():
    db.create_all()

@app.route('/estudiantes', methods=['POST'])
def agregar_estudiante():
    data = request.get_json()
    rut = data['rut']
    if Estudiante.query.get(rut):
        return jsonify({'mensaje': 'El estudiante ya existe'}), 400

    nuevo = Estudiante(
        rut=data['rut'],
        nombre=data['nombre'],
        edad=data['edad'],
        curso=data['curso']
    )
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({'mensaje': 'Estudiante agregado exitosamente'}), 201

@app.route('/estudiantes', methods=['GET'])
def obtener_todos():
    estudiantes = Estudiante.query.all()
    return jsonify([e.to_dict() for e in estudiantes])

@app.route('/estudiantes/<rut>', methods=['GET'])
def obtener_estudiante(rut):
    estudiante = Estudiante.query.get(rut)
    if estudiante:
        return jsonify(estudiante.to_dict())
    return jsonify({'mensaje': 'Estudiante no encontrado'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
