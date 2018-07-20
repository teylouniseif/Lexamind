#! python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  30 21:57:00 2018
@author: Saif Kurdi-Teylouni
"""
from storer.storer import storeUser, retrieveUser, retrieveUsersByTeam, storeLaw, deleteLaw, retrieveLaw, updateLaw, storeArchive, updateArchive, retrieveBill
from collections import namedtuple
from .team import User
from .html_template import Template
import jsonpickle, re

class Update(object):

    """username = ''
    identifier = ''
    lastUpdate= ''
    """

    def __init__(self, username, identifier, lastUpdate):
        self.username=username
        self.identifier=identifier
        self.lastUpdate=lastUpdate

    def get_Content(self):
        return self.lastUpdate

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
            strippedlawname=user.LawNamefromOfficaltoBill(lawname)
            cachedLaw=retrieveLaw(strippedlawname)
            if cachedLaw!=None:
                bills=cachedLaw.getDependantBills()
                for billid in bills:
                    bill=retrieveBill(billid)
                    print(bill.identifier+"here")
                    updatetext+=self.build_update(user, bill, strippedlawname)
        html=self.inject_update_in_template(updatetext)
        update=Update(user.username, user.username, html)
        storeArchive(update)

    def build_update(self, user, bill, cachedLaw):
        #build html src code
        if bill.legislature=="GazetteQuébec":
            billno=bill.title.split("_")[0]
        else:
            billno=bill.title.strip(bill.legislature)
        if len(bill.events)!=0:
            stage=bill.events[-1]["stage"]
            date=bill.events[-1]["date"]
        else:
            stage="N/A"
            date="N/A"
        hyperlink="N/A"
        if hasattr(bill, 'hyperlink'):
            hyperlink="<a href="+bill.hyperlink+">Contenu</a>"
        lawtitle=bill.legislature+" - " +cachedLaw.split("(")[0]
        html="                <tr class=\"data-row new\" style=\"padding: 0;vertical-align: top;text-align: left;\">\r\n"\
    		"                  <td class=\"even\" style=\"border-bottom: 1px solid rgba(0,0,0,0.2);border-collapse: collapse !important;word-wrap: break-word;-webkit-hyphens: auto;-moz-hyphens: auto;hyphens: auto;padding: 10px;vertical-align: top;text-align: left;font-family: 'Helvetica', sans-serif; width: 30%;\">"+billno+"</td>\r\n"\
    		"                  <td style=\"border-bottom: 1px solid rgba(0,0,0,0.2);border-collapse: collapse !important;word-wrap: break-word;-webkit-hyphens: auto;-moz-hyphens: auto;hyphens: auto;padding: 10px;vertical-align: top;text-align: left;font-family: 'Helvetica', sans-serif; width: 20%;\">"+lawtitle+"</td>\r\n"\
    		"                  <td class=\"even\" style=\"border-bottom: 1px solid rgba(0,0,0,0.2);border-collapse: collapse !important;word-wrap: break-word;-webkit-hyphens: auto;-moz-hyphens: auto;hyphens: auto;padding: 10px;vertical-align: top;text-align: left;font-family: 'Helvetica', sans-serif; width: 20%;\">"+stage+"</td>\r\n"\
    		"                  <td style=\"border-bottom: 1px solid rgba(0,0,0,0.2);border-collapse: collapse !important;word-wrap: break-word;-webkit-hyphens: auto;-moz-hyphens: auto;hyphens: auto;padding: 10px;vertical-align: top;text-align: left;font-family: 'Helvetica', sans-serif; width: 10%;\">"+date+"</td>\r\n"\
    		"                  <td class=\"even\" style=\"border-bottom: 1px solid rgba(0,0,0,0.2);border-collapse: collapse !important;word-wrap: break-word;-webkit-hyphens: auto;-moz-hyphens: auto;hyphens: auto;padding: 10px;vertical-align: top;text-align: left;font-family: 'Helvetica', sans-serif; width: 10%;\">"+bill.legislature+"</td>\r\n"\
    		"                  <td class=\"even\" style=\"border-bottom: 1px solid rgba(0,0,0,0.2);border-collapse: collapse !important;word-wrap: break-word;-webkit-hyphens: auto;-moz-hyphens: auto;hyphens: auto;padding: 10px;vertical-align: top;text-align: left;font-family: 'Helvetica', sans-serif; width: 10%;\">"+hyperlink+"</td>\r\n"\
    		"                </tr>\r\n"
        return html

    def inject_update_in_template(self, updatetext):
        return Template.emailStart+Template.rowfont+updatetext+Template.emailEnd

    def addUser(self, user):
        self.users.append(user)

    def getUsers(self):
        return self.users
