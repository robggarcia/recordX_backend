from flask import request, jsonify, session
import jwt
from functools import wraps
import os
from dotenv import load_dotenv
from modules.users import get_single_user

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")


# decorator for verifying the JWT
def token_required():
    token = None
    try:
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
            # return 401 if token is not passed
            if not token:
                return jsonify({'message': 'Token is missing!!'}), 401
        data = jwt.decode(token, JWT_SECRET, algorithms="HS256")
        print(data)
        id = str(data["_id"])
        user = get_single_user(id)
        print(user)
        return user
    except:
        return {'success': False, '_id': 0, "message": "Invalid Token"}

    # @wraps(f)
    # def decorated(*args, **kwargs):
    #     token = None
    #     # jwt is passed in the request header
    #     if 'x-access-token' in request.headers:
    #         token = request.headers['x-access-token']
    #         print(token)
    #     # return 401 if token is not passed
    #     if not token:
    #         return jsonify({'message': 'Token is missing !!'}), 401

    #     try:
    #         # decoding the payload to fetch the stored details
    #         data = jwt.decode(jwt=token, secret=JWT_SECRET, algorithm="HS256")
    #         print(data)
    #         # current_user = User.query\
    #         #     .filter_by(public_id = data['public_id'])\
    #         #     .first()
    #     except:
    #         return jsonify({
    #             'message': 'Token is invalid !!'
    #         }), 401
    #     # returns the current logged in users context to the routes
    #     return f(data, *args, **kwargs)

    return decorated
