from flask import Flask, render_template, request, send_from_directory
from flask_uploads import (UploadSet, configure_uploads, IMAGES,
                              UploadNotAllowed)
from flask_restful import Resource

class ImageUpload(Resource):
    @classmethod
    def post(self):
        photos = UploadSet('photos', IMAGES)
        if 'photo' in request.files:
            filename = photos.save(request.files['photo'])
            return filename
        return {'message': 'upload template'}

class ImageDownload(Resource):
    @classmethod
    def get(self, filename):
        photos = UploadSet('photos', IMAGES)
        return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'],
                               filename)
"""
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        return filename
    return {'message': 'upload template'}

@app.route('/upload/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'],
                               filename)

if __name__ == '__main__':
    app.run(debug=True)
"""