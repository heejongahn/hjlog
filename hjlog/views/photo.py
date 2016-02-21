from flask import request, jsonify, url_for
from flask.ext.login import login_required
from werkzeug import secure_filename
import os
import time

def register(app):
    @app.route('/photoajax', methods=['POST'])
    @login_required
    def photo_ajax():
        if request.method == 'POST':
            photo = request.files['file']
            if photo and allowed_file(photo.filename):
                filename = secure_filename(str(time.time())+photo.filename)
                photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                url = url_for('static', filename='image/photo/'+filename)
                return jsonify(correct=True, name=filename, url=url)

            elif not allowed_file(photo.filename):
                return jsonify(correct=False)

    ####################
    # Helper functions #
    ####################
    def allowed_file(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
