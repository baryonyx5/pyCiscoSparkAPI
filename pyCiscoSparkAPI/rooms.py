from restReq import RestReq


# A wrapper class for Room content
class Room:
    def __init__(self, id, title, created, lastActivity, sipAddress):
        self._id = id
        self._title = title
        self._created = created
        self._lastActivity = lastActivity
        self._sipAddress = sipAddress

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @property
    def created(self):
        return self._created

    @property
    def lastActivity(self):
        return self._lastActivity

    @property
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

    def __init__(self, token, timeout=None):
        self.restReq = RestReq(token, timeout)

    def getRooms(self, max=None, showSipAddress=None):
        if showSipAddress:
            showSipAddress = 'true'
        if not showSipAddress:
            showSipAddress = 'false'
        payload = {'max': max, 'showSipAddress': showSipAddress}
        response = self.restReq.get(self.ROOMS_URL, payload=payload)
        if response.status_code != 200:
            response.raise_for_status()
        else:
            room_array = []
            results = response.json()
            for r in results['items']:
                room_array.append(Room(r.get('id'), r.get('title'), r.get('created'),
                                       r.get('lastActivity'), r.get('sipAddress')))
            return room_array

    def getById(self, id, showSipAddress=False):
        payload = {'showSipAddress': showSipAddress}
        response = self.restReq.get(self.ROOMS_URL, id=id, payload=payload)
        if response.status_code != 200:
            response.raise_for_status()
        else:
            r = response.json()
            return Room(r.get('id'), r.get('title'), r.get('created'), r.get('lastActivity'),
                        r.get('sipAddress'))

    def newRoom(self, title):
        payload = {'title': title}
        response = self.restReq.post(self.ROOMS_URL, payload=payload)
        if response.status_code != 200:
            response.raise_for_status()
        else:
            r = response.json()
            return Room(r.get('id'), r.get('title'), r.get('created'), r.get('lastActivity'),
                        r.get('sipAddress'))

    def updateRoom(self, id, title):
        payload = {'title': title}
        response = self.restReq.put(self.ROOMS_URL, id=id, payload=payload)
        if response.status_code != 200:
            response.raise_for_status()
        else:
            r = response.json()
            return Room(r.get('id'), r.get('title'), r.get('created'), r.get('lastActivity'),
                        r.get('sipAddress'))

    def deleteRoom(self, id):
        response = self.restReq.delete(self.ROOMS_URL, id=id)
        if response.status_code != 204:
            response.raise_for_status()
        else:
            return
