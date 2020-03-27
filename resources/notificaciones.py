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
from models.participante import ParticipanteModel 
from models.premio import PremioModel, PremioParticipanteModel

from models.encuesta import EncuestaModel, EncuestaPaginaModel, EncuestaOpcionesModel, ParticipantesEncuestaModel
from schemas.encuesta import EncuestaSchema, EncuestaPaginaSchema, EncuestaOpcionesSchema, ParticipanteEncuestaSchema

from schemas.notificacion import NotificacionSchema, NotificacionTemplateSchema
from schemas.premio import PremioSchema, PremioParticipanteSchema
from models.notificacion import NotificacionModel, NotificacionTemplateModel  
from marshmallow import pprint

not_schema = NotificacionSchema()
not_schemas_template = NotificacionTemplateSchema(many=True)
not_schema_template = NotificacionTemplateSchema()
not_schemas = NotificacionSchema(many=True)

premio_schema = PremioSchema()

# Establish a connection to the database.
connect("mongodb://localhost:27017/ej1")

class NotificacionList(Resource):
    #Devolver aquellas en el estado sin eliminar
    @classmethod
    def get(self, id):
    #Participante id = part_id
        try:
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
            return {'message': f"No sellos_card in participante with id{ id }"}, 404
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
    # Es id de notificacion, no Template
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
            return {"message": "No se pudo eliminar la notificacion, porque no existe."}, 404
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
            return {"message": "No se pudo crear la notificacion."}, 404
        return {"message": "Notificacion guardada con éxito."}


class NotificacionesAdminList(Resource):
    # Obtiene los templates de las notificaciones que han sido creadas
    @classmethod
    def get(self):
        try:
            all_notifs = NotificacionTemplateModel.objects.raw({})
        except NotificacionTemplateModel.DoesNotExist:
            return {'message': f"No se encontró ninguna notificación"}, 404
        # TODO: Agregar el URL para la solicitud al API de la notificacion, el link a la notificacion
        # TODO: Buscar en Google TODO Python vsCode
        return  NotificacionTemplateSchema(
                    only=(
                    "_id",
                    "titulo",
                    "mensaje",
                    "fecha",
                    "tipo_notificacion",
                    "imagenIcon",
                    "bar_text",
                    "filtros"
                    ), many=True).dump(all_notifs),200

    # Crea un template de notificaciones y se envia a todos en la lista de filtros
    @classmethod
    def post(self):
        notificacion_json = request.get_json()
        # print(notificacion_json)
        n = not_schema_template.load(notificacion_json)
        pprint(n)
        # print("loaded")
        try:
            template = NotificacionTemplateModel()
            if "titulo" in n:
                template.titulo=n["titulo"]
            if "mensaje" in n:
                template.mensaje=n["mensaje"]
            if "imagenIcon" in n:
                template.imagenIcon=n["imagenIcon"]
            if "bar_text" in n:
                template.bar_text=n["bar_text"]
            if "fecha" in n:
                template.fecha=n["fecha"]
            else:
                template.fecha=dt.datetime.now()
            if  "tipo_notificacion" in n: 
                template.tipo_notificacion=n["tipo_notificacion"]
            if "link" in n:
                template.link=n["link"]
            if "filtros" in n:
                template.filtros = n["filtros"]
            else: 
                template.filtros = []
            template.save()
            filtersObids=[]
            for fil in n["filtros"]:
                filtersObids.append(ObjectId(fil))
            # Enviar a todos los participantes
            for p in ParticipanteModel.objects.raw({"_id": { "$in": filtersObids}}):
                # part_id = ObjectId(id)
                notif = NotificacionModel(
                id_participante=p._id,
                id_notificacion=template._id,
                estado=0,
                # Estado puede servir para actualizar tambien OJO! ahora esta fijo, pero podrías ser variable
                ).save()            
                # PYMODM no tiene soporte transaccional, en un futuro migrar a PYMONGO, que sí tiene soporte
            # return {"message": "Notificacion guardada con éxito."}
        except ValidationError as exc:
            print(exc.message)
            return {"message": "No se pudo crear o enviar la notificacion."}, 404
        return {"message": "Notificacion guardada con éxito.",
                    "_id": str(template._id),
                "Número de destinatarios:": len(template.filtros)}


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
            "filtros"
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
            return {"message": "No se encontro la notificación!"}, 404
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
            return {"message": "No se pudo actualizar la notificación."}, 404
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


