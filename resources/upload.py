import os
from flask import Flask, render_template, request, send_from_directory, jsonify
from flask_uploads import (UploadSet, configure_uploads, IMAGES,
                              UploadNotAllowed)
from flask_restful import Resource

# os.listdir() will get you everything that's in a directory - files and directories.
# If you want just files, you could either filter this down using os.path:
from os import listdir
from os.path import isfile, join

UPLOADED_PHOTOS_DEST='/mnt/a/Escom_Semestre9/Bubbletown/Bubbletown_api_v3_stable/static/img'
UPLOADED_EMOJIS_DEST = '/mnt/a/Escom_Semestre9/Bubbletown/Bubbletown_api_v3_stable/static/img/openmoji-72x72-color'
# UPLOADED_PHOTOS_DESTs = '/var/www/html/items-rest/static/img'

class ImageUpload(Resource):
    def post(self):
        photos = UploadSet('photos', IMAGES)
        if 'photo' in request.files:
            filename = photos.save(request.files['photo'])
            return filename, 200
        return {'message': 'file is not in request'}


class ImageDownload(Resource):
    def get(self, filename):
        # print(filename)
        try:
            pic = send_from_directory(os.getenv("UPLOADED_PHOTOS_DEST"),
                               filename)
            return pic
        except:
            return send_from_directory(os.getenv("UPLOADED_EMOJIS_DEST"),
                               filename)

class EmojiList(Resource):
    def get(self):
        onlyfiles = [f for f in listdir(os.getenv("UPLOADED_EMOJIS_DEST")) if isfile(join(os.getenv("UPLOADED_EMOJIS_DEST"), f))]
        # print(onlyfiles)
        return{"images": onlyfiles}

class ImageList(Resource):
    def get(self):
        onlyfiles = [f for f in listdir(os.getenv("UPLOADED_PHOTOS_DEST")) if isfile(join(os.getenv("UPLOADED_PHOTOS_DEST"), f))]
        # print(onlyfiles)
        return{"images": onlyfiles}
        