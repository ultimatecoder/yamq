import asyncio
import os


import subject
import stomp
import observer


class STOMP_Server(asyncio.Protocol):

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        try:
            frame = stomp.loads(data)
        except ValueError as e:
            error_frame = Frame(
                command="ERROR",
                headers={
                    "message": "Invalid frame received"
                },
                body=e.message
            )
            self.transport.write(stomp.dumps(error_frame))
            self.transport.close()

    def connect(self):
        pass

    def send(self, destination, message, **headers):
        pass

    def subscribe(self, id, destination, ack="auto", **headers):
        pass

    def unsubscribe(self, id, **headers):
        pass

    def ack(self, id, **headers):
        pass

    def nack(self, id, **headers):
        pass

    def disconnect(self, receipt, **headers):
        pass


class YampServer(asyncio.Protocol):

    def connection_made(self, transport):
        print("Connection received")
        self.transport = transport

    def data_received(self, data):
        command = data.strip()
        print(command)
        if command == b'SUBSCRIBE':
            print("Subscribed called")
        elif command == b'UNSUBSCRIBE':
            print("Unsubscribed called")
        elif command == b"DISCONNECT":
            print("Disconnect called")
        else:
            print("Unknown command")

    def connection_lost(self, exc):
        print("Connection closed")


if __name__ == '__main__':
    IP = os.getenv("YAMP_SERVER", "127.0.0.1")
    PORT = os.getenv("YAMP_PORT", "8000")

    event_loop = asyncio.get_event_loop()
    coro = event_loop.create_server(YampServer, IP, PORT)
    server = event_loop.run_until_complete(coro)

    print("Server started on {}:{}".format(IP, PORT))

    try:
        event_loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    event_loop.run_until_complete(server.wait_closed())
    event_loop.close()
