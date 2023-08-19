from flask import Flask
#convierte caracteres especiales a un formato seguro
from base_de_datos import conexion
from models.mascota import MascotaModel
from urllib.parse import quote_plus
from flask_migrate import Migrate
from flask_restful import Api
from controllers.usuario import UsuariosController,UsuarioController
from controllers.mascota import MascotasController
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint # * Agrega swagger a nuestro proyecto
from os import environ # ! importamos de os la environ para usar la variable de enterno
from dotenv import load_dotenv

#load_dotenv tiene que estar en la primera linea de nuestro archivo principal
#cargara las variables del archivo .env y podra ser utilizadas en todo el proyecto

load_dotenv()

app = Flask(__name__)
api = Api(app)
# * origins > indica los dominios que pueden acceder a mi API
CORS(app, origins = ['https://editor.swagger.io','http://mifrontend.com'], 
     methods = ['GET','POST', 'PUT', 'DELETE'], 
     #authorization: para cuestiones de autorizacion
     #content-type: ver la informacion que nos esta enviando el cliente
     #accept: ver que es lo que aceptara el cliente 
     allow_headers = ['authorization','content-type','accept'])

# * endpoint donde se podra acceder a la documentacion
SWAGGER_URL = '/docs' # ? Ejm : www.miweb.com/docs
# ! con esta ruto ahora se accedera de la sigte forma: http://127.0.0.1:5000/docs
#donde se almacena mi archivo de la documentacion 
API_URL = '/static/documentacion_swagger.json'

configuracionSwagger = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config = {
    # ?  el nombre de la pestaña del navegador
    'app_name':'Documentacion de Directorio de Mascotas'
})
# ? agrega otra aplicacion, que no sea Flask ,a nuestro proyecto Flask
app.register_blueprint(configuracionSwagger)

""" app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL') """

""" passwordBd = environ.get("DATABASE_URL").split(":")[2].split("@localhost")[0]
passwordConvertida = quote_plus(passwordBd)
urlBd = environ.get """

#? app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:%s@localhost:5432/directorio' % quote_plus("P@ssw0rd")

conexion.init_app(app)

Migrate(app=app,db=conexion)

#@app.route('/crear-tablas',methods = ['GET'])
#def crearTablas():
#    conexion.create_all()
#    return {
#        'message':'Creacion ejecutada'
#    }

# * Aca agregamos todas las rutas de nuestros controladores
api.add_resource(UsuariosController, '/usuarios')
api.add_resource(UsuarioController, '/usuario/<int:id>')
api.add_resource(MascotasController, '/mascotas')


if __name__ == '__main__':
    app.run(debug=True)