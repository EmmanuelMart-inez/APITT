from pymodm import connect, fields, MongoModel, EmbeddedMongoModel
from models.participante import ParticipanteModel
from bson.objectid import ObjectId
# Establish a connection to the database.
connect('mongodb://localhost:27017/ej1')


class EncuestaOpcionesModel(MongoModel):
    # descripcion = fields.CharField(default="")
    calificacion = fields.CharField()
    rubrica = fields.FloatField()
    icon = fields.URLField()
    # Icono sirve para las encuestas del tipo
    # emogie y puede ser un gif animado

class EncuestaPaginaModel(MongoModel):
    titulo = fields.CharField()
    tipo = fields.CharField()
    metrica = fields.CharField()
    opciones = fields.EmbeddedDocumentListField(
        EncuestaOpcionesModel, blank=True)
        # EncuestaOpcionesModel, default=[])


class EncuestaModel(MongoModel):
    titulo = fields.CharField()
    categoria = fields.CharField()
    fecha_creacion = fields.DateTimeField()
    metrica = fields.CharField()
    puntos = fields.FloatField()
    paginas = fields.EmbeddedDocumentListField(
        EncuestaPaginaModel, default=[], required=False)

    @classmethod
    def find_by_id(cls, _Objectid: str) -> "EncuestaModel":
        try:
            oid = ObjectId(_Objectid)
            notif = cls.objects.get({'_id': oid})
            print(notif)
            return notif
        except cls.DoesNotExist:
            return None
    
    
class ParticipantesEncuestaModel(MongoModel):
    id_participante = fields.CharField()
    id_encuesta = fields.CharField()
    fecha_respuesta = fields.DateTimeField()
    estado = fields.CharField()
    respuestas = fields.ListField(fields.CharField(), default=[], required=False)
    # fecha_creacion = AFTER

    @classmethod
    def find_by_id(cls, _Objectid: str) -> "ParticipantesEncuestaModel":
        try:
            oid = ObjectId(_Objectid)
            notif = cls.objects.get({'_id': oid})
            print(notif)
            return notif
        except cls.DoesNotExist:
            return None

    @classmethod
    def filter_by_date_range(cls, date_start: str, date_end: str, field: str) -> "ParticipantesEncuestaModel":
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
            
    @classmethod
    def filter_by_date(cls, date_start: str, tipo: str, scale: str, scale_value: int, field: str) -> "ParticipantesEncuestaModel":
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
    def filter_by_float_range(cls, tipo: str, field: str, float1: float, float2: float) -> "ParticipantesEncuestaModel":
        if tipo == '<>':
            try:
                users = cls.objects.raw({field : { "$gte" : float1, "$lte" : float2}})
                return users
            except cls.DoesNotExist:
                return None

    @classmethod
    def filter_by_float(cls, tipo: str, float1: float, field: str) -> "ParticipantesEncuestaModel":
        try:
            if tipo == '=':
                users = cls.objects.raw({field : float1})
                return users
            elif tipo == '>':
                users = cls.objects.raw({field : { "$gt " : float1}})
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
    def filter_by_integer_range(cls, tipo: str, field: str, int1: int, int2: int) -> "ParticipantesEncuestaModel":
        if tipo == '<>':
            try:
                users = cls.objects.raw({field : { "$gte" : int1, "$lte" : int2}})
                return users
            except cls.DoesNotExist:
                return None

    @classmethod
    def filter_by_integer(cls, tipo: str, int1: int, field: str) -> "ParticipantesEncuestaModel":
        try:
            if tipo == '=':
                users = cls.objects.raw({field : int1})
                return users
            elif tipo == '>':
                users = cls.objects.raw({field : { "$gt" : int1}})
                return users
            elif tipo == '=>':
                users = cls.objects.raw({field : { "$gte" : int1}})
                return users
            elif tipo == '<':
                users = cls.objects.raw({field : { "$lt" : int1}})
                return users
            elif tipo == '<=':
                users = cls.objects.raw({field : { "$lte" : int1}})
                return users
            return {'message': 'Tipo de filtro de flotante invalido'}, 400
        except cls.DoesNotExist:
            return None
    
    @classmethod
    def filter_by_string(cls, field: str, tipo: str, str1: str) -> "ParticipantesEncuestaModel":
        try:
            if tipo == 'es':
                users = cls.objects.raw({field : str1})
                return users
            elif tipo == 'no es':
                users = cls.objects.raw({field : { "$ne" : str1 }})
                return users
            elif tipo == 'contiene':
                users = cls.objects.raw({field : {"$regex": str1} })
                return users
            elif tipo == 'no contiene': 
                users = cls.objects.raw({field : { "$not" : {"$regex": str1} }})  
                return users
            return {'message': 'Tipo de filtro de flotante invalido'}, 400     
        except cls.DoesNotExist:
            return None
