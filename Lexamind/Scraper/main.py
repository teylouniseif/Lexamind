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
#deleteBillsByLegislature("Ontario")
#deleteLawsByLegislature("Ontario")


#x.addLaw("Procédure de conciliation et d’arbitrage des comptes des sexologues ; Code des professions, (GazetteQuébec)")
"""x.addLaw("police act, (Alberta)")
x.addLaw("charte de la ville de montréal, (Québec)")
x.addLaw("la loi de 1991 sur les audiologistes, (Ontario)")
x.addLaw("loi sur la sûreté des déplacements aériens")
x.addLaw("loi sur la protection des renseignements personnels dans le secteur privé")"""


#first step: add user
#x=User("dominique.payette@bnc.ca", "dominique.payette@bnc.ca", "billscraper")
#second step: add laws
#x.addLaw("Loi sur le financement des petites entreprises du Canada, LC 1998, c 36 (Canada)")

"""all=Team()
#all.addUser(x)

#all.store_users()
#all.store_accounts()
all.load_users_from_accounts()
dummyvar=1#print(all.users)

v=Information()
for y in all.users:
    print(y.username)
    if y.username=="annie.milette@bnc.ca":
        #y.addLaw("police act, (Alberta)")
        #storeUser(y)
        #storeAccount(y)
        pass
    v.addUser(y)
v.build_archives()

#choose the email to send update to
Email.send_Email("lexamindcooperathon@gmail.com")"""
