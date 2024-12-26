# mongodb.py
from pymongo import MongoClient

class MongoDBConnection:
    _instance = None

    @staticmethod
    def get_instance():
        if MongoDBConnection._instance is None:
            client = MongoClient('mongodb://localhost:27017/')
            MongoDBConnection._instance = client.company_data
        return MongoDBConnection._instance
