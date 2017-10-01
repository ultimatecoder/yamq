from bidict import bidict

from yamq import stomp


class Observer:

    def __init__(self, callback, loop):
        self.loop = loop
        self.callback = callback

    async def update(self, subject, message):
        self.loop.call_soon(self.callback, subject, message)


class ObserverSTOMP:

    def __init__(self, loop, transport):
        self.loop = loop
        self.transport = transport
        self.subscriptions = bidict()  # subscription_id: subject_obj

    def subscribe(self, subject, ack_type, subscription_id):
        import pdb; pdb.set_trace()  # XXX BREAKPOINT
        subject.subscribe(self, ack_type)
        self.subscriptions[subscription_id] = subject

    def unsubscribe(self, subscription_id):
        subject = self.subscriptions.get(subscription_id)
        subject.unsubscribe(self)

    def update_auto(self, message_frame):
        import pdb; pdb.set_trace()  # XXX BREAKPOINT
        self.transport(stomp.dumps(message_frame))

    def update_client(self, message_frame):
        pass

    def update_client_individual(self, mesasge_frame):
        pass

    def delete(self):
        for _, subject in self.subscriptions:
            subject.unsubscribe(self)

    def update(self, subject, message, ack):
        import pdb; pdb.set_trace()  # XXX BREAKPOINT
        subscrption_id = self.subscriptions.inv[subject]
        frame = stomp.MessageFrame(
            message=message,
            destination=subject.name,
            subscription_id=subscription_id,
            ack=ack
        )
        if ack == 'client-individual':
            self.update_client_inidividual(frame)
        elif ack == 'client':
            self.update_client(frame)
        else:
            self.update_auto(frame)
