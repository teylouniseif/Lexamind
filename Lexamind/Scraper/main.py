#! python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  30 21:57:00 2018
@author: Saif Kurdi-Teylouni
"""

from scrapers.ontario_scraper import Ontario
from scrapers.alberta_scraper import Alberta
from scrapers.assnat_scraper import Quebec
from scrapers.federal_scraper import Canada
from scrapers.newfoundland_scraper import Newfoundland
from scrapers.gazette_quebec_scraper import GazetteQuebec
from account_manager.team import Team, User
from account_manager.displayer import Information
from account_manager.emailer import Email
from scrapers.version_converter import call_python_version
from storer.database import Database
from storer.storer import retrieveLaw, deleteBillsByLegislature, retrieveBillsByLegislature, deleteLawsByLegislature, storeUser, storeAccount
import json
import jsonpickle

#y=Canada()
#y.retrieve_bills()
#y.store_bills()
#y=Ontario()
#y.retrieve_bills()
#y.store_bills()
#y=Quebec()
#y.retrieve_bills()
#y.store_bills()
#y=Alberta()
#y.retrieve_bills()
#y.store_bills()
#y=GazetteQuebec()
#y.retrieve_bills()
#y.store_bills()
#deleteBillsByLegislature("GazetteQuébec")
#deleteLawsByLegislature("GazetteQuébec")
    

#first step: add user
#x=User("nick.diaz@gmail.com", "nick.diaz@gmail.com", "billscraper")
#second step: add laws
#x.addLaw("Loi sur le financement des petites entreprises du Canada, LC 1998, c 36 (Canada)")

all=Team()
all.load_users_from_accounts()

v=Information()
for y in all.users:
    v.addUser(y)
v.build_archives()

#choose the email to send update to
#Email.send_Email("lexamindcooperathon@gmail.com")"""
