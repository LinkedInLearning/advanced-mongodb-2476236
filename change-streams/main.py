import os
import pymongo

client = pymongo.MongoClient(os.environ['CHANGE_STREAM_DB'])
print(client.changestream.collection.insert_one(
    {"message": "hello world"}).inserted_id)


client.changestream.collection.insert_one({
    "_id": 1,
    "user": "Naomi",
    "address": "Old Street 123"})
client.changestream.collection.update_one(
    {"_id": 1},
    {"$set": {"address": "Old street 123"}})
client.changestream.collection.delete_one({"_id": 1})
# client.changestream.collection.drop()
