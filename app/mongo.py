import pymongo

mongo_client = pymongo.MongoClient("mongodb://your_mongodb_url/")
db = mongo_client.my_test_db
