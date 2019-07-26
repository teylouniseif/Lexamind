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
import os, re
import csv
import copy
import datetime

encrypted_file = "encr.pdf"
decrypted_file = "decry.pdf"

"""
info to get:
gazette number:ex, 16 or 16A
gazette date

for each law of interest, any sort of action that is tied to it, reglement, decret, decisions
"""
from .scraper_api import Scraper, Bill

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
                dummyvar=1#print("There was an error finding the page")
                return False
        except:
            dummyvar=1#print("There was an issue connecting to the internet")
            exit()

        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page, "html.parser")

        # If you try to go to a bill url that doesn't exist
        if 'inexistant' in soup.text:
            return False

        return soup

    # The main function to scrape Publications du Quebec
    # The end year is the oldest year that we'll scrape pdfs for
    def retrieve_bills(self):
        # This url is very long because the original url kept redirecting to the main page
        url = "http://www2.publicationsduquebec.gouv.qc.ca/gazette_officielle/partie_2f-liste.php"
        soup = GazetteQuebec.Make_Soup(url)

        # False when there was an error connecting
        if soup == False:
            return False

        data = []

        rows = soup.find_all('div')

        start_year = datetime.datetime.now().year

        for r in rows:
            if 'style' in r.attrs and 'background' in r.attrs['style']:
                year_url = "http" + r.find("a")["onclick"].split("http")[1].split("'")[0]
                year = year_url.split("gazette=")[1]
                if int(year) < start_year:
                    break
                dummyvar=1#print("Now scraping: " + year)
                data += self.Find_Year_Data(year_url, year)

        GazetteQuebec.Convert_To_Csv(data)

        return data

    # Scrape all pdfs corresponding to a certain year
    def Find_Year_Data(self, url, year):
        dummyvar=1#print(url)
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

            dummyvar=1#print(gazette)
            #if number!="28":
                #continue


            dummyvar=1#print("Scraping pdf number: " + number)
            # get the last element of the table
            pdf_url = els[len(els)-1].find('a')['href']
            # Storing the gazette number, date, the url and the pdf
            dummyvar=1#print(els[0].find('a'))
            index_url= "http"+els[0].find('a')['onclick'].split("http")[1].split("\"")[0]
            #from index_url read every reglement title
            dummyvar=1#print(index_url+"hello")
            text=GazetteQuebec.Extract_Pdf(pdf_url)
            data.append([number, date, pdf_url, text])
            dummyvar=1#print(bytes(text, "UTF-8"))
            dummyvar=1#print(bill_info.hyperlink+"hey")
            bill_info=self.scrapeRegulationsinGazette(date, number, index_url, pdf_url, text)
            databill.extend(bill_info)

        self.bills=databill
        return data

    def scrapeRegulationsinGazette(self, date, number, index_url, pdf_url, text):
        soup=GazetteQuebec.Make_Soup(index_url)
        # False when there was an error connecting
        if soup == False:
            return []

        bills=[]

        bill_info = Bill(self.legislature+number+"_", self.legislature+number+"_", self.legislature)
        bill_info.setDetails(text)
        bill_info.setHyperlink(pdf_url)

        section_projects = soup.find('h2')
        dummyvar=1#print(section_projects.attrs)
        while section_projects!=None and 'class' in section_projects.attrs and ('titreRubrique' not in section_projects.attrs['class'][0] or 'Projets de règlement' not in section_projects.text) :
            dummyvar=1#print(section_projects.attrs['class'][0])

            section_projects = section_projects.findNext('h2')

        projects=[]
        while section_projects!=None and section_projects.findNext('a', attrs={'href': re.compile(".*http.*")}) != None:
            section_projects=section_projects.findNext('a', attrs={'href': re.compile(".*http.*")})
            projects.append(section_projects)

        section_regulations = soup.find('h2')
        while section_regulations!=None and 'class' in section_regulations.attrs and ('titreRubrique' not in section_regulations.attrs['class'][0] or 'Règlements et autres actes' not in section_regulations.text) :
            section_regulations = section_regulations.findNext('h2')

        regulations=[]
        while section_regulations!=None and section_regulations.findNext('a', attrs={'href': re.compile(".*http.*")}) != None:
            section_regulations=section_regulations.findNext('a', attrs={'href': re.compile(".*http.*")})
            regulations.append(section_regulations)

        projects=[x for x in projects if x not in regulations]

        for i in range(0 , len(projects)):
            if len(projects[i].text.split("—"))>1:
                bill=copy.deepcopy(bill_info)
                bill.addEvent("Avis", date, None, None)
                if len(projects[i].text.split("—")[0].split(","))>1:
                    dummyvar=1#print(projects[i].text.split("—")[-1]+ projects[i].text.split("—")[0].split(",")[1].strip("…")+ projects[i].text.split("—")[0].split(",")[0])
                    law=projects[i].text.split("—")[-1]+ " ; "+projects[i].text.split("—")[0].split(",")[1].strip("…")+ projects[i].text.split("—")[0].split(",")[0]
                else:
                    dummyvar=1#print(projects[i].text.split("—")[-1]+ " "+projects[i].text.split("—")[0])
                    law=projects[i].text.split("—")[-1]+ " ; "+projects[i].text.split("—")[0]
                bill.changeTitle(bill.identifier+law, bill.title+law)
                bill.addLaw(law)
                bills.append(bill)

        for i in range(0 , len(regulations)):
            if len(regulations[i].text.split("—"))>1:
                bill=copy.deepcopy(bill_info)
                bill.addEvent("Adoption", date, None, None)
                if len(regulations[i].text.split("—")[0].split(","))>1:
                    dummyvar=1#print(regulations[i].text.split("—")[-1]+ regulations[i].text.split("—")[0].split(",")[1].strip("…")+ regulations[i].text.split("—")[0].split(",")[0])
                    law=regulations[i].text.split("—")[-1]+ " ; "+regulations[i].text.split("—")[0].split(",")[1].strip("…")+ regulations[i].text.split("—")[0].split(",")[0]
                else:
                    dummyvar=1#print(regulations[i].text.split("—")[-1]+ regulations[i].text.split("—")[0])
                    law=regulations[i].text.split("—")[-1]+ " ; "+regulations[i].text.split("—")[0]
                bill.changeTitle(bill.identifier+law, bill.title+law)
                bill.addLaw(law)
                bills.append(bill)

        return bills

    # Downloads the pdf and extracts the text
    def Extract_Pdf(url):
        data = ""

        onlineFile = urlopen(Request(url)).read()
        pdfFile = PdfFileReader(BytesIO(onlineFile))

        if pdfFile.isEncrypted:
            fp, pdfFile = GazetteQuebec.decrypt_pdf(url)
            for pageNum in range(pdfFile.getNumPages()):
                currentPage = pdfFile.getPage(pageNum)
                data += currentPage.extractText()
            fp.close()
            # delete the files so we can reuse them
            os.system("rm " + encrypted_file)
            os.system("rm " + decrypted_file)

        else:
            for pageNum in range(pdfFile.getNumPages()):
                currentPage = pdfFile.getPage(pageNum)
                data += currentPage.extractText()

        return data

    # Requires qpdf!
    # If the pdf is encrypted, qpdf is used to decrypt it
    # Requires the pdf to be saved temporarily
    def decrypt_pdf(url):
        GazetteQuebec.save_pdf(url)
        command = ('qpdf --password="" --decrypt ' + encrypted_file + " " + decrypted_file)

        result = os.system(command)
        if result == 1:
            dummyvar=1#print("Failure at " + url)
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

    def find_all_sections_with_attr_within_elem(attr, elem, startsection):
        sections=[]
        unfileredsections = startsection.findAll(elem, attrs={attr: re.compile("para$")})
        dummyvar=1#print(unfileredsections)
        for i in range(0, len(unfileredsections)):
            if attr in unfileredsections[i].attrs.keys():
                sections.append(unfileredsections[i])
        return sections
