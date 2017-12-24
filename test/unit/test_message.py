# Copyright (C) 2017-2018 Jaysinh Shukla (jaysinhp@gmail.com)
# Please find copy of license at "LICENSE"
# at the root of the project.


from unittest import TestCase

from yamq import message


class TestMessage(TestCase):

    def test_message_creation(self):
        demo_message = message.Message("test message", "text/text")

        self.assertEqual(demo_message.message, "test message")
        self.assertEqual(demo_message.content_type, "text/text")
        self.assertTrue(hasattr(demo_message, "_id"))
        self.assertTrue(isinstance(demo_message._id, int))
        self.assertIn(demo_message._id, message.Message._messages)

    def test_message_is_deleted(self):
        demo_message = message.Message("test message", "text/text")

        self.assertIn(demo_message._id, message.Message._messages)

        demo_id = demo_message._id
        demo_message.delete()

        with self.assertRaises(KeyError):
            message.Message._messages[demo_id]

    def test_message_get(self):
        demo_message = message.Message("test message", "text/text")

        founded_demo_message = message.Message.get(demo_message._id)

        self.assertIs(demo_message, founded_demo_message)
