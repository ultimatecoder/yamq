from unittest import TestCase

from yamq import utils

class DemoAutoID(utils.AutoID):
    pass


class TestAutoID(TestCase):

    def test_auto_id_works_okay(self):
        """Combined tests in one method.

        AutoID increments the id according to number of objects created. There
        is no guarentee that the tests will perform in certain order. It might
        be diffecult assert with pre-fixed ID number. A quick work around is
        to test everything in one method so that you have grip over the expected
        ID number.
        """


        demo_obj = DemoAutoID()
        self.assertTrue(hasattr(demo_obj, '_id'))
        self.assertTrue(isinstance(demo_obj._id, int))
        self.assertEqual(demo_obj._id, 0)

        another_obj = DemoAutoID()
        self.assertEqual(another_obj._id, 1)

        del another_obj

        yet_another_obj = DemoAutoID()
        self.assertEqual(yet_another_obj._id, 2)
