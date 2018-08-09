#! python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  4 15:45:54 2018
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
from .scraper_api import Scraper, Bill
import csv
import re
import locale, time
from datetime import datetime


class Ontario( Scraper ):

    rgx_modified_title = '.*Loi modifiant.*'
    law_delimiter_str="et|en ce|afin|à|pour|concernant"

    def __init__(self):
        super(Scraper, self).__init__()
        self.legislature="Ontario"

    # If we want only the scrape the most recent bills
    # Set most_recent to True
    def retrieve_bills(self, most_recent = False, filename = None):
        url = "https://www.ola.org/fr/affaires-legislatives/projets-loi/"
        url_base = "https://www.ola.org"

        # Where all the data from the bills will be stored
        data = []

        # Checking internet connection and webpage
        try:
            response = requests.get(url)
        except:
            dummyvar=1#print("There was an issue connecting to the internet")
            return

        if response.status_code != 200:
            dummyvar=1#print("There was an error finding the first page")
            return

        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page, "html.parser")

        soup = soup.find('table')
        sessions = soup.findAll('tr')[1:]

        #if most_recent:
        #    sessions = [sessions[0]]
        sessions = [sessions[0]]


        for session in sessions:
            row = session.find('td')
            if not row:
                continue
            session = row.text
            session_url = url_base + row.find('a')['href']

            page = urllib2.urlopen(session_url)
            soup = BeautifulSoup(page, "html.parser")
            soup = soup.find('tbody')
            bills = soup.find_all("tr")

            counter = 1
            for bill in bills:
                bill = bill.findNext('td')
                bill_info = {}

                bill_info['id'] = bill.text.strip()

                if counter % 10 == 0:
                    dummyvar=1#print("Currently at bill " + bill_info['id'])
                counter += 1

                # has the title and the url for the detailed data
                title_url = bill.findNext('a')

                # the id is bill73 for example
                identifier = self.legislature + bill.text

                title = title_url.text.strip()

                billInst = Bill(identifier, title, self.legislature)

                bill_info['title'] = title

                bill_info['sponsor'] = bill.findNext('td', attrs = {'headers': 'view-field-member-table-column'}).text.strip()

                bill_info['date'] = []
                bill_info['stage'] = []
                bill_info['activity'] = []
                bill_info['committee'] = []
                # Getting the url of the detailed info

                info_url = url_base + title_url['href']
                bill_info = Ontario.Extract_Events_Ontario(info_url, bill_info, billInst)
                bill_info['details'] = Ontario.Extract_Info_Ontario(info_url)
                bill_info['url'] = info_url

                billInst.setHyperlink(info_url)
                billInst.setDetails(Ontario.Extract_Info_Ontario(info_url))

                Ontario.sanitizeEventsDate(billInst)

                dummyvar=1#print(billInst.details)

                self.scrapeLawsinBill(billInst)

                data.append(billInst)

        if filename == None:
            filename = 'Legislative_Assembly_of_Ontario.csv'

        self.bills=data
        return data

    def Extract_Events_Ontario(url, bill_info, billInst):
        data = {}

        # get the details of events
        url = url + '/etapes'

        try:
            response = requests.get(url)
        except:
            dummyvar=1#print("There was an issue connecting to the internet")
            return

        if response.status_code != 200:
            dummyvar=1#print("There was an error finding the detailed page")
            return

        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page).find('table')

        if not soup:
            time.sleep(1)
            # time out to let reconnect to internet
            soup = soup = BeautifulSoup(page, "html.parser").find('table')
            if not soup:
                return bill_info

        soup = soup.find('tr')
        data = soup.findNext('tr')
        while data:
            col = data.findNext('td')
            date = Ontario.get_date(col.text.strip())
            bill_info['date'].append(date)
            col = col.findNext('td')
            stage = col.text.strip()
            bill_info['stage'].append(stage)
            col = col.findNext('td')
            activity = col.text.strip()
            bill_info['activity'].append(activity)
            col = col.findNext('td')
            committee = col.text.strip()
            bill_info['committee'].append(committee)

            billInst.addEvent(stage, date, activity, committee)
            data = data.findNext('tr')

        return bill_info



    # Gets all the text from the detailed info page
    def Extract_Info_Ontario(url):
        try:
            response = requests.get(url)
        except:
            dummyvar=1#print("There was an issue connecting to the internet")
            return

        if response.status_code != 200:
            dummyvar=1#print("There was an error finding the detailed page")
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
            all_text = wordSection.find("h2", attrs = {'class' : "longtitle"})
            if all_text!=None:
                for txt in all_text:
                    dummyvar=1#print(txt)
                    text += txt.replace("\n", " ").replace("\r", " ")

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
                        dummyvar=1#print(modifiedLaw+"noni")
                        bill.addLaw(modifiedLaw)


    def sanitizeEventsDate(bill):
        #locale.setlocale(locale.LC_TIME, "fr-CA")
        for event in bill.events:
            dummyvar=1#print('noni'+event['date'])
            try:
                formatteddate=datetime.strptime(event['date'].strip(), '%d/%m/%Y').strftime('%Y-%m-%d')
                event['date']=formatteddate
                dummyvar=1#print('nonigood'+event['date'])
            except:
                pass
        return
        #locale.setlocale(locale.LC_TIME, "en-CA")

    # Get date, returns ##/##/#### - day/month/year
    def get_date(date):
        date = date.lower()
        # Finding the numbers in the date
        # The first is the date, the second is the year

        day = date.split(' ')[0]
        year = date.split(' ')[2]

        if int(day) < 10:
            day = '0' + day

        month = ""

        if 'jan' in date:
            month = '01'
        elif 'feb' in date:
            month = '02'
        elif 'mar' in date:
            month = '03'
        elif 'avr' in date or 'apr' in date:
            month = '04'
        elif 'mai' in date or 'may' in date:
            month = '05'
        elif 'juin' in date or 'jun' in date:
            month = '06'
        elif 'juil' in date or 'jul' in date:
            month = '07'
        elif 'ao' in date or 'aug' in date:
            month = '08'
        elif 'sep' in date:
            month = '09'
        elif 'oct' in date:
            month = '10'
        elif 'nov' in date:
            month = '11'
        elif 'dec' in date:
            month = '12'
        else:
            # No month
            return False

        return day + '/' + month + '/' + year
