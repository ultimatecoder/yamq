# Copyright (C) 2017-2018 Jaysinh Shukla (jaysinhp@gmail.com)
# Please find copy of license at "LICENSE"
# at the root of the project.


import unittest
import threading
from functools import partial

from test.utils.stomp import listeners


class TestListeners(unittest.TestCase):

    def setUp(self):
        self.listener = listeners.TestListener()

    def test_timeout_works_wait_for_message(self):
        kwargs = {'headers': {}, 'message': "test"}
        message_send = threading.Timer(
            10, self.listener.on_message, kwargs=kwargs)
        message_send.start()
        with self.assertRaises(TimeoutError):
            self.listener.wait_for_message(timeout=1)

        message_send = threading.Timer(
            1, self.listener.on_message, kwargs=kwargs)
        message_send.start()
        self.listener.wait_for_message(timeout=5)

    def test_without_timeout_works_for_wait_for_heartbeat(self):
        kwargs = {'headers': {}, 'message': "test"}
        message_send = threading.Timer(
            1, self.listener.on_message, kwargs=kwargs)
        message_send.start()
        self.listener.wait_for_message()

    def test_without_timeout_works_for_wait_for_message(self):
        heartbeat_send = threading.Timer(1, self.listener.on_heartbeat)
        heartbeat_send.start()
        self.listener.wait_for_heartbeat()

    def test_timeout_works_wait_for_hearbeat(self):
        heartbeat_send = threading.Timer(10, self.listener.on_heartbeat)
        heartbeat_send.start()
        with self.assertRaises(TimeoutError):
            self.listener.wait_for_heartbeat(timeout=1)

        heartbeat_send = threading.Timer(1, self.listener.on_heartbeat)
        heartbeat_send.start()
        self.listener.wait_for_heartbeat(timeout=5)
