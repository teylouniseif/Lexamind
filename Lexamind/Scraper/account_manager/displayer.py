#! python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  30 21:57:00 2018
@author: Saif Kurdi-Teylouni
"""
from storer.storer import storeUser, retrieveUser, retrieveUsersByTeam, storeLaw, deleteLaw, retrieveLaw, updateLaw
from collections import namedtuple
import user
import jsonpickle, re

class Update(object):

class Information( object ):

    """legislature="NONE"
    bills=[]"""

    def __init__(self):
        self.users=[]

    def set_users(self, users):
        self.users=users

    def build_archives(self):
        for user in self.users:
            build_update_by_user(user)

    def build_update_by_user(user):
        updatetext=""
        for lawname in user.lawnames:
            cachedLaw=retrieveLaw(lawname)
            if cachedLaw!=None:
                bills=cachedLaw.getDependantBills()
                for bill in bills
                updatetext+=build_update(user, bills, cachedLaw)
        update=Update(user, updatetext)
        storeArchive(update)

    def build_update(user, bills, cachedLaw):
        #build html src code
        pass

    def getUsers(self):
        return self.users
