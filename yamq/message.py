from yamq import utils


class Message(utils.AutoID):
    """Don't forget to call obj.delete() to delete the object actually from the memory."""

    _messages = {}

    def __init__(self, message, content_type):
        Message._messages[self._id] = self
        self.message = message
        self.content_type = content_type

    def delete(self):
        try:
            del Message._messages[self._id]
            # TODO: Not sure about calling the delete method manually! Should
            # my object really be delted from here!
            #self.__del__()
        except KeyError as e:
            # TODO: Not sure I should pass the key error silently here!
            pass

    @classmethod
    def get(cls, message_id):
        try:
            obj = cls._messages[message_id]
        except KeyError:
            raise ValueError("Message does not exists.")
        return obj

    def __del__(self):
        # TODO: I am totally confused my object will be removed from memory or
        # not. Because the __del__ will be only called when reference count of
        # the object will reach to ZERO. This reference count will not reach to
        # ZERO because the Message._messages dict will have reference of it.
        try:
            del message._messages[self._id]
        except keyerror:
            pass
