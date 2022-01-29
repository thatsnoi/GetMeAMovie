import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

class DataBase:
    def __init__(self):
        pass
    

    def create_connection(self):
        db_url = os.environ.get('DB_URL')
        db_name = os.environ.get('DB_NAME')
        user = os.environ.get('DB_USER')
        password = os.environ.get('DB_PASSWORD')
        collection_name = os.environ.get('DB_COLLECTION')

        try:
            self.connection = MongoClient(f'mongodb+srv://{user}:{password}@{db_url}')

            self.db = self.connection[db_name]
            self.movies_collection = self.db[collection_name]
        except ConnectionFailure as e:
            print(e)
    

    def close_connection(self):
        if self.connection:
            self.connection.close()
