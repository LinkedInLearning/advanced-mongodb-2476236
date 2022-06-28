import os
import pymongo
from bson.json_util import dumps

client = pymongo.MongoClient(os.environ['CHANGE_STREAM_DB'])
change_stream = client.changestream.collection.watch([{
    '$match': {
        'operationType': 'update',
        'updateDescription.updatedFields.address': {'$exists': True}
    }
}])
for change in change_stream:
    print(dumps(change))
    print('')  # for readability only
