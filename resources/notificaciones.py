import json
import datetime as dt
import functools
import uuid
from bson.objectid import ObjectId
from flask import request
from flask_restful import Resource

from pymongo import TEXT
from pymongo.operations import IndexModel
from pymodm import connect, fields, MongoModel, EmbeddedMongoModel
from pymodm.errors import ValidationError
from pymongo.errors import DuplicateKeyError

#from schemas.participante import ParticipanteSchema 
#from models.participante import ParticipanteModel 
from schemas.notificacion import NotificacionSchema
from models.notificacion import NotificacionModel 
from marshmallow import pprint

not_schema = NotificacionSchema()
not_schemas = NotificacionSchema(many=True)

# Establish a connection to the database.
connect("mongodb://localhost:27017/ej1")

class NotificacionList(Resource):
    @classmethod
    def get(self, id):
    #Participante id = part_id
        part_id = ObjectId(id)
        try:
            """
            Dependiendo del id que se consulta Pymodm genera
            una respuesta específica: 
            -Un query a el _id de la notificacion (_id) regresa:
                [
                    {
                        "_id": "5dfb4cbf23acb0be88ff5e9b",
                        "id_participante": "<ParticipanteModel object>",
                        "titulo": "Bienvenido al programa"
                    }
                ]
            
            -Un query a el _id del participante (id_participante) regresa:
            NotificacionModel(id_participante=ParticipanteModel(paterno='Martinez', email='correo@gmail.com', fecha_nacimiento=datetime.datetime(1997, 6, 6, 21, 0), _id=ObjectId('5dfb2779272294ec0c7052fc'), fecha_antiguedad=datetime.datetime(2019, 12, 19, 1, 32, 9, 278000), foto='https://estaticos.muyinteresante.es/media/cache/760x570_thumb/uploads/images/article/5536592a70a1ae8d775df846/dia-del-mono.jpg', tarjeta_sellos=TarjetaSellosModel(num_sellos=1, _id=ObjectId('5dfb3be68989a2f1e2918008')), nombre='Emmanuel3', password='12346', sexo='Masculino'), titulo='Bienvenido al programa', _id=ObjectId('5dfb4cbf23acb0be88ff5e9b'))
            NotificacionModel(id_participante=ParticipanteModel(paterno='Martinez', email='correo@gmail.com', fecha_nacimiento=datetime.datetime(1997, 6, 6, 21, 0), _id=ObjectId('5dfb2779272294ec0c7052fc'), fecha_antiguedad=datetime.datetime(2019, 12, 19, 1, 32, 9, 278000), foto='https://estaticos.muyinteresante.es/media/cache/760x570_thumb/uploads/images/article/5536592a70a1ae8d775df846/dia-del-mono.jpg', tarjeta_sellos=TarjetaSellosModel(num_sellos=1, _id=ObjectId('5dfb3be68989a2f1e2918008')), nombre='Emmanuel3', password='12346', sexo='Masculino'), titulo='Bienvenido al programa', _id=ObjectId('5dfb4d0268032c30e8e9fd00'))
            i,e. 
                [
                    {
                        "id_participante": "<ParticipanteModel object>",
                        "titulo": "Bienvenido al programa",
                        "_id": "5dfb4cbf23acb0be88ff5e9b"
                    },
                    {
                        "id_participante": "<ParticipanteModel object>",
                        "titulo": "Bienvenido al programa",
                        "_id": "5dfb4d0268032c30e8e9fd00"
                    }
                ]
            NOTE: Nice! :), en este caso, el primero es el que queremos.
            """
            participante_notifs_id = NotificacionModel.objects.raw({'id_participante': part_id})
            notifs = participante_notifs_id
            #for item in notifs:
            #    pprint(item)
            total_notifs = notifs.count()
        except NotificacionModel.DoesNotExist:
            return {'message': f"No sellos_card in participante with id{ id }"}
        # TODO: Agregar el URL para la solicitud al API de la notificacion, el link a la notificacion
        # TODO: Buscar en Google TODO Python vsCode
        return {"Notificaciones":
                    NotificacionSchema(
                    only=(
                    "_id",
                    "titulo",
                    # "id_participante"
                    "mensaje",
                    "fecha",
                    "imagenIcon",
                    "bar_text",
                    "tipo_notificacion",
                    ), many=True).dump(notifs),
                "Total": total_notifs    
                },200
    
    @classmethod
    def delete(self, id):
        notif_id = ObjectId(id)
        try:
            notif = NotificacionModel.objects.get({'_id': notif_id})
            notif.delete()
        except NotificacionModel.DoesNotExist as exc:
            print(exc)
            return {"message": "No se pudo eliminar la notificacion, porque no existe."}, 504 
        return {"message": "Eliminado"}, 200
    
    @classmethod
    def post(self, id):
        part_id = ObjectId(id)
        notificacion_json = request.get_json()
        print(notificacion_json)
        n = not_schema.load(notificacion_json)
        print("loaded")
        try:
            notif = NotificacionModel(
                id_participante=part_id,
                titulo=n["titulo"],
                mensaje=n["mensaje"],
                imagenIcon=n["imagenIcon"],
                bar_text=n["bar_text"],
                fecha=dt.datetime.now(),
                tipo_notificacion=n["tipo_notificacion"],
            ).save()
            print("guardado")
        except ValidationError as exc:
            print(exc.message)
            return {"message": "No se pudo crear la notificacion."}
        return {"message": "Notificacion guardada con éxito."}