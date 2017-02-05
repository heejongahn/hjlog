import os
import time

import boto3
from flask import request, jsonify, url_for
from flask.ext.login import login_required
from werkzeug import secure_filename

s3_client = boto3.client('s3')


def register(app):
    @app.route('/photoajax', methods=['POST'])
    @login_required
    def photo_ajax():
        photo = request.files['file']
        filename = secure_filename(str(time.time())+photo.filename)

        if photo and allowed_file(filename, app.config['ALLOWED_EXTENSIONS']):
            # Prodution
            if app.config['S3_BUCKET_NAME'] is not None:
                s3_client.upload_fileobj(photo,
                                         app.config['S3_BUCKET_NAME'],
                                         filename)
                url = app.config['S3_BASE_URL'] + filename
            # Development
            else:
                photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                url = url_for('static', filename='image/photo/'+filename)

            return jsonify(correct=True, name=filename, url=url)

        return jsonify(correct=False)

####################
# Helper functions #
####################


def allowed_file(filename, allowed_extensions):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in allowed_extensions
