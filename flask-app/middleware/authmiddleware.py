import jwt
from flask import request, jsonify
import datetime
import os

SECRET_KEY = os.getenv('hash-secret')


def encode_token(email: str):
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        'iat': datetime.datetime.utcnow(),
        'email': email
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')


def decode_token(token):
    try:
        decoded_payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return decoded_payload
    except jwt.ExpiredSignatureError:
        return jsonify(message='Token Expired'), 401
    except jwt.InvalidTokenError:
        return jsonify(message='Invalid token'), 401


def auth_middleware():
    token = request.headers.get('Authorization', None)
    if token == None:
        return jsonify(message='Kindly Login First'), 401

    try:
        decoded_payload = decode_token(token=token)
        request.decoded_payload = decoded_payload

    except jwt.ExpiredSignatureError:
        return jsonify(message='Token Expired'), 401
    except jwt.InvalidTokenError:
        return jsonify(message='Invalid token'), 401
    finally:
        return jsonify(message='No Token Found'), 404
