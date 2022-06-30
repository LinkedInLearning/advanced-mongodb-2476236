import os
import pymongo
from pymongo.server_api import ServerApi
from bson.json_util import dumps

client = pymongo.MongoClient(
    os.environ['DB'],
    server_api=ServerApi("1"))

change_stream = client.bigfiles["fs.files"].watch([{
    '$match': {
        'operationType': 'insert'
    }
}])

for change in change_stream:
    print(dumps(change))
    print('')  # for readability only
