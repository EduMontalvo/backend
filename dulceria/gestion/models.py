from django.db import models
from uuid import uuid4
# https://docs.djangoproject.com/en/4.2/topics/db/models/
class CategoriaModel(models.Model):

    opcionesNivelAzucar = (
        #? Si usaramos formularios dentro de django
        #? bd, lo que mostraria en el formulario
        ['MA', 'MUY_ALTO'],
        ['ALTO', 'ALTO'],
        ['MEDIO', 'MEDIO'],
        ['BAJO', 'BAJO'],
        ['MUY_BAJO', 'MUY_BAJO'],
        ['CERO', 'CERO']
    )

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    nombre = models.TextField(null=False)
    nivelAzucar = models.TextField(name='nivel_azucar', null=False, choices=opcionesNivelAzucar)
# Create your models here.

    class Meta:
        #? Se agrega la clase Meta para que Django cree una tabla en la base de datos con el nombre categoria
        # https://docs.djangoproject.com/en/4.2/ref/models/options/#db-table
        db_table = 'categoria'

class GolosinaModel(models.Model):
    tipoProcedencia = (
        ['NACIONAL', 'NACIONAL'],
        ['IMPORTADO', 'IMPORTADO']
    )


    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    nombre = models.TextField(null=False)
    fechaVencimiento = models.DateField(editable=False, null=False, name='fecha_vencimiento')
    precio = models.FloatField(null=False)
    procedencia = models.TextField(choices=tipoProcedencia, default='NACIONAL')

    # Relaciones
    # on_delete > cuando se elimina un registro de la categoria y esta tenga golosinas, como deberia actuar la base de datos? 
    # CASCADE > si se elimina la categoria, se eliminan las golosinas relacionadas con ella
    # PROTECT > evita la eliminacion y lanzara un error de tipo ProtectedError
    # RESTRICT > evita la eliminacion pero lanzara un error de tipo RestrictedError
    # SET_NULL > eliminara la categoria y cambiara el id por null (NOTA: no tendria que tener setteado null=False)
    #SET_DEFAULT > eliminara la categoria y cambiara el valor de sus golosinas a un valor por defecto
    #DO_NOTHING > no se debe utilizar esto, deja el id en esta columna a pesar que ya no exista por ende generara mala integridad de datos.

    # related_name > crea un atributo virtual en mi otro modelo para poder acceder a todos sus golosinas desde categoria, si no se define este parametro usara el siguiente formato NOMBRE_MODELO_set > GolosinaModel_set
    # internamente cuando se mande a llamar a este atributo generara un join entre las tablas de manera dinamica (no siempre se crea el join, solo cuando se llama)

    categoria = models.ForeignKey(to=CategoriaModel, db_column='categoria_id', on_delete=models.PROTECT,related_name='golosinas')
    
    class Meta:
        db_table = 'golosinas'
        # unique_together > se utiliza para que dos valores de la table por ejemplo nombre y fecha_vencimiento no se puedan repetir. Ejm: 
        # glacitas 2023/10/09 ✓    en este caso lo permite porque es el primer registro
        # morochas 2023/05/07 ✓    
        # glacitas 2023/10/09 X     en este caso no lo registrara porque ya existe uno igual, tienen que ser diferentes el nombre y la fecha de vencimiento, jamas se podra repetir en un registro el nombre y la fecha de vencimiento. constrain | restriccion

        unique_together = [['nombre', 'fecha_vencimiento']]
