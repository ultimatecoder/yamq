from itertools import count

from yamq import utils


class Message():
    """Don't forget to call obj.delete() to delete object from the memory!"""

    _messages = {}
    _last_id = count()

    def __init__(self, message, content_type):
        self._id = next(Message._last_id)
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
        try:
            del Message._messages[self._id]
        except KeyError:
            pass
