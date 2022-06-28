import gridfs
import os
import pymongo

db = pymongo.MongoClient(os.environ['CHANGE_STREAM_DB']).bigfiles
file_name = "./20MB_file"
file_data = open(file_name, "rb")
data = file_data.read()

fs = gridfs.GridFS(db)

# store file
a = fs.put(data, filename="20MB_file_python")
print(a)
b = fs.put(fs.get(a), filename="the_same_file")
print(b)

# retrieve
data = db.fs.files.find_one({'filename': "20MB_file_python"})
res = fs.get(data['_id']).read()
download_location = "./20MB_file_python"
output = open(download_location, "wb")
output.write(res)
output.close()

# retrieve parts
data = db.fs.files.find_one({'filename': "20MB_file_python"})
res = fs.get(data['_id']).readchunk()
print(res)
