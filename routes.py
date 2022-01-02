"""routes module"""
import os
import sys
from flask import request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from flask_jwt_extended import jwt_required, current_user, set_access_cookies
from models import User, Task
from app import app, jwt


UPLOAD_FOLDER = '/upload_folder'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# ТАСК АПИ


@app.route('/', methods=['GET'])
def index():
    """routes method"""
    return '<h1>159.65.85.134</h1>'


@app.route('/user', methods=['POST'])
def user():
    """routes method"""

    params = request.form

    if 'login' not in params or 'pas' not in params:
        return {
            "msg": 'требуется пароль или логин'
        }, 400

    user = User.authenticate(**params)

    if user == 0:
        user = User(**params)
        access_token = user.get_token()
        response = jsonify({"msg": user.save_to_db(),
                            "access_token": access_token})
        set_access_cookies(response, access_token)
        return response, 201
    elif user == 1:
        return {
            "msg": 'неправлиьный пароль',
        }, 400
    else:
        access_token = user.get_token()
        response = jsonify({'access_token': access_token})
        set_access_cookies(response, access_token)
        return response, 201


@app.route('/todo', methods=['POST'])
@jwt_required()
def todo():
    """routes method"""

    params = request.form
    user_id = current_user.id
    task = Task(**params)
    task.user_id = user_id
    task.save_to_db()
    return 'задача добавлена под номером ' + str(task.id), 201


@app.route('/todo/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_todo(id):
    """routes method"""

    task = Task.query.filter(Task.id == id).first()
    if task is None:
        return 'задача подно номером ' + str(id) + ' не существует', 418
    else:
        task.delete_from_db()
        return 'задача под номером ' + str(id) + ' успешно удалена', 202


@app.route('/todo/<int:id>', methods=['PUT'])
@jwt_required()
def change_todo(id):
    """routes method"""

    task = Task.query.filter(Task.id == id).first()
    if task is None:
        return 'задача под номером ' + str(id) + 'не существует', 418
    else:
        task.description = request.form['description']
        task.save_to_db()
        return 'задача под номером ' + str(id) + ' успешно изменена', 202


@app.route('/todo', methods=['GET'])
@jwt_required()
def get_todo():
    """routes method"""

    tasks = current_user.tasks
    response = {'login': current_user.login}
    for task in tasks:
        str_to_update = {f'id: {task.id}': f'описание: {task.description}'}
        response.update(str_to_update)
    print(response, file=sys.stderr)
    return response, 200


@ jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    """routes method"""

    identity = jwt_data["sub"]
    return User.query.filter_by(login=identity).one_or_none()
###

# ФАЙЛОВОЕ АПИ


@app.route('/files', methods=['POST'])
def files_post():
    """routes method"""

    if 'file' not in request.files:
        return {'res': 'пустое тело запроса, прикрепите файл'}, 400

    file = request.files['file']
    if allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return {'response': 'файл загружен'}, 201

    return {'response': 'недопустимое расширение файла'}, 406


@app.route('/files', methods=['GET'])
def files_get():
    """routes method"""

    path = app.config['UPLOAD_FOLDER']
    files_list = os.listdir(path)
    files = {}
    if not files_list:
        return {'response': 'нет загруженных файлов'}, 200

    for file in files_list:
        files |= ({file: str(os.stat(path + file).st_size) + ' bytes'})
    return files, 200


@app.route("/files/<string:name>", methods=['GET'])
def download_file(name):
    """routes method"""

    files_list = os.listdir(app.config['UPLOAD_FOLDER'])
    if name not in files_list:
        return {'response': f'{name} - файл не существует'}, 404

    return send_from_directory(
        app.config['UPLOAD_FOLDER'], name, as_attachment=False), 200


@app.route("/files/<string:name>", methods=['DELETE'])
def delete_file(name):
    """routes method"""

    if not os.path.exists(app.config['UPLOAD_FOLDER']+name):
        return {'response': f'{name} - файл не существует'}, 404
    os.remove(app.config['UPLOAD_FOLDER']+name)
    return {'response': f'{name} - файл удалён'}, 200


def allowed_file(filename):
    """routes method"""

    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
###
