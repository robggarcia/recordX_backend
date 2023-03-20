from flask import request, jsonify, session
import jwt
from functools import wraps
import os
from dotenv import load_dotenv
from modules.users import get_single_user

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")


# verifying the JWT
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
