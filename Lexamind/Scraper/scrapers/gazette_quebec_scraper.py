# -*- coding: utf-8 -*-
"""
Created on Sat Mar  3 15:28:38 2018
@author: Sacha Perry-Fagant
"""

# Make sure we can access the resoures file
import sys
import os
parentDir = os.getcwd().split('\\Scraper')[0]
if parentDir not in sys.path:
    sys.path.insert(0,parentDir)

import urllib.request as urllib2
from bs4 import BeautifulSoup
import requests
from urllib.request import Request, urlopen
from PyPDF2 import PdfFileReader
from io import BytesIO
import os, re
import csv

encrypted_file = "encr.pdf"
decrypted_file = "decry.pdf"
text_file = "text.txt"

"""
info to get:
gazette number:ex, 16 or 16A
gazette date

for each law of interest, any sort of action that is tied to it, reglement, decret, decisions
"""
from scraper_api import Scraper, Bill

class GazetteQuebec( Scraper ):

    rgx_modified_title = 'Règlement modifiant'
    law_delimiter_str="\n\n"

    RELEVANCYSTRING=r"(^loi(s)?|^règlement(s)?)\s+(modifié(e)(s)?|remplacé(e)(s)?|abrogé(e)(s)?).*"
    MOFIFIEDLAWSTRINGSTART=r"œ.*"#"(loi|code|règlement|charte).*"
    MOFIFIEDLAWSTRINGEND=r".*;\s*$|.*\.\s*$"

    def __init__(self):
        super(Scraper, self).__init__()
        self.legislature="GazetteQuébec"

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
    def retrieve_bills(self, start_year = 2018):
        # This url is very long because the original url kept redirecting to the main page
        url = "http://www2.publicationsduquebec.gouv.qc.ca/gazette_officielle/partie_2f-liste.php"
        soup = GazetteQuebec.Make_Soup(url)

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
                data += self.Find_Year_Data(year_url, year)

        GazetteQuebec.Convert_To_Csv(data)

        return data

    # Scrape all pdfs corresponding to a certain year
    def Find_Year_Data(self, url, year):
        soup = GazetteQuebec.Make_Soup(url)

        # False when there was an error connecting
        if soup == False:
            return []

        table = soup.find('table')
        while 'title' not in table.attrs:
            table = table.findNext('table')

        data = []
        databill = []

        rows = table.findAll('tr')
        for r in rows:
            els = r.findAll('td')

            # Finding the gazette number and data
            gazette = els[0].text
            date = gazette.split('No. ')[0]
            number = gazette.split('No. ')[1]

            #print(gazette)
            if number!="27":
                continue


            print("Scraping pdf number: " + number)
            # get the last element of the table
            pdf_url = els[len(els)-1].find('a')['href']
            # Storing the gazette number, date, the url and the pdf
            text=GazetteQuebec.Extract_Pdf(pdf_url)
            data.append([number, date, pdf_url, text])
            bill_info = Bill(self.legislature+number, self.legislature+number, self.legislature)
            bill_info.addEvent("Publication", date, None, None)
            bill_info.setDetails(text)
            bill_info.setHyperlink(pdf_url)
            print(bytes(text, "UTF-8"))
            print(bill_info.hyperlink+"hey")
            self.scrapeLawsinBill(bill_info)
            databill.append(bill_info)

        self.bills=databill
        return data

    def scrapeLawsinBill(self, bill):
        modification = re.split(GazetteQuebec.rgx_modified_title, bill.details)
        if modification==None:
            return
        else:
            #print(modification)
            for match in modification:
                modifiedLaws = match.split(GazetteQuebec.law_delimiter_str)[0]
                #print(modifiedLaws+"\n")
        """for
         in modifiedLaws:
            if modifiedLaw.find('Loi')!=-1 or modifiedLaw.find('Code')!=-1:
                #print(modifiedLaw+"noni")
                bill.addLaw(modifiedLaw)"""

    # Downloads the pdf and extracts the text
    def Extract_Pdf(url):
        data = ""

        onlineFile = urlopen(Request(url)).read()
        pdfFile = PdfFileReader(BytesIO(onlineFile))

        if pdfFile.isEncrypted:
            fp, pdfFile = GazetteQuebec.decrypt_pdf(url)
            fp.close()
            
            # Convert pdf to text
            os.system("pdftotext " + decrypted_file + " " + text_file)
            
            with open(text_file, encoding="utf8") as fl:
                for line in fl:
                    data += line
                fl.close()
            
            # delete the files so we can reuse them
            os.system("del " + encrypted_file)
            os.system("del " + decrypted_file)

        else:
            for pageNum in range(pdfFile.getNumPages()):
                currentPage = pdfFile.getPage(pageNum)
                data += currentPage.extractText()
            
            os.system("del " + text_file)


        return data

    # Requires qpdf!
    # If the pdf is encrypted, qpdf is used to decrypt it
    # Requires the pdf to be saved temporarily
    def decrypt_pdf(url):
        GazetteQuebec.save_pdf(url)
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
