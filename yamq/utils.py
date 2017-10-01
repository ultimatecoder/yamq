class AutoID:

    def __new__(cls, *args, **kwargs):
        try:
            new_id = cls.last_id + 1
        except AttributeError:
            new_id = 0
        obj = object.__new__(cls)
        obj._id = new_id
        cls.last_id = new_id
        return obj
