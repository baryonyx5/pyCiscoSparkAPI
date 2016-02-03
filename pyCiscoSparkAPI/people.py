from restReq import RestReq


# A wrapper class for Person content
class Person:
    def __init__(self, id, emails, displayName, avatar, created):
        self._id = id
        self._emails = emails
        self._displayName = displayName
        self._avatar = avatar
        self._created = created

    @property
    def id(self):
        return self._id

    @property
    def emails(self):
        return self._emails

    @property
    def displayName(self):
        return self._displayName

    @property
    def avatar(self):
        return self._avatar

    @property
    def created(self):
        return self._created

# A People class the exposes the API for -
#
# getPeople
# getPersonDetails
# getMe


class People:
    PEOPLE_URL = "https://api.ciscospark.com/v1/people"

    def __init__(self, token, timeout=None):
        self.restReq = RestReq(token, timeout=timeout)

    def getPeople(self, email=None, displayName=None, max=None):
        """
        Get a list of People using email address or displayName.
        Use only one of email address or displayName - not both.
        max can be used to restrict the number of People returned.
        """
        if email and displayName:
            raise Exception('Use either email address or displayName for getPeople, not both!')

        payload = {'email': email, 'displayName': displayName, 'max': max}
        response = self.restReq.get(self.PEOPLE_URL, payload=payload)

        if response.status_code != 200:
            response.raise_for_status()
        else:
            person_array = []
            results = response.json()
            for r in results['items']:
                person_array.append(Person(r.get('id'), r.get('emails'), r.get('displayName'),
                                           r.get('avatar'), r.get('created')))
            return person_array

    def getPeopleByEmail(self, email, max=None):
        """Get People by email address."""
        return self.getPeople(email=email, max=max)

    def getPeopleByDisplayName(self, displayName, max=None):
        """Get People by displayName"""
        return self.getPeople(displayName=displayName, max=max)

    def getPersonDetails(self, id):
        """Get details of a single person using an person id."""
        response = self.restReq.get(self.PEOPLE_URL, id=id)
        if response.status_code != 200:
            response.raise_for_status()
        else:
            r = response.json()
            return Person(r.get('id'), r.get('emails'), r.get('displayName'), r.get('avatar'),
                          r.get('created'))

    def getMe(self):
        """Get personal details of 'me' using token."""
        return self.getPersonDetails('me')
