# Copyright (C) 2017-2018 Jaysinh Shukla (jaysinhp@gmail.com)
# Please find copy of license at "LICENSE"
# at the root of the project.


import asyncio
import os
import subprocess
import signal
import time
import unittest

import stomp

from yamq import server


class TestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.host = os.environ.get('TEST_SERVER_HOST', 'localhost')
        cls.port = os.environ.get('TEST_SERVER_PORT', '8000')

    def setUp(self):
        self._server = subprocess.Popen(
            args=[
                "python", "main.py", "-d", self.host, "-p", self.port
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        if self._server.poll():
            stdout = self._server.stdout.read()
            self._server.stdout.close()
            stdout = stdout.decode('utf-8')
            error_message= "Problem while starting server.\n{}".format(stdout)
            raise OSError

    def tearDown(self):
        self._server.send_signal(signal.SIGINT)
        try:
            self._server.wait(timeout=15)
            if (self._server.returncode is not 0 and
                self._server.returncode is not -2):
                # NOTE: -2 is returncode when the server is closed just after
                # start. Such behaviour is common when test_* method is with
                # pass so tearDown is suddenly called after setUp. The actual
                # server has not started when it receives SIGINT.
                # TODO: Identify the value -2 and 0 as returncode is platform
                # independent or not.
                print("Returncode: {}".format(
                    self._server.returncode))
                stdout = self._server.stdout.read()
                print(stdout.decode('utf-8'))
                raise OSError
        except subprocess.TimeoutExpired:
            self._server.kill()
            stdout = self._server.stdout.read()
            print("Server killed. Server output: {}".format(
                stdout.decode('utf-8')))
            raise OSError

        self._server.stdout.close()
        self._server = None
