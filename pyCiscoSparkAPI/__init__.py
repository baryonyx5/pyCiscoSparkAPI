import json
import requests


import codecs
import sys
import logging
import httplib
import collections

httplib.HTTPConnection.debuglevel = 1
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True
UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)


# Simple Rest 'requests' class
class RestReq:
    CONTENT_TYPE = "application/json"
    def __init__(self,token,timeout=None):
        self.token = token
        self.timeout = timeout
        self.headers = {"Authorization":"Bearer "+self.token,"Content-type": self.CONTENT_TYPE}

    def get(self,base_url,payload=None,id=None):
        url = base_url
        if (id != None):
            url = url + "/" + id
        return requests.get(url,headers=self.headers,params=payload,timeout=self.timeout)

    def post(self,base_url,payload=None,id=None):
        url = base_url
        if (id != None):
            url = url + "/" + id
        return requests.post(url,headers=self.headers,json=payload,timeout=self.timeout)

    def put(self,base_url,payload=None,id=None):
        url = base_url
        if (id != None):
            url = url + "/" + id
        return requests.put(url,headers=self.headers,json=payload,timeout=self.timeout)

    def delete(self,base_url,id):
        url = base_url + "/" + id
        return requests.delete(url,headers=self.headers,timeout=self.timeout)

# A wrapper class for Person content
class Person:
    def __init__(self,id,emails,displayName,avatar,created):
        self._id = id
        self._emails = emails
        self._displayName = displayName
        self._avatar = avatar
        self._created = created

    def id(self):
        return self._id

    def emails(self):
        return self._emails

    def displayName(self):
        return self._displayName

    def avatar(self):
        return self._avatar

    def created(self):
        return self._created

# A People class the exposes the API for -
#
# getPeople
# getPersonDetails
# getMe
class People:
    PEOPLE_URL = "https://api.ciscospark.com/v1/people"
    def __init__(self,token,timeout=None):
        self.restReq = RestReq(token,timeout=None)

    def getPeople(self, email=None, displayName=None, max=None):
        if email != None and displayName != None:
            raise Exception('email and displayName are NOT None!')
        payload = { 'email' : email, 'displayName' : displayName, 'max' : max }
        response = self.restReq.get(self.PEOPLE_URL,payload=payload)
        if response.status_code != 200:
            response.raise_for_status()
        else:
            person_array = []
            results = response.json()
            for r in results['items']:
                person_array.append(Person(r.get('id'),r.get('emails'),r.get('displayName'),r.get('avatar'),r.get('created')))
            return person_array

    def getPersonDetails(self,id):
        response = self.restReq.get(self.PEOPLE_URL,id=id)
        if response.status_code != 200:
            response.raise_for_status()
        else:
            r = response.json()
            return Person(r.get('id'),r.get('emails'),r.get('displayName'),r.get('avatar'),r.get('created'))

    def getMe(self):
        return self.getPersonDetails('me')

# A wrapper class for Membership content
class Membership:
    def __init__(self,id,personId,personEmail,roomId,isModerator,isMonitor,created):
        self._id = id
        self._personId = personId
        self._personEmail = personEmail
        self._roomId = roomId
        self._isModerator = isModerator
        self._isMonitor = isMonitor
        self._created = created

    def id(self):
        return self._id

    def personId(self):
        return self._personId

    def personEmail(self):
        return self._personEmail

    def roomId(self):
        return self._roomId

    def isModerator(self):
        return self._isModerator

    def iMonitor(self):
        return self._isMonitor

    def created(self):
        return self._created

