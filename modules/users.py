from db.mongodb import get_user_collection, create_object
from bson import ObjectId, json_util
import bcrypt
import json


def get_all_users():
    user_col = get_user_collection()
    data = user_col.find({}, {"password": 0}).sort("admin", -1)
    users = create_object(data)
    return users


def get_single_user(user_id):
    user_col = get_user_collection()
    data = user_col.find_one({"_id": ObjectId(user_id)})
    user = json.loads(json_util.dumps(data))
    return user


def register_user(username, email, password):
    user_col = get_user_collection()
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    user_input = {'username': username, 'email': email, 'password': hashed}
    user_col.insert_one(user_input)
    new_user = user_col.find_one({"email": email})
    return new_user


def login_user(username, password):
    return users


def update_user(user_id, data):
    user_col = get_user_collection()
    updated = user_col.update_one({"_id": ObjectId(user_id)}, {"$set": data})
    return updated


def delete_user(user_id):
    user_col = get_user_collection()
    deleted = user_col.delete_one({"_id": ObjectId(user_id)})
    return deleted


def send_message(id, to_user, message):
    return data
