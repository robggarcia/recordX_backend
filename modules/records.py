from db.mongodb import get_record_collection, create_object
from bson import ObjectId, json_util
import json


def get_all_records():
    record_col = get_record_collection()
    data = record_col.find().sort("artist")
    records = create_object(data)
    return records


def get_single_record(record_id):
    record_col = get_record_collection()
    data = record_col.find_one({"_id": ObjectId(record_id)})
    album = json.loads(json_util.dumps(data))
    return album


def create_record(data):
    record_col = get_record_collection()
    new_id = record_col.insert_one(data).inserted_id
    data = record_col.find_one({"_id": ObjectId(new_id)})
    new_record = json.loads(json_util.dumps(data))
    return new_record


def update_record(record_id, data):
    record_col = get_record_collection()
    updated = record_col.update_one(
        {"_id": ObjectId(record_id)}, {"$set": data})
    return updated


def delete_record(record_id):
    record_col = get_record_collection()
    deleted = record_col.delete_one({"_id": ObjectId(record_id)})
    return deleted
