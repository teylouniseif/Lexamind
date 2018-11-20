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
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class Email(object):

    server = 'smtp.gmail.com'
    user = 'lexamindcooperathon@gmail.com'
    password = '1dragonball'

    def send_Email( recipient):

        server = smtplib.SMTP(Email.server, 587)
        server.ehlo()
        server.starttls()
        server.login(Email.user, Email.password)

        updateidentifier, updatehtml=retrieveArchive(recipient)
        update=Update(updateidentifier, updateidentifier, updatehtml)
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Lexamind Update"
        msg['From'] = Email.user
        msg['To'] = recipient
        if update!= None:
            msg.attach(MIMEText(update.get_Content(), 'html'))
            server.sendmail(Email.user, recipient, msg.as_string())

        server.quit()
