import os
import pymongo
import time
from bson.json_util import dumps

client = pymongo.MongoClient(os.environ['CHANGE_STREAM_DB'])


def run_change_stream(resume_token, sleep):
    try:
        with client.changestream.collection.watch() as stream:
            for change in stream:
                print(dumps(change))
                print('')  # for readability only
                resume_token = stream.resume_token
                sleep = 1
    except pymongo.errors.PyMongoError:
        # The ChangeStream encountered an unrecoverable error or the
        # resume attempt failed to recreate the cursor.
        if resume_token is None:
            # There is no usable resume token because there was a
            # failure during ChangeStream initialization.
            print("unrecoverable error")
        else:
            # Use the interrupted ChangeStream's resume token to create
            # a new ChangeStream. The new stream will continue from the
            # last seen insert change without missing any events.
            time.sleep(sleep)
            sleep = sleep * 2
            run_change_stream(resume_token, sleep)


run_change_stream(None, 1)
