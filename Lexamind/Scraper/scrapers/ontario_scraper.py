#! python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  4 15:45:54 2018
@author: Sacha Perry-Fagant
"""

import urllib.request as urllib2
from bs4 import BeautifulSoup
import requests
from .scraper_api import Scraper, Bill
import csv
import re
import locale, time
from datetime import datetime


# the main function that scrapes the Legislative Assembly of Ontario
# it will be saved as Legislative_Assembly_of_Ontario.csv
class Ontario( Scraper ):

    rgx_modified_title = '.*Loi modifiant.*'
    law_delimiter_str="et|en ce|afin|à|pour|concernant"

    def __init__(self):
        super(Scraper, self).__init__()
        self.legislature="Ontario"

    def retrieve_bills(self,  filename = None):
        url = "http://www.ontla.on.ca/web/bills/bills_all.do?locale=fr"
        url_base = "http://www.ontla.on.ca/web/bills/"

        # Where all the data from the bills will be stored
        data = []

        # Checking internet connection and webpage
        try:
            response = requests.get(url)
        except:
            print("There was an issue connecting to the internet")
            return

        if response.status_code != 200:
            print("There was an error finding the first page")
            return

        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page, "html.parser")
        bills = soup.find_all("td", attrs = {"class": "nocell"})

        counter = 1
        for bill in bills:
            if counter % 10 == 0:
                print("Currently at bill " + str(counter))
            counter += 1

            # Data is separated by commas in the CSV so the commas are removed
            bill_info = {}
            # the id is bill73 for example
            bill_info['id'] = bill.text

            # has the title and the url for the detailed data
            title_url = bill.findNext('td',attrs = {'class': 'titlecell'})

            # the id is bill73 for example
            identifier = self.legislature + bill.text

            title = title_url.text.strip().replace(","," ")

            billInst = Bill(identifier, title, self.legislature)

            bill_info['title'] = title_url.text.strip().replace(","," ")
            bill_info['sponsor'] = bill.findNext('td',attrs = {'class': 'sponsorcell'}).text

            bill_info['date'] = []
            bill_info['stage'] = []
            bill_info['activity'] = []
            bill_info['committee'] = []

            # Getting the url of the detailed info
            info_url = url_base + title_url.find('a')['href']
            bill_info = Ontario.Extract_Events_Ontario(info_url, bill_info, billInst)
            bill_info['details'] = Ontario.Extract_Info_Ontario(info_url)
            billInst.setDetails(Ontario.Extract_Info_Ontario(info_url))

            self.scrapeLawsinBill(billInst)

            data.append(billInst)

        if filename == None:
            # it will be saved as Legislative_Assembly_of_Ontario.csv
            filename = soup.find("meta", attrs = {'name' : "dc:publisher"})['content']
            filename = filename.replace(" ", "_")
            filename += ".csv"

        self.bills=data
        return data

    def Extract_Events_Ontario(url, bill_info, billInst):

        data = {}

        # get the details of events
        url = url.replace('ParlSessionID=','&detailPage=bills_detail_status')

        try:
            response = requests.get(url)
        except:
            print("There was an issue connecting to the internet")
            return

        if response.status_code != 200:
            print("There was an error finding the detailed page")
            return

        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page).find('table')

        if not soup:
            time.sleep(1)
            # time out to let reconnect to internet
            soup = soup = BeautifulSoup(page, "html.parser").find('table')
            if not soup:
                return bill_info

        counter = 0
        data = soup.find('tr', attrs = {'class':'evenrow'})
        while data:

            date=data.findNext('td', attrs = {'class' : "date"}).text.strip().replace(","," ")
            stage=data.findNext('td', attrs = {'class' : "stage"}).text.strip().replace(","," ")
            activity=data.findNext('td', attrs = {'class' : "activity"}).text.strip().replace(","," ")
            committee=data.findNext('td', attrs = {'class' : "committee"}).text.strip().replace(","," ")
            bill_info['date'].append(date)
            bill_info['stage'].append(stage)
            bill_info['activity'].append(activity)
            bill_info['committee'].append(committee)
            billInst.addEvent(stage, date, activity, committee)

            counter += 1
            if counter % 2 == 0:
                data = data.findNext('tr', attrs = {'class':'evenrow'})
            else:
                data = data.findNext('tr', attrs = {'class':'oddrow'})


        return bill_info


    # Gets all the text from the detailed info page
    def Extract_Info_Ontario(url):
        try:
            response = requests.get(url)
        except:
            print("There was an issue connecting to the internet")
            return

        if response.status_code != 200:
            print("There was an error finding the detailed page")
            return

        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page)

        text = ""
        wordSection = ""
        i = 1
        # check all the word sections starting at 1
        while wordSection != None:
            section = "WordSection" + str(i)

            wordSection = soup.find("div", attrs = {'class' : section})

            if wordSection == None:
                break

            # Finds all the text in the word section
            all_text = wordSection.find_all("span")
            for txt in all_text:
                text += txt.text
                text += "\n"
            i += 1
        return text

    def scrapeLawsinBill(self, bill):
        modification = re.findall(Ontario.rgx_modified_title, bill.details)
        if modification==None:
            return
        else:
            for match in modification:
                modifiedstripped=match.split('modifiant')[1]
                modifiedLaws = re.split(Ontario.law_delimiter_str, modifiedstripped)
                for modifiedLaw in modifiedLaws:
                    if modifiedLaw.find('Loi')!=-1 or modifiedLaw.find('Code')!=-1:
                        print(modifiedLaw+"noni")
                        bill.addLaw(modifiedLaw)
                        

    def sanitizeEventsDate(bill):
        locale.setlocale(locale.LC_TIME, "fr-CA")
        for event in bill.events:
            print('noni'+event['date'])
            try:
                formatteddate=datetime.strptime(event['date'].strip(), '%d %b %Y').strftime('%d/%m/%Y')
                event['date']=formatteddate
                print('nonigood'+event['date'])
            except:
                pass
        locale.setlocale(locale.LC_TIME, "en-CA")
