import argparse
import asyncio
import logging
import os
from functools import partial

import subject
import stomp
import observer
import message


class STOMP_Server(asyncio.Protocol):
    """Minimum supported version 1.2"""

    def connection_made(self, transport):
        self.transport = transport
        self.observer = observer.Observer(event_loop, self.transport)
        self.messages_buffer = asyncio.Queue()
        self.message_service_task = event_loop.create_task(
            self.message_processing_service()
        )

    def _close_connection(self, error_frame):
        response = stomp.dumps(error_frame)
        self.transport.write(response.encode("utf-8"))
        self.message_service_task.cancel()
        self.transport.close()

    def data_received(self, data):
        try:
            frame = stomp.loads(data.decode('utf-8'))
            print("Frame received for command: {}".format(frame.command))
            self.messages_buffer.put_nowait(frame)

        except ValueError as e:
            self._close_connection(
                stomp.Frame("Invalid frame received", str(e))
            )

    async def message_processing_service(self):
        print("Starting message_processing service")
        while True:
            frame = await self.messages_buffer.get()
            try:
                if frame.command == 'SUBSCRIBE':
                    await self.subscribe(
                        frame.headers['id'], frame.headers['destination'],
                        frame.headers['ack']
                    )
                elif frame.command in ["STOMP", "CONNECTED"]:
                    await self.stomp(
                        frame.headers["accept-version"],
                        frame.headers.get("host")
                    )
                elif frame.command == "SEND":
                    await self.send(frame.headers['destination'], frame.body)
                elif frame.command == "ACK":
                    message_id = int(
                        frame.headers.get('id') or frame.headers.get('message-id')
                    )
                    subscription_id = frame.headers.get('subscription')
                    print("Ack received for frame: {}".format(message_id))
                    await self.ack(message_id, subscription_id)
                elif frame.command == "UNSUBSCRIBE":
                    await self.unsubscribe(frame.headers['id'])
                elif frame.command == "DISCONNECT":
                    await self.disconnect(frame.headers['receipt'])
                else:
                    error_message = (
                        "Invalid command received or supported command"
                    )
                    self._close_connection(frame.ErrorFrame(error_message))

            except KeyError as e:
                self._close_connection(
                    stomp.ErrorFrame("Required header value is missing", str(e))
                )

    async def stomp(self, accepted_version, host=None):
        response = stomp.dumps(stomp.ConnectedFrame())
        self.transport.write(response.encode("utf-8"))

    async def connect(self):
        pass

    async def send(self, destination, raw_message, **headers):
        user_subject = subject.Subject(name=destination, loop=event_loop)
        message_obj = message.Message(raw_message)
        notify_func = partial(user_subject.notify, message_obj)
        event_loop.call_soon(notify_func)

    async def subscribe(self, subscription_id, destination, ack="auto", **headers):
        user_subject = subject.Subject(destination, loop=event_loop)
        subscriber_function = partial(
            self.observer.subscribe, user_subject, ack, subscription_id
        )
        event_loop.call_soon(subscriber_function)

    async def unsubscribe(self, subscription_id, **headers):
        unsubscribe_func = partial(self.observer.unsubscribe, subscription_id)
        event_loop.call_soon(unsubscribe_func)

    async def ack(self, message_id, subscription_id, **headers):
        await self.observer.message_received(message_id)

    async def nack(self, message_id, **headers):
        pass

    async def disconnect(self, receipt_id, **headers):
        event_loop.call_soon(self.observer.delete)
        recept_frame = stomp.ReceiptFrame(receipt_id)
        reply = stomp.dumps(recept_frame)
        self.transport.write(reply.encode('utf-8'))
        self.message_service_task.cancel()
        self.transport.close()

    def connection_lost(self, exc):
        event_loop.call_soon(self.observer.delete)
        self.message_service_task.cancel()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d", "--host",
        type=str,
        nargs="?",
        default="localhost",
        help="Host name on which the server will bind to."
    )
    parser.add_argument(
        "-p", "--port",
        type=int,
        nargs='?',
        default=8000,
        help=(
            "Port number on which the server will listen for incoming requests."
        )
    )
    parser.add_argument(
        "-l", "--log",
        type=str,
        nargs='?',
        default="DEBUG",
        choices= ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET"],
        help="Decide the level of log the application should throw."
    )
    args = parser.parse_args()
    event_loop = asyncio.get_event_loop()
    coro = event_loop.create_server(STOMP_Server, args.host, args.port)
    server = event_loop.run_until_complete(coro)

    logging.info("Server started on {}:{}".format(args.host, args.port))

    try:
        event_loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    event_loop.run_until_complete(server.wait_closed())
    event_loop.close()
