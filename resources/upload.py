import os
from flask import Flask, render_template, request, send_from_directory
from flask_uploads import (UploadSet, configure_uploads, IMAGES,
                              UploadNotAllowed)
from flask_restful import Resource

UPLOADED_PHOTOS_DEST = 'static/img'

class ImageUpload(Resource):
    def post(self):
        photos = UploadSet('photos', IMAGES)
        if 'photo' in request.files:
            filename = photos.save(request.files['photo'])
            return filename, 200
        return {'message': 'file is not in request'}


class ImageDownload(Resource):
    def get(self, filename):
        print(filename)
        return send_from_directory(os.getenv("UPLOADED_PHOTOS_DEST"),
                               filename)