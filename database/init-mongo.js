// Create a new database
db = db.getSiblingDB('job_db');

// Create a new collection
db.createCollection('indeed_jobs');

// Create a user to access the database
db.createUser({
    user: "job_seeker",
    pwd: "getajob",
    roles: [
        { role: "readWrite", db: "job_db" }
    ]
});