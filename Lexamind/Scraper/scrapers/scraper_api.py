#! python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  30 21:57:00 2018
@author: Saif Kurdi-Teylouni
"""
from storer.storer import storeBill

class Scraper( object ):

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
