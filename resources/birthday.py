from bson.objectid import ObjectId
import datetime as dt

from flask_restful import Resource
from flask import request

from pymodm.errors import ValidationError
from pymongo.errors import DuplicateKeyError

from models.birthday import BirthdayModel
from schemas.birthday import BirthdaySchema
from marshmallow import pprint

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
                vigencia=item["vigencia"],
                fecha_creacion=dt.datetime.now()
            ).save()
        except ValidationError as exc:
            print(exc.message)
            return {"message": "Error: No se pudo crear el premio de cumpleños"}   
        return {'message': "Elemento creado",
                '_id': str(item._id)
        }, 200

class BirthdaySetter(Resource): 
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

    