#! python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  30 21:57:00 2018
@author: Saif Kurdi-Teylouni
"""
import json
from pymongo import MongoClient
# pprint library is used to make the output look more pretty
from pprint import pprint
# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string

class Database( object ):

    def addRecord(self, data, database_url="localhost:27017"):
        print(json.dumps(data))
        client = MongoClient(database_url)
        db=client.Lexamind
        record1 = db.Users
        #page = open("test.json", 'r')
        #parsed = json.loads(page.read())

        #for item in parsed["Records"]:
        record1.insert(data)

        #db=client.admin
        # Issue the serverStatus command and print the results
        #serverStatusResult=db.command("serverStatus")
        #pprint(serverStatusResult)
