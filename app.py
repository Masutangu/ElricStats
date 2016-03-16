from flask import Flask
from flask.ext.pymongo import PyMongo
from bson.json_util import dumps


app = Flask('elric')
mongo = PyMongo(app)

@app.route('/')
def index():
    return "welcome elric!<br> " \
           "type /period_jobs to check all period jobs info. <br>" \
           "type /period_jobs/&lt;job_id&gt; to check specific period jobs info. <br>" \
           "type /job_records to check all executed jobs' records. <br>" \
           "type /job_records/&lt;job_id&gt; to check specific job's records."


@app.route('/period_jobs')
def all_period_jobs():
    jobs = mongo.db.elric_jobs.find({}, {'serialized_job': False})
    return dumps(jobs)


@app.route('/period_jobs/<job_id>')
def specific_period_job(job_id):
    job = mongo.db.elric_jobs.find_one_or_404({'_id': job_id}, {'serialized_job': False})
    return dumps(job)


@app.route('/job_records/<job_id>')
def all_job_records(job_id):
    job = mongo.db.elric_execute_records.find_one_or_404({'_id': job_id}, {'serialized_job': False})
    print job
    return dumps(job)


@app.route('/job_records')
def specific_job_record():
    jobs = mongo.db.elric_execute_records.find({}, {'serialized_job': False})
    return dumps(jobs)


if __name__ == "__main__":
    app.run()
