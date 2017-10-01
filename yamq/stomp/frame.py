class Frame:

    def __init__(self, command, headers, body=""):
        self.command = command
        self.headers = headers
        self.body = body

    def __repr__(self):
        return "<Frame {}>".format(self.command)


class ConnectedFrame(Frame):

    def __init__(self, version="1.2", heart_beat=None, session=None,
                 server=None):
        command = "CONNECTED"
        headers = {
            "version": version,
        }

        if heart_beat:
            headers["heart-beat"] = heart_beat
        if session:
            headers["session"] = session
        if server:
            headers["server"] = server
        super().__init__(command, headers)


class MessageFrame(Frame):

    def __init__(self, message, destination, subscription_id, ack=None):
        command = "MESSAGE"
        headers = {
            'destination': destination,
            'message-id': message._id,
            'content-type': message.content_type,
            'subscription': subscription_id
        }

        if ack:
            headers['ack'] = ack
        super().__init__(command, headers, message.message)
