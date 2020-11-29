#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 29 13:37:36 2020

@author: clairericks
"""
from avyReport import createChart
import smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


message = createChart()
with open('avyreport.txt', 'w') as file: 
    file.write(message)
    

port = 465

# Enter password for email
# password = 

subject = 'Avy Report'
body = 'Daily Avy Report'

# Enter emails
# sender_email = 
# receiver_email = 

message = MIMEMultipart()
message['From'] = sender_email
message['To'] = receiver_email
message['Subject'] = subject

message.attach(MIMEText(body, 'plain'))

filename = 'avyreport.txt'
with open(file, 'r') as attachment: 
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())

encoders.encode_base64(part)
part.add_header(
    'Content-Disposition', 
    f'attachment; filename= {filename}',
)

message.attach(part)
text = message.as_string()

context = ssl.create_default_context()
with smtplib.SMTP_SSL('smtp.gmail.com', port, context=context) as server: 
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, text)
