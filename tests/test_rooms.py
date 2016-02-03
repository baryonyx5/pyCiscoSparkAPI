"""pyCiscoSparkAPI Rooms Test Module."""

import os
import time
import pytest
from requests import HTTPError
from pyCiscoSparkAPI import SparkClient

stamp = time.strftime('%m%d%Y%H%M%S')
TOKEN = os.environ['SPARK_ACCESS_TOKEN']
client = SparkClient(TOKEN)
title = '%s-%s' % ('pyCiscoSparkAPI-Test-Rooms', stamp)


class TestSparkRooms(object):
    roomId = ''

    def teardown_class(cls):
        """Ensure any room created is deleted."""
        try:
            client.rooms.deleteRoom(cls.roomId)
        except Exception:
            pass

    def test_delete_room_fail(self):
        """Test attempt to delete a room that does not exist."""
        with pytest.raises(HTTPError) as exc_info:
            client.rooms.deleteRoom('ABCD' * 19)
        assert '400' in str(exc_info)

    def test_getRoomById_fail(self):
        """Test attempt to get room with invalid id."""
        with pytest.raises(HTTPError) as exc_info:
            client.rooms.getById('ABCD' * 19)
        assert '400' in str(exc_info)

    def test_newRoom_pass(self):
        """Test successful attempt to add a room."""
        r = client.rooms.newRoom(title)
        self.__class__.roomId = r.id
        assert r.title == title
        assert r.id is not None
        assert r.lastActivity is None
        assert r.created is not None
        assert r.sipAddress is None

    def test_getRoomById_pass(self):
        """.Test successful attempt to get room by ID."""
        r = client.rooms.getById(self.__class__.roomId)
        assert r.title == title

    def test_updateRoom_pass(self):
        """Test update of existing room."""
        r = client.rooms.updateRoom(self.__class__.roomId, title + '-UPDATE')
        assert r.title == title + '-UPDATE'
        assert r.id == self.__class__.roomId

    def test_deleteRoom_pass(self):
        """Test successful deletion of room."""
        client.rooms.deleteRoom(self.__class__.roomId)
