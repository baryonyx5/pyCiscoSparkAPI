from restReq import RestReq

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
# getMembershipsByPersonId
# getMembershipsByPersonEmail
# createMembershipToRoom
# getMembershipDetails
# updateMembership
# deleteMembership
class Memberships:
    MEMBERSHIPS_URL = "https://api.ciscospark.com/v1/memberships"

    def __init__(self,token,timeout=None):
        self.restReq = RestReq(token,timeout)

    def getMemberships(self,roomId=None,personId=None,personEmail=None,max=None):
        """Get an array of all of my Memberships
        This request can be queryied by roomId, personId, or personEmail address.
        The number of items return can be restricted by max.
        """
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

    def getMembershipsByPersonId(self,personId):
        return self.getMemberships(personId=personId)

    def getMembershipsByPersonEmail(self,personEmail):
        return self.getMemberships(personEmail=personEmail)

    def createMembershipToRoom(self,roomId,personId=None,personEmail=None,isModerator=None):
        """
        if personId == None and personEmail == None:
            raise Exception("personId or personEmail should not be None")
        if personId != None and personEmail != None:
            raise Exception("personId or personEmail can be set - not both!")
        """
        payload = { 'roomId' : roomId, 'personId' : personId, 'personEmail': personEmail, 'isModerator' : isModerator }
        response = self.restReq.post(self.MEMBERSHIPS_URL,payload)
        if response.status_code != 200:
            response.raise_for_status()
        else:
            r  = response.json()
            return Membership(r.get('id'),r.get('personId'),r.get('personEmail'),r.get('roomId'),r.get('isModerator'),r.get('isMonitor'),r.get('created'))

    def createMemebershipToRoomByPersonId(self,roomId,personId,isModerator=None):
        return self.createMembershipToRoom(roomId,personId=personId,isModerator=isModerator)

    def createMembershipToRoomByPersonEmail(self,roomId,personEmail,isModerator=None):
        return self.createMembershipToRoom(roomId,personEmail=personEmail,isModerator=isModerator)

    def getMembershipDetails(self,membershipId):
        response = self.restReq.get(self.MEMBERSHIPS_URL,id=membershipId)
        if response.status_code != 200:
            response.raise_for_status()
        else:
            r  = response.json()
            return Membership(r.get('id'),r.get('personId'),r.get('personEmail'),r.get('roomId'),r.get('isModerator'),r.get('isMonitor'),r.get('created'))

    def updateMembershipModerator(self,membershipId,isModerator):
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

