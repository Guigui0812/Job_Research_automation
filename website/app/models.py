from .services import DatabaseConnection

db_connection = DatabaseConnection()

# Model for a job document
class Job:
    def __init__(self, job_id, job_title, job_description, job_location, job_posted_date, job_company):
        self.id = job_id
        self.title = job_title
        self.description = job_description
        self.location = job_location
        self.date = job_posted_date
        self.company = job_company

    # Find all job where is title is contained in the job document
    @staticmethod
    def find_by_title(title):
        query = {"title": {"$regex": title, "$options": "i"}}
        return db_connection.find(query)

    @staticmethod
    def find_all():
        return db_connection.find_all()