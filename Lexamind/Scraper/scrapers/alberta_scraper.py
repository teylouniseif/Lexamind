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
import re
import dateutil.parser as dparser
from datetime import datetime
import subprocess

from .scraper_api import Scraper, Bill

class Alberta( Scraper ):

    rgx_modified_title = r"[^\r\n]*"

    def __init__(self):
        super(Scraper, self).__init__()
        self.legislature="Alberta"

    # Takes in a url, checks the connection and returns the soup
    def Make_Soup(url):

        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        headers = {'User-Agent': user_agent}
        # If there's an issue connecting to the internet, end the program
        try:
            response = requests.get(url, headers=headers)
        except:
            dummyvar=1#print("There was an issue connecting to the internet")
            exit()

        if response.status_code != 200:
            dummyvar=1#print("There was an error finding the page")
            return False

        # If you try to go to a bill url that doesn't exist
        # You are sent back to the main page
        if "bills_home" in requests.post(url).url:
            dummyvar=1#print("Nonexistant bill")
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

        start_year = str(datetime.now().year-2)

        urls = {}
        for row in rows:
            title = row.find('td').text
            # We're only going up to 2016, so the last is the 2015-2016 Legislature
            if start_year in title:
                break

            cols = row.findAll('td')
            # Some Legislatures don't have any bills
            # Make sure we have 3 colums (meaning that the third one has the url)
            if len(cols) >2:
                #urls.append(cols[2].find('a')['href'])
                urls[title]=cols[2].find('a')['href']

        for leg, url in urls.items():
            data += self.Legislature(base + url, leg)

        self.bills=data

        #Convert_To_Csv(data)
        return data

    def Legislature(self, url, leg):
        data = []

        base = "https://www.assembly.ab.ca/net/"
        soup = Alberta.Make_Soup(url)

        if soup == False:
            return data

        info = soup.find('tr', attrs = {'class': 'trtitle'})
        counter=0
        while info != None:
            counter+=1
            #if counter!=1:
            #    continue
            row = []
            # Contains the title
            row.append(info.text)

            id=info.text
            for s in info.text.split():
                if any(char.isdigit() for char in s):
                    id=s
                    break
            bill_info = Bill(self.legislature+id+leg, info.text, self.legislature)

            billtitle=self.legislature+id+leg
            """if billtitle!="Alberta1829th Legislature, 4th Session (2018)":
                info=info.findNextSibling('tr')
                info=info.findNextSibling('tr')
                continue"""

            detailed_url = base + str((info.find('a')['href']))
            details = Alberta.Find_Details(detailed_url, bill_info)

            bill_info.setDetails(details)
            self.scrapeLawsinBill(bill_info)

            # Now the info contains the bill history
            info = info.findNextSibling('tr')
            readings = info.text

            # parsing text
            # The data is always in the order:
            # First Reading, Second Reading, Committee of the Whole, Third Reading, Royal Assent
            row.append(readings.split('First Reading')[1].split('Second Reading')[0])
            date=readings.split('First Reading')[1].split('Second Reading')[0].split("(")[1].split("aft")[0]
            bill_info.addEvent("First Reading", date, None, None)
            if 'Second Reading' in readings:
                    row.append(readings.split('Second Reading')[1].split('Committee of the Whole')[0])
                    date=readings.split('Second Reading')[1].split('Committee of the Whole')[0].split("(")[1].split("aft")[0]
                    bill_info.addEvent("Second Reading", date, None, None)
                    if 'Committee of the Whole' in readings:
                        row.append(readings.split('Committee of the Whole')[1].split('Third Reading')[0])
                        date=readings.split('Committee of the Whole')[1].split('Third Reading')[0].split("(")[1].split("aft")[0]
                        bill_info.addEvent("Committee of the Whole", date, None, None)
                        if 'Third Reading' in readings:
                            row.append(readings.split('Third Reading')[1].split('Royal Assent')[0])
                            date=readings.split('Third Reading')[1].split('Royal Assent')[0].split("(")[1].split("aft")[0]
                            bill_info.addEvent("Third Reading", date, None, None)
                            if 'Royal Assent' in readings:
                                row.append(readings.split('Royal Assent')[1])
                                date=readings.split('Royal Assent')[1].split("(")[1].split("aft")[0]
                                bill_info.addEvent("Royal Assent", date, None, None)

            Alberta.sanitizeEventsDate(bill_info)

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
    def Find_Details(url, bill_info):
        soup = Alberta.Make_Soup(url)
        if soup == False:
            return []
        dl = soup.find('div', attrs = {'class':'b_downloads'})
        # All the pages I've seen have been in pdf format
        pdf = dl.find('a')['href']

        bill_info.setHyperlink("https://www.assembly.ab.ca"+pdf)

        return Alberta.Extract_Pdf("https://www.assembly.ab.ca"+pdf)

    def decompress_pdf(temp_buffer):
        temp_buffer.seek(0)  # Make sure we're at the start of the file.

        process = subprocess.Popen(['pdftk.exe',
                                    '-',  # Read from stdin.
                                    'output',
                                    '-',  # Write to stdout.
                                    'uncompress'],
                                    stdin=temp_buffer.getvalue(),
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
        print("\nnow\n")
        stdout, stderr = process.communicate()
        return StringIO(stdout)

    # Downloads the pdf and extracts the text
    def Extract_Pdf(url):
        print(url)
        data = ""

        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        onlineFile = urlopen(Request(url,headers={'User-Agent': user_agent})).read()
        try:
        #temporarylocation="testout.pdf"
        #with open(temporarylocation,'wb') as out: ## Open temporary file as bytes
        #    out.write(BytesIO(onlineFile).read())
        #pdfFile = PdfFileReader(Alberta.decompress_pdf(out))
            pdfFile = PdfFileReader(BytesIO(onlineFile))
            for pageNum in range(pdfFile.getNumPages()):
                    currentPage = pdfFile.getPage(pageNum)
                    data += currentPage.extractText()#.replace("\n", "\s")
        except:
            print("There was an issue connecting to the internet")
            return ""

        print("we here")

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

    def scrapeLawsinBill(self, bill):
        modification = re.findall(Alberta.rgx_modified_title, bill.details)
        dummyvar=1#print(bill.details)
        if modification==None:
            return
        else:
            previousmatch=None
            modification=[x.strip() for x in modification if x.strip()]
            for match in modification:
                dummyvar=1#print(match)
                modifiedstripped=re.search('.*amended.*', match)
                #print(modifiedstripped)
                if modifiedstripped==None:
                    previousmatch=match
                else:
                    if match.find('Act')==-1 and match.find('Code')==-1:
                        if previousmatch.find('Act')!=-1 or previousmatch.find('Code')!=-1:
                            bill.addLaw(previousmatch)
                            print(previousmatch)
                    else:
                        bill.addLaw(match)
                        print(match)

    def sanitizeEventsDate(bill):
        for event in bill.events:
            datedelimiter=re.compile(r"[0-9]{4}").split(event['date'])[1]
            if datedelimiter.strip()!='':
                datestripped= event['date'].split(datedelimiter)[0].strip()
            else:
                datestripped= event['date'].strip()
            dummyvar=1#print(datedelimiter)
            try:
                formatteddate=datetime.strptime(datestripped, '%b. %d, %Y').strftime('%Y-%m-%d')
                event['date']=formatteddate
            except:
                formatteddate=datetime.strptime(datestripped, '%b %d, %Y').strftime('%Y-%m-%d')
                event['date']=formatteddate
