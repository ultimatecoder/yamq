import asyncio
import os


import subject
import stomp
import observer
import message

SUBJECTS = {}
#MESSAGES = {}

#MESSAGE_ID = -1


#def create_message(message):
#    MESSAGE_ID += 1
#    MESSAGES[MESSAGE_ID] = message
#    return MESSAGE_ID


class STOMP_Server(asyncio.Protocol):
    """Minimum supported version 1.2"""

    def connection_made(self, transport):
        self.transport = transport
        self.subscription = {}
        self.observer = observer.ObserverSTOMP(event_loop, self.transport)

    def data_received(self, data):
        try:
            frame = stomp.loads(data.decode('utf-8'))
            if frame.command == 'SUBSCRIBE':
                self.subscribe(
                    frame.headers['id'], frame.headers['destination'],
                    frame.headers['ack']
                )
            elif frame.command in ["STOMP", "CONNECTED"]:
                self.stomp(
                    frame.headers["accept-version"],
                    frame.headers.get("host")
                )
            elif frame.command == "SEND":
                self.send(frame.headers['destination'], frame.body)
            else:
                print("Invalid command for now.")
        except ValueError as e:
            error_frame = stomp.Frame(
                command="ERROR",
                headers={
                    "message": "Invalid frame received"
                },
                body=str(e)
            )
            response = stomp.dumps(error_frame)
            self.transport.write(response.encode("utf-8"))
            self.transport.close()

    def stomp(self, accepted_version, host=None):
        response = stomp.dumps(stomp.ConnectedFrame())
        return self.transport.write(response.encode("utf-8"))

    def connect(self):
        pass

    def send(self, destination, raw_message, **headers):
        user_subject = SUBJECTS.get(destination)
        if not user_subject:
            user_subject = subject.SubjectSTOMP(
                name=destination, loop=event_loop
            )
            SUBJECTS[destination] = subject
        message_obj = message.Message(raw_message)
        self.loop.call_soon(user_subject.notify(message_obj))

    def subscribe(self, subject_id, destination, ack="auto", **headers):
        user_subject = SUBJECTS.get(destination)
        if not user_subject:
            user_subject = subject.SubjectSTOMP(
                name=destination, loop=event_loop
            )
            SUBJECTS[destination] = subject
        self.subscription[subject_id] = subject
        user_subject.subscribe(self.observer, subscrption_id, ack)

    def unsubscribe(self, subject_id, **headers):
        user_subject = self.subscription.get(subject_id)
        if not user_subject:
            # TODO: Return Error frame here
            pass
        user_subject.unsubscribe(self.observer)

    def ack(self, id, **headers):
        pass

    def nack(self, id, **headers):
        pass

    def disconnect(self, receipt, **headers):
        for user_subject in self.subscription.values():
            user_subject.unsubscribe(self.observer)


#class YampServer(asyncio.Protocol):
#
#    def connection_made(self, transport):
#        print("Connection received")
#        self.transport = transport
#
#    def data_received(self, data):
#        command = data.strip()
#        print(command)
#        if command == b'SUBSCRIBE':
#            print("Subscribed called")
#        elif command == b'UNSUBSCRIBE':
#            print("Unsubscribed called")
#        elif command == b"DISCONNECT":
#            print("Disconnect called")
#        else:
#            print("Unknown command")
#
#    def connection_lost(self, exc):
#        print("Connection closed")


if __name__ == '__main__':
    IP = os.getenv("YAMP_SERVER", "127.0.0.1")
    PORT = os.getenv("YAMP_PORT", "8000")

    event_loop = asyncio.get_event_loop()
    #coro = event_loop.create_server(YampServer, IP, PORT)
    coro = event_loop.create_server(STOMP_Server, IP, PORT)
    server = event_loop.run_until_complete(coro)

    print("Server started on {}:{}".format(IP, PORT))

    try:
        event_loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    event_loop.run_until_complete(server.wait_closed())
    event_loop.close()
