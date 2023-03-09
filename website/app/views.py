from flask import Flask, jsonify
from .models import Job

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World'

@app.route('/jobs', methods=['GET'])
def get_jobs():
    jobs = Job.find_all()
    if jobs:
        return jsonify(jobs), 200
    else:
        return jsonify({"message": "User not found"}), 404