from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from marshmallow import ValidationError
from dotenv import load_dotenv

load_dotenv(".env")

from ma import ma
from oa import oauth
from models.empleado import Usuario
from resources.facebook_login import FacebookLogin, FacebookAuthorize
from resources.google_login import GoogleLogin, GoogleCallback
from resources.participante import Participante, ParticipanteList, WelcomeParticipante, Autenticacion, LoginSocialNetwork, RegistroSocialNetwork
from resources.upload import ImageUpload, ImageDownload
from resources.tarjeta import TarjetaSellos, TarjetaPuntos
from resources.notificaciones import NotificacionList #Task:Desacoplar list
from resources.premio import Premio, PremioList #Task:Desacoplar list
from resources.movimiento import MovimientoList, Movimiento
from resources.encuesta import Encuesta, EncuestaParticipante, ControlEncuestas, AdministradorEncuestas
from resources.ayuda import  AyudaList
from resources.producto import CatalogoList, Catalogo

from flask_uploads import (UploadSet, configure_uploads, IMAGES,
                              UploadNotAllowed)

app = Flask(__name__)
app.config.from_object("default_config")
app.config.from_envvar("APPLICATION_SETTINGS")
app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
api = Api(app)
jwt = JWTManager(app)

"""
@app.before_first_request
def create_tables():
    db.create_all()
"""


@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400


# api.add_resource(UserRegister, "/register")
# api.add_resource(User, "/user/<int:user_id>")
# api.add_resource(UserLogin, "/login")
api.add_resource(FacebookLogin, "/login/facebook")
api.add_resource(
    FacebookAuthorize, "/login/facebook/authorized", endpoint="facebook.authorize"
)
api.add_resource(GoogleLogin, "/login/google")
api.add_resource(GoogleCallback, "/login/google/callback")
api.add_resource(Participante, "/participante/<string:id>")
api.add_resource(WelcomeParticipante, "/wparticipante/<string:id>")
api.add_resource(ParticipanteList, "/participante")
api.add_resource(TarjetaSellos, "/tarjetasellos/<string:id>")
api.add_resource(TarjetaPuntos, "/tarjetapuntos/<string:id_participante>")
api.add_resource(NotificacionList, "/notificaciones/<string:id>")
api.add_resource(Catalogo, "/catalogo/<string:vartipo>")
api.add_resource(CatalogoList, "/catalogo")
api.add_resource(Premio, "/premios")
api.add_resource(PremioList, "/premios/<string:id>")
api.add_resource(MovimientoList, "/movimientos/<string:id_participante>")
api.add_resource(Movimiento, "/movimiento/<string:id_movimiento>")
api.add_resource(Encuesta, "/encuesta")
api.add_resource(EncuestaParticipante, "/encuesta/<string:id_encuesta>")
api.add_resource(ControlEncuestas, "/controlencuestas/<string:id_participanteencuesta>")
api.add_resource(AdministradorEncuestas, "/controlencuestas")
api.add_resource(AyudaList, "/ayuda")
api.add_resource(ImageUpload, "/upload")
api.add_resource(ImageDownload, "/download/<string:filename>")
api.add_resource(Autenticacion, "/autenticacion")
api.add_resource(LoginSocialNetwork, "/autenticacion/<string:socialNetwork>")
api.add_resource(RegistroSocialNetwork, "/registro/<string:socialNetwork>")
# api.add_resource(SetPassword, "/user/password")

if __name__ == "__main__":
    ma.init_app(app)
    # oauth.init_app(app)
    #app.run(ssl_context="adhoc")
    app.run(port=5000)



# TODO: 

# Refactorizar
# Clases de servicios y modelos
    # Codigos
    # Movimientos
    # Encuesta (Cerrada y abierta)
    # Logout