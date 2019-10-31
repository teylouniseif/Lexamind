#! python3
# -*- coding: utf-8 -*-

from scrapy.crawler import CrawlerProcess
#from federal_scraper.parl_spider.spiders.parl import ParlSpider

from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import signals
from scrapy.utils.project import get_project_settings
from scrapy import Spider
from scrapy.http import Request
from scrapy.xlib.pydispatch import dispatcher
from .scraper_api import Scraper, Bill
import re

class Canada(Scraper, Spider):
    name = 'parl_ca'
    allowed_domains = ['parl.ca']
    start_urls = (
        'https://www.parl.ca/LegisInfo/Home.aspx?',
    )

    rgx_modified_title_list = [".*Loi.*",".*Code.*"]
    law_delimiter_str="est|sont|;|dans|dont"

    # start_urls = ['http://www.parl.ca/LegisInfo/BillDetails.aspx?Language=F&billId=8804045']

    def __init__(self):
        super(Canada, self).__init__()
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        self.legislature="Canada"

    def parse(self, response):
        bills = response.xpath('//*[@class="BillTitle"]/@href').extract()
        for bill in bills:
            items={}
            bill1=Bill(None, None, None)#self.legislature)
            result=Request(bill.replace('Language=E', 'Language=F'),
                          meta={'items': items},
                          callback=self.parse_bill)
            yield result

        next_page_urls = response.xpath('//*[@class="resultPagingSection"]//@href').extract()
        for url in next_page_urls:
            absolute_url = response.urljoin(url)
            yield Request(absolute_url)

    def parse_bill(self, response):
        bill_name = response.xpath(
            '//*[@id="ctl00_ParlSessControl_lblParliamentSession"]//text()').extract()
        if bill_name:
            bill_name = ''.join(bill_name)

        date = response.xpath(
            '//*[@id="ctl00_ParlSessControl_lblSessionDateRange"]/text()').extract_first()


        bill_number_and_title = response.xpath(
            '//*[@id="ctl00_PageContentSection_BillNumber"]/text()|'
            '//*[@id="ctl00_PageContentSection_BillTitlePanel"]//text()').extract()
        if bill_number_and_title:
            bill_number_and_title = [nt.strip() for nt in bill_number_and_title]
            bill_number_and_title = tuple(list(filter(None, bill_number_and_title)))
            bill_number_and_title = ' '.join(bill_number_and_title)
        else:
            bill_number_and_title = ''

        items_without_dict = {'bill_name': bill_name,
                              'date': date,
                              'bill_number_and_title': bill_number_and_title}

        containers = response.xpath('//*[@class="StatusTable"]')
        item_dict = {}
        for container in containers:
            stage = container.xpath('.//*[contains(@class, "MajorStage")]/text()').extract_first()

            chamber = container.xpath('.//*[contains(@class, "MajorStage")]/preceding::div[@class="ChamberGroupTitle"]//text()').extract()
            chamber = [c.strip() for c in chamber]
            chamber = tuple(list(filter(None, chamber)))
            chamber = chamber[-1]

            names = container.xpath('.//*[@class="StatusCol1 col-xs-9 col-md-9 col-lg-9"]/div[1]/text()').extract()
            names = [n.strip() for n in names]
            names = tuple(list(filter(None, names)))

            values = container.xpath(
                './/*[@class="StatusCol2 col-xs-3 col-md-3 col-lg-3"]/span//text()|'
                './/*[@class="StatusCol2 col-xs-3 col-md-3 col-lg-3"]/a/text()').extract()
            values = [v.strip() for v in values]
            values = tuple(list(filter(None, values)))

            for n, v in zip(names, values):
                item_dict[chamber + ' - ' + stage + ' - ' + n] = v


        items = dict(item_dict.items() | items_without_dict.items())

        latest_publication = response.xpath(
            u'//a[text()="Dernière version"]/@href').extract_first()
        if latest_publication:
            latest_publication = latest_publication.replace('//', '')
            latest_publication = 'https://' + latest_publication
            result=Request(latest_publication,
                          meta={'items': items},
                          callback=self.parse_latest_publication)
            yield result
        else:
            bill=Bill(self.legislature+items['bill_number_and_title'], self.legislature+items['bill_number_and_title'], self.legislature)
            for k in item_dict.keys():
                if k!='bill_number_and_title' and k!='bill_name' and k!='date':
                    bill.addEvent(k, item_dict[k], None, None)
            self.add_bill(bill)
            yield items

    def parse_latest_publication(self, response):
        table_of_contents = response.xpath(
            '//li[contains(@class, "Level1")]/a/text()').extract()

        row_list = []
        rows = response.xpath('//*[@style="margin-top: 10pt; text-align: justify; font-family: Verdana, Helvetica, sans-serif;font-weight: bold;"]|//*[@style="margin-top: 10pt; text-align: justify; font-size: 0.8rem;font-family: Verdana, Helvetica, sans-serif;font-weight: bold;"]|//*[@style="margin-top: 3pt; text-align: justify; font-size: 0.8rem;font-family: Verdana, Helvetica, sans-serif;font-weight: bold;"]')
        for row in rows:
            row_text = row.xpath('.//text()').extract()
            row_text = ''.join(row_text)
            row_list.append(row_text)

        row_dict = {}
        row_dict['Latest Publication'] = ', '.join(row_list)
        row_dict['Table of contents'] = tuple(table_of_contents)

        #print(row_dict['Latest Publication'])

        #add bill
        result = dict(response.meta['items'].items() | row_dict.items())
        bill=Bill(self.legislature+result['bill_number_and_title'], self.legislature+result['bill_number_and_title'], self.legislature)

        """if bill.title!="CanadaC-74 Loi portant exécution de certaines dispositions du budget déposé au Parlement le 27 février 2018 et mettant en oeuvre d'autres mesures":
            yield result
        else:"""
        bill.setDetails(result['Latest Publication'])
        bill.setHyperlink(response.request.url)
        self.scrapeLawsinBill(bill)
        for k in response.meta['items'].keys():
            if k!='bill_number_and_title' and k!='bill_name' and k!='date':
                bill.addEvent(k, response.meta['items'][k], None, None)
        self.add_bill(bill)

    def retrieve_bills(self):

        settings = get_project_settings()
        #parl_spider=__import__('federal_scraper.parl_spider')
        #settings.setmodule(parl_spider)
        process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
        'LOG_STDOUT' : False,
        'LOG_FILE' : 'scrapy_output.txt',
        'ITEM_PIPELINES': {
                'scrapers.federal_scraper.CanPipeline': 1}
        })
        process.crawl(Canada)
        dummyvar=1#print("hellononi")
        process.start()
        return

    def spider_closed(self, spider):
        self.bills=spider.bills
        #print(self.bills)
        dummyvar=1#print(self.bills)
        return

    def scrapeLawsinBill(self, bill):
        for i in range(len(bill.details.split("Loi"))-1):
            if i==0:
                continue
            modifiedstripped=bill.details.split("Loi")[i]
            #print(modifiedstripped+"\n")
            modifiedLaw = re.split(Canada.law_delimiter_str, modifiedstripped)[0]
            print(modifiedLaw+"\n")
            dummyvar=1#print("Loi"+modifiedLaw)
            bill.addLaw("Loi"+re.compile(r"\(|,|;|\.").split(modifiedLaw)[0])
        for i in range(len(bill.details.split("Code"))-1):
            if i==0:
                continue
            modifiedstripped=bill.details.split("Code")[i]
            modifiedLaw = re.split(Canada.law_delimiter_str, modifiedstripped)[0]
            dummyvar=1#print("Code"+modifiedLaw)
            bill.addLaw("Code"+re.compile(r"\(|,|;|\.").split(modifiedLaw)[0])

class CanPipeline(object):
    def close_spider(self, spider):
        #for bill in spider.bills:
        #    dummyvar=1#print(bill.identifier)
        return
