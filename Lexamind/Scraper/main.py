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
from storer.storer import retrieveLaw, deleteBillsByLegislature, retrieveBillsByLegislature, deleteLawsByLegislature
import json
import jsonpickle

"""y=Canada()
y.retrieve_bills()
y.store_bills()

y=Ontario()
y.retrieve_bills()
y.store_bills()
y=Quebec()
y.retrieve_bills()
y.store_bills()"""
"""y=Alberta()
y.retrieve_bills()
y.store_bills()"""
"""y=GazetteQuebec()
y.retrieve_bills()
y.store_bills()"""
#deleteBillsByLegislature("Ontario")
#deleteLawsByLegislature("Ontario")



x=User("dominique.payette@bnc.ca", "dominique.payette@bnc.ca", "billscraper")
#x=User("lexamindcooperathon@gmail.com", "lexamindcooperathon@gmail.com", "billscraper")
#x=User("gmorency@edilex.com", "gmorency@edilex.com", "edilex")
x.addLaw("Loi sur le financement des petites entreprises du Canada, LC 1998, c 36 (Canada)")
x.addLaw("Loi canadienne sur les sociétés par actions, LRC 1985, c C-44 (Canada)")
x.addLaw("Loi sur la publicité légale des entreprises, RLRQ c P-44.1 (Québec)")
x.addLaw("Loi sur les sociétés par actions, RLRQ c S-31.1 (Québec)")
x.addLaw("Franchises Act, SBC 2015, c 35 (Colombie-Britannique)")
x.addLaw("Loi électorale du Canada, LC 2000, c 9 (Canada)")
x.addLaw("Loi concernant le financement des partis politiques, LQ 2010, c 36 (Québec)")
x.addLaw("Builders' Lien Act, RSA 2000, c B-7 (Alberta)")
#x.addLaw("Builders' Lien Act (Colombie-Britannique)")
#x.addLaw("Builders' Lien Act (Manitoba)")
#x.addLaw("Mechanics' Lien Act (Nouveau-Brunswick)")
x.addLaw("Construction Lien Act, RSO 1990, c C.30 (Ontario)")
#x.addLaw("The Builders' Lien Act (Saskatchewan)")
#x.addLaw("Mechanics' Lien Act (Terre-Neuve et Labrador)")
#x.addLaw("Mechanics Lien Act (Territoires du Nord-Ouest)")
#x.addLaw("Builders Lien Act (Yukon)")
#x.addLaw("Code civil du Québec, Livre sixième, Titre troisième (Québec)")
x.addLaw("Code civil du Québec, RLRQ c CCQ-1991 (Québec)")
#x.addLaw("Land Title Act (Colombie-Britannique)")
x.addLaw("Land Title and Survey Authority Act, SBC 2004, c 66 (Colombie-Britannique)")
#x.addLaw("Land Registration Act (Nouvelle-Écosse)")
#x.addLaw("Registry Act (Nouvelle-Écosse)")
#x.addLaw("Registry Act (Île du Prince Édouard)")
x.addLaw("Registry Act, RSO 1990, c R.20 (Ontario)")
#x.addLaw("Registry Act (Nouveau-Brunswick)")
#x.addLaw("Registry Act (Manitoba)")
x.addLaw("Land Titles Act, RSA 2000, c L-4 (Alberta)")
#x.addLaw("The Land Titles Act, 2000 (Saskatchewan)")
#x.addLaw("Registration of Deeds Act, 2009 (Terre-Neuve et Labrador)")
#x.addLaw("Code civil du Québec, Livre sixième, Titre deuxième (Québec)")
x.addLaw("Personal Property Security Act, RSA 2000, c P-7 (Alberta)")
#x.addLaw("Personal Property Security Act (Colombie-Britannique)")
#x.addLaw("Personal Property Security Act (Manitoba)")
#x.addLaw("Personal Property Security Act (Nouvelle-Écosse)")
x.addLaw("Personal Property Security Act, RSO 1990, c P.10 (Ontario)")
#x.addLaw("Personal Property Security Act (Nouveau-Brunswick)")
#x.addLaw("Personal Property Security Act (Île du Prince Édouard)")
#x.addLaw("Personal Property Security Act (Saskatchewan)")
#x.addLaw("Code civil du Québec, Livre sixième, Titre troisième (Québec)")
#x.addLaw("Personal Property Security Act (Terre-Neuve et Labrador)")
#x.addLaw("Personal Property Security Act (Territoires du Nord-Ouest)")
#x.addLaw("Personal Property Security Act (Territoires du Nord-Ouest)")
#x.addLaw("Personal Property Security Act (Yukon)")
x.addLaw("Loi sur la marine marchande du Canada, LC 2001, c 26 (Canada)")
x.addLaw("New Home Buyer Protection Act, SA 2012, c N-3.2(Alberta)")
x.addLaw("Loi sur la faillite et l'insolvabilité, LRC 1985, c B-3 (Canada)")
x.addLaw("Loi sur le recyclage des produits de la criminalité et le financement des activités terroristes, LC 2000, c 17 (Canada)")
#x.addLaw("B-8 - Mécanismes de dissuasion et de détection du recyclage des produits de la criminalité et du financement des activités terroristes (BSIF – CAN)")

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

"""bills=retrieveBillsByLegislature("Canada")
for bill in bills:
    #print(bill.title)
    #print(bill.identifier)

    print("in this bill %s\n", bill.identifier)
    for law in bill.lawnames:
            print(law)"""

all=Team()
#all.addUser(x)

#all.store_users()
#all.store_accounts()
all.load_users_from_accounts()
dummyvar=1#print(all.users)

v=Information()
for y in all.users:
    v.addUser(y)
v.build_archives()

#choose the email to send update to
Email.send_Email("lexamindcooperathon@gmail.com")
