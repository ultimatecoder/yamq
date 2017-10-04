class Subject:

    _objects = {}

    def __new__(cls, name, loop):
        try:
            obj = cls._objects[name]
        except KeyError as e:
            obj = super().__new__(cls)
            obj.observers = {}  # observer_obj: ack_type
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
