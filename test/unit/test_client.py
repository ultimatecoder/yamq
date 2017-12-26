# Copyright (C) 2017-2018 Jaysinh Shukla (jaysinhp@gmail.com)
# Please find copy of license at "LICENSE"
# at the root of the project.


import unittest
from unittest import mock
import os
import imp

from test.utils import client


class TestClient(unittest.TestCase):

    @mock.patch('stomp.Connection12', autospec=True)
    def test_methods(self, Connection12):
        """Test connection api

        Assert call of obj.subscribe actually translates to
        obj._client.subscribe while calling."""
        client_obj = client.STOMP_1_2()
        client_obj._client = Connection12()
        client_obj.subscribe('/queue/test', 1)

        self.assertIs(client_obj.subscribe, client_obj._client.subscribe)
        client_obj._client.subscribe.assert_called_once_with('/queue/test', 1)

        client_obj.send('/queue/test', {'body': 'test'})

        self.assertIs(client_obj.send, client_obj._client.send)
        client_obj._client.send.assert_called_once_with(
            '/queue/test', {'body': "test"}
        )
