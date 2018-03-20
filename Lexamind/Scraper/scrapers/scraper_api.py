#! python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  30 21:57:00 2018
@author: Saif Kurdi-Teylouni
"""
from storer.storer import storeBill
from collections import namedtuple

class Scraper( object ):

    legislature="NONE"
    bills=[]

    def __init__(self):
        self.bills=[]

    def retrieve_bills( self , filename):
        pass

    def format_bills(self, collection):
        pass

    def store_bills(self):
        for bill in self.bills:
            #need to update law table also
            #need to define uniform bill object in this class for inhertiance
            storeBill(bill)

class Bill( object):

    title = ''
    identifier = ''
    events=[]
    details=''
    #laws=set()

    def __init__(self, identifier, title):
        self.title=title
        self.identifier=identifier

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
        pass
        #self.laws.add(law)
