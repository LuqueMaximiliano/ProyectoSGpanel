# models.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=False)
    username = db.Column(db.String(150), nullable=False, unique=True)
    cedula = db.Column(db.String(20), nullable=False, unique=True)
    birth_date = db.Column(db.Date, nullable=False)
    role = db.Column(db.String(20), nullable=False)
    profile_picture = db.Column(db.String(100), nullable=True)
    password_hash = db.Column(db.String(100), nullable=False)
    cartas_leidas = db.Column(db.Integer, default=0)
    cartas_recibidas = db.Column(db.Integer, default=0)
    linea_amarilla = db.Column(db.Integer, default=0)
    linea_azul = db.Column(db.Integer, default=0)
    videollamadas = db.Column(db.Integer, default=0)
    notas_voz_recibidas = db.Column(db.Integer, default=0)
    notas_voz_enviadas = db.Column(db.Integer, default=0)
    regalo_virtual = db.Column(db.Integer, default=0)
    presente = db.Column(db.Integer, default=0)
    video_perfil = db.Column(db.Integer, default=0)
    adjunto_visto = db.Column(db.Integer, default=0)
    comision = db.Column(db.Float, default=0.0)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
