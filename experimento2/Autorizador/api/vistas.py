from flask import request
from modelos import db, Accion, AccionSchema, Usuario, UsuarioSchema
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


class VistaAccionActualizar(Resource):
    @jwt_required()
    def put(self):
        id_usuario = get_jwt_identity()
        usuario = Usuario.query.filter(Usuario.id==id_usuario).first_or_404()
        if usuario is None:
            return "El usuario no existe", 404
        else:
            acciones = usuario.acciones.all()
            accion =Accion.query.filter(Accion.accion==ACTUALIZAR).first_or_404()
            if acciones is None or accion not in acciones:
                return "El usuario no posee permisos para esta acción", 403
            else:
                return "El usuario posee permisos para esta acción", 200

class VistaAccionConsultar(Resource):
    
    @jwt_required()
    def get(self):
        id_usuario = get_jwt_identity()
        usuario = Usuario.query.filter(Usuario.id==id_usuario).first_or_404()
        if usuario is None:
            return "El usuario no existe", 404
        else:
            acciones = usuario.acciones.all()
            accion =Accion.query.filter(Accion.accion==CONSULTAR).first_or_404()
            if acciones is None or accion not in acciones:
                return "El usuario no posee permisos para esta acción", 403
            else:
                return "El usuario posee permisos para esta acción", 200