# A Memberships class the exposes the API for -
#
# getMemberships
# getMembershipsByRoom
# getMembershipsByPerson
# createMembershipToRoom
# getMembershipDetails
# updateMembership
# deleteMembership
class Memberships:
    MEMBERSHIPS_URL = "https://api.ciscospark.com/v1/memberships"

    def __init__(self,token,timeout=None):
        self.restReq = RestReq(token,timeout)

    def getMemberships(self,roomId=None,personId=None,personEmail=None,max=None):
        if personId != None and personEmail != None:
            raise Exception('personId and personEmail are NOT None!')
        payload = { 'roomId' : roomId, 'personId' : personId, 'personEmail' : personEmail, 'max' : max }
        response = self.restReq.get(self.MEMBERSHIPS_URL,payload)
        if response.status_code != 200:
            response.raise_for_status()
        else:
            membership_array = []
            results  = response.json()
            for r in results['items']:
                membership_array.append(Membership(r.get('id'),r.get('personId'),r.get('personEmail'),r.get('roomId'),r.get('isModerator'),r.get('isMonitor'),r.get('created')))
            return membership_array

    def getMembershipsByRoom(self,roomId):
        return self.getMemberships(roomId=roomId)

    def getMembershipsByPerson(self,personId=None,personEmail=None):
        return self.getMemberships(personId=personId,personEmail=personEmail)

    def createMembershipToRoom(self,roomId,personId=None,personEmail=None,isModerator=False):
        if personId == None and personEmail == None:
            raise Exception("personId or personEmail should not be None")
        if personIde != None and personEmail != None:
            raise Exception("personId or personEmail can be set - not both!")
        payload = { 'roomId' : roomId, 'personId' : personId, 'personEmail': personEmail, 'isModerator' : isModerator }
        response = self.restReq.post(self.MEMBERSHIPS_URL,payload)
        if response.status_code != 200:
            response.raise_for_status()
        else:
            r  = response.json()
            return Membership(r.get('id'),r.get('personId'),r.get('personEmail'),r.get('roomId'),r.get('isModerator'),r.get('isMonitor'),r.get('created'))

    def getMembershipDetails(self,membershipId):
        response = self.restReq.get(self.MEMBERSHIPS_URL,id=membershipId)
        if response.status_code != 200:
            response.raise_for_status()
        else:
            r  = response.json()
            return Membership(r.get('id'),r.get('personId'),r.get('personEmail'),r.get('roomId'),r.get('isModerator'),r.get('isMonitor'),r.get('created'))

    def updateMembership(self,membershipId,isModerator):
        payload = { 'isModerator' : isModerator }
        response = self.restReq.put(self.MEMBERSHIPS_URL,id=membershipId,payload=payload)
        if response.status_code != 200:
            response.raise_for_status()
        else:
            r  = response.json()
            return Membership(r.get('id'),r.get('personId'),r.get('personEmail'),r.get('roomId'),r.get('isModerator'),r.get('isMonitor'),r.get('created'))

    def deleteMembership(self,membershipId):
        response = self.restReq.delete(self.MEMBERSHIPS_URL,id=membershipId)
        if response.status_code != 204:
            response.raise_for_status()
        else:
            return

# A wrapper class for Room content
class Room:
    def __init__(self):
        self._id = None
        self._title = None
        self._created = None
        self._lastActivity = None
        self._sipAddress = None

    def __init__(self,id,title,created,lastActivity,sipAddress):
        self._id = id
        self._title = title
        self._created = created
        self._lastActivity = lastActivity
        self._sipAddress = sipAddress

    def id(self):
        return self._id

    def title(self):
        return self._title

    def created(self):
       return self._created

    def lastActivity(self):
       return self._lastActivity

    def sipAddress(self):
       return self._sipAddress

# A Memberships class the exposes the API for -
# getRooms
# getById
# newRoom
# updateRoom
# deleteRoom
class Rooms:
    ROOMS_URL = "https://api.ciscospark.com/v1/rooms"

    def __init__(self,token,timeout=None):
        self.restReq = RestReq(token,timeout)

    def getRooms(self,max=None,showSipAddress=None):
        if showSipAddress == True:
            showSipAddress = 'true'
        if showSipAddress == False:
            showSipAddress = 'false'
        payload = { 'max' : max, 'showSipAddress': showSipAddress }
        response = self.restReq.get(self.ROOMS_URL,payload=payload)
        if response.status_code != 200:
            response.raise_for_status()
        else:
            room_array = []
            results = response.json()
            for r in results['items']:
                room_array.append(Room(r.get('id'),r.get('title'),r.get('created'),r.get('lastActivity'),r.get('sipAddress')))
            return room_array

    def getById(self,id,showSipAddress=False):
        payload = { 'showSipAddress': showSipAddress }
        response = self.restReq.get(self.ROOMS_URL,id=id,payload=payload)
        if response.status_code != 200:
            response.raise_for_status()
        else:
            r = response.json()
            return Room(r.get('id'),r.get('title'),r.get('created'),r.get('lastActivity'),r.get('sipAddress'))

    def newRoom(self,title):
        payload = { 'title' : title }
        response = self.restReq.post(self.ROOMS_URL,payload=payload)
        if response.status_code != 200:
            response.raise_for_status()
        else:
            r = response.json()
            return Room(r.get('id'),r.get('title'),r.get('created'),r.get('lastActivity'),r.get('sipAddress'))

    def updateRoom(self,id,title):
        payload = { 'title' : title }
        response = self.restReq.put(self.ROOMS_URL,id=id,payload=payload)
        if response.status_code != 200:
            response.raise_for_status()
        else:
            r = response.json()
            return Room(r.get('id'),r.get('title'),r.get('created'),r.get('lastActivity'),r.get('sipAddress'))

    def deleteRoom(self,id):
        response = self.restReq.delete(self.ROOMS_URL,id=id)
        if response.status_code != 204:
            response.raise_for_status()
        else:
            return

