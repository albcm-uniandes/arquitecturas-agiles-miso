from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields

db = SQLAlchemy()

usuario_accion = db.Table('usuario_accion',
    db.Column('usuario_id', db.Integer, db.ForeignKey('usuario.id'), primary_key = True),
    db.Column('accion_id', db.Integer, db.ForeignKey('accion.id'), primary_key = True))

class Accion(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    accion = db.Column(db.String(128))
    usuarios = db.relationship('Usuario', secondary = 'usuario_accion', back_populates="acciones",
    lazy='dynamic',
    passive_deletes=True)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    contrasena = db.Column(db.String(50))
    acciones = db.relationship('Accion', secondary = 'usuario_accion', back_populates="usuarios",
    lazy='dynamic',
   )

class AccionSchema(SQLAlchemyAutoSchema):
    class Meta:
         model = Accion
         include_relationships = True
         load_instance = True

class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
         model = Usuario
         include_relationships = True
         load_instance = True