#! python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  30 21:57:00 2018
@author: Saif Kurdi-Teylouni
"""

from scrapers.ontario_scraper import Ontario
from scrapers.version_converter import call_python_version
from federal_scraper.federal_scraper import my_function
from storer.database import Database

y=Ontario()
data=y.retrieve_bills()
#data=Ontario()
x=Database()
x.addRecord(data)

#result = call_python_version("2.7", "scrapers.federal_scraper", "my_function",
#                             ["Mr", "Bear"])

#result = call_python_version("2.7", "federal_scraper.federal_scraper", "my_function",[])

#my_function()
