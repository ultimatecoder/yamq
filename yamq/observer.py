import asyncio

from bidict import bidict

import stomp


class Observer:

    def __init__(self, loop, transport):
        self.loop = loop
        self.transport = transport
        self.subscriptions = bidict()  # subscription_id: subject_obj
        self.messages_buffer = asyncio.Queue()
        self.pending_ack = {}  # message_id: message_frmae
        self.last_message = None
        self.message_sending_service = self.loop.create_task(
            self.message_sender()
        )

    def subscribe(self, subject, ack_type, subscription_id):
        subject.subscribe(self, ack_type)
        self.subscriptions[subscription_id] = subject

    def unsubscribe(self, subscription_id):
        subject = self.subscriptions.get(subscription_id)
        subject.unsubscribe(self)

    async def update_auto(self, message_frame):
        response = stomp.dumps(message_frame)
        self.transport.write(response.encode('utf-8'))

    async def update_client(self, message_frame):
        pass

    async def update_client_individual(self, mesasge_frame):
        pass

    def delete(self):
        for _, subject in self.subscriptions.items():
            subject.unsubscribe(self)
        self.loop.call_soon(self.message_sending_service.cancel)

    async def message_received(self, message_id):
        if message_id == self.last_message.headers.get('message-id'):
            self.client_delivery_task.cancel()

    async def send_auto(self, message_frame):
        response = stomp.dumps(message_frame)
        self.transport.write(response.encode('utf-8'))

    async def send_client(self, message_frame):
        response = stomp.dumps(message_frame)
        response = response.encode('utf-8')
        for i in range(3):
            self.transport.write(response)
            await asyncio.sleep(20)

    async def message_sender(self):
        while True:
            message_frame = await self.messages_buffer.get()
            ack = message_frame.headers.get('ack')
            if ack == 'auto':
                await self.send_auto(message_frame)
                self.messages_buffer.task_done()
            elif ack == 'client':
                self.last_message = message_frame
                self.client_delivery_task = self.loop.create_task(
                    self.send_client(message_frame))
                try:
                    await self.client_delivery_task
                    # TODO: Print error message here that message is failed.
                    print("Message delivery failed. ID: {}, Message: {}".format(
                        self.last_message.headers['message-id'],
                        self.last_message.body
                    ))
                    self.last_message = None
                except asyncio.CancelledError as e:
                    # TODO: Make Log that message is delivered
                    pass
                self.messages_buffer.task_done()
            else:
                # TODO: Return error frame from here!
                pass

    def update(self, subject, message, ack):
        subscription_id = self.subscriptions.inv[subject]
        frame = stomp.MessageFrame(
            message=message,
            destination=subject.name,
            subscription_id=subscription_id,
            ack=ack
        )
        message.delete()
        self.messages_buffer.put_nowait(frame)
