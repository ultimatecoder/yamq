import unittest
from unittest import mock

from yamq import subject, observer


class TestSubjectSTOMP(unittest.TestCase):

    def setUp(self):
        self.loop = unittest.mock.Mock()
        self.transport = unittest.mock.Mock()

    def test_object_creation(self):
        obj_1 = subject.SubjectSTOMP(name="test_queue_1", loop=self.loop)

        self.assertDictEqual(obj_1.observers, {})
        obj_1.delete()

    def test_subjects_are_unique(self):
        self.assertDictEqual(subject.SubjectSTOMP._objects, {})

        obj_1 = subject.SubjectSTOMP(name="test_queue_1", loop=self.loop)

        self.assertDictEqual(subject.SubjectSTOMP._objects, {obj_1.name: obj_1})

        obj_2 = subject.SubjectSTOMP(name="test_queue_2", loop=self.loop)

        self.assertDictEqual(subject.SubjectSTOMP._objects, {
            obj_1.name: obj_1,
            obj_2.name: obj_2
        })

        obj_3 = subject.SubjectSTOMP(name=obj_1.name, loop=self.loop)

        self.assertIs(obj_3, obj_1)
        self.assertDictEqual(subject.SubjectSTOMP._objects, {
            obj_1.name: obj_1,
            obj_2.name: obj_2
        })

        obj_1.delete()
        obj_2.delete()
        obj_3.delete()

    def test_subscribers_are_preserved(self):
        observer_1 = observer.ObserverSTOMP(self.loop, self.transport)
        observer_2 = observer.ObserverSTOMP(self.loop, self.transport)

        obj_1 = subject.SubjectSTOMP(name="test_queue_1", loop=self.loop)
        obj_1.subscribe(observer_1)
        obj_1.subscribe(observer_2)

        self.assertDictEqual(obj_1.observers, {
            observer_1: "auto",
            observer_2: "auto"
        })

        obj_2 = subject.SubjectSTOMP(name="test_queue_2", loop=self.loop)
        obj_2.subscribe(observer_1)

        self.assertDictEqual(obj_2.observers, {observer_1: "auto"})

        import pdb; pdb.set_trace()  # XXX BREAKPOINT
        obj_3 = subject.SubjectSTOMP(name="test_queue_1", loop=self.loop)
        self.assertDictEqual(obj_3.observers, {
            observer_1: "auto",
            observer_2: "auto"
        })
