#! python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  30 21:57:00 2018
@author: Saif Kurdi-Teylouni
"""
from .database import Database

def storeBill(bill):
    record=Database.createDocumentfromField(bill, bill.identifier)
    Database.addRecord(record, "Lexamind", "Bills")

def retrieveBill(id):
    encodedbill=Database.findRecord(id, "Lexamind", "Bills")
    if encodedbill==None:
        return None
    return Database.returnObjfromDocument(encodedbill)

def storeUser(user):
    record=Database.createDocumentfromField(user, 'identifier')
    Database.addRecord(record, "Lexamind", "Users")

def retrieveUser(id):
    encodeduser=Database.findRecord(id, "Lexamind", "Users")
    if encodeduser==None:
        return None
    return Database.returnObjfromDocument(encodeduser)

def storeLaw(law):
    record=Database.createDocumentfromField(law, law.identifier)
    Database.addRecord(record, "Lexamind", "Laws")

def deleteLaw(law):
    record=Database.createDocumentfromField(law, law.identifier)
    Database.deleteRecord(record, "Lexamind", "Laws")

def retrieveLaw(id):
    encodedlaw=Database.findRecord(id, "Lexamind", "Laws")
    if encodedlaw==None:
        return None
    return Database.returnObjfromDocument(encodedlaw)

def updateLaw(law):
    record=Database.createDocumentfromField(law, law.identifier)
    Database.updateRecord(record, "Lexamind", "Laws")
