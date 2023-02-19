from db.mongodb import create_object, get_user_collection
from bson import ObjectId, json_util
import json


def get_messages(user_id):
    user_col = get_user_collection()
    data = user_col.find_one({"_id": ObjectId(user_id)}, {
                             "username": 1, "messages": 1})
    messages = json.loads(json_util.dumps(data))
    return messages


def send_message(from_user, to_user, message):
    user_col = get_user_collection()
    data = {'from_user': from_user, 'message': message}
    try:
        # try pushing into the messages array
        updated = user_col.update_one({"username": to_user}, {
                                      "$push": {'messages': data}})
    except:
        # otherwise create a new array for the user
        updated = user_col.update_one({"username": to_user}, {
                                      "$set": {'messages': [data]}})
    return updated
