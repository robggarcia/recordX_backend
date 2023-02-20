from pymongo import MongoClient
from flask import Flask, redirect, url_for, request, session, jsonify
from flask_cors import CORS, cross_origin
import json
from bson import ObjectId, _get_object_size
from typing import Any
import bcrypt
from dotenv import load_dotenv
import os
import jwt
import datetime

from db.mongodb import get_record_collection, get_user_collection
from modules.records import get_all_records, get_single_record, create_record, update_record, delete_record
from modules.users import get_all_users, get_single_user, update_user, register_user, login_user, delete_user
from modules.token_required import token_required
from modules.messages import get_messages, send_message
from modules.favorites import get_favorites, add_favorite, delete_favorite

load_dotenv()


app = Flask(__name__)
app.secret_key = os.getenv('JWT_SECRET')
JWT_SECRET = os.getenv("JWT_SECRET")

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

user_col = get_user_collection()
record_col = get_record_collection()


@app.route('/api/health')
def health():
    return {"success": True, "message": "The server is up and running. It is healthy."}


@app.route('/api/records', methods=['GET', 'POST'])
def records_route():
    if request.method == 'GET':
        records = get_all_records()
        return {"success": True, "data": records}
    if request.method == 'POST':
        user_val = token_required()
        try:
            username = user_val["username"]
        except:
            return {"success": False, "message": "Invalid token provided"}
        try:
            user_val["admin"]
            data = request.get_json()
            # TODO: check to see if record already exists in database
            new_record = create_record(data)
            return {"success": True, "data": new_record}
        except:
            return {"success": False, "message": "Admin access required"}, 401


@app.route('/api/records/<record_id>', methods=['GET', 'PATCH', 'DELETE'])
def album_route(record_id):
    if request.method == 'GET':
        album = get_single_record(record_id)
        return {"success": True, "data": album}
    if request.method == 'PATCH':
        user_val = token_required()
        try:
            username = user_val["username"]
        except:
            return {"success": False, "message": "Invalid token provided"}
        data = request.get_json()
        try:
            user_val["admin"]
            updated = update_record(record_id, data)
            if updated.modified_count > 0:
                return {"success": True, "message": "Record successfully updated"}
            else:
                return {"success": False, "message": "Unable to update record"}, 404
        except:
            return {"success": False, "message": "Admin access required"}, 401
    if request.method == 'DELETE':
        user_val = token_required()
        try:
            username = user_val["username"]
        except:
            return {"success": False, "message": "Invalid token provided"}
        try:
            print("DELETE RECORD CALLED")
            user_val["admin"]
            deleted = delete_record(record_id)
            print(f"Deleted: {deleted.deleted_count}")
            if deleted.deleted_count > 0:
                return {"success": True, "message": "Record successfully deleted"}
            else:
                return {"success": False, "message": "Unable to delete record"}, 404
        except:
            return {"success": False, "message": "Admin access required"}, 401


@app.route("/api/users", methods=["GET", "POST"])
def users_route():
    if request.method == 'GET':
        users = get_all_users()
        return {"success": True, "data": users}


@app.route('/api/users/<user_id>', methods=['GET', 'PATCH', 'DELETE'])
def single_user_route(user_id):
    user_val = token_required()
    try:
        username = user_val["username"]
    except:
        return {"success": False, "message": "Invalid token provided"}
    if user_val:
        if request.method == 'GET':
            user = get_single_user(user_id)
            return {"success": True, "data": user}
        if request.method == 'PATCH':
            data = request.get_json()
            try:
                updated = update_user(user_id, data)
                if updated.modified_count > 0:
                    return {"success": True, "message": "User successfully updated"}
                else:
                    return {"success": False, "message": "Unable to update user"}, 404
            except:
                return {"success": False, "message": "Invalid user id"}, 500
        if request.method == 'DELETE':
            try:
                user_val["admin"]
                print("DELETE USER CALLED")
                deleted = delete_user(user_id)
                print(f"Deleted: {deleted.deleted_count}")
                if deleted.deleted_count > 0:
                    return {"success": True, "message": "User successfully deleted"}
                else:
                    return {"success": False, "message": "Unable to delete user"}, 404
            except:
                return {"success": False, "message": "Admin access required"}, 401
    return {'success': False, 'message': 'Must be logged in to perform this action'}, 401


