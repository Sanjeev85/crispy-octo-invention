from flask import request, jsonify, Blueprint, redirect, session
from model.User import User  # Import the User model
import bcrypt
from middleware.authmiddleware import encode_token

auth = Blueprint('auth', __name__)


@auth.route('/signup', methods=['POST'])
def register():
    try:
        username = request.form.get('signupEmail')
        password = request.form.get('signupPassword')
        name = request.form.get('signupName')
        image_path = f"/static/profile.jpg" 
        print(username, password, name, image_path)


        if  User.objects(email=username).first() == None:
            session['user_info'] = {
                'name': name,
                 'picture': image_path
            }

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            newUser = User(email=username, password=hashed_password, name=name, profile_pic = image_path)
            newUser.save()
        else:
            raise KeyError('User already exist')

        return redirect('/image_upload')
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500


@auth.route('/login', methods=['POST'])
def login():
    try:
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.objects(email=email).first()
        # print(user.to_json())
        print('reached')

        if user:
            if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                token = encode_token(user.email)
                session['user_info'] = {
                    'name': user.name,
                    'picture': '/static/profile.jpg',
                    'token': token
                }

                return redirect('/image_upload')
            else:
                return jsonify({'message': 'Invalid password'}), 401
        else:
            print('else part ')
            return jsonify({'message': 'User not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500
