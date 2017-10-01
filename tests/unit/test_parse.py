from unittest import TestCase

from yamq import stomp


class TestParse(TestCase):

    def setUp(self):
        self.frame = stomp.Frame(
            command="SUBSCRIBE",
            headers={
                "destination": "/queue/foo",
                "ack": "client"
            }
        )

    def test_dumps_okay(self):
        response = stomp.dumps(self.frame)
        expected_response = (
            'SUBSCRIBE\r\n',
            'ack:client\r\n',
            'destination:/queue/foo\r\n',
            '\r\n',
            '\r\n',
            '\x00',
        )
        for line in expected_response:
            self.assertIn(line, response)

    def test_dump_error(self):
        with self.assertRaises(ValueError):
            stomp.dumps("invalid")

    def test_loads_okay(self):
        responses = [
            (
                'SUBSCRIBE\r\n'
                'ack:client\r\n'
                'destination:/queue/foo\r\n'
                '\r\n'
                '\r\n'
                '\x00'
            ),
            (
                'SEND\n'
                'content-length:11\n'
                'destination:/queue/test\n'
                '\n'
                'hello world'
                '\x00'
            )
        ]
        for response in responses:
            self.assertIs(type(stomp.loads(response)), stomp.Frame)

    def test_loads_error(self):
        response = (
            'SUBSCRIBE\r\n'
            'ackclient\r\n'
            '\x00'
        )
        with self.assertRaises(ValueError):
            stomp.loads(response)
