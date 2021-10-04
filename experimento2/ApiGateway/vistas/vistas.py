from flask import request
from flask_restful import Resource
import requests
import json

class VistaLogIn(Resource):
    def post(self):  
        content = requests.post(
            "http://192.168.1.11:5001/login",
            json=request.json
        )  

        if content.status_code != 200:
            return "El usuario no existe", content.status_code
        else:
            respuesta = content.json()
            return {"mensaje":"Inicio de sesión exitoso", "token": respuesta["token"]}

class VistaAccionConsultar(Resource):
    
    def get(self, paciente_id):
        
        headers = {'Authorization': f"Bearer {request.headers['Authorization']}"}

        respuestaPermisosConsultar = requests.get(
            "http://192.168.1.11:5001/consultar",
            headers=headers
        )

        if respuestaPermisosConsultar.status_code != 200:
            return "El usuario no posee permisos para esta acción", 403

        respuestaConsulta = requests.get(
            f"http://192.168.1.11:5002/citas_medicas/{paciente_id}"
        )

        if respuestaConsulta.status_code == 200:
            return respuestaConsulta.json(), 200
        else:
            return "No pudo consultar las citas médicas", respuestaConsulta.status_code   

class VistaAccionActualizar(Resource):
    
    def put(self, paciente_id):
        
        headers = {'Authorization': f"Bearer {request.headers['Authorization']}"}

        respuestaPermisosActualizacion = requests.put(
            "http://192.168.1.11:5001/actualizar",
            headers=headers
        )

        if respuestaPermisosActualizacion.status_code != 200:
            return "El usuario no posee permisos para esta acción", 403

        respuestaActualizacion = requests.put(
            f"http://192.168.1.11:5002/paciente/{paciente_id}",
            json=request.json
        )

        if respuestaActualizacion.status_code == 200:
            return respuestaActualizacion.json(), 200
        else:
            return "No pudo actualizar la información del paciente", respuestaActualizacion.status_code              
