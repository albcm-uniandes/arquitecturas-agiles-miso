from flask import request
from ..modelos import db, Accion, AccionSchema, Usuario, UsuarioSchema
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, create_access_token,get_jwt_identity
accion_schema = AccionSchema()
usuario_schema = UsuarioSchema()
ACTUALIZAR = 'actualizar'
CONSULTAR = 'consultar'
class VistaLogIn(Resource):
    def post(self):
        usuario = Usuario.query.filter(Usuario.nombre == request.json["nombre"], Usuario.contrasena == request.json["contrasena"]).first()
        db.session.commit()
        if usuario is None:
            return "El usuario no existe", 404
        else:
            token_de_acceso = create_access_token(identity = usuario.id)
            return {"mensaje":"Inicio de sesión exitoso", "token": token_de_acceso}

class VistaAccion(Resource):

    @jwt_required()
    def put(self):
        usuario = get_jwt_identity()
        #usuario = Usuario.query.filter_by(id=current_user.id).first_or_404()
        if usuario is None:
            return "El usuario no existe", 404
        else:
            accion = usuario.acciones.filter_by(accion=ACTUALIZAR).first_or_404()
            if accion is None:
                return "El usuario no posee permisos para esta acción", 403
            else:
                return "El usuario posee permisos para esta acción", 200

    @jwt_required()
    def get(self):
        usuario = get_jwt_identity()
        #usuario = Usuario.query.filter_by(id=id_usuario).first_or_404()
        if usuario is None:
            return "El usuario no existe", 404
        else:
            accion = usuario.acciones.filter_by(accion=CONSULTAR).first_or_404()
            if accion is None:
                return "El usuario no posee permisos para esta acción", 403
            else:
                return "El usuario posee permisos para esta acción", 200
