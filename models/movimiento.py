from pymodm import connect, fields, MongoModel, EmbeddedMongoModel
from models.participante import ParticipanteModel
# from venta import Venta
import datetime as dt
# Establish a connection to the database.
connect('mongodb://localhost:27017/ej1')


class MovimientoAppModel(MongoModel):
    id_participante = fields.ReferenceField(ParticipanteModel)
    # id_venta = fields.ReferenceField(Venta)
    nombre = fields.CharField()
    tipo = fields.CharField()
    total = fields.FloatField()
    fecha = fields.DateTimeField()
    imagen_icon = fields.URLField()

    @classmethod
    def add_movimiento(cls, id_par, nombre, tipo, total, imagen_icon) -> "NotificacionModel":
        try:
            movimiento = cls(
                id_participante=id_par,
                nombre=nombre,
                tipo=tipo,
                total=total,
                fecha=dt.datetime.now(),
                imagen_icon=imagen_icon
            ).save()            
        except ValidationError as exc:   
            return None
        return movimiento