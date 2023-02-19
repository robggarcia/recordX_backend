from db.mongodb import get_user_collection
from bson import ObjectId, json_util
import json
from modules.records import get_single_record


def get_favorites(user_id):
    user_col = get_user_collection()
    data = user_col.find_one({"_id": ObjectId(user_id)}, {
                             "username": 1, "favorites": 1})
    favorites = json.loads(json_util.dumps(data))
    return favorites


def add_favorite(user_id, record_id):
    user_col = get_user_collection()
    record = get_single_record(record_id)
    data = {'record_id': record_id, 'record': record}
    try:
        # try pushing into the favorites array
        updated = user_col.update_one({"_id": ObjectId(user_id)}, {
                                      "$push": {'favorites': data}})
    except:
        # otherwise create a new array for the user
        updated = user_col.update_one({"_id": ObjectId(user_id)}, {
                                      "$set": {'favorites': [data]}})
    return updated


def delete_favorite(user_id, record_id):
    user_col = get_user_collection()
    record = get_single_record(record_id)
    deleted = user_col.update_one({"_id": ObjectId(user_id)}, {
                                  '$pull': {'favorites': {"record_id": record_id}}})
    return deleted
