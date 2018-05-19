#! python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  30 21:57:00 2018
@author: Saif Kurdi-Teylouni
"""
from .database import Database
import numpy

def storeBill(bill):
    bill.details=bill.details.encode('utf-8')
    record=Database.createDocumentfromField(bill, bill.identifier)
    if(retrieveBill(bill.identifier)==None):
        Database.addRecord(record, "Lexamind", "Bills")

def retrieveBill(id):
    encodedbill=Database.findRecord(id, "Lexamind", "Bills")
    if encodedbill==None:
        return None
    bill=Database.returnObjfromDocument(encodedbill)
    bill.details=bill.details.decode()
    return bill

def retrieveBillsByLegislature(legislature):
    encodedbills=Database.findAllRecordsBySubstringMatch(legislature , "Lexamind", "Bills")
    if encodedbills==None:
        return None
    bills=[]
    for encodedbill in encodedbills:
        bill=Database.returnObjfromDocument(encodedbill)
        bill.details=bill.details.decode()
        bills.append(bill)
    return bills

def storeUser(user):
    record=Database.createDocumentfromField(user, user.identifier)
    Database.addRecord(record, "Lexamind", "Users")

def retrieveUser(id):
    encodeduser=Database.findRecord(id, "Lexamind", "Users")
    if encodeduser==None:
        return None
    return Database.returnObjfromDocument(encodeduser)

def retrieveUsersByTeam(team):
    if team==None:
        encodedusers=Database.findAllRecords("Lexamind", "Users")
    else:
        encodedusers=Database.findAllRecordsBySubstringMatch(team , "Lexamind", "Users")
    if encodedusers==None:
        return None
    users=[]
    for encodeduser in encodedusers:
        user=Database.returnObjfromDocument(encodeduser)
        users.append(user)
    return users

def storeLaw(law):
    print(law.identifier)
    record=Database.createDocumentfromField(law, law.identifier)
    Database.addRecord(record, "Lexamind", "Laws")
    #Database.createSearchIndexfromRecord(law.identifier, "Lexamind", "Laws")

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

"""def storeArchive(archive):
    record=Database.createDocumentfromField(archive, archive.identifier)
    Database.addRecord(record, "Lexamind", "Archives")

def deleteArchive(archive):
    record=Database.createDocumentfromField(archive, archive.identifier)
    Database.deleteRecord(record, "Lexamind", "Archives")

def retrieveArchive(id):
    encodedarchive=Database.findRecord(id, "Lexamind", "Archives")
    if encodedarchive==None:
        return None
    return Database.returnObjfromDocument(encodedarchive)

def updateArchive(archive):
    record=Database.createDocumentfromField(archive, archive.identifier)
    Database.updateRecord(record, "Lexamind", "Archives")"""

def storeArchive(archive):
    record={}
    record["_id"]=archive.identifier
    record["lastUpdate"]=archive.lastUpdate
    #record["messages"]=archive.messages
    Database.addRecord(record, "Lexamind", "Archives")

def deleteArchive(archive):
    record={}
    record["_id"]=archive.identifier
    Database.deleteRecord(record, "Lexamind", "Archives")

def retrieveArchive(id):
    archive=Database.findRecord(id, "Lexamind", "Archives")
    if archive==None:
        return None
    return archive["_id"], archive["lastUpdate"]

def updateArchive(archive):
    record={}
    record["_id"]=archive.identifier
    record["lastUpdate"]=archive.lastUpdate
    #record["messages"]=archive.messages
    Database.updateRecord(record, "Lexamind", "Archives")

def storeAccount(user):
    record={}
    record["_id"]=user.identifier
    record["laws"]=",".join(user.lawnames)
    record["password"]=user.password
    Database.addRecord(record, "Lexamind", "Accounts")

def deleteAccount(user):
    record={}
    record["_id"]=user.identifier
    Database.deleteRecord(record, "Lexamind", "Accounts")

def retrieveAccount(id):
    pass

def updateAccount(user):
    record={}
    record["_id"]=user.identifier
    record["laws"]=",".join(user.lawnames)
    record["password"]=user.password
    Database.updateRecord(record, "Lexamind", "Accounts")
