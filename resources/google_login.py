# Python standard libraries
import json
import os, sys
import sqlite3

# Third party libraries
from flask import Flask, redirect, request, url_for
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from oauthlib.oauth2 import WebApplicationClient
import requests

import functools
import uuid
from bson.objectid import ObjectId
from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_pymongo import PyMongo
from flask_marshmallow import Marshmallow
from ma import ma
from pymodm import MongoModel, EmbeddedMongoModel, fields, connect
from pymodm.errors import ValidationError
from pymongo.errors import DuplicateKeyError
from models.empleado import Empleado, Usuario, Cajero
from schemas.user import UserSchema, EmpSchema
user_schema = UserSchema()
# user_schema = UserSchema()
# Establish a connection to the database.
connect("mongodb://localhost:27017/ej1")

# Configuration
##NOTE! Change to enviroment variables! WARNING!!
GOOGLE_CLIENT_ID = "946048112602-apgp1r9ajs510tu5gu7smjrlhllr5lu7.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "XRpSsSV-BMIBpnKcN7ijg7G9"
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)


# OAuth2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)

class GoogleLogin(Resource):
    @classmethod
    def get(cls):
        # Find out what URL to hit for Google login
        google_provider_cfg = get_google_provider_cfg()
        authorization_endpoint = google_provider_cfg["authorization_endpoint"]

        # Use library to construct the request for login and provide
        # scopes that let you retrieve user's profile from Google
        request_uri = client.prepare_request_uri(
            authorization_endpoint,
            redirect_uri=request.base_url + "/callback",
            scope=["openid", "email", "profile"],
        )
        return redirect(request_uri)

#class GoogleAuthorize(Resource):
class GoogleCallback(Resource):
    @classmethod
    def get(cls):
        # Get authorization code Google sent back to you
        code = request.args.get("code")

        # Find out what URL to hit to get tokens that allow you to ask for
        # things on behalf of a user
        google_provider_cfg = get_google_provider_cfg()
        token_endpoint = google_provider_cfg["token_endpoint"]

        # Prepare and send request to get tokens! Yay tokens!
        token_url, headers, body = client.prepare_token_request(
            token_endpoint,
            authorization_response=request.url,
            redirect_url=request.base_url,
            code=code,
        )
        token_response = requests.post(
            token_url,
            headers=headers,
            data=body,
            auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
        )

        # Parse the tokens!
        client.parse_request_body_response(json.dumps(token_response.json()))

        # Now that we have tokens (yay) let's find and hit URL
        # from Google that gives you user's profile information,
        # including their Google Profile Image and Email
        userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
        uri, headers, body = client.add_token(userinfo_endpoint)
        userinfo_response = requests.get(uri, headers=headers, data=body)

        # We want to make sure their email is verified.
        # The user authenticated with Google, authorized our
        # app, and now we've verified their email through Google!
        if userinfo_response.json().get("email_verified"):
            unique_id = userinfo_response.json()["sub"]
            users_email = userinfo_response.json()["email"]
            picture = userinfo_response.json()["picture"]
            users_name = userinfo_response.json()["given_name"]
            last_name = userinfo_response.json()["family_name"]
            full_name = userinfo_response.json()["name"]
            print(userinfo_response.json())
        else:
            return "User email not available or not verified by Google.", 400

        # Create a user in our db with the information provided
        # by Google
        try:
            Usuario(username="Emmanuel").save()
            myuser = Usuario.objects.get({'username': users_name})
            user = UserSchema().dump(myuser)
            print(str(myuser._id))
        except Usuario.DoesNotExist:
            return {"message": "No se encontro el usuario"}

        # ! Temporality get a token to do transactions.

        access_token = create_access_token(identity=user['_id'], fresh=True)
        refresh_token = create_refresh_token(user['_id'])

        return {"access_token": access_token, "refresh_token": refresh_token}, 200

        # Doesn't exist? Add to database

        # Begin user session by logging the user in

        # Send user back to homepage

        ##NOTE: Save! the id to support changes of email, username ...etc
        #        sub does not change, i think

def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()