from bson.objectid import ObjectId
#from models.participante import ParticipanteModel
from pymongo import TEXT
from pymongo.operations import IndexModel
from pymodm import connect, fields, MongoModel, EmbeddedMongoModel

# import datetime as dt

from models.tarjeta import TarjetaPuntosModel, TarjetaSellosModel

from datetime import *
from dateutil.relativedelta import *
import calendar
import dateutil.parser
# Establish a connection to the database.
connect('mongodb://localhost:27017/ej1')

# This is an EmbeddedMongoModel, which means that it will be stored *inside*
# another document (i.e. a Participante),



class FacebookFieldsModel(EmbeddedMongoModel):
    public_fields = fields.CharField()
    email = fields.EmailField()
    birthday = fields.DateTimeField()
    user_photo = fields.URLField()  # "Change to ImageField"
    token = fields.CharField()


class GoogleFieldsModel(EmbeddedMongoModel):
    name = fields.CharField()
    given_name = fields.CharField()
    family_name = fields.CharField()
    picture = fields.URLField()
    email = fields.EmailField()
    email_verified = fields.BooleanField()
    token = fields.CharField()


class ParticipanteModel(MongoModel):
    # _id = fields.ObjectIdField(primary_key=True)
    nombre = fields.CharField()
    paterno = fields.CharField()
    email = fields.EmailField()
    password = fields.CharField()
    sexo = fields.CharField()
    fecha_nacimiento = fields.DateTimeField()
    fecha_antiguedad = fields.DateTimeField()
    foto = fields.URLField()
    direccion = fields.CharField()
    intentos = fields.IntegerField()
    ultimo_inicio_sesion = fields.DateTimeField()
    secret_key = fields.CharField()
    token_user = fields.CharField()
    fresh_token = fields.CharField()
    facebook_fields = fields.EmbeddedDocumentListField(
        FacebookFieldsModel, default=[])
    facebook_id = fields.CharField()
    google_fields = fields.EmbeddedDocumentListField(
        GoogleFieldsModel, default=[])
    google_id = fields.CharField()
    tarjeta_sellos = fields.ReferenceField(TarjetaSellosModel)
    tarjeta_puntos = fields.ReferenceField(TarjetaPuntosModel)
    saldo = fields.FloatField(default=0)
    sellos = fields.IntegerField(default=0)


    @classmethod
    def find_by_username(cls, username: str) -> "ParticipanteModel":
        try:
            ParticipanteModel(nombre=username).save()
            user = cls.objects.get({'nombre': username})
            return user
        except cls.MultipleObjectsReturned:
            return None
        except cls.DoesNotExist:
            return None
    
    @classmethod
    def find_by_email(cls, email: str) -> "ParticipanteModel":
        try:
            user = cls.objects.get({'email': email})
            return user
        except cls.MultipleObjectsReturned:
            return None
        except cls.DoesNotExist:
            return None

    @classmethod
    def find_by_socialNetwork(cls, socialNetwork: str, id: str, email: str) -> "ParticipanteModel":
        try:
            print(socialNetwork, id)
            if socialNetwork == 'google':
                user = cls.objects.get({'google_id': id})
                print(user)
            if socialNetwork == 'facebook':
                user = cls.objects.get({'facebook_id': id})
            return user
        except cls.MultipleObjectsReturned:
            print("multiple objects")
            return None
        except cls.DoesNotExist:
            print("does not exist")
            return None

    @classmethod
    def find_by_id(cls, _Objectid: str) -> "ParticipanteModel":
        try:
            oid = ObjectId(_Objectid)
            user = cls.objects.get({'_id': oid})
            return user
        except cls.DoesNotExist:
            return None

    @classmethod
    def find_by_credentials(cls, email: str, password: str) -> "ParticipanteModel":
        try:
            user = cls.objects.get({'email': email, 'password': password})
            return user
        except cls.DoesNotExist:
            return None

    @classmethod
    def filter_by_date_range(cls, date_start: str, date_end: str) -> "ParticipanteModel":
        date_s = dateutil.parser.parse(date_start)
        date_e = dateutil.parser.parse(date_end)
        # print(type(date_s))
        # date_s = dt.datetime.fromisoformat(date_start)
        try: 
            users = cls.objects.raw({'fecha_antiguedad' : {"$gte" : date_s, "$lt": date_e}}) 
            # users = list(cls.objects.raw({'fecha_antiguedad' : date_s}) )
            # print(users)
            print(list(users))
            return users
        except cls.DoesNotExist:
            return None


    @classmethod
    def filter_by_dateExample(cls, date_start: str) -> "ParticipanteModel":
        date_s = dateutil.parser.parse(date_start)
        fecha = date_s.replace(hour=0, minute=0, second=0, microsecond=0)
        fecha2 =  date_s.replace(hour=23, minute=59, second=59, microsecond=59)
        print(fecha, fecha2)
        # print(type(date_s))
        # date_s = dt.datetime.fromisoformat(date_start)
        try: 
            users = cls.objects.raw({'fecha_antiguedad' : {"$gte" : fecha, "$lt": fecha2}})  
            # users = list(cls.objects.raw({'fecha_antiguedad' : date_s}) )
            # print(users)
            print(list(users))
            return users
        except cls.DoesNotExist:
            return None

    @classmethod
    def filter_by_date(cls, date_start: str, tipo: str, scale: str, scale_value: str) -> "ParticipanteModel":
        date_s = dateutil.parser.parse(date_start)
        # print(type(date_s))
        # date_s = dt.datetime.fromisoformat(date_start)
        try: 
            # Relative Dates
            if tipo == 'anterior':
                if scale == 'dias':
                    rdate = date_s.replace(hour=0, minute=0, second=0, microsecond=0)+relativedelta(days=+scale_value)
                elif scale == 'semanas':
                    date.replace(hour=0, minute=0, second=0, microsecond=0)+relativedelta(weeks=-scale_value)
                elif scale == 'meses':
                    date.replace(hour=0, minute=0, second=0, microsecond=0)+relativedelta(months=-scale_value)
                elif scale == 'años':
                    date.replace(hour=0, minute=0, second=0, microsecond=0)+relativedelta(years=-scale_value)
                elif scale == 'minutos':
                    date+relativedelta(minutes=-scale_value)
                elif scale == 'horas':
                    date+relativedelta(hours=-scale_value)
                users = cls.objects.raw({'fecha_antiguedad' : {"$gte" : rdate, "$lt": date_s}})
                return users
            elif tipo == 'siguiente':
                if scale == 'dias':
                    rdate = date_s.replace(hour=23, minute=59, second=59, microsecond=59)+relativedelta(days=+scale_value)
                elif scale == 'semanas':
                    rdate = date.replace(hour=23, minute=59, second=59, microsecond=59)+relativedelta(weeks=+scale_value)
                elif scale == 'meses':
                    rdate = date.replace(hour=23, minute=59, second=59, microsecond=59)+relativedelta(months=+scale_value)
                elif scale == 'años':
                    rdate = date.replace(hour=23, minute=59, second=59, microsecond=59)+relativedelta(years=+scale_value)
                elif scale == 'minutos':
                    rdate = date+relativedelta(minutes=+scale_value)
                elif scale == 'horas':
                    rdate = date+relativedelta(hours=+scale_value)
                    # relativedelta( date_s.date)
                users = cls.objects.raw({'fecha_antiguedad' : {"$gte" : date_s.replace(hour=0, minute=0, second=0, microsecond=0), "$lt": rdate.replace(hour=23, minute=59, second=59, microsecond=59)}})
                return users
            elif tipo == 'actual':
                users = cls.objects.raw({'fecha_antiguedad' : {"$gte" : rdate, "$lt": date_s}})
                return users
            elif tipo == 'antes':
                pass
            elif tipo == 'despues':
                pass

            user = cls.objects.raw({ 'fecha_antiguedad' :  date_s }) 
            # users = list(cls.objects.raw({'fecha_antiguedad' : date_s}) )
            # print(user)
            # print(list(user))
            return user
        except cls.DoesNotExist:
            return None

    @classmethod
    def save_to_db(self):
        self.save()
    

    
