from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Estudiante(db.Model):
    __tablename__ = 'estudiantes'

    rut = db.Column(db.String, primary_key=True)
    nombre = db.Column(db.String, nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    curso = db.Column(db.String, nullable=False)

    def to_dict(self):
        return {
            "rut": self.rut,
            "nombre": self.nombre,
            "edad": self.edad,
            "curso": self.curso
        }
