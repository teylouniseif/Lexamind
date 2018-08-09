# -*- coding: utf-8 -*-
"""
Created on Sun Jan 14 12:52:44 2018
@author: Sacha Perry-Fagant
"""
import urllib.request as urllib2
from bs4 import BeautifulSoup
import requests
import csv, re
from datetime import datetime

from .scraper_api import Scraper, Bill

class Newfoundland( Scraper ):

    rgx_modified_title = r"[^\r\n]*"#'.*amended.*|.*repealed.*'#'.*is\s*amended\s*by\s*this.*'

    stages=["First Reading","Second Reading","Committee","Amendments","Third Reading","Royal Assent"]

    def __init__(self):
        super(Scraper, self).__init__()
        self.legislature="Newfoundland"

    # Checks if connected to the internet
    def CheckInternet(url):
        try:
            response = requests.get(url)
        except:
            dummyvar=1#print("There was an issue connecting to the internet")
            return False

        if response.status_code != 200:
            dummyvar=1#print("There was an error finding the page")
            return False

        return True

    # Checks for the text "Sorry, this page could not be found!"
    def PageExists(soup):
        if soup.find('body') != None:
            if "Sorry, this page could not be found!" in soup.find('body').text:
                return False

        return True

    # The main function
    # Returns all the data in an array
    # Saves the data as "House_of_Assembly_Newfoundland_and_Labrador.csv"
    def retrieve_bills(self, filename = "House_of_Assembly_Newfoundland_and_Labrador.csv"):

        url = "http://assembly.nl.ca/HouseBusiness/Bills/"

        # Checking internet connection and webpage
        if not Newfoundland.CheckInternet(url):
            return

        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page, "html.parser")

        # Checks if page exists
        if not Newfoundland.PageExists(soup):
            return

        # Find the most recent assembly
        # It will only take the first row assembly (currenly 48th)
        assemblies = soup.find("ul", attrs = {"class":"list-unstyled"})

        data = []
        urls = []

        links = assemblies.findAll('a')
        for link in links:
            urls.append(url + link['href'])

        # Combine the data from each of the sessions of the assembly
        for url in urls:
            data+=(self.Get_Session(url))

        #Newfoundland.Convert_to_csv(data, fileName = filename)

        self.bills=data

        return data

    def Get_Session(self, url):
        data = []

        # Checking internet connection and webpage
        if not Newfoundland.CheckInternet(url):
            return data

        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page, "html.parser")
        bill_table = soup.find("table", attrs = {"class": "bills table table-bordered table-striped table-responsive"})
        bills = bill_table.find_all("tr")

        # Checks if page exists
        if not Newfoundland.PageExists(soup):
            return data

        # Getting bill data
        for bill in bills:

            # 9 colums + details
            bill_data = []
            cols = bill.find_all("td")

            # in the case of empty table row
            if cols[0].text == "\xa0":
                continue

            bill_info = Bill(self.legislature+cols[0].text, cols[1].text, self.legislature)

            stageid= 0
            for c in cols[2:7]:
                if c!="&nbsp;":
                    bill_info.addEvent(Newfoundland.stages[stageid], c.text, None, None)
                stageid+=1
                bill_data.append(c.text)

            if cols[1].find('a') != None:
                details = Newfoundland.find_details(url + cols[1].find('a')['href'])
                bill_data.append(details[0])
                bill_data.append(details[1])
                text=details[0]+details[1]
                bill_info.setDetails(text)
                self.scrapeLawsinBill(bill_info)
            else:
                # If there is no link to bill text, fill the details with ""
                bill_data.append("")
                bill_data.append("")

            Newfoundland.sanitizeEventsDate(bill_info)

            data.append(bill_info)

        return data

    # Finds both of the detailed pages
    # Takes in the url of one of the detailed pages
    # hasNext is True if we are looking at the first detailed page,
    # False if we're looking at the second page
    # This is so we only need one function
    def find_details(url, hasNext = True):

        # Checking internet connection and webpage
        if not Newfoundland.CheckInternet(url):
            return ["",""]

        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page, "html.parser")

        if not Newfoundland.PageExists(soup):
            return ["",""]

        soup.encode('utf-8')
        paragraphs = soup.find_all("p")
        text = ""

        # Will hold the link to the next detailed page if it exists
        nextPage = None

        for par in paragraphs:
            # Cleaning up the data
            temp = par.text.replace('\n','')
            temp = temp.replace('\r',' ')
            text += temp
            text += "\n"
            # If there's a link to a more detailed page, follow it
            # If nextPage is not None, then we already have the next page
            if par.find('a') != None and nextPage == None:
                link = par.find('a')
                if 'href' in str(link) and "BILL" in link.text:
                    nextPage = par.find('a')['href']

        # If there is a next page and we're looking for the next page
        if nextPage != None and hasNext:
            # hasNext is false now since we already have the first page
            details2 = Newfoundland.find_details(nextPage, False)[0]
        else:
            details2 = ""

        return [text, details2]


    # Transform the list to CSV
    def Convert_to_csv(data, fileName = "test.csv"):
        csvfile = open(fileName, 'w', newline='',encoding="utf-8")
        file = csv.writer(csvfile)
        labels = ['No.','Bill','First Reading','Second Reading','Committee','Amendments','Third Reading','Royal Assent','Act','Details','Details2']
        file.writerow(labels)
        for row in data:
            file.writerow(row)
        csvfile.close()
        return


    # Reads in the saved data
    # To test that it was saved properly
    def Reload_data(filepath = "House_of_Assembly_Newfoundland_and_Labrador.csv"):
        csvfile = open(filepath, 'r', newline='',encoding="utf-8")
        data = []
        file = csv.reader(csvfile)
        for row in file:
            data.append(row)
        csvfile.close()
        return data

    def scrapeLawsinBill(self, bill):
        """modification = re.findall(Newfoundland.rgx_modified_title, bill.details)
        if modification==None:
            return
        else:
            for match in modification:
                modifiedstripped=match.split('amended')[0]
                if modifiedstripped!=None and modifiedstripped.find('Act')!=-1 and modifiedstripped.find('Act')!=0:
                    if modifiedstripped.find('the Act')==-1:
                        modifiedstripped2=modifiedstripped.split('Act')[0]
                        modifiedstripped3=modifiedstripped2.split('the')
                        modifiedstripped4=modifiedstripped3[len(modifiedstripped3)-1]
                        dummyvar=1#print(modifiedstripped4+'Act'+bill.identifier)
                        bill.addLaw(modifiedstripped4+'Act')"""
        modification = re.findall(Newfoundland.rgx_modified_title, bill.details)
        if modification==None:
            return
        else:
            previousmatch=None
            for match in modification:
                modifiedstripped=re.search('.*amended.*|.*repealed.*', match)
                #modifiedstripped=match.search('amended')
                if modifiedstripped==None:
                    continue
                else:
                    modifiedstripped=match.split('amended')[0]
                    if modifiedstripped.find('Act')==-1 and previousmatch!=None:
                        modifiedstripped=previousmatch
                    if modifiedstripped.find('Act')!=-1 and modifiedstripped.find('the Act')==-1 and modifiedstripped.find('this Act')==-1:
                        modifiedstripped2=modifiedstripped.split('Act')[0]
                        modifiedstripped3=modifiedstripped2.split('the')
                        modifiedstripped4=modifiedstripped3[len(modifiedstripped3)-1]
                        dummyvar=1#print(modifiedstripped4+'Act'+ bill.identifier)
                        bill.addLaw(modifiedstripped4+'Act')
                previousmatch=match

    def sanitizeEventsDate(bill):
        for event in bill.events:
            datestripped= event['date'].strip()
            if datestripped=="No" or datestripped=="" or datestripped=="Yes":
                continue
            try:
                formatteddate=datetime.strptime(datestripped, '%b. %d/%Y').strftime('%d/%m/%Y')
                event['date']=formatteddate
            except:
                formatteddate=datetime.strptime(datestripped, '%b %d/%Y').strftime('%d/%m/%Y')
                event['date']=formatteddate
            dummyvar=1#print(formatteddate)
