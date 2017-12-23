# Copyright (C) 2017-2018 Jaysinh Shukla
# Please find copy of license at "LICENSE"
# at the root of the project.


import unittest
from unittest import mock

from yamq import subject, observer, message


class TestSubject(unittest.TestCase):

    def setUp(self):
        self.loop = unittest.mock.Mock()
        self.transport = unittest.mock.Mock()

    def test_object_creation(self):
        obj_1 = subject.Subject(name="test_queue_1", loop=self.loop)

        self.assertDictEqual(obj_1.observers, {})
        obj_1.delete()

    def test_subjects_are_unique(self):
        self.assertDictEqual(subject.Subject._objects, {})

        obj_1 = subject.Subject(name="test_queue_1", loop=self.loop)

        self.assertDictEqual(subject.Subject._objects, {obj_1.name: obj_1})

        obj_2 = subject.Subject(name="test_queue_2", loop=self.loop)

        self.assertDictEqual(subject.Subject._objects, {
            obj_1.name: obj_1,
            obj_2.name: obj_2
        })

        obj_3 = subject.Subject(name=obj_1.name, loop=self.loop)

        self.assertIs(obj_3, obj_1)
        self.assertDictEqual(subject.Subject._objects, {
            obj_1.name: obj_1,
            obj_2.name: obj_2
        })

        obj_1.delete()
        obj_2.delete()
        obj_3.delete()

    def test_subscribers_are_preserved(self):
        observer_1 = observer.Observer(self.loop, self.transport)
        observer_2 = observer.Observer(self.loop, self.transport)

        obj_1 = subject.Subject(name="test_queue_1", loop=self.loop)
        obj_1.subscribe(observer_1)
        obj_1.subscribe(observer_2)

        self.assertDictEqual(obj_1.observers, {
            observer_1: "auto",
            observer_2: "auto"
        })

        obj_2 = subject.Subject(name="test_queue_2", loop=self.loop)
        obj_2.subscribe(observer_1)

        self.assertDictEqual(obj_2.observers, {observer_1: "auto"})

        obj_3 = subject.Subject(name="test_queue_1", loop=self.loop)
        self.assertDictEqual(obj_3.observers, {
            observer_1: "auto",
            observer_2: "auto"
        })

        obj_1.delete()
        obj_2.delete()
        obj_3.delete()

    def test_get(self):
        obj_1 = subject.Subject(name="test_queue_1", loop=self.loop)
        returned_obj = subject.Subject.get(obj_1.name)
        self.assertIs(obj_1, returned_obj)

        returned_obj = subject.Subject.get("test_queue_2")
        self.assertIsNone(returned_obj)

        obj_1.delete()

    def test_delete(self):
        obj_1 = subject.Subject(name="test_queue_1", loop=self.loop)
        returned_obj = subject.Subject.get("test_queue_1")

        self.assertIs(obj_1, returned_obj)

        obj_1.delete()
        returned_obj = subject.Subject.get("test_queue_1")

        self.assertIsNone(returned_obj)

    def test_unsubscribe(self):
        obj_1 = subject.Subject(name="test_queue_1", loop=self.loop)

        observer_1 = observer.Observer(self.loop, self.transport)
        observer_2 = observer.Observer(self.loop, self.transport)

        obj_1.subscribe(observer_1, "auto")
        obj_1.subscribe(observer_2, "auto")

        self.assertDictEqual(obj_1.observers, {
            observer_1: "auto",
            observer_2: "auto"
        })

        obj_1.unsubscribe(observer_1)

        self.assertDictEqual(obj_1.observers, {observer_2: "auto"})

        obj_1.unsubscribe(observer_2)
        self.assertDictEqual(obj_1.observers, {})

        # It must call the subject_obj.delete() if there are no observers.
        self.assertIsNone(subject.Subject.get('test_queue_1'))
        obj_1.delete()

    def test_z_notify(self):
        obj_1 = subject.Subject(name="test_queue_1", loop=self.loop)

        observer_1 = observer.Observer(self.loop, self.transport)
        observer_2 = observer.Observer(self.loop, self.transport)

        message_obj = message.Message("Test Message")

        observer_1.subscribe(obj_1, "auto", "1")
        observer_2.subscribe(obj_1, "auto", "2")

        obj_1.notify(message_obj)

        obj_1.delete()