class NotificacionAcciones(Resource):
    @classmethod
    def get(self, id, accion):
        if accion == 'ninguna':
            n = NotificacionTemplateModel.find_by_id(id)
            if not n:
                return {"message": "No se encontro la notificación"}, 404
            return {"notificacion": NotificacionTemplateSchema(
                only=(
                "_id",
                "titulo",
                "mensaje",
                "fecha",
                "imagenIcon",
                "bar_text",
                "tipo_notificacion",
                "link",
                "filtros"
                )).dump(n)}, 200
        elif accion == 'premio':
            n = NotificacionTemplateModel.find_by_id(id)
            pprint(n)
            if not n:
                return {"message": "No se encontro el premio"}, 404
            p = PremioModel.find_by_id(n.link)
            if not p:
                return {"message": "No se encontro el premio"}, 404
            return {"notificacion": NotificacionTemplateSchema(
                only=(
                "_id",
                "titulo",
                "mensaje",
                "fecha",
                "imagenIcon",
                "bar_text",
                "tipo_notificacion",
                "link",
                "filtros"
                )).dump(n),
             "premio":  PremioSchema(
                    only=(
                        "_id",
                        "nombre", 
                        "puntos", 
                        "codigo_barras", 
                        "codigo_qr",
                        "imagen_icon",
                        "imagen_display",
                        "fecha_creacion", 
                        "fecha_vigencia", 
                        # "fecha_redencion",
                        # "id_producto",
                        "id_participante"
                    )).dump(p)
            }, 200               
        elif accion == 'encuesta':
            n = NotificacionTemplateModel.find_by_id(id)
            pprint(n)
            if not n:
                return {"message": "No se encontro la notificacion"}, 404
            en = EncuestaModel.find_by_id(n.link)
            if not en:
                return {"message": "No se encontro la encuesta"}, 404
            return {
                "notificacion": NotificacionTemplateSchema(
                    only=(
                    "_id",
                    "titulo",
                    "mensaje",
                    "fecha",
                    "imagenIcon",
                    "bar_text",
                    "tipo_notificacion",
                    "link",
                    "filtros"
                    )).dump(n),
                "encuesta": EncuestaSchema(
                        only=(
                            "_id",
                            "titulo",
                            "categoria",
                            "fecha_creacion",
                            "fecha_respuesta",
                            "metrica",
                            "puntos",
                            "paginas",
                        )).dump(en)
            }, 200
    
    # Actualizar una notificacion con o sin su Premio o Encuesta
    @classmethod 
    def put(self, id, accion):
        n = NotificacionTemplateModel.find_by_id(id)
        if not n:
            return {"message": "No se encontro la notificación!"}, 404
        noti_json = request.get_json()
        # pprint(noti_json["notificacion"])
        noti = not_schema_template.load(noti_json["notificacion"])
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
            if "filtros" in noti:
                n.filtros=noti["filtros"]
            n.save()
        except ValidationError as exc:
            print(exc.message)
            return {"message": "No se pudo actualizar la notificación."}, 404
        if accion == 'ninguna':
            return {"notificacion": NotificacionTemplateSchema(
                only=(
                "_id",
                "titulo",
                "mensaje",
                "fecha",
                "imagenIcon",
                "bar_text",
                "tipo_notificacion",
                "link",
                )).dump(n)}, 200
            # /admin/notificaciones/<string:id> patch! ya existe!
        elif accion == 'premio':
            p = PremioModel.find_by_id(n.link)
            if not p:
                return {"message": "No se encontro el premio"}, 404
            # p_req = request.get_json()
            # pprint(p_req)
            premio = premio_schema.load(noti_json["premio"])
            # pprint(p_req["premio"])
            pprint(premio)
            try:
                if "nombre" in premio:
                    p.nombre = premio["nombre"] 
                if "puntos" in premio:
                    p.puntos = premio["puntos"] 
                if "codigo_barras" in premio:
                    p.codigo_barras = premio["codigo_barras"] 
                if "codigo_qr" in premio:
                    p.codigo_barras = premio["codigo_barras"] 
                if "imagen_icon" in premio:
                    p.imagen_icon = premio["imagen_icon"] 
                if "imagen_display" in premio:
                    p.imagen_icon = premio["imagen_icon"] 
                if "fecha_creacion" in premio:
                    p.imagen_icon = premio["imagen_icon"] 
                if "fecha_vigencia" in premio:
                    p.fecha_vigencia = premio["fecha_vigencia"] 
                if "fecha_redencion" in premio:
                    p.fecha_redencion = premio["fecha_redencion"] 
                p.save()
            except ValidationError as exc:
                print(exc.message)
                return {"message": "No se pudo actualizar el premio."}, 400
            return {"notificacion": NotificacionTemplateSchema(
                only=(
                "_id",
                "titulo",
                "mensaje",
                "fecha",
                "imagenIcon",
                "bar_text",
                "tipo_notificacion",
                "link",
                )).dump(n),
             "premio":  PremioSchema(
                    only=(
                        "_id",
                        "nombre", 
                        "puntos", 
                        "codigo_barras", 
                        "codigo_qr",
                        "imagen_icon",
                        "imagen_display",
                        "fecha_creacion", 
                        "fecha_vigencia", 
                        # "fecha_redencion",
                        # "id_producto",
                        "id_participante"
                    )).dump(p)
            }, 200               
        elif accion == 'encuesta':
            e = EncuestaModel.find_by_id(n.link)
            if not e:
                return {"message": "No se encontro la encuesta"}, 404
            noti_json = request.get_json()
            encuesta = EncuestaSchema().load(noti_json["encuesta"])
            try:
                # Encuesta
                if "titulo" in encuesta:
                    e.titulo=encuesta["titulo"]
                if "categoria" in encuesta:
                    e.categoria=encuesta["categoria"]
                e.fecha_creacion=dt.datetime.now()
                if "metrica" in encuesta:
                    e.metrica=encuesta["metrica"]
                if "puntos" in encuesta:
                    e.puntos=encuesta["puntos"]
                if "paginas" in encuesta:
                    e.paginas=encuesta["paginas"]
                    pprint(e.paginas)
                    # for pagina in e.paginas:
                    #     print(1)
                e.save()
                n.save()
            except ValidationError as exc:
                print(exc.message)
                return {"message": "No se pudo actualizar la notificación."}, 404
            return {
                "notificacion": NotificacionTemplateSchema(
                    only=(
                    "_id",
                    "titulo",
                    "mensaje",
                    "fecha",
                    "imagenIcon",
                    "bar_text",
                    "tipo_notificacion",
                    "link"
                    )).dump(n),
                "encuesta": EncuestaSchema(
                        only=(
                            "_id",
                            "titulo",
                            "categoria",
                            "fecha_creacion",
                            "fecha_respuesta",
                            "metrica",
                            "puntos",
                            "paginas",
                        )).dump(e)
            }, 200
        
    # Eliminar notificación
    @classmethod
    def delete(self, id, accion):
        if accion == 'ninguna':
            n = NotificacionTemplateModel.find_by_id(id)
            if not n:
                return {"message": "No se encontro la notificación"}, 404
            try:
                for p in NotificacionModel.objects.raw({"id_notificacion": n._id}):
                    p.delete()
                n.delete()
            except:
                return {"message": "No se pudo efectuar esta operación"},404 
            return {"message": "Notificacion eliminada"}, 200
        elif accion == 'premio':
            n = NotificacionTemplateModel.find_by_id(id)
            pprint(n)
            if not n:
                return {"message": "No se encontro la notificacion"}, 404
            p = PremioModel.find_by_id(n.link)
            if not p:
                return {"message": "No se encontro el premio"}, 404
            try:
                for np in NotificacionModel.objects.raw({"id_notificacion": n._id}):
                    np.delete()
                for pp in PremioParticipanteModel.objects.raw({"id_premio": p._id}):
                    pp.delete()
                n.delete()
                p.delete()
            except:
                return {"message": "No se pudo efectuar esta operación"},404 
            return {"message": "Notificación y premio eliminados"}, 200               
        elif accion == 'encuesta':
            n = NotificacionTemplateModel.find_by_id(id)
            pprint(n)
            if not n:
                return {"message": "No se encontro la notificacion"}, 404
            en = EncuestaModel.find_by_id(n.link)
            if not en:
                return {"message": "No se encontro la encuesta"}, 404
            try:
                for np in NotificacionModel.objects.raw({"id_notificacion": n._id}):
                    np.delete()
                for ep in ParticipantesEncuestaModel.objects.raw({"id_encuesta": en._id}):
                    ep.delete()
                n.delete()
                en.delete()
            except:
                return {"message": "No se pudo efectuar esta operación"},404 
            return {"message": "Notificación y encuesta eliminados"}, 200   

    # Enviar de nuevo notificación y su especialización si es que tiene
    # El id es necesario para recuperar la notificación y entonces re-enviarla
    # <accion>: No sirve para nada en este endpoint
    # TODO: Implementar filtros / segmentación : <accion> se puede utilizar para realizar filtrados y segms
    @classmethod
    def post(self, id, accion):
        n = NotificacionTemplateModel.find_by_id(id)
        if not n:
            return {"message": "No se encontro la notificación"}, 404
        response_envio = NotificacionTemplateModel.send_to_participantes(n)
        if response_envio["status"] == 404:
            return {"message": "No se pudo crear o enviar la notificacion."}, 404
        if accion == 'ninguna':
                return {"message": "Notificacion reenviada con éxito.",
                    "Número de destinatarios:": response_envio["total"]}
        elif accion == 'premio':
            p = PremioModel.find_by_id(n.link)
            if not p:
                return {"message": "No se encontro el premio"}, 404
            response_envio = PremioModel.send_to_participantes(n)
            if response_envio["status"] == 404:
                return {"message": "No se pudo crear o enviar la notificacion."}, 404
            return {"message": "Notificacion reenviada con éxito.",
                "Número de destinatarios:": response_envio["total"]}
        elif accion == 'encuesta':
            n = NotificacionTemplateModel.find_by_id(id)
            pprint(n)
            if not n:
                return {"message": "No se encontro la notificacion"}, 404
            en = EncuestaModel.find_by_id(n.link)
            if not en:
                return {"message": "No se encontro la encuesta"}, 404
            response_envio = EncuestaModel.send_to_participantes(n)
            if response_envio["status"] == 404:
                return {"message": "No se pudo crear o enviar la notificacion."}, 404
            return {"message": "Notificacion reenviada con éxito.",
                "Número de destinatarios:": response_envio["total"]}
