import pymongo

class DatabaseConnection:

    def __init__(self, db_name="job_db", collection_name="hellowork_jobs"):
        self.client = pymongo.MongoClient("mongodb://job_seeker:getajob@localhost:27017/job_db?authSource=job_db")
        self.db = self.client["job_db"]
        self.collection = self.db["hellowork_jobs"]

    # Display all documents in the collection
    def find_all(self):
        return self.collection.find()
    
    # Display all documents that match the query
    def find(self, query):
        return self.collection.find(query)