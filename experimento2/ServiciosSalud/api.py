from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////mnt/salud.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)

class CitaMedica(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer)
    id_paciente = db.Column(db.Integer)
    dia = db.Column(db.String(10))
    hora = db.Column(db.String(5))
    medico = db.Column(db.String(100))
    cerrada = db.Column(db.Boolean, default=False)
    
class Paciente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    apellido = db.Column(db.String(100))
    tipo_identificacion = db.Column(db.Integer)
    numero_identificacion = db.Column(db.String(100))
    direccion = db.Column(db.String(255))
    telefono = db.Column(db.String(100))
    email = db.Column(db.String(255))

class CitaMedicaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        fields = ("id_paciente", "dia", "hora", "medico", "especialidad", "cerrada")

class PacienteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        fields = ("id", "nombre", "apellido", "tipo_identificacion", "numero_identificacion", "direccion", "telefono", "email")

citas_medicas_schema = CitaMedicaSchema(many=True)
paciente_schema = PacienteSchema()

class CitasMedicasResource(Resource):

    def get(self, usuario_id, paciente_id):
        citas_medicas = CitaMedica.query.filter(CitaMedica.id_usuario == usuario_id, CitaMedica.id_paciente == paciente_id)
        return citas_medicas_schema.dump(citas_medicas)

class PacienteResource(Resource):

    def get(self, paciente_id):
        return paciente_schema.dump(Paciente.query.get_or_404(paciente_id))

    def put(self, paciente_id):
        paciente = Paciente.query.get_or_404(paciente_id)
        if 'nombre' in request.json:
            paciente.nombre = request.json['nombre']
        if 'apellido' in request.json:
            paciente.apellido = request.json['apellido']
        if 'direccion' in request.json:
            paciente.direccion = request.json['direccion']
        if 'telefono' in request.json:
            paciente.telefono = request.json['telefono']
        if 'email' in request.json:
            paciente.email = request.json['email']
        db.session.commit()
        return paciente_schema.dump(paciente)

class DatosPrueba:

    @staticmethod
    def cargarDatosPrueba():
      citas_medicas = CitaMedica.query.all()
      n_citas_medicas = len(citas_medicas)
      
      pacientes = Paciente.query.all()
      n_pacientes = len(pacientes)
      
      if n_citas_medicas == 0:
          with open("MOCK_DATA_citas.json") as file1:
             data_citas = json.loads(file1.read())
          
          i = 1
          for cita in data_citas:
              nueva_cita = CitaMedica(
                  id_usuario=cita['id_usuario'],
                  id_paciente=cita['id_paciente'],
                  dia=cita['dia'],
                  hora=cita['hora'],
                  medico=cita['medico'],
                  cerrada=i%2==0,
              )
              db.session.add(nueva_cita)
              i = i + 1
          db.session.commit()        
            
      if n_pacientes == 0:
          with open("MOCK_DATA_pacientes.json") as file2:
              data_pacientes = json.loads(file2.read())
          
          for paciente in data_pacientes:
              nuevo_paciente = Paciente(
                  nombre=paciente['nombre'],
                  apellido=paciente['apellido'],
                  tipo_identificacion=paciente['tipo_identificacion'],
                  numero_identificacion=paciente['numero_identificacion'],
                  direccion=paciente['direccion'],
                  telefono=paciente['telefono'],
                  email=paciente['email'],
              )
              db.session.add(nuevo_paciente)
          db.session.commit()

api.add_resource(CitasMedicasResource, '/citas_medicas/<int:usuario_id>/<int:paciente_id>')
api.add_resource(PacienteResource, '/paciente/<int:paciente_id>')

if __name__ == '__main__':
    db.create_all()
    _ = DatosPrueba()
    _.cargarDatosPrueba()
    app.run(debug=True, host='0.0.0.0', ssl_context='adhoc')
