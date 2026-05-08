import functools
from flask import jsonify, request
from datetime import datetime, timezone
from uuid import UUID

from db import db

from models.auth_tokens import AuthTokens

def validate_uuid4(uuid_string):
    try:
        UUID(uuid_string, version=4)
        return True
    except:
        return False



# def validate_token():
#     auth_header = request.headers.get('Authorization')
#     if not auth_header or not auth_header.startswith("Bearer "):
#         return False

#     token = auth_header.split(" ", 1)[1]
#     # if not auth_header or not validate_uuid4(auth_header):
#     #     return False

#     existing_token = db.session.query(AuthTokens).filter(AuthTokens.auth_token == auth_header).first()

#     if existing_token:
#         if existing_token.expiration_date > datetime.now():
#             return existing_token

#     return False


def validate_token():
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        return False

    token = auth_header.split(" ", 1)[1]

    if not validate_uuid4(token):
        return False

    existing_token = (
        db.session
        .query(AuthTokens)
        .filter(AuthTokens.auth_token == token)
        .first()
    )

    if existing_token and existing_token.expiration_date > datetime.now():
        return existing_token

    return False



def fail_response():
    return jsonify({"message": "authentication required"}), 401



def authenticate(func):
    @functools.wraps(func)
    def wrapper_authenticate(*args,**kwargs):
        auth_info = validate_token()

        return(
            func(*args, **kwargs) if auth_info else fail_response()
        )
    
    return wrapper_authenticate


def authenticate_return_auth(func):
    @functools.wraps(func)
    def wrapper_authenticate(*args, **kwargs):
        auth_info = validate_token()
      
        kwargs['auth_info'] = auth_info

        return (
            func(*args, **kwargs) if auth_info else fail_response()
        )

    return wrapper_authenticate
