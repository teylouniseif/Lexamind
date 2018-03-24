#! python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  30 21:57:00 2018
@author: Saif Kurdi-Teylouni
"""
from storer.storer import storeBill, storeLaw, deleteLaw, retrieveLaw, updateLaw
from collections import namedtuple
import jsonpickle

class Bill( object):

    """title = ''
    identifier = ''
    events=[]
    details=''
    lawnames=["Perospero", "Katakuri", "Oven", "Smoothie", "Daifuku", "Compote", "Cracker", "Snack"]"""

    def __init__(self, identifier, title):
        self.title=title
        self.identifier=identifier
        self.lawnames=["Perospero", "Katakuri", "Oven", "Smoothie", "Daifuku", "Compote", "Cracker", "Snack"]
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
        self.lawnames.append(law)

class Law( object):

    """title = ''
    identifier = ''
    billtitles=[]"""

    def __init__(self, identifier, title):
        self.title=title
        self.identifier=identifier
        self.billtitles=[]

    def addBillTitle(self, billtitle):
        self.billtitles.append(billtitle)


class Scraper( object ):

    """legislature="NONE"
    bills=[]"""

    def __init__(self):
        self.bills=[]

    def retrieve_bills( self , filename):
        pass

    def format_bills(self, collection):
        pass

    def store_bills(self):
        for bill in self.bills:
            storeBill(bill)
            #need to update law table also
            for lawname in bill.lawnames:
                law=Law(lawname, lawname)
                cachedLaw=retrieveLaw(lawname)
                if cachedLaw==None:
                    law.addBillTitle(bill.title)
                    storeLaw(law)
                else:
                    print(cachedLaw.billtitles)
                    cachedLaw.addBillTitle(bill.title)
                    updateLaw(cachedLaw)
