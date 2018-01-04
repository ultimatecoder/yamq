# Copyright (C) 2017-2018 Jaysinh Shukla (jaysinhp@gmail.com)
# Please find copy of license at "LICENSE"
# at the root of the project.


from stomp import listener


class TestListener(listener.TestListener):

    def _wait_timeout(condition, available):
        def wrapper(func):
            def wrapper_function(self, timeout=None):
                if timeout:
                    condition_ = getattr(self, condition)
                    available_ = getattr(self, available)
                    with condition_:
                        timein = True
                        while not available_:
                            timein = condition_.wait(timeout=timeout)
                            if not timein:
                                raise TimeoutError
                            else:
                                break
                    setattr(self, available, False)
                else:
                    func(self)
            return wrapper_function
        return wrapper

    @_wait_timeout('message_condition', 'message_received')
    def wait_for_message(self, timeout=None):
        super().wait_for_message()

    @_wait_timeout('heartbeat_condition', 'heartbeat_received')
    def wait_for_heartbeat(self, timeout=None):
        super().wait_for_heartbeat()
