#! python2
# -*- coding: utf-8 -*-

from scrapy.crawler import CrawlerProcess
#from federal_scraper.parl_spider.spiders.parl import ParlSpider

from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import signals
from scrapy.utils.project import get_project_settings

from scrapy import Spider
from scrapy.http import Request


class ParlSpider(Spider):
    name = 'parl_ca'
    allowed_domains = ['parl.ca']
    start_urls = (
        'https://www.parl.ca/LegisInfo/Home.aspx?ParliamentSession=42-1&Page=1',
    )

    # start_urls = ['http://www.parl.ca/LegisInfo/BillDetails.aspx?Language=F&billId=8804045']

    def parse(self, response):
        bills = response.xpath('//*[@class="BillTitle"]/@href').extract()
        for bill in bills:
            yield Request(bill.replace('Language=E', 'Language=F'),
                          callback=self.parse_bill)

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
            latest_publication = 'https://www.' + latest_publication
            yield Request(latest_publication,
                          meta={'items': items},
                          callback=self.parse_latest_publication)
        else:
            yield items

    def parse_latest_publication(self, response):
        table_of_contents = response.xpath(
            '//li[contains(@class, "Level1")]/a/text()').extract()

        row_list = []
        rows = response.xpath('//*[@style="margin-top: 10pt; text-align: justify; font-size: 0.8rem;font-family: Verdana, Helvetica, sans-serif;font-weight: bold;"]|//*[@style="margin-top: 3pt; text-align: justify; font-size: 0.8rem;font-family: Verdana, Helvetica, sans-serif;font-weight: bold;"]')
        for row in rows:
            row_text = row.xpath('.//text()').extract()
            row_text = ''.join(row_text)
            row_list.append(row_text)

        row_dict = {}
        row_dict['Latest Publication'] = ', '.join(row_list)
        row_dict['Table of contents'] = tuple(table_of_contents)


        all_items = dict(response.meta['items'].items() | row_dict.items())
        yield all_items

def my_function():

    settings = get_project_settings()
    #parl_spider=__import__('federal_scraper.parl_spider')
    #settings.setmodule(parl_spider)
    process = CrawlerProcess({
    'LOG_STDOUT' : False,
    'LOG_FILE' : 'scrapy_output.txt'})
    process.crawl(ParlSpider)
    print("hellononi")
    process.start()

    """spider = ParlSpider()
    settings = get_project_settings()
    parl_spider=__import__('federal_scraper.parl_spider')
    settings.setmodule(parl_spider)
    crawler = Crawler(ParlSpider, settings)
    crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
    #crawler.configure()
    crawler.crawl(spider)
    crawler_process.start()
    log.start()
    reactor.run() # the script will block here until the spider_closed signal was sent"""
    return
