from flask import Flask, send_from_directory, current_app
from PIL import Image
from flask import Blueprint, jsonify, request
import os



upload = Blueprint('image', __name__)



@upload.route('/upload', methods=['POST'])
def upload_image():
    try:
        file = request.files['file']
        if not os.path.exists(current_app.static_folder):
            os.mkdir(current_app.static_folder)

        filename = os.path.join(current_app.static_folder, file.filename)
        file.save(filename)


        return jsonify({'msg':'File Uploaded Successfully'})
    except:
        return jsonify(msg='Internal Server Error'), 500

@upload.route('/get_file_details', methods=['GET'])
def get_filenames():
    return jsonify({'images' : os.listdir(current_app.static_folder)})

    
@upload.route('/')
def get():
    return jsonify({'msg': 'singer'})
