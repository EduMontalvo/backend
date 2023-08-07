from base_de_datos import conexion
from models.usuario import UsuarioModel
from flask_restful import Resource, request
from dtos.usuario import UsuarioRequestDTO
from marshmallow.exceptions import ValidationError
from sqlalchemy.exc import IntegrityError

class UsuariosController(Resource):
    #Cuando creamos un metodo con el mismo nombre que el metodo http si se llama a este metodo se ingresara al metodo de la clase
    #Es decir cuando hagamos la paticion desde el html con el metodo get se motrara el metodo get de la clase
    def get(self):
        #SELECT * FROM usuarios
        usuarios = conexion.session.query(UsuarioModel).all();
        dto = UsuarioRequestDTO()
        resultado = dto.dump(usuarios,many=True)
        print(usuarios)
        print(resultado)
        
        return {
            'content':resultado
        }
    def post(self):

        data:dict = request.get_json()
        
        dto = UsuarioRequestDTO()
        
        try:
            dataValidada = dto.load(data)
            print(dataValidada)

            nuevoUsuario = UsuarioModel(**dataValidada)
            #nuevoUsuario = UsuarioModel(
            #    nombre = data.get('nombre',''),
            #    apellido = data.get('apellido',''),
            #    correo = data.get('correo'),
            #    telefono = data.get('telefono'),
            #    linkedinUrl = data.get('linkedinUrl')
            #)
            #Agregamos el nuevo registro a la cola del cursor
            conexion.session.add(nuevoUsuario)
            #Guardamos de manera permanente nuestro usuario en la bd , si hay 
            conexion.session.commit()

            return {
                'message': 'Usuario creado exitosamente'
            },201
        except ValidationError as error:

            return{
                'message':'error usuario creado exitosamente',
                'content': error.args
            }
        except IntegrityError as error:
            return{
                'message': 'Error al crear el usuario',
                'content': 'El usuario ya existe'
            },400
        except Exception as error:
            return {
                'message': 'Error al crear el usuario',
                'content': error.args
            },400
        
class UsuarioController(Resource):
    def put(self,id):
        usuarioEncontrado = conexion.session.query(UsuarioModel).filter_by(id=id).first()
        if not usuarioEncontrado:
            return {
                'message':'El usuario a actualizar no existe'
            },404
        data = request.get_json()
        dto = UsuarioRequestDTO()
        try:
            dataValidada = dto.load(data)
            usuarioActualizados = conexion.session.query(UsuarioModel).filter_by(id=id).update(dataValidada)
            print(usuarioActualizados)
            conexion.session.commit()
            return {
                'message':'Usuario actualizado exitosamente'
            }
        except ValidationError as error:
            return{
                'message':'Error al actualizar el usuario',
                'content': error.args
            },400
        except IntegrityError as error:
            errorTexto: str = error.args[0]
            columna = errorTexto.split('la llave')[1]
            if columna.find('correo'):
                return{
                    'message':'Error al actualizar el usuario',
                    'content': 'El usuario con ese correo ya existe'
                }
            elif columna.find('nombre'): 
                return{
                    'message':'Error al actualizar el usuario',
                    'content': 'El usuario con ese correo ya existe'
                }
    def delete(self,id):
        usuarioEncontrado = conexion.session.query(UsuarioModel).filter_by(id=id).first()
        if not usuarioEncontrado:
            return {
                'message':'El usuario no existe'
            },404
        conexion.session.query(UsuarioModel).filter_by(id=id).delete()
        conexion.session.commit()
        return {
            'message':'Usuario eliminado exitosamente'
        }
    
    def get(self, id):
        usuarioEncontrado = conexion.session.query(UsuarioModel).filter_by(id=id).first()
        if not usuarioEncontrado:
            return {
                'message':'El usuario no existe'
            },404
        
        dto = UsuarioRequestDTO()
        usuarioConvertido = dto.dump(usuarioEncontrado)

        return {
            'content':usuarioConvertido
        }