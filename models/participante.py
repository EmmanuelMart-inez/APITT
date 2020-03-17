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
    def filter_by_date_range(cls, date_start: str, date_end: str, field: str) -> "ParticipanteModel":
        date_s = dateutil.parser.parse(date_start)
        date_e = dateutil.parser.parse(date_end)
        # print(type(date_s))
        # date_s = dt.datetime.fromisoformat(date_start)
        try: 
            users = cls.objects.raw({field : {"$gte" : date_s, "$lt": date_e}}) 
            # users = list(cls.objects.raw({'fecha_antiguedad' : date_s}) )
            # print(users)
            print(list(users))
            return users
        except cls.DoesNotExist:
            return None


    # @classmethod
    # def filter_by_dateExample(cls, date_start: str) -> "ParticipanteModel":
    #     date_s = dateutil.parser.parse(date_start)
    #     fecha = date_s.replace(day=1, hour=0, minute=0, second=0, microsecond=0)+relativedelta(months=+1, days=-1)
    #     fecha3= fecha+relativedelta(months=+1, days=-1)

    #     fecha2 =  date_s.replace(hour=23, minute=59, second=59, microsecond=59)
    #     print(fecha, fecha3)
    #     # print(type(date_s))
    #     # date_s = dt.datetime.fromisoformat(date_start)
    #     try: 
    #         users = cls.objects.raw({'fecha_antiguedad' : {"$gte" : fecha, "$lt": fecha2}})  
    #         # users = list(cls.objects.raw({'fecha_antiguedad' : date_s}) )
    #         # print(users)
    #         print(list(users))
    #         return users
    #     except cls.DoesNotExist:
    #         return None

    @classmethod
    def filter_by_date(cls, date_start: str, tipo: str, scale: str, scale_value: int, field: str) -> "ParticipanteModel":
        date_s = dateutil.parser.parse(date_start)
        # print(type(date_s))
        # date_s = dt.datetime.fromisoformat(date_start)
        try: 
            # Relative Dates
            if tipo == 'anterior':
                if scale == 'dias':
                    rdate = date_s.replace(hour=0, minute=0, second=0, microsecond=0)-relativedelta(days=+scale_value)
                elif scale == 'semanas':
                    rdate = date_s.replace(hour=0, minute=0, second=0, microsecond=0)-relativedelta(weeks=+scale_value)
                elif scale == 'meses':
                    rdate = date_s.replace(hour=0, minute=0, second=0, microsecond=0)-relativedelta(months=+scale_value)
                elif scale == 'años':
                    rdate = date_s.replace(hour=0, minute=0, second=0, microsecond=0)-relativedelta(years=+scale_value)
                elif scale == 'minutos':
                    rdate = date_s-relativedelta(minutes=+scale_value)
                elif scale == 'horas':
                    rdate = date_s-relativedelta(hours=+scale_value)
                users = cls.objects.raw({field : {"$gte" : rdate, "$lt": date_s}})
                return users
            elif tipo == 'siguiente':
                if scale == 'dias':
                    rdate = date_s.replace(hour=23, minute=59, second=59, microsecond=59)+relativedelta(days=+scale_value)
                elif scale == 'semanas':
                    rdate = date_s.replace(hour=23, minute=59, second=59, microsecond=59)+relativedelta(weeks=+scale_value)
                elif scale == 'meses':
                    rdate = date_s.replace(hour=23, minute=59, second=59, microsecond=59)+relativedelta(months=+scale_value)
                elif scale == 'años':
                    rdate = date_s.replace(hour=23, minute=59, second=59, microsecond=59)+relativedelta(years=+scale_value)
                elif scale == 'minutos':
                    rdate = date_s+relativedelta(minutes=+scale_value)
                elif scale == 'horas':
                    rdate = date_s+relativedelta(hours=+scale_value)
                users = cls.objects.raw({field : {"$gte" : date_s, "$lt": rdate.replace(hour=23, minute=59, second=59, microsecond=59)}})
                return users
            # NOTE: No importa el valor de `scale_value` en esta consulta
            elif tipo == 'actual':
                if scale == 'dias':
                    rdate = date_s.replace(hour=0, minute=0, second=0, microsecond=0)
                # Forma de calcular los dias a restar para obtener la semana actual = #día % 8 - 1
                elif scale == 'semanas':
                    month_day = date_s.day % 8 - 1
                    print(month_day)
                    rdate = date_s.replace(day=month_day, hour=0, minute=0, second=0, microsecond=0)+relativedelta()
                elif scale == 'meses':
                    rdate = date_s.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
                elif scale == 'años':
                    rdate = date_s.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
                elif scale == 'minutos':
                    rdate = date_s.replace(second=0, microsecond=0)
                elif scale == 'horas':
                    rdate = date_s.replace(minute=0, second=0, microsecond=0)
                else:
                    return None
                users = cls.objects.raw({field : {"$gte" : rdate, "$lt": date_s}})
                return users
            elif tipo == 'antes':
                users = cls.objects.raw({field : { "$lt": date_s}})
                return users
            elif tipo == 'despues':
                users = cls.objects.raw({field : { "$gte": date_s}})
                return users
            return {'message': 'Tipo de filtro de fecha invalido'}, 400
        except cls.DoesNotExist:
            return None

    @classmethod
    def filter_by_float_range(cls, tipo: str, field: str, float1: float, float2: float) -> "ParticipanteModel":
        if tipo == '<>':
            try:
                users = cls.objects.raw({field : { "$gt" : float1, "$lt" : float2}})
                return users
            except cls.DoesNotExist:
                return None

    @classmethod
    def filter_by_float(cls, tipo: str, float1: float, field: str) -> "ParticipanteModel":
        try:
            if tipo == '=':
                users = cls.objects.raw({field : float1})
                return users
            elif tipo == '>':
                users = cls.objects.raw({field : { "$gt" : float1}})
                return users
            elif tipo == '=>':
                users = cls.objects.raw({field : { "$gte" : float1}})
                return users
            elif tipo == '<':
                users = cls.objects.raw({field : { "$lt" : float1}})
                return users
            elif tipo == '<=':
                users = cls.objects.raw({field : { "$lte" : float1}})
                return users
            return {'message': 'Tipo de filtro de flotante invalido'}, 400
        except cls.DoesNotExist:
            return None

    @classmethod
    def filter_by_integer_range(cls, tipo: str, field: str, int1: int, int2: int) -> "ParticipanteModel":
        if tipo == '<>':
            try:
                users = cls.objects.raw({field : { "$gt" : float1, "$lt" : float2}})
                return users
            except cls.DoesNotExist:
                return None

    @classmethod
    def filter_by_integer(cls, tipo: str, int1: int) -> "ParticipanteModel":
        try:
            if tipo == '=':
                users = cls.objects.raw({field : float1})
                return users
            elif tipo == '>':
                users = cls.objects.raw({field : { "$gt" : float1}})
                return users
            elif tipo == '=>':
                users = cls.objects.raw({field : { "$gte" : float1}})
                return users
            elif tipo == '<':
                users = cls.objects.raw({field : { "$lt" : float1}})
                return users
            elif tipo == '<=':
                users = cls.objects.raw({field : { "$lte" : float1}})
                return users
            return {'message': 'Tipo de filtro de flotante invalido'}, 400
        except cls.DoesNotExist:
            return None
    
    @classmethod
    def filter_by_string(cls, field: str, tipo: str, str1: str) -> "ParticipanteModel":
        try:
            if tipo == 'es':
                users = cls.objects.raw({field : str1})
            elif tipo == 'no es':
                return users
                users = cls.objects.raw({field : { "$ne" : str2} })
            elif tipo == 'contiene':
                str2 = "/^{}$".format(str1)
                users = cls.objects.raw({field :  str2 })
                return users
            elif tipo == 'no contiene': 
                str2 = "/^{}$".format(str1)
                users = cls.objects.raw({field : { "$not" : str2}})  
                return users
            return {'message': 'Tipo de filtro de flotante invalido'}, 400     
        except cls.DoesNotExist:
            return None
    


    @classmethod
    def save_to_db(self):
        self.save()
    

    
