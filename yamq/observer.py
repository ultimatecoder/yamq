class Observer:

    def __init__(self, callback, loop):
        self.loop = loop
        self.callback = callback

    async def update(self, subject, message):
        self.loop.call_soon(self.callback, subject, message)