@app.route("/api/users/register", methods=['POST'])
def register():
    username = request.get_json()["username"]
    email = request.get_json()["email"]
    password = request.get_json()["password"]
    print(username, email, password)

    user_found = user_col.find_one({"username": username})
    email_found = user_col.find_one({"email": email})
    try:
        if email_found or user_found:
            message = 'This user already exists in database'
            return {"success": False, "message": message}
        else:
            new_user = register_user(username, email, password)
            print(f"New User Created: {new_user}")
            new_email = new_user["email"]
            _id = str(new_user["_id"])
            print("creating token")
            # token = jwt.encode(
            #     {"email": email, "username": username, "_id": _id}, JWT_SECRET, algorithm="HS256")
            token = jwt.encode(
                {"_id": _id, "email": email, "username": username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=45)}, JWT_SECRET, algorithm="HS256")
            print(token)
            return {"success": True, "message": f"New User created with email: {new_email}", "token": token}
    except:
        return {"success": False, "message": "Invalid input. Unable to register user"}, 500


@app.route("/api/users/login", methods=["POST"])
def login():
    messsage = 'Please login to your account'
    if request.method == "POST":
        email = request.get_json()["email"]
        password = request.get_json()["password"]

        # if session["email"] == email:
        #     # return redirect(url_for("logged_in"))
        #     return "User already logged in"

        email_found = user_col.find_one({"email": email})
        if email_found:
            email_val = email_found["email"]
            passwordcheck = email_found["password"]
            _id = str(email_found["_id"])
            username = email_found["username"]
            print(f"user Id:  {id}")

            if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):

                token = jwt.encode(
                    {"_id": _id, "email": email_val, "username": username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=45)}, JWT_SECRET, algorithm="HS256")
                return {"success": True, "message": f"User logged in with email: {email_val}", "token": token}
            else:
                # if "email" in session:
                #     return "already logged in"
                message = 'Wrong password'
                return {"success": False, "message": message}
        else:
            message = 'Email not found'
            return {"success": False, "message": message}
    return {"success": False, "message": message}


@app.route("/api/users/logout", methods=["POST"])
def logout():
    session["email"] = None
    return {'success': True, 'message': 'User logged out'}


@app.route('/api/messages', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def messages():
    user_val = token_required()
    try:
        from_user = user_val["username"]
    except:
        return {"success": False, "message": "Invalid token provided"}
    if request.method == 'GET':
        # get all messages from a user
        from_id = user_val["_id"]["$oid"]
        messages = get_messages(from_id)
        return {'success': True, 'username': from_user, 'data': messages}
    if request.method == 'POST':
        # send a message to a specific user
        to_user = request.get_json()["to_user"]
        message = request.get_json()["message"]
        print(from_user, to_user, message)
        updated = send_message(from_user, to_user, message)
        if updated.modified_count > 0:
            return {"success": True, "message": "Message sent successfuly"}
        else:
            return {"success": False, "message": "Unable to send message"}, 404


@app.route('/api/records/favorites', methods=['GET', 'POST', 'DELETE'])
def favorite():
    user_val = token_required()
    try:
        user_id = user_val["_id"]["$oid"]
    except:
        return {"success": False, "message": "Invalid token provided"}
    if request.method == 'GET':
        # get list of all favorite albums
        favorites = get_favorites(user_id)
        return {'success': True, 'data': favorites}
    if request.method == 'POST':
        record_id = request.get_json()['record_id']
        result = add_favorite(user_id, record_id)
        if result.modified_count > 0:
            return {"success": True, "message": "Album added to favorites"}
        else:
            return {"success": False, "message": "Unable to add to favorites"}, 404
    if request.method == 'DELETE':
        record_id = request.get_json()['record_id']
        result = delete_favorite(user_id, record_id)
        if result.modified_count > 0:
            return {"success": True, "message": "Album removed to favorites"}
        else:
            return {"success": False, "message": "Unable to remove from favorites"}, 404


@app.errorhandler(404)
def handle_404(e):
    return {'success': False, 'message': 'Error. Not found'}, 404


@app.route("/")
def api_working():
    return "welcome to the recordX api"


if __name__ == "__main__":
    app.run(host='localhost', port=3500, debug=True)
