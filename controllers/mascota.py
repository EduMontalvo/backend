from base_de_datos import conexion
from models.mascota import MascotaModel
from flask_restful import Resource, request
from dtos.mascota import MascotaRequestDto


class MascotasController(Resource):
    def post(self): #Se crea un metodo post que maneja una solicitud POST
        body = request.get_json()   # Se hace un request ó una peticion y los devuelve en formato JSON
        dto = MascotaRequestDto()   # Se llama a MascotaRequestDto de dtos/mascotas.py, en esa consulta llama a models/mascota.py y la guarda para poder acceder a sus metodos y propiedades definidas , algo asi como que coje el formato 

        try:
            dataValidada = dto.load(body) # Con el metodo load: se encarga de cargar y validar los datos de body en este caso la respuesta a la peticion que se almacena en body.Esto quiere decir que los datos se asignan a los campos correspondientes y se procede a verificar, y esto se almacenara en dataValidada que contendran los datos validados y listos para ser utilizados.
            nuevaMascota = MascotaModel(**dataValidada) # Se utiliza el operador ** para desempaquetar los elementos del diccionario dataValida , clave:valor.Esto significa que los valores del diccionario dataValidada se asignarán a los atributos correspondientes de la instancia de MascotaModel.
            conexion.session.add(nuevaMascota) # En SQLAlchemy, una sesión se utiliza para realizar operaciones de inserción, actualización y eliminación en la base de datos. Al llamar al método add de la sesión y pasarle la instancia nuevaMascota, se agrega la instancia a la sesión para que se realicen las operaciones de inserción correspondientes en la base de datos.
            conexion.session.commit()   # En SQLAlchemy, una transacción es un conjunto de operaciones de base de datos que se agrupan y se confirman o se deshacen en conjunto. Al llamar al método commit en la sesión, se confirman todas las operaciones realizadas en la sesión, lo que significa que se guardan los cambios en la base de datos.

            return {
                'message': 'Mascota creada exitosamente'
            }, 201
        except Exception as e:
            return {
                'message': 'Error al crear la mascota',
                'content': e.args
            }, 400