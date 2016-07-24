#!/usr/bin/env python

#######################################################################
# Import libraries
#######################################################################
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

#######################################################################
# Perform initializations
#######################################################################
# connection fields
from_address = "XXXX@gmail.com" # the email account you created
from_pass = "XXXX" # the password for this new email account

# email fields
to_address = "XXXX@gmail.com" # the email where you will receive updates
email_subject = "RPi Update (test)" # the email's subject
email_body = "An update from your RPi" # the email's body

#######################################################################
# Main logic
#######################################################################
# populate the message
msg = MIMEMultipart()
msg['From'] = from_address
msg['To'] = to_address
msg['Subject'] = email_subject
msg.attach(MIMEText(email_body, 'plain'))

# Connect to the email server
server = smtplib.SMTP('smtp.gmail.com', 587) # hostname, port
server.starttls()

# Authenticate
server.login(from_address, from_pass)

# format and send the email
text = msg.as_string() # package the email into a single string
server.sendmail(from_address, to_address, text)
server.quit()
