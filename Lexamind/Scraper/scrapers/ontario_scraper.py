#! python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  4 15:45:54 2018
@author: Sacha Perry-Fagant
"""

import urllib.request as urllib2
from bs4 import BeautifulSoup
import requests
from .scraper_api import Scraper
import csv


class Ontario( Scraper ):

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
        soup = BeautifulSoup(page, "html.parser")
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


    # Transform the dictionary to CSV
    def Convert_to_csv(data, fileName = "test.csv"):
        csvfile = open(fileName, 'w', newline='')
        file = csv.writer(csvfile)
        labels = ['id', 'title', 'date', 'stage', 'activity', 'committee', 'details']
        file.writerow(labels)
        for row in data:
            text = []
            text.append(row['id'])
            text.append(row['title'])
            text.append(row['date'][0])
            text.append(row['stage'][0])
            text.append(row['activity'][0])
            text.append(row['committee'][0])
            text.append(str(row['details'].encode('utf-8')))
            file.writerow(text)
            # if there are multiple rows
            if len(row['date']) > 1:
                for i in range(1, len(row['date'])):
                    text = ["",""]
                    text.append((row['date'][i]))
                    text.append((row['stage'][i]))
                    text.append(row['activity'][i])
                    text.append(row['committee'][i])
                    file.writerow(text)

        csvfile.close()

    # Reads in the lines from the file and cleans them up
    def test_csv(filename = "Legislative_Assembly_of_Ontario.csv"):
        file = open(filename, mode = 'r')
        lines = file.readlines()
        file.close()
        clean_lines = []
        for line in lines:
            clean = line.replace('\\xa0', ' ')
            clean = clean.replace('\\xc2', ' ')
            clean = clean.replace('\\n', '\n')
            clean = clean.replace('"','')
            clean = clean.replace('"','')
            clean = clean.replace("b'", "")
            clean_lines.append(clean)
        return clean_lines

    # the main function that scrapes the Legislative Assembly of Ontario
    # it will be saved as Legislative_Assembly_of_Ontario.csv
    def retrieve_bills(self,  filename = None):
        url = "http://www.ontla.on.ca/web/bills/bills_current.do?locale=fr"
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
        bills = soup.find_all("div", attrs = {"class": "billstatus"})

        counter = 1
        for bill in bills:
            if counter != 1:
                continue

            if counter % 10 == 0:
                print("Currently at bill " + str(counter))
            counter += 1

            # Data is separated by commas in the CSV so the commas are removed
            bill_info = {}
            # the id is bill73 for example
            bill_info['id'] = bill.get("id").replace(","," ")

            # has the title and the url for the detailed data
            title_url = bill.find('a', href=True)

            bill_info['title'] = title_url.text.strip().replace(","," ")


            bill_info['date'] = []
            bill_info['stage'] = []
            bill_info['activity'] = []
            bill_info['committee'] = []

            # If there is more than one row in the table, save all rows
            # Each attribute is saved in a list for that attribute
            current_row = bill.findNext('tbody').find('tr')
            while current_row != None:
                bill_info['date'].append(current_row.find('td', attrs = {'class' : "date"}).text.strip().replace(","," "))
                bill_info['stage'].append(current_row.find('td', attrs = {'class' : "stage"}).text.strip().replace(","," "))
                bill_info['activity'].append(current_row.find('td', attrs = {'class' : "activity"}).text.strip().replace(","," "))
                bill_info['committee'].append(current_row.find('td', attrs = {'class' : "committee"}).text.strip().replace(","," "))

                current_row = current_row.findNextSibling('tr')

            # Getting the url of the detailed info
            info_url = url_base + title_url['href']
            bill_info['details'] = Ontario.Extract_Info_Ontario(info_url)

            data.append(bill_info)

        if filename == None:
            # it will be saved as Legislative_Assembly_of_Ontario.csv
            filename = soup.find("meta", attrs = {'name' : "dc:publisher"})['content']
            filename = filename.replace(" ", "_")
            filename += ".csv"
        Ontario.Convert_to_csv(data, filename)

        return data
