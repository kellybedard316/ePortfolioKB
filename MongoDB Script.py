#Kelly Bedard Final Project

import json
from bson import json_util
from bson import SON
import datetime
import bottle
from bottle import delete, route, run, request, abort
from pymongo import MongoClient


connection = MongoClient('localhost', 27017)
db = connection['market']
collection = db['stocks']

def createDocument(document):
		try:
			document = input("What document(s) do you wish to create? (include quotes and brackets) ") #take user input for documents for creation
			result = collection.save(document)
			return "Successfully created document."
		except:
			return "Document not inserted."

def readDocument():
	try:
		query = input("What document do you wish to read? (include quotes and brackets) ") #take user input for search criteria
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
			criteria = input("Which document(s) do you want to update? (include quotes and brackets) ") #take user input for search criteria
			newValue = input("Enter the new value(s): ") #take user input for value to update
			updatedValue = {"$set":newValue} #set value to update
			update = collection.update(criteria, updatedValue) #implement both the search and the update values
			updateDoc = json.dumps(update, default=json_util.default)
			return updateDoc
		except:
			return "Nothing was updated."
		
def deleteDocument():
		try:
			remove = input("What do you want to delete? (include quotes) ") #take user input for deletion criteria
			delete = collection.delete_one(remove)
			count = delete.deleted_count
			deleteDoc = json.dumps(count, default=json_util.default)
			return  deleteDoc + " document(s) deleted."

		except:
			return "None Deleted"
			
def readNumberDocument():
	try:
		low = input("Enter low: ") #take user input foe low value
		high = input("Enter high: ") #take user input foe high value
		found = collection.find({"50-Day Simple Moving Average":{"$lte":high, "$gte":low}})
		count = found.count()
		readDoc = json.dumps(count, default=json_util.default)
		return readDoc + " documents found."

	except:
		return "Nothing found."
	
def readStringDocument():
	try:
		industry = input("Enter industry (include quotes): ") #take user input for industry value
		found = collection.find({"Industry":industry},{"Ticker":1})
		for x in found:
			readDoc = json.dumps(x, default=json_util.default)
			print(readDoc)

	except:
		return "Nothing found."

def aggregateDocument():
	try:
		sector = input("Enter sector (include quotes): ") #take user input for sector value
		pipeline = [{"$match":{"Sector":sector}},
               {"$group":{"_id":"$Industry",
    	         "outstandingShares":{"$sum":"$Shares Outstanding"}}}]
		aggregate = list(collection.aggregate(pipeline))
		print(aggregate)

	except:
		return "No results."

def main():
	myDocument = {"Ticker":"Test","Volume":555}
	
	print createDocument(myDocument) 
	print readDocument()
	print updateDocument()
	print deleteDocument()
	print readNumberDocument()
	print readStringDocument()
	print aggregateDocument()

main()

#Create new document
@route('/create', method='POST')
def create():
    try:
        earnings_date = datetime.datetime.now()
        _id = json_util.ObjectId.from_datetime(earnings_date)
        new_doc = collection.insert({
            "_id": str(json_util.ObjectId(_id)),
						'Ticker' : request.json.get('ticker'),
						'Sector' : request.json.get('sector'),
						'Shares Outstanding' : request.json.get('shares_outstanding'),
						'Earnings Date' : request.json.get('earnings_date'),
						'Country' : request.json.get('country'),
						'Industry' : request.json.get('industry'),
						'Company' : request.json.get('company_name')})
    except NameError:
        abort(404, "Not Found")
    return new_doc

#Read new document created
@route('/read', method='GET')
def read():
    try:
        name = request.query.company_name
        found = {"company_name":name}
    except NameError:
        abort(404, "Not Found")
    if not found:
        abort(404, "Not Found")
    return json.dumps(found, indent=4, default=json_util.default)

		
#Update new document created
@route('/update', method='GET')
def update():
    try:
			tickerSearch = request.query.ticker
			tickerQuery = {"Ticker":tickerSearch}
			countryQuery = request.query.country
			update = {"$set": {"Country": countryQuery}}

    except NameError:
			abort(404, "Not Found")

    return json.dumps(countryQuery, update, indent=4,default=json_util.default)

#Delete new document created
@route('/delete', method='GET')
def delete():
	try:
		ticker = request.query.ticker
		remove = {"Ticker":ticker}
		delete = collection.delete_one(remove)
		count = delete.deleted_count
		deleteDoc = json.dumps(count, default=json_util.default)
		return "Successfully deleted document(s) from collection."
	except NameError:
		abort(404, "Delete Failed")

	
#Get summary of document based on Ticker
@route('/summary', method='GET')
def summary():
	try:
		ticker = request.query.ticker
		pipeline = [{"$match":{"Ticker":ticker}},
               {"$group":{"_id":{"Ticker":"$Ticker",
													"Sector":"$Sector",
													"Industry":"$Industry",
													"Company":"$Company",
													"Price":"$Price",
													"Dividend Yield":"$Dividend Yield",
													"EPS":"$EPS (ttm)",
													"Volume":"$Volume",
													"Shares Outstanding":"$Shares Outstanding"}}}]
		aggregate = list(collection.aggregate(pipeline))
		
	except NameError:
		abort(404, "Not Found")

	return json.dumps(aggregate, indent=4, default=json_util.default)
	
#Get portfolio of documents for top 5 stocks
@route('/portfolio', method='GET')
def summary():
	try:
		industry = request.query.industry
		pipeline = [{"$match":{"Industry":industry}},
							 {"$sort":{"EPS growth this year":-1}},
							 {"$limit":5},
               {"$group":{"_id":{"Ticker":"$Ticker",
													"Sector":"$Sector",
													"Industry":"$Industry",
													"Company":"$Company",
													"Price":"$Price",
													"Dividend Yield":"$Dividend Yield",
													"EPS":"$EPS (ttm)",
													"Volume":"$Volume",
													"Shares Outstanding":"$Shares Outstanding",
													"Volatility (Month)":"$Volatility (Month)",
													"EPS growth this year":"$EPS growth this year"}}}]
		aggregate = list(collection.aggregate(pipeline))
		
	except NameError:
		abort(404, "Not Found")

	return json.dumps(aggregate, indent=4, default=json_util.default)

if __name__ == '__main__':
	#app.run(debug=True)
	run(host='localhost', port=8080)

