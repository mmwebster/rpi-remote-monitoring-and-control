#!/usr/bin/env python

#######################################################################
# Class definitions
#######################################################################
class Secret:
    def __init__(self):
        self.secrets = {"email_password": "xxxxxxxxx"}

    def fetch(self, key):
        if key in self.secrets.keys():
            return self.secrets[key]
        else:
            raise "ERROR: passed invalid key to fetch_secret"
            return None
