import pymongo

class DatabaseConnection:

    def __init__(self, db_name="job_db", collection_name="hellowork_jobs"):
        self.client = pymongo.MongoClient("mongodb://job_seeker:getajob@localhost:27017/job_db?authSource=job_db")
        self.db = self.client["job_db"]
        self.collection = self.db["hellowork_jobs"]

    def insert(self, data):
        self.collection.insert_one(data)

    def find(self, data):
        return self.collection.find_one(data)

    def update(self, data, new_data):
        self.collection.update_one(data, new_data)

    def delete(self, data):
        self.collection.delete_one(data)

    # Display all documents in the collection
    def find_all(self):
        return self.collection.find()