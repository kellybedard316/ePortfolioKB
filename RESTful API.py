#Kelly Bedard Project 2

import json
from bson import json_util
import datetime
import bottle
from bottle import delete, route, run, request, abort
from pymongo import MongoClient

connection = MongoClient('localhost', 27017)
db = connection['city']
collection = db['inspections']

# set up URI paths for REST service

@route('/hello', method='GET')
def hello():
		try:
			request.query.name
			name = request.query.name
			string = "{\"hello\":"+request.query.name+"}"

		except NameError:
			abort(404, "Not Found")

		return json.loads(json.dumps(string, indent=4, default=json_util.default))

@route('/strings', method='POST')
def strings():
		try:
			new_str = {'first':request.json.get('string1'), 'second':request.json.get('string2')}

		except NameError:
			abort(404, "Not Found")

		return new_str

#Create new document
@route('/create', method='POST')
def create():
    try:
        date = datetime.datetime.now()
        _id = json_util.ObjectId.from_datetime(date)
        new_doc = collection.insert({
            "_id": str(json_util.ObjectId(_id)),
            'id': request.json.get('id'),
            'certificate_number':request.json.get('certificate_number'),
            'business_name':request.json.get('business_name'),
            'date': request.json.get('date'),
            'result': request.json.get('result'),
            'sector': request.json.get('sector')})
    except NameError:
        abort(404, "Not Found")
    return new_doc

#Read new document created
@route('/read', method='GET')
def read():
    try:
        request.query.business_name
        name = request.query.business_name
        found = {"business_name":name}
    except NameError:
        abort(404, "Not Found")
    if not found:
        abort(404, "Not Found")
    return json.dumps(found, indent=4, default=json_util.default)

		
#Update new document created
@route('/update', method='GET')
def update():
    try:
			idSearch = request.query.id
			idQuery = {"id":idSearch}
			resultQuery = request.query.result
			update = {"$set": {"result": resultQuery}}

    except NameError:
			abort(404, "Not Found")

    return json.dumps(idQuery, update, indent=4,default=json_util.default)

#Delete new document created
@route('/delete', method='GET')
def delete():
	try:
		request.query.id
		id = request.query.id
		remove = {"id":id}
		delete = collection.delete_one(remove)
		count = delete.deleted_count
		deleteDoc = json.dumps(count, default=json_util.default)
		return "Successfully deleted document with "+id+" from collection."
	except NameError:
		abort(404, "Delete Failed")
			
if __name__ == '__main__':
	#app.run(debug=True)
	run(host='localhost', port=8080)