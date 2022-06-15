from email import message
from email.policy import default
from flask_pymongo import PyMongo
from flask import Flask, request, Response, json, jsonify
from bson.json_util import dumps
app = Flask(__name__)
mongodb_client = PyMongo(app, uri="mongodb://localhost:27017/film")
db = mongodb_client.db
coll = db.rent

@app.route('/')
def index():
    return jsonify(message='Welcome to api crud operations')

@app.route("/api", methods=['GET'])
def retrieve_data():
    data = list(coll.find())
    result = [d for d in data]
    res = json.dumps(result,default=str)
    return Response(response=res,status=200,mimetype='application/json')

@app.route("/api/add", methods=['POST'])
def insert_data():
    data = request.json
    # jdata = json.loads(data.decode('utf-8'))
    load = coll.insert_one(data)
    res = load.inserted_id
    print('success data insertion')
    return Response(response=res,status=200, mimetype='application/json')

@app.route('/api/update/<string:fname>', methods=['PATCH'])
def update_by_title(fname):
    qset = {'title' : fname}
    data = request.json
    record = coll.find_one(qset)
    if record is not None:
        result = coll.update_one(qset,{'$set': data })
        if result.modified_count > 0:
            return f"Succesfully Record '{fname}' Updated"
        else:
            return f"title '{fname}' mismatch" 
    else:
        return f"Mismatch movie title '{fname}'"

@app.route('/api/delete/<string:fname>', methods=['DELETE'])
def delete_by_title(fname):
    qset = {'title' :  fname}
    record = coll.delete_one(qset)
    count = record.deleted_count
    if count > 0:
        return f'record "{fname}" deleted succesfully!'
    else:
        return f'record with name "{fname}" not found'


@app.route('/api/<string:fname>', methods=['GET'])
def film_details(fname):
    qset = {'title': fname}
    record = coll.find_one(qset)
    res = dumps(record)
    return Response(response=res, status=200)

@app.route('/api/actor/<string:actor_name>', methods=['GET'])
def title_by_actor(actor_name):
    qset = {'list_actors': {'$regex': actor_name}}
    records = list(coll.find(qset, {'title': 1, '_id':0}))
    if len(records) == 0:
        return jsonify({"status" : f"With Actor {actor_name} doesn't have any data"})
    else:
        data = [d for d in records]
        res = dumps(data)
        return Response(response=res, status=200)

    return Response(response=jsonify(res), status=200)

if __name__ == "__main__":
    app.run(debug=True, port=8001)