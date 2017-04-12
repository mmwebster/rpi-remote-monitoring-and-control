#!/usr/bin/env python

#######################################################################
# Class definitions
#######################################################################
class Secret:
    def __init__(self):
        self.secrets = {"email_password": "xxxxxxxxx", "email_from": "your.new.email@gmail.com", "email_to": "your.existing.email@gmail.com"}

    def fetch(self, key):
        if key in self.secrets.keys():
            return self.secrets[key]
        else:
            raise "ERROR: passed invalid key to fetch_secret"
            return None
