#! python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  30 21:57:00 2018
@author: Saif Kurdi-Teylouni
"""
from storer.storer import storeBill, retrieveBillsByLegislature, storeLaw, deleteLaw, retrieveLaw, updateLaw
from collections import namedtuple
import jsonpickle, re


class Bill( object):

    """title = ''
    identifier = ''
    events=[]
    details=''
    lawnames=["Perospero", "Katakuri", "Oven", "Smoothie", "Daifuku", "Compote", "Cracker", "Snack"]"""

    def __init__(self, identifier, title, legislature):
        self.title=title
        self.identifier=identifier
        self.legislature=''
        self.lawnames=[]
        self.events=[]
        self.details=''

    def addEvent(self, stage, date, activity, committee):
        event={'stage':'0', 'date':'0', 'activity':'0', 'committee':'0'}
        event['stage']=stage
        event['date']=date
        event['activity']=activity
        event['committee']=committee
        self.events.append(event)

    def setDetails(self, details):
        self.details=details

    def addLaw(self, law):
        sanitizedlaw=str(law.strip().lower())
        self.lawnames.append(sanitizedlaw)

class Law( object):

    """title = ''
    identifier = ''
    billtitles=[]"""

    def __init__(self, identifier, title):
        self.title=title
        self.identifier=identifier
        self.bills={}

    def addDependentBill(self, bill):
        self.bills[bill.identifier]=bill.title

    def getDependantBills(self):
        return self.bills


class Scraper( object ):

    """legislature="NONE"
    bills=[]"""

    def __init__(self):
        self.bills=[]
        self.legislature=""

    def retrieve_bills( self , filename):
        pass

    def format_bills(self, collection):
        pass

    def load_bills(self):
        self.bills=retrieveBillsByLegislature(self.legislature)
        for bill in self.bills:
            for law in bill.lawnames:
                print(law)

    def store_bills(self):
        for bill in self.bills:
            storeBill(bill)
            #need to update law table also
            for lawname in bill.lawnames:
                law=Law(lawname, lawname)
                cachedLaw=retrieveLaw(lawname)
                if cachedLaw==None:
                    law.addDependentBill(bill)
                    storeLaw(law)
                else:
                    cachedLaw.addDependentBill(bill)
                    updateLaw(cachedLaw)

    def scrapeLawsinBill(self, bill):
        pass
