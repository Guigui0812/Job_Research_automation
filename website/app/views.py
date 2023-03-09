from flask import Flask, render_template, request, url_for, redirect, jsonify
from bson.json_util import dumps
from .models import Job

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World'

@app.route('/jobs', methods=['GET'])
def get_jobs():
    cursor_job = Job.find_all()
    list_jobs = list(cursor_job)

    print(list_jobs[0]["title"])

    if list_jobs:
        return render_template('jobs.html', jobs=list_jobs)
    else:
        return jsonify({"message": "User not found"}), 404