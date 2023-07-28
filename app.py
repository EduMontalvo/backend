from flask import Flask
#convierte caracteres especiales a un formato seguro
from urllib.parse import quote_plus
from base_de_datos import conexion
from models.usuario import UsuarioModel
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:%s@localhost:5432/directorio' % quote_plus("P@ssw0rd")

conexion.init_app(app)

Migrate(app=app,db=conexion)

#@app.route('/crear-tablas',methods = ['GET'])
#def crearTablas():
#    conexion.create_all()
#    return {
#        'message':'Creacion ejecutada'
#    }

if __name__ == '__main__':
    app.run(debug=True)