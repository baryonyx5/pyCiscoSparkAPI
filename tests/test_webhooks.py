"""pyCiscoSparkAPI Webhooks Test Module."""

import os
import time
import pytest
from requests import HTTPError
from pyCiscoSparkAPI import SparkClient

stamp = time.strftime('%m%d%Y%H%M%S')
TOKEN = os.environ['SPARK_ACCESS_TOKEN']
client = SparkClient(TOKEN, debug=False)
hook_name = '%s-%s' % ('pyCiscoSparkAPI-Webhook', stamp)
room_name = '%s-%s' % ('pyCiscoSparkAPI-Room', stamp)
url = '%s/%s' % ('http://pycisco.sparkapi.com', stamp)


class TestSparkWebHooks(object):
    hookId = ''
    roomId = ''

    def setup_class(cls):
        """Create room for webhook."""
        r = client.rooms.newRoom(room_name)
        cls.roomId = r.id

    def teardown_class(cls):
        """Ensure room created in setup is deleted and any orphaned hooks are removed."""
        client.rooms.deleteRoom(cls.roomId)

        try:
            client.webhooks.deleteWebHook(cls.hookId)
        except Exception:
            pass

    def test_getWebHooks_fail(self):
        """Test result of getWebHooks when none exist."""
        wh = client.webhooks.getWebHooks()
        assert wh == []

    def test_getById_fail(self):
        """Test attempt to get webhook with invalid id."""
        with pytest.raises(HTTPError) as exc_info:
            client.webhooks.getById('ABCD' * 19)
        assert '400' in str(exc_info)

    def test_getByName_fail(self):
        """Test result of getByName with invalid name."""
        wh = client.webhooks.getByName('blahblah')
        assert wh == []

    def test_newWebHook_pass(self):
        """Test successful attempt to add a webhook."""
        roomId = 'roomId=%s' % self.__class__.roomId
        h = client.webhooks.newWebHook(name=hook_name, targetUrl=url, resource='messages',
                                       event='created', filt=roomId)
        self.__class__.hookId = h.id
        assert h.name == hook_name
        assert h.id is not None
        assert h.targetUrl == url

    def test_getWebHooks_pass(self):
        """Test successful attempt to get getWebHooks."""
        wh = client.webhooks.getWebHooks()
        assert wh[0].id

    def test_getById_pass(self):
        """Test successful attempt to get webhook by id."""
        h = client.webhooks.getById(self.__class__.hookId)
        assert h.id == self.__class__.hookId

    def test_getByName_pass(self):
        """Test successful attempt to get webhooks by name."""
        wh = client.webhooks.getByName(hook_name)
        assert wh[0].name == hook_name

    def test_getByUrl_pass(self):
        """Test successful attempt to get webhooks by url."""
        wh = client.webhooks.getByUrl(url)
        assert wh[0].targetUrl == url

    def test_updateWebHook_pass(self):
        """Test update of existing webhook."""
        new_name = hook_name + '-UPDATE'
        h = client.webhooks.updateWebHook(self.__class__.hookId, name=new_name)
        assert h.name == new_name
        assert h.id == self.__class__.hookId

    def test_deleteWebHook_pass(self):
        """Test successful deletion of webhook."""
        client.webhooks.deleteWebHook(self.__class__.hookId)
