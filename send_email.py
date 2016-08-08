#!/usr/bin/env python
# -*- coding: utf-8 -*-

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders


fromaddr = 'pinochet.server@gmail.com'

# Credentials (if needed)
username = 'pinochet.server@gmail.com'
password = 'Mc_2200mhat'

toaddr = 'kaminskip@mail.ru'


msg = MIMEMultipart()
msg['From'] = username
msg['To'] = toaddr
msg['Subject'] = "TEST EMAIL"

body = "TEST MESSAGE"
msg.attach(MIMEText(body, 'plain'))

filename = "neoline.py"
attachment = open("./neoline.py", "rb")

part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

msg.attach(part)

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(username, password)
text = msg.as_string()
server.sendmail(username, toaddr, text)
server.quit()
print 'Done!'