#! python2
# -*- coding: utf-8 -*-

from scrapy.crawler import CrawlerProcess
from federal_scraper.parl_spider.spiders.parl import ParlSpider

from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import signals
from scrapy.utils.project import get_project_settings

#def my_function(X, Y):
#    return "Hello %s %s!" % (X, Y)


def my_function():

    import subprocess
    import os

    os.path.dirname(os.path.realpath(__file__))

    python3_command = "py -2 -m scrapy crawl parl"  # launch your python2 script using bash
    f = open("outputFile","wb")
    process = subprocess.Popen(python3_command.split(), stdout=f, cwd="C:/Users/teylo/Desktop/Lexamind/Scraper/federal_scraper")#stdout=subprocess.PIPE)
    output, error = process.communicate()  # receive output from the python2 script

    print( error)

    print(output)
    """settings = get_project_settings()
    parl_spider=__import__('federal_scraper.parl_spider')
    settings.setmodule(parl_spider)
    process = CrawlerProcess(settings)
    process.crawl(ParlSpider)
    print("hellononi")
    process.start()"""

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
