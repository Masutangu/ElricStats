from flask import Flask
from flask.ext.pymongo import PyMongo
from bson.json_util import dumps
from utils import convert_period_job, convert_job_records
from bson.timestamp import Timestamp



app = Flask('elric')
mongo = PyMongo(app)

"""
db.elric_jobs.aggregate([{$project:{date:{$concat: (Date("$next_timestamp")).toString()}}}])

cursor = mongo.db.elric_jobs.aggregate([{
            '$project':{
                'lastModified':{
                    '$dateToString': {'format':"%Y-%m-%d", 'date':"$lastModified"}
                },


db.elric_jobs.aggregate([{$project:{date:{$dateToString: {format:"%Y-%m-%d", date:"$lastModified"}}}}])
"""


@app.route('/')
def index():
    return "welcome elric!<br> " \
           "type /period_jobs to check all period jobs info. <br>" \
           "type /period_jobs/&lt;job_id&gt; to check specific period jobs info. <br>" \
           "type /job_records to check all executed jobs' records. <br>" \
           "type /job_records/&lt;job_id&gt; to check specific job's records."


@app.route('/period_jobs')
def all_period_jobs():
    cursor = mongo.db.elric_jobs.find({}, {'serialized_job': False})
    jobs = [convert_period_job(job) for job in cursor]
    return dumps(jobs)

    # try:
    #     cursor = mongo.db.elric_jobs.aggregate([{
    #         '$project':{
    #             'lastModified':{
    #                 '$dateToString': {'format':"%Y-%m-%d", 'date':"$lastModified"}
    #             },
    #             'next_timestamp':{
    #                 '$concat': (str(Timestamp('$next_timestamp', 0).as_datetime()))
    #                                             }
    #                                                 }}])
    #
    #     return dumps(cursor)
    # except Exception as e:
    #     print e
    #


@app.route('/period_jobs/<job_id>')
def specific_period_job(job_id):
    job = mongo.db.elric_jobs.find_one_or_404({'_id': job_id}, {'serialized_job': False})
    return dumps(convert_period_job(job))


@app.route('/job_records/<job_id>')
def all_job_records(job_id):
    job = mongo.db.elric_execute_records.find_one_or_404({'_id': job_id}, {'serialized_job': False})
    return dumps(convert_job_records(job))


@app.route('/job_records')
@app.route('/job_records/<page>')
def specific_job_record(page=1):
    cursor = mongo.db.elric_execute_records.find({}, {'serialized_job': False})
    jobs = [convert_job_records(job) for job in cursor]
    return dumps(jobs)


if __name__ == "__main__":
    app.run()