# A wrapper class for Message content
class Message:
    def __init__(self,id,roomId,personId,personEmail,created,text):
        self._id = id
        self._roomId = roomId
        self._personId = personId
        self._personEmail = personEmail
        self._created = created
        self._text = text

    def id(self):
       return self._id

    def roomId(self):
       return self._roomId

    def personId(self):
       return self._personId

    def personEmail(self):
       return self._personEmail

    def created(self):
       return self._created

    def text(self):
       return self._text

# A Nessages class the exposes the API for -
# getMessagesByRoom
# sendMessageToRoom
# sendMessageToPerson
# getMessagesById
# deleteMessage
class Messages:
    MESSAGES_URL = "https://api.ciscospark.com/v1/messages"

    def __init__(self,token,timeout=None):
        self.restReq = RestReq(token,timeout)

    def getMessagesByRoom(self,roomId,before=None,beforeMessage=None,max=None):
        payload = { 'roomId' : roomId, 'before' : before, 'beforeMessage' : beforeMessage, 'max' : max }
        response = self.restReq.get(self.MESSAGES_URL,payload=payload)
        if response.status_code != 200:
            response.raise_for_status()
        else:
            message_array = []
            results = response.json()
            for r in results['items']:
                message_array.append(Message(r.get('id'),r.get('roomId'),r.get('personId'),r.get('pesonEMail'),r.get('created'),r.get('text')))
            return message_array

    def sendMessageToRoom(self,roomId,text,files=None):
        payload = { 'roomId' : roomId, 'text' : text , 'files' : files}
        response = self.restReq.post(self.MESSAGES_URL,payload=payload)
        if response.status_code != 200:
            response.raise_for_status()
        else:
            r = response.json()
            return Message(r.get('id'),r.get('roomId'),r.get('personId'),r.get('pesonEMail'),r.get('created'),r.get('text'))

    def sendMessageToPerson(self,text,toPersonId=None,toPersonEmail=None,files=None):
        if toPersonID != None and toPersonEmail != None:
            raise Exception('toPersonId and toPersonEmail are NOT None!')
        payload = { 'text' : text, 'toPersonId' : toPersonId, 'toPersonEmail' : toPersonEmail, 'files' : files }
        response = self.restReq.post(self.MESSAGES_URL,payload=payload)
        if response.status_code != 200:
            response.raise_for_status()
        else:
            r = response.json()
            return Message(r.get('id'),r.get('roomId'),r.get('personId'),r.get('pesonEMail'),r.get('created'),r.get('text'))

    def getMessagesById(self,messageId):
        payload = { 'id' : messageId }
        response = self.restReq.get(self.MESSAGES_URL,payload=payload)
        if response.status_code != 200:
            response.raise_for_status()
        else:
            r = response.json()
            return Message(r.get('id'),r.get('roomId'),r.get('personId'),r.get('pesonEMail'),r.get('created'),r.get('text'))

    def deleteMessage(self,messageId):
        response = self.restReq.delete(self.MESSAGES_URL,id=messageId)
        if response.status_code != 204:
            response.raise_for_status()
        else:
            return

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
