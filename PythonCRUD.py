import json
from bson import json_util
from pymongo import MongoClient

connection = MongoClient('localhost', 27017)
db = connection['city']
collection = db['inspections']

def createDocument(document):
		try:
			result = collection.save(document)
			return True
		except:
			return False

def readDocument():
	try:
		query = {"address.zip":11242}
		found = collection.find(query)
		if found.count() > 0:
			for x in found:
				readDoc = json.dumps(x, default=json_util.default)
				return readDoc
		else:
			return "Not Found"
	except:
		return 

def updateDocument():
		try:
			criteria = {"address.zip":"","address.state":{"$ne":""}}
			newValue = {"$set":{"address.state":""}}
			update = collection.update(criteria, newValue)
			updateDoc = json.dumps(update, default=json_util.default)
			return updateDoc
		except:
			return "None Updated"
		
def deleteDocument():
		try:
			remove = {"keyName" : "test value data"}
			delete = collection.delete_one(remove)
			count = delete.deleted_count
			deleteDoc = json.dumps(count, default=json_util.default)
			return deleteDoc
		except:
			return "None Deleted"

			
def main():
	myDocument = {"keyName" : "test value data"}
	
	print createDocument(myDocument) 
	print readDocument()
	print updateDocument()
	print deleteDocument()
	
main()