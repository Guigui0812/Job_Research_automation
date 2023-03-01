// Create a new database
db = db.getSiblingDB('job_db');

// Create a new collection
db.createCollection('hellowork_jobs');

// Create a user to access the database
db.createUser({
    user: "myuser",
    pwd: "mypassword",
    roles: [
        { role: "readWrite", db: "job_db" }
    ]
});