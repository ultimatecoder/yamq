import asyncio
from unittest import TestCase, mock

from yamq import subject
from yamq import observer


class AsyncCallback:

    def __init__(self):
        self.called = 0
        self.last_args = ()
        self.last_kwargs = {}

    def method(self, *args, **kwargs):
        self.called += 1
        self.last_args = args
        self.last_kwargs = kwargs


class TestSubject(TestCase):

    def setUp(self):
        self.loop = asyncio.get_event_loop()

    def _assert_callbacks(self, callback, called, *args, **kwargs):
        self.assertEqual(callback.called, called)
        self.assertEqual(callback.last_args, args)
        self.assertEqual(callback.last_kwargs, kwargs)

    def test_notify(self):
        subject_1 = subject.Subject("subject_1", self.loop)

        callback_1 = AsyncCallback()
        callback_2 = AsyncCallback()

        observer_1 = observer.Observer(callback_1.method, self.loop)
        observer_2 = observer.Observer(callback_2.method, self.loop)

        subject_1.subscribe(observer_1)
        subject_1.subscribe(observer_2)

        message = "test message"
        self.loop.run_until_complete(subject_1.notify(message))

        self._assert_callbacks(callback_1, 1, subject_1.name, message)
        self._assert_callbacks(callback_2, 1, subject_1.name, message)

    def test_observer_only_called_once(self):
        subject_1 = subject.Subject("Subject_1", self.loop)

        callback_1 = AsyncCallback()

        observer_1 = observer.Observer(callback_1.method, self.loop)

        subject_1.subscribe(observer_1)
        subject_1.subscribe(observer_1)

        message = "test message"
        self.loop.run_until_complete(subject_1.notify(message))
        self._assert_callbacks(callback_1, 1, subject_1.name, message)

    def test_observer_can_subscribe_to_multiple_subject(self):
        subject_1 = subject.Subject("subject_1", self.loop)
        subject_2 = subject.Subject("subject_2", self.loop)

        callback_1 = AsyncCallback()
        observer_1 = observer.Observer(callback_1.method, self.loop)

        subject_1.subscribe(observer_1)
        subject_2.subscribe(observer_1)

        message = "test message subject1"
        self.loop.run_until_complete(subject_1.notify(message))
        self._assert_callbacks(callback_1, 1, subject_1.name, message)

        message = "test message subject2"
        self.loop.run_until_complete(subject_2.notify(message))
        self._assert_callbacks(callback_1, 2, subject_2.name, message)

    def test_observer_can_unsubscribe(self):
        subject_1 = subject.Subject("subject_1", self.loop)

        callback_1 = AsyncCallback()
        observer_1 = observer.Observer(callback_1.method, self.loop)

        subject_1.subscribe(observer_1)
        subject_1.unsubscribe(observer_1)

        message = "test message subject1"
        self.loop.run_until_complete(subject_1.notify(message))
        self._assert_callbacks(callback_1, 0)

    def test_subject_has_empty_observer(self):
        subject_1 = subject.Subject("subject_1", self.loop)
        self.assertSetEqual(subject_1.observers, set())
