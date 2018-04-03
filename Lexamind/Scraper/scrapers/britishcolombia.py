import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

MONGO_URL = 'localhost'
MONGO_DB = 'Lexamind'
MONGO_COLLECTION = 'Bills'
BILLS_URLS = ['http://www.bclaws.ca/civix/document/id/bills/billscurrent/3rd41st_government',
              'http://www.bclaws.ca/civix/document/id/bills/billscurrent/3rd41st_members']

client = MongoClient(MONGO_URL, 27017)
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]

for bill_url in BILLS_URLS:
    result = requests.get(bill_url)
    soup = BeautifulSoup(result.content, "html.parser")

    trs = soup.select("table tr")[1:]
    i = 0
    while i < len(trs):
        title = trs[i].select("td strong")[0].text
        member = trs[i].select("td")[0].text.replace('(', '').replace(')', '')
        bill_no = title.split(":")[0].replace('Bill', '').strip()
        data_td = trs[i + 2].select("td")
        first_reading = ", ".join(map(lambda x: x.strip(), data_td[0].text.split('\n')))
        second_reading = ", ".join(map(lambda x: x.strip(), data_td[2].text.split('\n')))
        committee = ", ".join(map(lambda x: x.strip(), data_td[4].text.split('\n')))
        report = ", ".join(map(lambda x: x.strip(), data_td[6].text.split('\n')))
        amended = ", ".join(map(lambda x: x.strip(), data_td[7].text.split('\n')))
        third_reading = ", ".join(map(lambda x: x.strip(), data_td[8].text.split('\n')))
        royal_assent = ", ".join(map(lambda x: x.strip(), data_td[10].text.split('\n')))
        chap = ", ".join(map(lambda x: x.strip(), data_td[11].text.split('\n')))
        i = i + 3
        doc = {'number': bill_no, 'title': title, 'member': member, 'first_reading': first_reading,
               'second_reading': second_reading, 'third_reading': third_reading, 'committee': committee,
               'report': report, 'amended': amended, 'royal_assent': royal_assent, 'chap': chap}
        collection.insert_one(doc)
        print("Added bill number {} to MongoDB".format(bill_no))

print("Data saved to bills-collection in bills-db")
