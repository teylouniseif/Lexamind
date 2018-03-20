#! python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  30 21:57:00 2018
@author: Saif Kurdi-Teylouni
"""
from .database import Database

def storeBill(bill):
    record=Database.createCollectionIdfromField(bill, bill.identifier)
    Database.addRecord(record, "Lexamind", "Bills")

def retrieveBill(id):
    return Database.findRecord(id, "Lexamind", "Bills")

def storeUser(user):
    record=Database.createCollectionIdfromField(user, 'identifier')
    Database.addRecord(record, "Lexamind", "Users")

def retrieveUser(id):
    return Database.findRecord(id, "Lexamind", "Users")

def storeLaw(law):
    record=Database.createCollectionIdfromField(law, 'identifier')
    Database.addRecord(record, "Lexamind", "Laws")

def retrieveLaw(id):
    return Database.findRecord(id, "Lexamind", "Laws")

def updateLaw(law):
    record=Database.createCollectionIdfromField(law, 'identifier')
    Database.updateRecord(record, "Lexamind", "Laws")
