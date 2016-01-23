import json
import requests

from people      import People
from memberships import Memberships
from rooms       import Rooms
from messages    import Messages


import codecs
import sys
import logging
import httplib
import collections

#httplib.HTTPConnection.debuglevel = 1
#logging.basicConfig()
#logging.getLogger().setLevel(logging.DEBUG)
#requests_log = logging.getLogger("requests.packages.urllib3")
#requests_log.setLevel(logging.DEBUG)
#requests_log.propagate = True
#UTF8Writer = codecs.getwriter('utf8')
#sys.stdout = UTF8Writer(sys.stdout)

# Wrappers SparkClient class
class SparkClient:
    def __init__(self,token,timeout=None):
        self.token = token
        self.timeout = timeout

        # API handlers
        self.people      = People(token,self.timeout)
        self.rooms       = Rooms(token,self.timeout)
        self.memberships = Memberships(token,self.timeout)
        self.messages    = Messages(token,self.timeout)
