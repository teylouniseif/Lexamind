#! python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  30 21:57:00 2018
@author: Saif Kurdi-Teylouni
"""
from storer.storer import storeUser, retrieveUser, retrieveUsersByTeam, storeLaw, deleteLaw, retrieveLaw, updateLaw, storeArchive
from collections import namedtuple
from .team import User
import jsonpickle, re

class Update(object):

    """username = ''
    identifier = ''
    htmlupdates= ''
    """

    def __init__(self, username, identifier, htmlupdates):
        self.username=username
        self.identifier=identifier
        self.htmlupdates=htmlupdates

class Information( object ):

    """legislature="NONE"
    bills=[]"""

    def __init__(self):
        self.users=[]

    def set_users(self, users):
        self.users=users

    def build_archives(self):
        for user in self.users:
            self.build_update_by_user(user)

    def build_update_by_user(self, user):
        updatetext=""
        for lawname in user.lawnames:
            cachedLaw=retrieveLaw(lawname)
            if cachedLaw!=None:
                bills=cachedLaw.getDependantBills()
                updatetext+=self.build_update(user, bills, cachedLaw)
        html=self.inject_update_in_template(updatetext)
        html="noni"
        update=Update(user.username, user.username, html)
        storeArchive(update)

    def build_update(self, user, bills, cachedLaw):
        #build html src code
        return ""

    def inject_update_in_template(self, updatetext):
        return ""

    def addUser(self, user):
        self.users.append(user)

    def getUsers(self):
        return self.users
