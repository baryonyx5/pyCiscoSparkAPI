from restReq import RestReq


# A wrapper class for Message content
class Message:
    def __init__(self, id, roomId, personId, personEmail, created, text, files=None):
        self._id = id
        self._roomId = roomId
        self._personId = personId
        self._personEmail = personEmail
        self._created = created
        self._text = text
        self._files = files

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

    def files(self):
        return self._files

# A Messages class the exposes the API for -
# getMessagesByRoom
# sendMessageToRoom
# sendMessageToPerson
# getMessagesById
# deleteMessage


class Messages:
    MESSAGES_URL = "https://api.ciscospark.com/v1/messages"

    def __init__(self, token, timeout=None):
        self.restReq = RestReq(token, timeout)

    def getMessagesByRoom(self, roomId, before=None, beforeMessage=None, max=None):
        payload = {'roomId': roomId, 'before': before, 'beforeMessage': beforeMessage, 'max': max}
        response = self.restReq.get(self.MESSAGES_URL, payload=payload)
        if response.status_code != 200:
            response.raise_for_status()
        else:
            message_array = []
            results = response.json()
            for r in results['items']:
                message_array.append(Message(r.get('id'), r.get('roomId'), r.get('personId'),
                                             r.get('personEmail'), r.get('created'),
                                             r.get('text'), r.get('files')))
            return message_array

    def sendMessageToRoom(self, roomId, text, files=None):
        payload = {'roomId': roomId, 'text': text, 'files': files}
        response = self.restReq.post(self.MESSAGES_URL, payload=payload)
        if response.status_code != 200:
            response.raise_for_status()
        else:
            r = response.json()
            return Message(r.get('id'), r.get('roomId'), r.get('personId'), r.get('personEmail'),
                           r.get('created'), r.get('text'), r.get('files'))

    def sendMessageToPerson(self, text, toPersonId=None, toPersonEmail=None, files=None):
        if toPersonId and toPersonEmail:
            raise Exception('use toPersonId or toPersonEmail - not both!')
        payload = {'text': text, 'toPersonId': toPersonId, 'toPersonEmail': toPersonEmail,
                   'files': files}
        response = self.restReq.post(self.MESSAGES_URL, payload=payload)
        if response.status_code != 200:
            response.raise_for_status()
        else:
            r = response.json()
            return Message(r.get('id'), r.get('roomId'), r.get('personId'), r.get('personEmail'),
                           r.get('created'), r.get('text'), r.get('files'))

    def sendMessageToPersonId(self, text, toPersonId, files=None):
        return self.sendMessageToPerson(text, toPersonId=toPersonId, files=files)

    def sendMessageToPersonEmail(self, text, toPersonEmail, files=None):
        return self.sendMessageToPerson(text, toPersonEmail=toPersonEmail, files=files)

    def getMessageById(self, messageId):
        response = self.restReq.get(self.MESSAGES_URL, id=messageId)
        if response.status_code != 200:
            response.raise_for_status()
        else:
            r = response.json()
            return Message(r.get('id'), r.get('roomId'), r.get('personId'), r.get('personEmail'),
                           r.get('created'), r.get('text'), r.get('files'))

    def deleteMessage(self, messageId):
        response = self.restReq.delete(self.MESSAGES_URL, id=messageId)
        if response.status_code != 204:
            response.raise_for_status()
        else:
            return
