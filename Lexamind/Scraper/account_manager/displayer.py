#! python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  30 21:57:00 2018
@author: Saif Kurdi-Teylouni
"""
from storer.storer import storeUser, retrieveUser, retrieveUsersByTeam, storeLaw, deleteLaw, retrieveLaw, updateLaw, storeArchive
from collections import namedtuple
from .team import User
from .html_template import Template
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
                for bill in bills:
                    updatetext+=self.build_update(user, bill, cachedLaw)
        html=self.inject_update_in_template(updatetext)
        update=Update(user.username, user.username, html)
        storeArchive(update)

    def build_update(self, user, bill, cachedLaw):
        #build html src code
        billno=bill.title.strip(bill.legislature)
        html="                <tr class=\"data-row new\" style=\"padding: 0;vertical-align: top;text-align: left;\">\r\n"\
    		"                  <td class=\"even\" style=\"border-bottom: 1px solid rgba(0,0,0,0.2);border-collapse: collapse !important;word-wrap: break-word;-webkit-hyphens: auto;-moz-hyphens: auto;hyphens: auto;padding: 10px;vertical-align: top;text-align: left;font-family: 'Helvetica', sans-serif;\">"+match.changeType+"</td>\r\n"\
    		"                  <td style=\"border-bottom: 1px solid rgba(0,0,0,0.2);border-collapse: collapse !important;word-wrap: break-word;-webkit-hyphens: auto;-moz-hyphens: auto;hyphens: auto;padding: 10px;vertical-align: top;text-align: left;font-family: 'Helvetica', sans-serif;\">"+cachedLaw+"</td>\r\n"\
    		"                  <td class=\"even\" style=\"border-bottom: 1px solid rgba(0,0,0,0.2);border-collapse: collapse !important;word-wrap: break-word;-webkit-hyphens: auto;-moz-hyphens: auto;hyphens: auto;padding: 10px;vertical-align: top;text-align: left;font-family: 'Helvetica', sans-serif;\">"+billno+"</td>\r\n"\
    		"                  <td style=\"border-bottom: 1px solid rgba(0,0,0,0.2);border-collapse: collapse !important;word-wrap: break-word;-webkit-hyphens: auto;-moz-hyphens: auto;hyphens: auto;padding: 10px;vertical-align: top;text-align: left;font-family: 'Helvetica', sans-serif;\">"+formatter.format(match.changeTime)+"</td>\r\n"\
    		"                  <td class=\"even\" style=\"border-bottom: 1px solid rgba(0,0,0,0.2);border-collapse: collapse !important;word-wrap: break-word;-webkit-hyphens: auto;-moz-hyphens: auto;hyphens: auto;padding: 10px;vertical-align: top;text-align: left;font-family: 'Helvetica', sans-serif;\">"+bill.legislature+"</td>\r\n"\
    		"                  <td class=\"even\" style=\"border-bottom: 1px solid rgba(0,0,0,0.2);border-collapse: collapse !important;word-wrap: break-word;-webkit-hyphens: auto;-moz-hyphens: auto;hyphens: auto;padding: 10px;vertical-align: top;text-align: left;font-family: 'Helvetica', sans-serif;\">"+"nourlfornow"+"</td>\r\n"\
    		"                </tr>\r\n"
        return html

    def inject_update_in_template(self, updatetext):
        return Template.emailStart+Template.rowfont+updatetext+Template.emailEnd

    def addUser(self, user):
        self.users.append(user)

    def getUsers(self):
        return self.users
