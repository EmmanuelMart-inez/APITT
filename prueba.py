#from models.participante import ParticipanteModel
from schemas.participante import ParticipanteSchema
from marshmallow import pprint

p_schema = ParticipanteSchema()

pdic = {

    "nombre": "Emmanuel",
    "fecha_nacimiento": "2020-06-06T21:00:00"
}

rest = p_schema.load(pdic)
print(rest)
if "nombre" in rest:
    print("tiene el campo")

rest2 = p_schema.dump(rest)
pprint(type(rest2))

print("hola")