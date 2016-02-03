"""pyCiscoSparkAPI init."""

from people import People
from memberships import Memberships
from rooms import Rooms
from messages import Messages
from webhooks import WebHooks
import codecs
import sys
import logging
import httplib


def init_logging():
    httplib.HTTPConnection.debuglevel = 1
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True
    UTF8Writer = codecs.getwriter('utf8')
    sys.stdout = UTF8Writer(sys.stdout)


# Wrappers SparkClient class
class SparkClient:
    def __init__(self, token, timeout=None, debug=False):
        self.token = token
        self.timeout = timeout
        self.debug = debug

        # API handlers
        self.people = People(token, self.timeout)
        self.rooms = Rooms(token, self.timeout)
        self.memberships = Memberships(token, self.timeout)
        self.messages = Messages(token, self.timeout)
        self.webhooks = WebHooks(token, self.timeout)

        if self.debug:
            init_logging()
