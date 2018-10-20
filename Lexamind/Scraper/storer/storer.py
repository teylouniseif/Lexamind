#! python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  30 21:57:00 2018
@author: Saif Kurdi-Teylouni
"""
from .database import Database
import numpy

remote_database="mongodb+srv://Lexamind:Lexamind@cluster0-zowtj.mongodb.net/test"

def storeBill(bill):
    bill.details=bill.details.encode('utf-8')
    record=Database.createDocumentfromField(bill, bill.identifier)
    if(retrieveBill(bill.identifier)==None):
        Database.addRecord(record, "Lexamind", "Bills", remote_database)

def retrieveBill(id):
    encodedbill=Database.findRecord(id, "Lexamind", "Bills", remote_database)
    if encodedbill==None:
        return None
    bill=Database.returnObjfromDocument(encodedbill)
    bill.details=bill.details.decode()
    return bill

def retrieveBillsByLegislature(legislature):
    encodedbills=Database.findAllRecordsBySubstringMatch(legislature , "Lexamind", "Bills", remote_database)
    if encodedbills==None:
        return None
    bills=[]
    for encodedbill in encodedbills:
        bill=Database.returnObjfromDocument(encodedbill)
        bill.details=bill.details.decode()
        bills.append(bill)
    return bills

def deleteBill(bill):
    record=Database.createDocumentfromField(bill, bill.identifier)
    Database.deleteRecord(record, "Lexamind", "Bills", remote_database)

def deleteBillsByLegislature(legislature):
    Database.deleteAllRecordsBySubstringMatch( legislature, "Lexamind", "Bills",  remote_database)

def storeUser(user):
    record=Database.createDocumentfromField(user, user.identifier)
    Database.addRecord(record, "Lexamind", "Users", remote_database)

def retrieveUser(id):
    encodeduser=Database.findRecord(id, "Lexamind", "Users", remote_database)
    if encodeduser==None:
        return None
    return Database.returnObjfromDocument(encodeduser)

def retrieveUsersByTeam(team):
    if team==None:
        encodedusers=Database.findAllRecords("Lexamind", "Users", remote_database)
    else:
        encodedusers=Database.findAllRecordsBySubstringMatch(team , "Lexamind", "Users", remote_database)
    if encodedusers==None:
        return None
    users=[]
    for encodeduser in encodedusers:
        user=Database.returnObjfromDocument(encodeduser)
        users.append(user)
    return users

def storeLaw(law):
    dummyvar=1#print(law.identifier)
    record=Database.createDocumentfromField(law, law.identifier)
    Database.addRecord(record, "Lexamind", "Laws", remote_database)
    #Database.createSearchIndexfromRecord(law.identifier, "Lexamind", "Laws")

def deleteLaw(law):
    record=Database.createDocumentfromField(law, law.identifier)
    Database.deleteRecord(record, "Lexamind", "Laws", remote_database)

def deleteLawsByLegislature(legislature):
    Database.deleteAllRecordsBySubstringMatch( "("+legislature.lower()+")", "Lexamind", "Laws",  remote_database)

def retrieveLaw(id):
    encodedlaw=Database.findRecord(id, "Lexamind", "Laws", remote_database)
    if encodedlaw==None:
        return None
    return Database.returnObjfromDocument(encodedlaw)

def updateLaw(law):
    dummyvar=1#print(law.identifier)
    record=Database.createDocumentfromField(law, law.identifier)
    Database.updateRecord(record, "Lexamind", "Laws", remote_database)

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
    record["messages"]=archive.lastUpdate
    Database.addRecord(record, "Lexamind", "Archives", remote_database)

def deleteArchive(archive):
    record={}
    record["_id"]=archive.identifier
    Database.deleteRecord(record, "Lexamind", "Archives", remote_database)

def retrieveArchive(id):
    archive=Database.findRecord(id, "Lexamind", "Archives", remote_database)
    if archive==None:
        return None
    return archive["_id"], archive["lastUpdate"]

def updateArchive(archive):
    record={}
    record["_id"]=archive.identifier
    record["lastUpdate"]=archive.lastUpdate
    record["messages"]=archive.lastUpdate
    Database.updateRecord(record, "Lexamind", "Archives", remote_database)

def storeAccount(user):
    record={}
    record["_id"]=user.identifier
    dummyvar=1#print(user.lawnames)
    lawnames=[]
    for law in user.lawnames:
        lawnames.append(law.split("(")[1].split(")")[0]+" - "+law.split("(")[0])
    record["laws"]=str(sorted(lawnames))
    record["password"]=user.password
    Database.addRecord(record, "Lexamind", "Accounts", remote_database)

def deleteAccount(user):
    record={}
    record["_id"]=user.identifier
    Database.deleteRecord(record, "Lexamind", "Accounts", remote_database)

def retrieveAllAccounts():
    accounts=Database.findAllRecords("Lexamind", "Accounts", remote_database)
    if accounts==None:
        return None
    accs=[]
    for account in accounts:
        dummyvar=1#print(account)
        acc={'username':account['_id'],'lawnames':account['laws'], 'password':account['password']}
        accs.append(acc)
    return accs

def retrieveAccount(id):
    pass

def updateAccount(user):
    record={}
    record["_id"]=user.identifier
    record["laws"]=str(user.lawnames)
    record["password"]=user.password
    Database.updateRecord(record, "Lexamind", "Accounts", remote_database)
