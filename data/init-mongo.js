// Create user and database
db.createUser({
    user: 'job_seeker',
    pwd: 'password',
    roles: [
        {
            role: 'readWrite',
            db: 'job_db',
        },
    ],
});

// Create collections
db = new Mongo().getDB("job_db");

db.createCollection('hellowork_jobs', { capped: false });