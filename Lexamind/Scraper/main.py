#! python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  30 21:57:00 2018
@author: Saif Kurdi-Teylouni
"""

from scrapers.ontario_scraper import Ontario
from scrapers.version_converter import call_python_version
from federal_scraper.federal_scraper import my_function
from storer.database import Database
import json
import jsonpickle

y=Ontario()
y.load_bills()
#y.retrieve_bills()
#y.store_bills()
"""newbill=Database.findRecord("Perospero", "Lexamind", "Laws")
print(jsonpickle.decode(newbill['item']).title)
#print(jsonpickle.decode(newbill['item']).billtitles)
newbill=Database.findRecord("Ontariobill1", "Lexamind", "Bills")
print(jsonpickle.decode(newbill['item']).title)
details=jsonpickle.decode(newbill['item']).details
print('littlenoni')
print(str(details, 'utf-8'))"""
#y.store_bills()
#data=Ontario()
x=Database()
"""for bill in y.bills:
    #bill['_id']=bill['identifier']
    record=Database.createDocumentfromField(bill, 'identifier')
    #x.deleteRecord(bill, "Lexamind", "Users")
    Database.addRecord(record, "Lexamind", "Users")
    bill.title='noni'
    record=Database.createDocumentfromField(bill, 'identifier')
    Database.updateRecord(record, "Lexamind", "Users")
    newbill=Database.findRecord(record['_id'], "Lexamind", "Users")
    print(jsonpickle.decode(newbill['item']).title)
    print(jsonpickle.decode(newbill['item']).details)"""

#result = call_python_version("2.7", "scrapers.federal_scraper", "my_function",
#                             ["Mr", "Bear"])

#result = call_python_version("2.7", "federal_scraper.federal_scraper", "my_function",[])

#my_function()
