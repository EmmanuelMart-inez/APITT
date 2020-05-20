from bson.objectid import ObjectId
import datetime as dt

from flask_restful import Resource
from flask import request

from pymodm.errors import ValidationError
from pymongo.errors import DuplicateKeyError

from models.birthday import BirthdayModel
from models.participante import ParticipanteModel
from models.premio import PremioParticipanteModel
from models.notificacion import NotificacionTemplateModel, NotificacionModel
from schemas.birthday import BirthdaySchema
from marshmallow import pprint

from datetime import *
from dateutil.relativedelta import *
import calendar
import dateutil.parser

class Birthday(Resource):
    @classmethod
    def get(self):
        try:
            bir = BirthdayModel.objects.all()
        except BirthdayModel.DoesNotExist:
            return {"message": "No se encontro ninguna configuración cumpleaños"}, 400
        return BirthdaySchema(many=True).dump(bir), 200

    @classmethod
    def post(self):
        item_json = request.get_json()
        item = BirthdaySchema().load(item_json)
        try:
            item = BirthdayModel(
                # tipo=item["tipo"],
                id_notificacion=item["id_notificacion"],
                id_promocion=item["id_promocion"],
                trigger=item["trigger"],
                antiguedad=item["antiguedad"],
                vigencia=item["vigencia"],
                fecha_creacion=dt.datetime.now()
            ).save()
        except ValidationError as exc:
            print(exc.message)
            return {"message": "Error: No se pudo crear el premio de cumpleños"}   
        return {'message': "Elemento creado",
                '_id': str(item._id)
        }, 200
    
    @classmethod
    def put(self):
        bir_all = BirthdayModel.objects.all()
        # pprint(bir)
        if not bir_all:
            return {"message": "No se encontró el premio de cumpleaños"}, 404
        item_json = request.get_json()
        item = BirthdaySchema().load(item_json)
        for birthday in bir_all:
            bir = birthday
        try:
            if "id_notificacion" in item:
                bir.id_notificacion = item["id_notificacion"]
            if "id_promocion" in item:
                bir.id_promocion = item["id_promocion"]
            if "antiguedad" in item:
                bir.trigger = item["trigger"]
            if "antiguedad" in item:
                bir.antiguedad = item["antiguedad"]
            if "vigencia" in item:
                bir.vigencia = item["vigencia"]
            bir.fecha_creacion = dt.datetime.now()
            bir.save()
        except ValidationError as exc:
            print(exc.message)
            return {"message": "Error: No se pudo actualizar el premio de cumpleños"}   
        return {'message': "Elemento actualizado",
                '_id': str(bir._id)
        }, 200

# Enviar ahora premios de cumpleaños!
class BirthdaySetter(Resource): 
    # No se ocupa el id en este metodo, solo es un diferenciador del Recurso anterior
    # Se envia a todos los participantes que cumplan 
    # años y las restricciones. (Envio de premio a participantes)
    # Si ya se le envió un premio al participante, no se vuelve a enviar hasta el proximo cumpleaños (año)
    @classmethod
    def post(self, id):
        # Get premios
        bir_all = BirthdayModel.objects.all()
        # pprint(bir)
        if not bir_all:
            return {"message": "No se encontró el premio de cumpleaños"}, 404
        # item_json = request.get_json()
        # item = BirthdaySchema().load(item_json)
        # Get notificacion
        # TODO: Obtener la última configuración
        for birthday in bir_all:
            bir = birthday
        notificacion = NotificacionTemplateModel.find_by_id(bir.id_notificacion)
        if not notificacion:
            return {"message": "No se encontró la notificacion"}, 404
        # Enviar notificaciones
        # Enviar premio
        notificacion_id_premio = notificacion.link
        current_date = datetime.now()
        print("current_date", current_date)
        current_day = current_date.day
        current_month = current_date.month
        current_year = current_date.year
        maxdays = 0
        count_sends = 0
        premio = None
        for p in ParticipanteModel.objects.all():
            if p.fecha_nacimiento and p.fecha_nacimiento != "null":
                maxdays = bir.trigger
                bmonth = p.fecha_nacimiento.month
                r_maxdate = current_date+relativedelta(days=+maxdays)
                r_mindate = current_date-relativedelta(days=+maxdays)
                r_participante_birthdate = p.fecha_nacimiento.replace(year=current_year)
                r_antiguedad = current_date - p.fecha_antiguedad
                r_antiguedad = r_antiguedad.days 
                #  Verificar si no se ha enviado antes el premio al participante
                # print("data id_par:{}, id_premio: {}".format(str(p._id), notificacion_id_premio))
                tienePremio = PremioParticipanteModel.find_by_two_fields('id_participante', str(p._id), 'id_premio', notificacion_id_premio)
                # Verificar si en ESTE año no ha canjeado el premio, en caso de que no, enviar premio
                canjeado = False
                if tienePremio and tienePremio.fechas_redencion:
                    if len(tienePremio.fechas_redencion) > 0:
                        for fecha in tienePremio.fechas_redencion:
                            if fecha.year == current_date.year:
                                canjeado = True
                #OLD: tieneNotificacion = NotificacionModel.find_by_field('id_notificacion', str(notificacion._id))
                if r_mindate < r_participante_birthdate < r_maxdate and r_antiguedad >= bir.antiguedad:
                    if not canjeado and not tienePremio:
                        # Realizar envío de un nuevo premio
                        if(notificacion.tipo_notificacion == "premio"):
                            premio = PremioParticipanteModel(
                                id_participante = str(p._id),
                                id_premio = notificacion_id_premio,
                                estado = 0,
                                fecha_creacion = datetime.now(),
                                id_promocion = bir.id_promocion,
                            ).save()
                            notif = NotificacionModel(
                                id_participante = str(p._id),
                                id_notificacion = str(notificacion._id),
                                estado = 0
                            ).save()
                            # print("Envio", list(premio), str(premio._id))
                            if premio:
                                count_sends+=1
        return {"Total de envios:": count_sends}, 200   
        # TODO: ELIMINAR CADUCADOS  
                # print(str(p.fecha_nacimiento.day), "..", p.fecha_nacimiento.month)
            # elif bir.trigger == '10 dias antes y despues':
            # elif bir.trigger == 'solo durante el dia de su cumpleanos':
            # elif bir.trigger == 'durante el mes de su cumpleanos':
            # if bir.trigger
    
    # Actualizar configuración de cumpleaños
    @classmethod
    def patch(self, id):
        bir = BirthdayModel.find_by_id(id)
        pprint(bir)
        if not bir:
            return {"message": "No se encontró el premio de cumpleaños"}, 404
        item_json = request.get_json()
        item = BirthdaySchema().load(item_json)
        try:
            if "id_notificacion" in item:
                bir.id_notificacion = item["id_notificacion"]
            if "id_promocion" in item:
                bir.id_promocion = item["id_promocion"]
            if "trigger" in item:
                bir.trigger = item["trigger"]
            if "antiguedad" in item:
                bir.antiguedad = item["antiguedad"]
            if "vigencia" in item:
                bir.vigencia = item["vigencia"]
            bir.fecha_creacion = item["fecha_creacion"]
            bir.save()
        except ValidationError as exc:
            print(exc.message)
            return {"message": "Error: No se pudo actualizar el premio de cumpleños"}   
        return {'message': "Elemento actualizado",
                '_id': str(bir._id)
        }, 200
    
    # AFTTER
    @classmethod
    def delete(self, id):
        pass

    