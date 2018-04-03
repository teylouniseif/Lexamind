# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 13:08:04 2018
@author: Sacha Perry-Fagant
"""
import urllib.request as urllib2
from bs4 import BeautifulSoup
import requests
import csv
from urllib.request import Request, urlopen
from PyPDF2 import PdfFileReader
from io import BytesIO
testing = False

from .scraper_api import Scraper, Bill

class Alberta( Scraper ):

    def __init__(self):
        super(Scraper, self).__init__()
        self.legislature="Alberta"

    # Takes in a url, checks the connection and returns the soup
    def Make_Soup(url):

        # If there's an issue connecting to the internet, end the program
        try:
            response = requests.get(url)
        except:
            print("There was an issue connecting to the internet")
            exit()

        if response.status_code != 200:
            print("There was an error finding the page")
            return False

        # If you try to go to a bill url that doesn't exist
        # You are sent back to the main page
        if "bills_home" in requests.post(url).url:
            print("Nonexistant bill")
            return False

        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page, "html.parser")

        return soup

    # The main function to scrape the Legislative Assembly of Alberta
    def retrieve_bills(self, fileName=None):
        url = "https://www.assembly.ab.ca/net/index.aspx?p=bills_statusarchive"
        base = "https://www.assembly.ab.ca/net/"
        soup = Alberta.Make_Soup(url)

        # False when there was an error connecting
        if soup == False:
            return False

        data = []

        rows = soup.find('div', attrs = {"id":"mainbox"}).findAll('tr')

        urls = []
        for row in rows:
            title = row.find('td').text
            # We're only going up to 2016, so the last is the 2015-2016 Legislature
            if '2014' in title:
                break

            cols = row.findAll('td')
            # Some Legislatures don't have any bills
            # Make sure we have 3 colums (meaning that the third one has the url)
            if len(cols) >2:
                urls.append(cols[2].find('a')['href'])

        for url in urls:
            data += Alberta.Legislature(base + url)

        self.bills=data

        #Convert_To_Csv(data)
        return data

    def Legislature(url):
        data = []

        base = "https://www.assembly.ab.ca/net/"
        soup = Alberta.Make_Soup(url)

        if soup == False:
            return data

        info = soup.find('tr', attrs = {'class': 'trtitle'})
        while info != None:
            row = []
            # Contains the title
            row.append(info.text)

            bill_info = Bill(self.legislature+info.text, info.text)

            detailed_url = base + str((info.find('a')['href']))
            details = Alberta.Find_Details(detailed_url)

            bill_info.setDetails(details)

            # Now the info contains the bill history
            info = info.findNextSibling('tr')
            readings = info.text

            # parsing text
            # The data is always in the order:
            # First Reading, Second Reading, Committee of the Whole, Third Reading, Royal Assent
            row.append(readings.split('First Reading')[1].split('Second Reading')[0])
            if 'Second Reading' in readings:
                    row.append(readings.split('Second Reading')[1].split('Committee of the Whole')[0])
                    if 'Committee of the Whole' in readings:
                        row.append(readings.split('Committee of the Whole')[1].split('Third Reading')[0])
                        if 'Third Reading' in readings:
                            row.append(readings.split('Third Reading')[1].split('Royal Assent')[0])
                            if 'Royal Assent' in readings:
                                row.append(readings.split('Royal Assent')[1])

            #bill_info.addEvent(stage, date, activity, committee)

            # Cleaning up the data
            for i in range(len(row)):
                row[i] = row[i].replace('\x97',"").strip()

            # Makes sure there the correct number of rows
            # to preseve the csv format
            while len(row) < 6:
                row.append("")

            # Go on to the next element
            info = info.findNextSibling('tr')

            # The full bill text
            row.append(details)
            data.append(bill_info)


        return data

    # Finds the pdf url and extracts the text
    def Find_Details(url):
        soup = Alberta.Make_Soup(url)
        if soup == False:
            return []
        dl = soup.find('div', attrs = {'class':'b_downloads'})
        # All the pages I've seen have been in pdf format
        pdf = dl.find('a')['href']

        return Alberta.Extract_Pdf(pdf)


    # Downloads the pdf and extracts the text
    def Extract_Pdf(url):
        data = ""

        onlineFile = urlopen(Request(url)).read()
        pdfFile = PdfFileReader(BytesIO(onlineFile))

        for pageNum in range(pdfFile.getNumPages()):
                currentPage = pdfFile.getPage(pageNum)
                data += currentPage.extractText()

        return data

    # Transform the list to CSV
    def Convert_To_Csv(data, fileName = "Legislative_Assembly_of_Alberta.csv"):
        csvfile = open(fileName, 'w', newline='',encoding="utf-8")
        file = csv.writer(csvfile)
        labels = ['Title','First Reading', 'Second Reading', 'Committee of the Whole', 'Third Reading', 'Royal Assent','Details']
        file.writerow(labels)

        max_row = 0

        for row in data:
            file.writerow(row)
            if len(row[6]) > max_row:
                max_row = len(row[6])
        csvfile.close()

        max_row += 1000
        # To make sure we can load in the data later
        # This is for testing purposes
        if testing:
            csv.field_size_limit(max_row)

        return


    # Reads in the saved data
    # To test that it was saved properly
    def Reload_Data(filepath = "Legislative_Assembly_of_Alberta.csv"):
        csvfile = open(filepath, 'r', newline='',encoding="utf-8")
        data = []
        file = csv.reader(csvfile)

        for row in file:
            data.append(row)
        csvfile.close()
        return data
