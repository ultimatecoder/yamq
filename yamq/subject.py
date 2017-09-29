class Subject:

    def __init__(self, name, loop):
        self.name = name
        self.observers = set()
        self.loop = loop

    def __repr__(self):
        return "<Subject object: %s>" % (self.name,)

    def subscribe(self, observer):
        self.observers.add(observer)

    def unsubscribe(self, observer):
        try:
            self.observers.remove(observer)
        except KeyError:
            # TODO: I am not sure you should silently pass
            pass

    async def notify(self, message):
        """Follows PUSH stratergy."""
        for observer in self.observers:
            await observer.update(self.name, message)
