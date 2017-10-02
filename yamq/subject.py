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


class SubjectSTOMP:

    _objects = {}

    def __new__(cls, name, loop):
        try:
            obj = cls._objects[name]
        except KeyError as e:
            obj = super().__new__(cls)
            obj.observers = {}
            obj.name = name
            obj.loop = loop
            cls._objects[name] = obj
        return obj

    def __repr__(self):
        return "<Subject object: %s>" % (self.name,)

    @classmethod
    def get(cls, name):
        return cls._objects.get(name)

    def delete(self):
        try:
            del self.__class__._objects[self.name]
        except KeyError:
            pass

    def subscribe(self, observer, ack="auto"):
        self.observers[observer] = ack

    def unsubscribe(self, observer):
        try:
            del self.observers[observer]
        except KeyError:
            # TODO: I am not sure you should silently pass
            pass

        if not self.observers:
            self.delete()

    def notify(self, message):
        for observer, ack_type in self.observers.items():
            observer.update(self, message, ack_type)
