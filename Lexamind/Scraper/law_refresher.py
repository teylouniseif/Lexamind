#!/usr/bin/python3
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
from storer.storer import retrieveLaw, deleteBillsByLegislature, retrieveBillsByLegislature, deleteLawsByLegislature, storeUser, storeAccount, deleteAllBills, deleteAllLaws
import json
import jsonpickle

deleteAllBills()
deleteAllLaws()
y=Canada()
y.retrieve_bills()
y.store_bills()
y=Ontario()
y.retrieve_bills()
y.store_bills()
y=Quebec()
y.retrieve_bills()
y.store_bills()
y=Alberta()
y.retrieve_bills()
y.store_bills()
y=GazetteQuebec()
y.retrieve_bills()
y.store_bills()
