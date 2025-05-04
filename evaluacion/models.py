from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Evaluacion(db.Model):
    __tablename__ = 'evaluaciones'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rut = db.Column(db.String, nullable=False)
    asignatura = db.Column(db.String, nullable=False)
    nota = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "rut": self.rut,
            "asignatura": self.asignatura,
            "nota": self.nota
        }
