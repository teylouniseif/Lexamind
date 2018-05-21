# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 13:08:04 2018
@author: Sacha Perry-Fagant
"""
import urllib.request as urllib2
from bs4 import BeautifulSoup
import requests
import csv
from PyPDF2 import PdfFileReader
import feedparser
import os, re
import operator
testing = True

temp_pdf = "temp.pdf"

from .scraper_api import Scraper, Bill

class Quebec( Scraper ):

    RELEVANCYSTRING=r"(^loi(s)?|^règlement(s)?)\s+(modifié(e)(s)?|remplacé(e)(s)?|abrogé(e)(s)?).*"
    MOFIFIEDLAWSTRINGSTART=r"œ.*"#"(loi|code|règlement|charte).*"
    MOFIFIEDLAWSTRINGEND=r".*;\s*$|.*\.\s*$"

    def __init__(self):
        super(Scraper, self).__init__()
        self.legislature="Quebec"

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

        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page, "html.parser")

        # If you try to go to a bill url that doesn't exist
        # You are sent to an error page
        titles = soup.findAll('h1')
        for title in titles:
            fr_err = "La page ne peut être affichée"
            en_err = "Page cannot be displayed"
            if en_err in title.text or fr_err in title.text:
                print("Nonexistant bill")
                return False

        return soup

    # The main function to scrape the Legislative Assembly of Alberta
    def retrieve_bills(self, rss = False):

        data = []
        databill = []
        rss_data = []
        if rss:
            rss_data = Quebec.find_feed_updates()
            return rss_data

        url = "http://www.assnat.qc.ca/fr/travaux-parlementaires/projets-loi/projets-loi-41-1.html"
        base = "http://www.assnat.qc.ca"

        soup = Quebec.Make_Soup(url)
        # False when there was an error connecting
        if soup == False:
            return False

        table = soup.find('table', attrs = {"id":'tblListeProjetLoi'})
        bills = table.find('tbody').findAll('tr')

        counter=0
        for bill in bills:

            if counter > 50:
                continue
            else:
                counter=counter+1
            number = int(bill.findNext('td').text.strip())
            link = bill.findNext('a')
            title = link.text.split(" (PDF")[0] # So we don't get the information about the PDF
            bill_info = Bill(self.legislature+str(number), title, self.legislature)
            link = link.findNext('a')
            url = base + link['href']
            details, text = Quebec.get_text(url)

            stages=details[0]
            dates=details[1]
            for stage, date in zip(stages, dates):
                bill_info.addEvent(stage, date, None, None)

            bill_info.setDetails(text)
            self.scrapeLawsinBill(bill_info)

            other = Quebec.filter_values(details) # All the other details

            info = [title]
            info.append(url)
            info.append(number)
            info.extend(other)
            info.append(text)
            data.append(info)
            databill.append(bill_info)

        self.bills=databill

        Quebec.sort_data(data)
        Quebec.Convert_To_Csv(data)
        return data

    # Goes through all the data and replaces missing values with "N/A"
    def filter_values(data):
        labels = ["Presentation","Adoption du principe","Consultations particulières","Dépôt du rapport de commission - Consultation","Étude détaillée en commission", "Prise en considération du rapport de commission", "Sanction"]

        ent = []

        for l in labels:
            if l in data[0]:
                idx = data[0].index(l)
                ent.append(data[1][idx])
                ent.append(data[2][idx])
            else:
                ent.append("N/A")
                ent.append("N/A")

        return ent

    # Transform the list to CSV
    def Convert_To_Csv(data, fileName = "assemblee_nationale.csv"):
        csvfile = open(fileName, 'w', newline='',encoding="utf-8")
        file = csv.writer(csvfile)
        labels = ["title","Url","Bill Number","Presentation Date","Presentation url","Adoption du principe Date","Adoption du principe Url","Consultations particulières Date","Consultations particulières url","Dépôt du rapport de commission - Consultation Date","Dépôt du rapport de commission - Consultation url","Étude détaillée en commission date", "Étude détaillée en commission url", "Prise en considération du rapport de commission Date","Prise en considération du rapport de commission url", "Sanction Date","Sanction url", "text"]
        file.writerow(labels)

        max_row = 0

        for row in data:
            file.writerow(row)
            if len(row[len(row)-1]) > max_row:
                max_row = len(row[len(row)-1])
        csvfile.close()

        max_row += 1000
        # To make sure we can load in the data later
        # This is for testing purposes
        if testing:
            csv.field_size_limit(max_row)

    # Returns the same value multiple times
    # Easier just to use the main scraper function
    def find_feed_updates():
        data = []
        feed = feedparser.parse('http://www.assnat.qc.ca/fr/rss/SyndicationRSS-210.html')
        for item in feed['entries']:
            elem = []
            elem.append(item['title'].split(': ')[1].split(' - ')[0])

            # this is the bill number
            elem.append(int(item['title'].split('projet de loi ')[1].split(' :')[0]))

            # elem.append(get_date(item['published']))
            elem.append(item['link'])
            details, text = Quebec.get_text(item['link'])
            info = Quebec.filter_values(details)
            elem.extend(info)
            elem.append(text)
            data.append(elem)

        Quebec.sort_data(data)
        Quebec.Convert_To_Csv(data, "rss_assemblee.csv")
        return data

    # Gets the header title and the dates under that header
    # If there are multiple dates, it takes the most recent one
    def get_text(url):
        labels = []
        data = []
        urls = []

        soup = Quebec.Make_Soup(url)
        if soup == False:
            return []

        line = soup.find('h3')

        # The important pdf is under this section
        while line.text != 'Présentation':
            line = line.findNext('h3')

        line = line.findNext('ul',attrs = {'class':'ListeLien'})
        link = line.findNext('a')
        pdf_url = link['href']

        text = Quebec.Extract_Pdf(pdf_url)

        lines = line.findAll("li")

        i = 0
        presentation_date = 'N/A'
        # The date is in the line "Séance du date month year"
        while i < len(lines) and 'Séance' not in lines[i].text :
            i += 1

        if 'Séance' in lines[i].text:
            presentation_date = Quebec.get_date(lines[i].text)

        labels.append("Presentation")
        data.append(presentation_date)
        urls.append(pdf_url)

        # Goes through all of the titles
        # Stores the ones with dates under them in
        while line.findNext('h3') != None:
            line = line.findNext('h3')
            title = line.text.strip()

            # Sanction is a special case that requires different code
            if title == "Sanction":
                continue

            lines = line.findNext('ul',attrs = {'class':'ListeLien'}).findAll('li')
            i = 0
            # The date is in the line "Séance du date month year"
            dates = []
            date_urls = []
            for el in lines:
                if 'Séance' in el.text:
                    dates.append(Quebec.get_date(el.text))
                    if el.find('a') != None:
                        date_urls.append(el.find('a')['href'])
                    else:
                        date_urls.append("N/A")
            # Only record the information if there's a date
            if len(dates) > 0:
                labels.append(title)
                # Get the most recent date (The date at the end of the list)
                # TODO: Check that the most recent date is always at the end
                data.append(dates[len(dates)-1])
                urls.append("http://www.assnat.qc.ca" + date_urls[len(date_urls)-1])


        while line != None and line.text.strip() != 'Sanction':
            line = line.findNext('h3')

        if line == None:
            line = soup.find('h3')
            sanction_date = "N/A"
        else:
            sanction_date = Quebec.get_date(line.findNext('span').next_sibling)

        data.append(sanction_date)
        labels.append('Sanction')
        urls.append("N/A") # No url for the sanction date

        return [labels, data, urls], text


    # Downloads the pdf and extracts the text
    def Extract_Pdf(url):
        data = ""

        r = requests.get(url, allow_redirects=True)
        open(temp_pdf, 'wb').write(r.content)

        fp = open(temp_pdf,'rb')
        pdfFile = PdfFileReader(fp)
        for pageNum in range(pdfFile.getNumPages()):
            currentPage = pdfFile.getPage(pageNum)
            try:
                data += currentPage.extractText()
            except:
                continue
        fp.close()

        os.system("del " + temp_pdf)

        return data


    # Takes in a title with a date in it and returns the date
    # In a better format
    # The original format is something along the lines of '12 juin 2014'
    # Returns in format year month date
    def get_date(date):
        #return date
        date = date.lower()

        # Finding the date
        letter = date[0]
        i = 1
        while not letter.isdigit() and i < len(date):
            letter = date[i]
            i += 1

        day = letter

        # The date has two digits
        if date[i].isdigit():
            day += date[i]
        else:
            day = '0' + day

        # Finding the month
        i += 1
        letter = date[i]

        while not letter.isdigit() and i < len(date):
            letter = date[i]
            i += 1

        year = ""

        while letter.isdigit() and i < len(date):
            year += letter
            letter = date[i]
            i += 1

        month = ""

        if 'janvier' in date:
            month = '01'
        elif 'février' in date:
            month = '02'
        elif 'mars' in date:
            month = '03'
        elif 'avril' in date:
            month = '04'
        elif 'mai' in date:
            month = '05'
        elif 'juin' in date:
            month = '06'
        elif 'juillet' in date:
            month = '07'
        elif 'août' in date:
            month = '08'
        elif 'septembre' in date:
            month = '09'
        elif 'octobre' in date:
            month = '10'
        elif 'novembre' in date:
            month = '11'
        elif 'decembre' in date:
            month = '12'

        return year + month + day


    def Reload_Data(filepath = "assemblee_nationale.csv"):
        csvfile = open(filepath, 'r', newline='',encoding="utf-8")
        data = []
        file = csv.reader(csvfile)
        for row in file:
            data.append(row)
        csvfile.close()
        return data

    # The data scraped is not in numerical order
    # This function puts them in the correct order
    def sort_data(data):
        data.sort(key = operator.itemgetter(2))

    def scrapeLawsinBill(self, bill):
        index=0
        text=bill.details.lower()
        text2=str(text.encode('utf-8'))
        lawstrings = re.compile(r"[\r\n]+").split(text)
        #while index < len(lawstrings):
        it=iter(lawstrings)
        try:
            while next(it):

                #use iter to stop loop

                index+=1
                #strg=lawstrings[index]
                strg=next(it)

                #print(strg)

                if strg.isdigit() or strg.strip()=='':
                    continue

                if re.compile(Quebec.RELEVANCYSTRING).search(strg)==None:
                    continue
    			#this bill at this point affect laws or regulations that are (repeal, amendment or replacement)
                else:
                    law=""
                    index+=1
                    #strg=lawstrings[index]
                    strg=next(it)
                    #print(strg)
                    while re.compile(Quebec.MOFIFIEDLAWSTRINGSTART).search(strg)!=None:
                        #at this point check that law affected is one that we are interested in
                        law+=strg
    					#System.out.println(str);
    					#here certain laws modified can span more than one line
    					#use semi-colon or dot at end of line as delimiter of law changed
                        while re.compile(Quebec.MOFIFIEDLAWSTRINGEND).search(strg)==None:
                            index+=1
                            #strg=lawstrings[index]
                            strg=next(it)
                            law+=strg

                        index+=1
                        #strg=lawstrings[index]
                        strg=next(it)

                        bill.addLaw(re.compile(r".*œ\s|\s\(|;|\.").split(law)[1])

                        while strg.isdigit() or strg.strip()=='':
                            index+=1
                            #print(strg)
                            #strg=lawstrings[index]
                            strg=next(it)

                        if re.compile(Quebec.RELEVANCYSTRING).search(strg)!=None:
                            index+=1
                            #strg=lawstrings[index]
                            strg=next(it)

                        law=""
        except StopIteration:
            print("this is the end")
