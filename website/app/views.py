from flask import Flask, render_template, request, url_for, redirect, jsonify
from bson.json_util import dumps
from .models import Job

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/jobs', methods=['POST'])
def get_jobs():

    title = request.form['title']
    cursor_job = Job.find_by_title(title)
    list_jobs = list(cursor_job)

    if list_jobs:
        return render_template('jobs.html', jobs=list_jobs)
    else:
        return jsonify({"message": "User not found"}), 404