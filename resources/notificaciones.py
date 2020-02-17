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
from schemas.notificacion import NotificacionSchema, NotificacionTemplateSchema
from models.notificacion import NotificacionModel, NotificacionTemplateModel  
from marshmallow import pprint

not_schema = NotificacionSchema()
not_schemas_template = NotificacionTemplateSchema(many=True)
not_schema_template = NotificacionTemplateSchema()
not_schemas = NotificacionSchema(many=True)

# Establish a connection to the database.
connect("mongodb://localhost:27017/ej1")

class NotificacionList(Resource):

    #Devolver aquellas en el estado sin eliminar

    @classmethod
    def get(self, id):
    #Participante id = part_id
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
            part_id = ObjectId(id)
            participante_notifs_id = NotificacionModel.objects.raw({'id_participante': part_id, 'estado': 0})
            notifsList=[]
            for n in participante_notifs_id:
                pprint(n.id_notificacion)
                notifsList.append(n.id_notificacion)
            #for item in notifs:
            #    pprint(item)
            total_notifs = len(notifsList)
        except NotificacionModel.DoesNotExist:
            return {'message': f"No sellos_card in participante with id{ id }"}
        # TODO: Agregar el URL para la solicitud al API de la notificacion, el link a la notificacion
        # TODO: Buscar en Google TODO Python vsCode
        return {"Notificaciones":
                    NotificacionTemplateSchema(
                    only=(
                    "_id",
                    "titulo",
                    # "id_participante"
                    "mensaje",
                    "fecha",
                    "imagenIcon",
                    "bar_text",
                    "tipo_notificacion",
                    "link",
                    # "estado"
                    ), many=True).dump(notifsList),
                "Total": total_notifs    
                },200
    
    #Solo para el uso del admin del sistema 
    # Es id de encuesta, no Template
    @classmethod
    def delete(self, id):
        notif_id = ObjectId(id)
        try:
            notif = NotificacionModel.objects.get({'_id': notif_id})
            notif.delete()
            #TODO: Marcar como eliminada la encuesta o desde el app hacerlo, checar
        except NotificacionModel.DoesNotExist as exc:
            print(exc)
            return {"message": "No se pudo eliminar la notificacion, porque no existe."}, 400 
        return {"message": "Eliminado"}, 200
    
    ## Historial notificaciones
    @classmethod
    def patch(self, id):
        notif_id = ObjectId(id)
        try:
            notif = NotificacionModel.objects.get({'_id': notif_id})
            notif.estado=1
            notif.save()
            #TODO: Marcar como eliminada la encuesta o desde el app hacerlo, checar
        except NotificacionModel.DoesNotExist as exc:
            print(exc)
            return {"message": "No se pudo eliminar la notificacion, porque no existe."}, 504 
        return {"message": "Eliminado"}, 200
    
    # Crear una notificación para un participante
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
                id_notificacion=n["id_notificacion"],
                estado=n["estado"],
            ).save()            
            print("guardado")
        except ValidationError as exc:
            print(exc.message)
            return {"message": "No se pudo crear la notificacion."}
        return {"message": "Notificacion guardada con éxito."}


class NotificacionesAdminList(Resource):
    # Obtiene los templates de las notificaciones que han sido creadas
    @classmethod
    def get(self):
        try:
            all_notifs = NotificacionTemplateModel.objects.raw({})
        except NotificacionTemplateModel.DoesNotExist:
            return {'message': f"No se encontró ninguna notificación"}
        # TODO: Agregar el URL para la solicitud al API de la notificacion, el link a la notificacion
        # TODO: Buscar en Google TODO Python vsCode
        return  NotificacionTemplateSchema(
                    only=(
                    "_id",
                    "titulo",
                    "fecha",
                    "tipo_notificacion"
                    ), many=True).dump(all_notifs),200

    # Crea un template de notificaciones
    @classmethod
    def post(self):
        notificacion_json = request.get_json()
        print(notificacion_json)
        n = not_schemas_template.load(notificacion_json)
        print("loaded")
        try:
            template = NotificacionTemplateModel(
                titulo=n["titulo"],
                mensaje=n["mensaje"],
                imagenIcon=n["imagenIcon"],
                bar_text=n["bar_text"],
                fecha=dt.datetime.now(),
                tipo_notificacion=n["tipo_notificacion"],
                link=n["link"],
            ).save()
            print("guardado")
        except ValidationError as exc:
            print(exc.message)
            return {"message": "No se pudo crear la notificacion."}
        return {"message": "Notificacion guardada con éxito.",
                    "_id": str(template._id)}


class NotificacionesAdmin(Resource):
    # Obtiene el template de una notificación
    @classmethod
    def get(self, id):
        print("Admin")
        n = NotificacionTemplateModel.find_by_id(id)
        
        if not n:
            print("no se encontro")
            return {"message": "No se encontro el la notificación!"}, 404
        return NotificacionTemplateSchema(
            only=(
            "_id",
            "titulo",
            "mensaje",
            "fecha",
            "imagenIcon",
            "bar_text",
            "tipo_notificacion",
            "link",
            )).dump(n), 200

    @classmethod
    def delete(self, id):
        notif_id = ObjectId(id)
        try:
            notif = NotificacionTemplateModel.objects.get({'_id': notif_id})
            notif.delete()
            #TODO: Marcar como eliminada la encuesta o desde el app hacerlo, checar
        except NotificacionTemplateModel.DoesNotExist as exc:
            print(exc)
            return {"message": "No se pudo eliminar el template de la notificacion, porque no existe."}, 400 
        return {"message": "Eliminado"}, 200

    #  Editar una notifiación existente
    @classmethod
    def patch(self, id):
        n = NotificacionTemplateModel.find_by_id(id)
        if not n:
            return {"message": "No se encontro el la notificación!"}
        noti_json = request.get_json()
        # print(user_json)
        noti = not_schema_template.load(noti_json)
        try:
            if "tipo_notificacion" in noti:
                n.tipo_notificacion=noti["tipo_notificacion"]
            if "imagenIcon" in noti:
                n.imagenIcon=noti["imagenIcon"]
            if "titulo" in noti:
                n.titulo=noti["titulo"]
            if "fecha" in noti:
                n.fecha=noti["fecha"]
            if "bar_text" in noti:
                n.bar_text=noti["bar_text"]
            if "mensaje" in noti:
                n.mensaje=noti["mensaje"]
            if "link" in noti:
                n.link=noti["link"]
            n.save()
        except ValidationError as exc:
            print(exc.message)
            return {"message": "No se pudo actualizar la notificación."}
        return NotificacionTemplateSchema(
            only=(
            "_id",
            "titulo",
            "mensaje",
            "fecha",
            "imagenIcon",
            "bar_text",
            "tipo_notificacion",
            "link",
            )).dump(n), 200
