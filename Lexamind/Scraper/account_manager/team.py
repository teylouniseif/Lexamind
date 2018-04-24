#! python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  30 21:57:00 2018
@author: Saif Kurdi-Teylouni
"""
from storer.storer import storeUser, retrieveUser, retrieveUsersByTeam, storeLaw, deleteLaw, retrieveLaw, updateLaw
from collections import namedtuple
import jsonpickle, re

class User( object):

    """username = ''
    identifier = ''
    password=''
    lawnames=["Perospero", "Katakuri", "Oven", "Smoothie", "Daifuku", "Compote", "Cracker", "Snack"]"""

    def __init__(self, username, identifier, password, team):
        self.username=title
        self.identifier=identifier
        self.team=team
        self.lawnames=[]

    def addLaw(self, law):
        sanitizedlaw=str(law.strip().lower())
        self.lawnames.append(sanitizedlaw)

class Team( object ):

    """legislature="NONE"
    bills=[]"""

    def __init__(self):
        self.users=[]
        self.teamname=""

    def load_users(self):
        self.users=retrieveUsersByTeam(self.teamname)
        for user in self.users:
            for law in user.lawnames:
                print(law)

    def store_user(self):
        for user in self.users:
            storeUser(user)
            #need to update law table also
            for lawname in user.lawnames:
                law=Law(lawname, lawname)
                cachedLaw=retrieveLaw(lawname)
                if cachedLaw==None:
                    storeLaw(law)

    def getUsers(self):
        return self.users
