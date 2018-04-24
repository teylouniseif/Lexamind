# -*- coding: utf-8 -*-
"""
Created on Sat Mar  3 15:28:38 2018
@author: Sacha Perry-Fagant
"""

import urllib.request as urllib2
from bs4 import BeautifulSoup
import requests
from urllib.request import Request, urlopen
from PyPDF2 import PdfFileReader
from io import BytesIO
import os
import csv

encrypted_file = "encr.pdf"
decrypted_file = "decry.pdf"

"""
info to get:
gazette number:ex, 16 or 16A
gazette date

for each law of interest, any sort of action that is tied to it, reglement, decret, decisions
"""


# Takes in a url, checks the connection and returns the soup
def Make_Soup(url):

    response = ""

    # If there's an issue connecting to the internet, end the program
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print("There was an error finding the page")
            return False
    except:
        print("There was an issue connecting to the internet")
        exit()

    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page, "html.parser")

    # If you try to go to a bill url that doesn't exist
    if 'inexistant' in soup.text:
        return False

    return soup

# The main function to scrape Publications du Quebec
# The end year is the oldest year that we'll scrape pdfs for
def Scrape_Quebec(start_year = 2018):
    # This url is very long because the original url kept redirecting to the main page
    url = "http://www2.publicationsduquebec.gouv.qc.ca/gazette_officielle/partie_2f-liste.php"
    soup = Make_Soup(url)

    # False when there was an error connecting
    if soup == False:
        return False

    data = []

    rows = soup.find_all('div')

    for r in rows:
        if 'style' in r.attrs and 'background' in r.attrs['style']:
            year_url = "http" + r.find("a")["onclick"].split("http")[1].split("'")[0]
            year = year_url.split("gazette=")[1]
            if int(year) < start_year:
                break
            print("Now scraping: " + year)
            data += Find_Year_Data(year_url, year)

    Convert_To_Csv(data)

    return data

# Scrape all pdfs corresponding to a certain year
def Find_Year_Data(url, year):
    soup = Make_Soup(url)

    # False when there was an error connecting
    if soup == False:
        return []

    table = soup.find('table')
    while 'title' not in table.attrs:
        table = table.findNext('table')

    data = []

    rows = table.findAll('tr')
    for r in rows:
        els = r.findAll('td')

        # Finding the gazette number and data
        gazette = els[0].text
        date = gazette.split('No. ')[0]
        number = gazette.split('No. ')[1]
        print("Scraping pdf number: " + number)
        # get the last element of the table
        pdf_url = els[len(els)-1].find('a')['href']
        # Storing the gazette number, date, the url and the pdf
        data.append([number, date, pdf_url, Extract_Pdf(pdf_url)])

    return data


# Downloads the pdf and extracts the text
def Extract_Pdf(url):
    data = ""

    onlineFile = urlopen(Request(url)).read()
    pdfFile = PdfFileReader(BytesIO(onlineFile))

    if pdfFile.isEncrypted:
        fp, pdfFile = decrypt_pdf(url)
        for pageNum in range(pdfFile.getNumPages()):
            currentPage = pdfFile.getPage(pageNum)
            data += currentPage.extractText()
        fp.close()
        # delete the files so we can reuse them
        os.system("del " + encrypted_file)
        os.system("del " + decrypted_file)

    else:
        for pageNum in range(pdfFile.getNumPages()):
            currentPage = pdfFile.getPage(pageNum)
            data += currentPage.extractText()

    return data

# Requires qpdf!
# If the pdf is encrypted, qpdf is used to decrypt it
# Requires the pdf to be saved temporarily
def decrypt_pdf(url):
    save_pdf(url)
    command = ('qpdf --password="" --decrypt ' + encrypted_file + " " + decrypted_file)

    result = os.system(command)
    if result == 1:
        print("Failure at " + url)
    fp = open(decrypted_file,'rb')
    pdfFile = PdfFileReader(fp)
    return fp, pdfFile

# Saves the pdf under the name of encrypted_file
# This file will be deleted later
def save_pdf(url):
    r = requests.get(url, stream = True)
    file = open(encrypted_file, 'wb')
    file.write(r.content)
    file.close()

def Convert_To_Csv(data, fileName = "Gazette_Officielle.csv"):
    csvfile = open(fileName, 'w', newline='',encoding="utf-8")
    file = csv.writer(csvfile)
    labels = ['Number','date','url','pdf']
    file.writerow(labels)
    for row in data:
        file.writerow(row)
    csvfile.close()
    return

    file.close()

    return
