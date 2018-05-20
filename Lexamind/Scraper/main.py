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
from account_manager.team import Team, User
from account_manager.displayer import Information
from account_manager.emailer import Email
from scrapers.version_converter import call_python_version
#from federal_scraper.federal_scraper import my_function
#from scrapers.federal_scraper import my_function
from storer.database import Database
from storer.storer import retrieveLaw
import json
import jsonpickle

#Email.send_Email("teylouniseif@gmail.com")

"""y=Quebec()
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

print("noni")"""

#for bill in y.bills:
    #if len(bill.events)!=0:
    #    print(bill.events[0]['date']+"\n")
    #print(bill.title)
    #print(bill.details)
    #if len(bill.lawnames)!=0:
    #    print(bill.lawnames[0]+"noni")

#y.retrieve_bills()
#y.store_bills()
"""newbill=Database.findRecord("Perospero", "Lexamind", "Laws")
print(jsonpickle.decode(newbill['item']).title)
#print(jsonpickle.decode(newbill['item']).billtitles)
newbill=Database.findRecord("Ontariobill1", "Lexamind", "Bills")
print(jsonpickle.decode(newbill['item']).title)
details=jsonpickle.decode(newbill['item']).details
print('littlenoni')
print(str(details, 'utf-8'))"""
#y.store_bills()
#data=Ontario()
#law=retrieveLaw("code de la sécurité routière".encode("utf-8"))
#print(law.title)

x=User("teylouniseif@gmail.com", "teylouniseif@gmail.com", "diazbrother")
x.addLaw("police act")
x.addLaw("charte de la ville de montréal")
x.addLaw("la loi de 1991 sur les audiologistes")
x.addLaw("loi sur la sûreté des déplacements aériens")

all=Team()
all.addUser(x)

all.store_users()
all.store_accounts()
#all.load_users_from_accounts()


v=Information()
for y in all.users:
    print("noice")
    v.addUser(y)
v.build_archives()

input("wait")

Email.send_Email("teylouniseif@gmail.com")

#emails=[BillGates@gmail.com,SteveJobs@yahoo.com,BillJobs@aol.com,nick@gmail.com,vic@gmail.com,prince@yahoo.in]

laws=["""RÈGLEMENT (CE) N o 593/2008 DU PARLEMENT EUROPÉEN ET DU CONSEIL du 17 juin 2008 sur la loi applicable aux obligations contractuelles\n
Electronic Code of Federal Regulations (USA)\n
RÈGLEMENT (UE) 2016/679 DU PARLEMENT EUROPÉEN ET DU CONSEIL du 27 avril 2016 relatif à la protection des personnes physiques à l'égard du traitement des données à caractère personnel et à la libre circulation de ces données, et abrogeant la directive 95/46/CE (règlement général sur la protection des données)\n
Loi sur les mesures extraterritoriales étrangères (CAN)\n
Loi sur le recyclage des produits de la criminalité et le financement des activités terroristes (CAN)\n
B-8 - Mécanismes de dissuasion et de détection du recyclage des produits de la criminalité et du financement des activités terroristes (BSIF – CAN)\n""",

"""Code de procédure civil (QC)\n
Rules of Civil Procedure (ON)\n
Loi sur la publicité légale des entreprises (QC)\n
Loi sur les sociétés par actions (QC)\n
Code civil du Québec (QC)\n
Personal Property Security Act (ON)\n
Loi canadienne sur les sociétés par actions (CAN)\n
Loi sur les assurances (QC)\n
Loi sur les contrats des organismes publics (QC)\n
Loi sur les sociétés de fiducie et de prêt (CAN)\n
Loi sur les sociétés de fiducie et les sociétés d’épargne(QC)\n
Electronic Commerce Act (Ont.)\n
Loi sur la faillite et l'insolvabilité (CAN)\n
Loi canadienne sur la protection des renseignements\n
personnels et les documents électroniques (CAN)\n
Loi sur la protection des renseignements personnels dans le secteur privé (QC)\n
Consumer Protection Act (Ont.)\n
Loi sur la protection du consommateur (QC)\n""",

"""Code canadien du travail (CAN)\n
Loi canadienne sur les droits de la personne (CAN)\n
Loi sur l'équité en matière d'emploi (CAN)\n
Loi sur les normes du travail (QC)\n
Loi sur les accidents du travail et les maladies professionnelles (QC)\n
Charte des droits et libertés de la personne (QC)\n
Loi sur la santé et la sécurité du travail (QC)\n
Loi sur l'équité salariale (QC)\n
Loi de 2000 sur les normes d'emploi (ON)\n
Code des droits de la personne (ON)\n
Loi sur la santé et la sécurité au travail (ON)\n
Loi sur l'équité salariale (ON)\n""",

"""Charte de la langue française\n
Code civil du Québec\n
Loi sur la transparence et l’éthique en matière de lobbyisme\n
Loi sur la distribution de produits et services financiers\n
Loi concernant le cadre juridique des technologies de l’information\n
Loi sur les impôts\n
Loi sur l’assurance-dépôts\n
Loi sur la protection des renseignements personnels dans le secteur privé\n
Loi sur la protection du consommateur\n
Loi sur le recouvrement de certaines créances\n
Loi sur les assurances\n
Loi sur les biens non réclamés\n
Loi sur les instruments dérivés\n
Loi sur les loteries, les concours publicitaires et les appareils d’amusement\n
Loi sur les régimes complémentaires de retraite\n
Loi sur les sociétés de fiducie et les sociétés d’épargne\n
Loi sur les valeurs mobilières\n""",

"""Code de procédure civil (QC)\n
Rules of Civil Procedure (ON)\n
Loi sur la publicité légale des entreprises (QC)\n
Loi sur les sociétés par actions (QC)\n
Code civil du Québec (QC)\n
Personal Property Security Act (ON)\n
Loi canadienne sur les sociétés par actions (CAN)\n
Loi sur les mesures extraterritoriales étrangères (CAN)\n
Loi sur le recyclage des produits de la criminalité et le financement des activités terroristes (CAN)\n""",

"""Ligne directrice – Gouvernance d’entreprise (BSIF)\n
Loi sur les Banques (CAN)\n
Loi sur les contrats des organismes publics (QC)\n
Loi sur les valeurs mobilières (QC)\n
Règlement de l'Autorité des marchés financiers pour l'application de la Loi sur les contrats des organismes publics (QC)\n
Règlement sur les personnes physiques membres d'un groupe (banques) (CAN)\n
Règlementation en valeurs mobilières\n
Loi sur le lobbying (CAN)\n"""]

#password=["gates123", "jobs4days", "therealjobs", "diazbrother", "vic451","princeofwales"]

"""for bill in y.bills:
    #bill['_id']=bill['identifier']
    record=Database.createDocumentfromField(bill, 'identifier')
    #x.deleteRecord(bill, "Lexamind", "Users")
    Database.addRecord(record, "Lexamind", "Users")
    bill.title='noni'
    record=Database.createDocumentfromField(bill, 'identifier')
    Database.updateRecord(record, "Lexamind", "Users")
    newbill=Database.findRecord(record['_id'], "Lexamind", "Users")
    print(jsonpickle.decode(newbill['item']).title)
    print(jsonpickle.decode(newbill['item']).details)"""
