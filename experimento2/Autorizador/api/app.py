from flask import Flask
from flask_restful import Api
from .modelos import db
from .vistas import VistaLogIn,VistaAccion
from flask_jwt_extended import JWTManager
from flask_cors import CORS, cross_origin

def create_app(config_name):
    app = Flask(__name__)  
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///autorizador.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY']='albcm-uniandes'
    app.config['PROPAGATE_EXCEPTIONS'] = True
    return app
app = create_app('default')
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()
cors = CORS(app)
api = Api(app)
api.add_resource(VistaLogIn, '/logIn')
api.add_resource(VistaAccion, '/consultar')
api.add_resource(VistaAccion, '/actualizar')

jwt = JWTManager(app)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
