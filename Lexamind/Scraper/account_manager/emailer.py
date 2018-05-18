#! python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  30 21:57:00 2018
@author: Saif Kurdi-Teylouni
"""
from storer.storer import retrieveArchive
from .displayer import Update
import jsonpickle, re
import smtplib

class Email(object):

    server = 'smtp.gmail.com'
    user = 'lexamindcooperathon@gmail.com'
    password = 'billscraper'

    def send_Email( recipient):

        server = smtplib.SMTP(Email.server, 587)
        server.ehlo()
        server.starttls()
        server.login(Email.user, Email.password)

        update=retrieveArchive(recipient)
        if update!= None:
            server.sendmail(Email.user, recipient, update.get_Content())

        server.quit()
