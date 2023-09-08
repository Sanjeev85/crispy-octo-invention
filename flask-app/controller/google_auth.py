import requests
from flask import Blueprint, Flask, request, redirect, session
import os
from dotenv import load_dotenv
import json


load_dotenv()

googleAuth = Blueprint('googleauth', __name__)

googleAuth.secret_key = os.getenv('session_secret')  # Change this to a strong, random secret key

# Google OAuth 2.0 credentials
GOOGLE_CLIENT_ID = os.getenv('CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('CLIENT_SECRET')
# Update this to match your project's settings
GOOGLE_REDIRECT_URI = 'http://localhost:5000/googleauth/callback'


# Google OAuth endpoints
GOOGLE_AUTH_URL = 'https://accounts.google.com/o/oauth2/auth'
GOOGLE_TOKEN_URL = 'https://accounts.google.com/o/oauth2/token'
GOOGLE_USER_INFO_URL = 'https://www.googleapis.com/oauth2/v1/userinfo'


@googleAuth.route('/')
def index():
    if 'google_token' in session:
        access_token, refresh_token = session['google_token']
        if is_token_valid(access_token):
            user_info = get_user_info(access_token)
            json_string = json.dumps(user_info, indent=4)
            print(json_string)
            return f'Logged in as: {user_info["email"]}'
        else:
            # Access token has expired; attempt to refresh it
            new_access_token = refresh_access_token(refresh_token)
            if new_access_token:
                session['google_token'] = (new_access_token, refresh_token)
                user_info = get_user_info(new_access_token)
                return f'Logged in as: {user_info["email"]}'
    return redirect('/googleauth/login')


@googleAuth.route('/login')
def login():
    scopes = 'https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile'

    # oAuth2 Authorization url
    auth_url = f'{GOOGLE_AUTH_URL}?client_id={GOOGLE_CLIENT_ID}&redirect_uri={GOOGLE_REDIRECT_URI}&response_type=code&scope={scopes}&prompt=consent'
    return redirect(auth_url)


@googleAuth.route('/callback')
def callback():
    # Handle the callback from Google after successful authentication
    code = request.args.get('code')
    
    if code:
        # Exchange the code for an access token and refresh token
        tokens = exchange_code_for_tokens(code)
        if tokens:
            session['google_token'] = tokens
            user_info = get_user_info(tokens[0])

            if 'google_token' in session:
                session['user_info'] = user_info
                return redirect('/image_upload')
            else:
                return 'Session not set. Authentication failed.'
        else:
            return 'Failed to exchange code for tokens.'
    else:
        return 'Authentication failed.'


def is_token_valid(access_token):
    return True


def refresh_access_token(refresh_token):
    data = {
        'refresh_token': refresh_token,
        'client_id': GOOGLE_CLIENT_ID,
        'client_secret': GOOGLE_CLIENT_SECRET,
        'grant_type': 'refresh_token',
    }
    response = requests.post(GOOGLE_TOKEN_URL, data=data)
    if response.status_code == 200:
        tokens = response.json()
        return tokens.get('access_token')
    else:
        return None


def exchange_code_for_tokens(code):
    data = {
        'code': code,
        'client_id': GOOGLE_CLIENT_ID,
        'client_secret': GOOGLE_CLIENT_SECRET,
        'redirect_uri': GOOGLE_REDIRECT_URI,
        'grant_type': 'authorization_code',
    }
    response = requests.post(GOOGLE_TOKEN_URL, data=data)
    if response.status_code == 200:
        tokens = response.json()
        return (tokens.get('access_token'), tokens.get('refresh_token'))
    else:
        return None


def get_user_info(access_token):
    user_info_response = requests.get(GOOGLE_USER_INFO_URL, params={
                                      'access_token': access_token})
    if user_info_response.status_code == 200:
        user_info = user_info_response.json()
        return user_info
    else:
        return None
