#! python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  30 21:57:00 2018
@author: Saif Kurdi-Teylouni
"""
import jsonpickle
import json
from pymongo import MongoClient
# pprint library is used to make the output look more pretty
from pprint import pprint
# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string

class Database( object ):

    collections=["Users", "Bills", "Laws"]

    def createDocumentfromField(data, field):
        converted_data={}
        converted_data['item']= jsonpickle.encode(data)
        converted_data['_id']=field
        return converted_data

    def returnObjfromDocument(document):
        return jsonpickle.decode(document['item'])

    def findCollection( database, collection,  database_url="localhost:27017"):
        client = MongoClient(database_url)
        db=client[database]
        col = db[collection]
        return col

    def addRecord( data, database, collection,  database_url="localhost:27017"):
        #page = open("test.json", 'r')
        #print(json.dumps(data))
        #col=Database.findCollection(database, collection, database_url)
        col=Database.findCollection(database, collection, database_url)
        #for item in parsed["Records"]:
        #col.insert(data)
        col.update({'_id':data["_id"]}, data, upsert=True)

        #db=client.admin
        # Issue the serverStatus command and print the results
        #serverStatusResult=db.command("serverStatus")
        #pprint(serverStatusResult)

    def deleteRecord( data, database, collection,  database_url="localhost:27017"):
        print(json.dumps(data))
        col=Database.findCollection(database, collection, database_url)
        col.delete_one({'_id':data["_id"]})

    def updateRecord( data, database, collection,  database_url="localhost:27017"):
        col=Database.findCollection(database, collection, database_url)
        col.replace_one({'_id':data["_id"]}, data)

    def findRecord( id, database, collection,  database_url="localhost:27017"):
        col=Database.findCollection(database, collection, database_url)
        return col.find_one({'_id':id})

    def findAllRecordsBySubstringMatch( substring, database, collection,  database_url="localhost:27017"):
        col=Database.findCollection(database, collection, database_url)
        return col.find({'_id': { '$regex' : substring}})

    def findAllRecords( database, collection,  database_url="localhost:27017"):
        col=Database.findCollection(database, collection, database_url)
        return col.find({})

    def findRecordByStringOverlapMatch( substring, database, collection,  database_url="localhost:27017"):
        col=Database.findCollection(database, collection, database_url)
        return col.find_one({'$text': {'$search': substring}})

    def createSearchIndexfromRecord( string, database, collection,  database_url="localhost:27017"):
        col=Database.findCollection(database, collection, database_url)
        return col.create_index([('_id',pymongo.TEXT)])
