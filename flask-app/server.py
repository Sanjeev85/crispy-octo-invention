from flask import Flask, make_response, jsonify, request, render_template, session, redirect
from controller.auth_controller import auth 
from controller.upload_image import upload
from controller.google_auth import googleAuth
from flask_cors import CORS
from dotenv import load_dotenv
from flask_limiter import Limiter
from middleware.authmiddleware import auth_middleware
from flask_limiter.util import get_remote_address
from mongoengine import connect
from flask import Flask, request, session
from dotenv import load_dotenv
import os


load_dotenv()

app = Flask(__name__)
app.config.from_object('config')
CORS(app)
Limiter(key_func=get_remote_address, app = app, default_limits=['5/minute'])
connect(os.getenv('db_name'))

app.static_folder = 'upload'  
app.static_url_path = '/static'



# Register the views from the views.py file
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(googleAuth, url_prefix='/googleauth')
app.register_blueprint(upload, url_prefix= '/image')



# apply jwt auth to /image blueprint
@app.before_request
def apply_auth_middleware():
    if request.blueprint == 'image':
        auth_middleware()

@app.route('/')
def index():
    return redirect('/login')


@app.route('/login', methods=['GET'])
def login_form():
    return render_template('login.html') 

@app.route('/signup', methods=['GET'])
def signup_form():
    return render_template('register.html') 

@app.route('/image_upload')
def images():
    user_info = session['user_info']
    return render_template('imageUpload.html', user_info=user_info)

@app.route('/show_images')
def show_images():
    return render_template('showImage.html')


@app.errorhandler(429)
def ratelimit_handler(e):
    return make_response(
            jsonify(msg=f"ratelimit exceeded {e.description}")
            , 429
    )

@app.route('/logout') 
def logout():
    session.clear()
    return 'Logged Out Successfully'





    

if __name__ == '__main__':
    app.run(debug=True)