#!/usr/bin/env python

#######################################################################
# Import libraries
#######################################################################
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

#######################################################################
# Class definitions
#######################################################################
class Mailer:
    def __init__(self, from_address, from_pass, to_address):
        # save props
        self.from_address = from_address
        self.from_pass = from_pass
        self.to_address = to_address

        # Connect to the email server
        self.server = smtplib.SMTP('smtp.gmail.com', 587) # hostname, port
        self.server.starttls()

        # Authenticate
        self.server.login(from_address, from_pass)

    def send(self, subject, body):
        # format message w/ defaults
        msg = MIMEMultipart()
        msg['From'] = self.from_address
        msg['To'] = self.to_address
        # define subject and body
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # format and send the email
        text = msg.as_string() # package the email into a single string
        self.server.sendmail(self.from_address, self.to_address, text)

        print("Mailer: Sent email to " + self.to_address)

    # @desc Sends a test email
    def test(self):
        self.send("RPi Test", "Mailer class is functioning properly")

    def __exit__(self, exc_type, exc, traceback):
        print("Mailer: Exiting, cleaning up")
        self.server.quit()
