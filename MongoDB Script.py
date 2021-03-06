#Kelly Bedard

import json
from bson import json_util
from bson import SON
import datetime
import bottle
from bottle import delete, route, run, request, abort
from pymongo import MongoClient
import sys
from sys import exit

connection = MongoClient('localhost', 27017)
db = connection['market']
collection = db['stocks']

def createDocument():
	answer = raw_input("Do you want to create a new document (Y/N)?")
	if answer == "Y" or answer == "y":
		document = input("What document(s) do you wish to create? (include quotes and brackets) ") #take user input for documents for creation
		try:
			confirm = raw_input("Are you sure? ") #take user input to confirm action
			if confirm == "Y" or confirm == "y":			
				result = collection.save(document)
				return "Successfully created document."
			else:
				return "Nothing created."
		except:
			return "Document not inserted."

def readDocument():
	answer = raw_input("Do you want to read a document (Y/N)?")
	try:
		if answer == "Y" or answer == "y":
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
	answer = raw_input("Do you want to update a document (Y/N)? ")
	if answer == "Y" or answer == "y":
		criteria = input("Which document(s) do you want to update? (include quotes and brackets) ") #take user input for search criteria
		newValue = input("Enter the new value(s): ") #take user input for value to update
		try:
			confirm = raw_input("Are you sure? ") #take user input to confirm action
			if confirm == "Y" or confirm == "y":
					updatedValue = {"$set":newValue} #set value to update
					update = collection.update(criteria, updatedValue) #implement both the search and the update values
					updateDoc = json.dumps(update, default=json_util.default)
					return updateDoc
			else:
				return "Nothing updated."
		except:
			return "Nothing was updated."
		
def deleteDocument():
	answer = raw_input("Do you want to delete a document (Y/N)? ")
	if answer == "Y" or answer == "y":
		remove = input("What do you want to delete? (include quotes) ") #take user input for deletion criteria
		try:
			confirm = raw_input("Are you sure? ") #take user input to confirm action
			if confirm == "Y" or confirm == "y":
					delete = collection.delete_many(remove)
					count = delete.deleted_count
					deleteDoc = json.dumps(count, default=json_util.default)
					return  deleteDoc + " document(s) deleted."
			else:
				return "Nothing deleted."
		except:
			return "None Deleted"

def readNumberDocument():
	answer = raw_input("Do you want to see how many documents fall within a chosen range (Y/N)? ")
	try:
		if answer == "Y" or answer == "y":
			field = input("What field do you want to search? (include quotes) ") #take user input to specify field to query
			low = input("Enter low: ") #take user input for low value
			high = input("Enter high: ") #take user input for high value
			found = collection.find({field:{"$lte":high, "$gte":low}}) #apply user input to conduct query
			count = found.count()
			readDoc = json.dumps(count, default=json_util.default)
			return readDoc + " documents found."

	except:
		return "Nothing found."
	
def readStringDocument():
	answer = raw_input("Do you want to pull values based on a specific field (Y/N)? ")
	try:
		if answer == "Y" or answer == "y":
			field = input("What field do you want to search? (include quotes) ") #take user input to specify field to search
			value = input("What value do you want to search? (include quotes) ") #take user input to specify the value to search 
			output = input("What data do you want to see? (include quotes) ") 
			sort = input("Sort ascending: 1 or descending: -1? ") #take user input to determing sorting
			found = collection.find({field:value},{output:sort})
			for x in found:
				readDoc = json.dumps(x, default=json_util.default)
				print(readDoc)

	except:
		return "Nothing found."

def aggregateDocument():
	answer = raw_input("Do you want to aggregate a pipeline (Y/N)? ")
	try:
		if answer == "Y" or answer == "y":
			field = input("What field do you want to search? (include quotes) ") #take user input to specify field to search
			value = input("What value do you want to search? (include quotes) ") #take user input to specify the value to search 
			groupId = input("What field would you like to group by? (include $ and quotes) ") #take user input to specify what field should be grouped
			alias = input("What value do you want to set for the aggregation results? (include quotes) ") #take user input to set variable output
			action = input("Select an option: $sum / $avg / $min / $max (include quotes) ") #take user input to specify how to handle data
			agg = input("What value would you like to aggregate? (include $ and quotes) ") #take user input to specify where to apply the action
			pipeline = [{"$match":{field:value}},
								 {"$group":{"_id":groupId,
								 alias:{action:agg}}}]
			aggregate = list(collection.aggregate(pipeline))
			print(aggregate)

	except:
		return "No results."

def menu():
	selection = input("What would you like to do?\n"
		"1: Create Document\n"
		"2: Read Document\n"
		"3: Update Document\n"
		"4: Delete Document\n"
		"5: Count docuemnts with data in a chosen range\n"
		"6: View data of chosen field and value\n"
		"7: Aggregate Pipeline\n"
		"8: Quit\n"
		"Enter Selection: ")	
	return selection

def main():	
	result = True
	rest = raw_input("Would you like to start the RESTful API Service? (Y/N) ")
	if rest == "y" or rest == "Y":
		pass
	if rest == "n" or rest == "N":
		while result == True:
			option = menu()
			if option == 1:
				print createDocument() 
			if option == 2:
				print readDocument()
			if option == 3:
				print updateDocument()
			if option == 4:
				print deleteDocument()
			if option == 5:
				print readNumberDocument()
			if option == 6:
				print readStringDocument()
			if option == 7:
				print aggregateDocument()
			if option == 8:
				print("Quitting")
				result = False
				exit()
			if option < 1 or option > 8:
				print("Invalid Selection.")
			newselection = raw_input("Would you like to continue? (Y/N) ")
			if newselection == "y" or newselection == "Y":
				print option 
			if newselection == "n" or newselection == "N":
				result = False
				exit()

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
	
	


