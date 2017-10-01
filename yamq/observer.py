import stomp


class Observer:

    def __init__(self, callback, loop):
        self.loop = loop
        self.callback = callback

    async def update(self, subject, message):
        self.loop.call_soon(self.callback, subject, message)


class ObserverSTOMP:

    def __init__(self, loop, transport):
        self.loop = loop
        self.transport = transport

    async def ack_auto(self, frame):
        pass

    async def update(self, subject, message, message_id, subscription_id, ack):
        frame = stomp.MessageFrame(
            subject,
            message_id,
            subscription_id,
            message,
            ack
        )
        pass
