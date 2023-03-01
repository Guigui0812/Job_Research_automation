import pymongo

# Class to interface with MongoDB
class MongoDbInterface:

    # Constructor
    def __init__(self, host, port, db_name, collection_name):
            
            # Get the client
            self.client = pymongo.MongoClient("mongodb://myuser:mypassword@localhost:27017/job_db?authSource=job_db")
    
            # Get the database
            self.db = self.client[db_name]
    
            # Get the collection
            self.collection = self.db[collection_name]

    # Function to insert a document
    def insert_many(self, documents):
        self.collection.insert_many(documents)

    # Get all documents from the collection
    def get_all(self):
        return self.collection.find()
    
    # Ask database if a document exists with the same idoffer
    def exists(self, idoffer):
        if self.collection.find_one({"idoffer": idoffer}):
            return True
        else:
            return False