# Copyright (C) 2017-2018 Jaysinh Shukla (jaysinhp@gmail.com)
# Please find copy of license at "LICENSE"
# at the root of the project.


import asyncio
import os
import sys
import time

import stomp

from yamq import server
from test.utils.stomp import listeners


class STOMP_1_2:

    def __init__(self):
        host = os.environ.get('TEST_SERVER_HOST', 'localhost')
        port = int(os.environ.get('TEST_SERVER_PORT', '8000'))

        self._connection = stomp.Connection12([(host, port)])
        self.listener = listeners.TestListener()
        self._connection.set_listener('', self.listener)
        # NOTE:
        # * Putting time.sleep because the socket takes some time to process the
        # request to get connected. The *.start() will open the trnasport object.
        # reference: https://stackoverflow.com/questions/11585377/
        #
        # * The connection.start() is depricated in the master version.
        time.sleep(1)
        self._connection.start()
        self._connection.connect(wait=True)

    def __getattr__(self, name):
        return getattr(self._connection, name)
