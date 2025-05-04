from flask import Flask, request, jsonify
from models import db, Evaluacion
import os
import requests

app = Flask(__name__)

# Configurar conexión a la base de datos desde variable de entorno
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://admin:admin@localhost:5432/microservicios')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar base de datos
db.init_app(app)

# Crear las tablas al iniciar la app
with app.app_context():
    db.create_all()

@app.route('/evaluaciones', methods=['POST'])
def agregar_evaluacion():
    data = request.get_json()
    rut = data['rut']

    # Verificar si el estudiante existe usando el microservicio estudiante
    try:
        respuesta = requests.get(f"http://estudiante:5000/estudiantes/{rut}")
        if respuesta.status_code != 200:
            return jsonify({'mensaje': 'Estudiante no encontrado. No se puede agregar la evaluación.'}), 400
    except Exception as e:
        return jsonify({'mensaje': f'Error al verificar el estudiante: {str(e)}'}), 500

    # Crear evaluación si el estudiante existe
    nueva_eval = Evaluacion(
        rut=rut,
        asignatura=data['asignatura'],
        nota=data['nota']
    )
    db.session.add(nueva_eval)
    db.session.commit()
    return jsonify({'mensaje': 'Evaluación agregada exitosamente'}), 201

@app.route('/evaluaciones', methods=['GET'])
def obtener_todas():
    evaluaciones = Evaluacion.query.all()
    return jsonify([e.to_dict() for e in evaluaciones])

@app.route('/evaluaciones/<rut>', methods=['GET'])
def obtener_por_rut(rut):
    evaluaciones = Evaluacion.query.filter_by(rut=rut).all()
    if evaluaciones:
        return jsonify([e.to_dict() for e in evaluaciones])
    return jsonify({'mensaje': 'No se encontraron evaluaciones para este estudiante'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
