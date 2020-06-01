import os
from flask import Flask, render_template, request, send_from_directory, jsonify
from flask_uploads import (UploadSet, configure_uploads, IMAGES,
                              UploadNotAllowed)
from flask_restful import Resource

# os.listdir() will get you everything that's in a directory - files and directories.
# If you want just files, you could either filter this down using os.path:
from os import listdir
from os.path import isfile, join

#UPLOADED_PHOTOS_DEST = 'static/img'
UPLOADED_PHOTOS_DEST = '/var/www/html/items-rest/static/img'
UPLOADED_EMOJIS_DEST = '/var/www/html/items-rest/static/img/openmoji-72x72-color'

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
            pic = send_from_directory('/var/www/html/items-rest/static/img',
                               filename)
            return pic
        except:
            return send_from_directory('/var/www/html/items-rest/static/img/openmoji-72x72-color',
                               filename)

class EmojiList(Resource):
    def get(self):
        onlyfiles = [f for f in listdir('/var/www/html/items-rest/static/img/openmoji-72x72-color') if isfile(join('/var/www/html/items-rest/static/img/openmoji-72x72-color', f))]
        # print(onlyfiles)
        return{"images": onlyfiles}

class ImageList(Resource):
    def get(self):
        onlyfiles = [f for f in listdir('/var/www/html/items-rest/static/img') if isfile(join('/var/www/html/items-rest/static/img', f))]
        print(onlyfiles)
        return{"images": onlyfiles}