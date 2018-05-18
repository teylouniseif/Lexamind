#! python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  30 21:57:00 2018
@author: Saif Kurdi-Teylouni
"""
from storer.storer import storeUser, retrieveUser, retrieveUsersByTeam, storeLaw, deleteLaw, retrieveLaw, updateLaw
from scrapers.scraper_api import Law
from collections import namedtuple
import jsonpickle, re

class User( object):

    """username = ''
    identifier = ''
    password=''
    team=''
    lawnames=["Perospero", "Katakuri", "Oven", "Smoothie", "Daifuku", "Compote", "Cracker", "Snack"]"""

    def __init__(self, username, identifier, password, lawnames=[], team=None):
        self.username=username
        self.identifier=identifier
        self.team=team
        self.password=password
        self.lawnames=lawnames

    def addLaw(self, law):
        sanitizedlaw=str(law.strip().lower())
        self.lawnames.append(sanitizedlaw)

class Team( object ):

    """teamname="NONE"
    users=[]"""

    def __init__(self, users=[], teamname=None):
        self.users=users
        self.teamname=teamname

    def load_users(self):
        self.users=retrieveUsersByTeam(self.teamname)
        for user in self.users:
            for law in user.lawnames:
                print("this is it: "+law)

    def store_users(self):
        for user in self.users:
            storeUser(user)
            #need to update account table
            storeAccount(user)
            #need to update law table also
            for lawname in user.lawnames:
                law=Law(lawname, lawname)
                cachedLaw=retrieveLaw(lawname)
                if cachedLaw==None:
                    storeLaw(law)

    def addUser(self, user):
        self.users.append(user)

    def getUsers(self):
        return self.users
