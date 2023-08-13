from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models.mascota import MascotaModel

class MascotaRequestDto(SQLAlchemyAutoSchema):
    class Meta:
        model = MascotaModel
