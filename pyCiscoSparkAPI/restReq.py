import requests


# Simple Rest 'requests' class
class RestReq:
    CONTENT_TYPE = "application/json"

    def __init__(self, token, timeout=None):
        self.token = token
        self.timeout = timeout
        self.headers = {"Authorization": "Bearer " + self.token, "Content-type": self.CONTENT_TYPE}

    def get(self, base_url, payload=None, id=None):
        url = base_url
        if id:
            url = url + "/" + id
        return requests.get(url, headers=self.headers, params=payload, timeout=self.timeout)

    def post(self, base_url, payload=None, id=None):
        url = base_url
        if id:
            url = url + "/" + id
        return requests.post(url, headers=self.headers, json=payload, timeout=self.timeout)

    def put(self, base_url, payload=None, id=None):
        url = base_url
        if id:
            url = url + "/" + id
        return requests.put(url, headers=self.headers, json=payload, timeout=self.timeout)

    def delete(self, base_url, id):
        url = base_url + "/" + id
        return requests.delete(url, headers=self.headers, timeout=self.timeout)
