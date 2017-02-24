import unittest


from .lamp import Lamp 
from .parser_bytes import Parser

class TestLamp(unittest.TestCase):
    """Test class Lamp."""

    @classmethod
    def setUpClass(cls):
        cls.lamp = Lamp()

    def test_init_lamp(self):
        """Init Lamp."""
        self.assertEqual(self. lamp.status, 'off')
        self.assertEqual(self.lamp.color, '#000000')

    def test_change_status(self):
        """Change status"""
        test_lamp = Lamp()
        test_lamp.status = 'on'
        self.assertEqual(test_lamp.status, 'on')

    def test_change_color(self):
        """Change status"""
        test_lamp = Lamp()
        test_lamp.color = '#ffffff'
        self.assertEqual(test_lamp.color, '#ffffff')

    def test_change_stay(self):
        """ """
        test_commands = [('on', ''), ('off', ''), ('change_color', '#01ff02')]
        answer = [('on', '#ffffff'),
                  ('off', '#000000'),
                  ('off', '#01ff02')]
        test_lamp = Lamp()
        for message_number in range(len(test_commands)):
            command, arg  = test_commands[message_number]
            if command not in dir(test_lamp):
                print('unknow command = ', command)
                continue

            method = getattr(test_lamp, command)
            if arg:
                method(arg)
            else:
                method()
            self.assertEqual(
                (test_lamp.status, test_lamp.color), answer[message_number])
         


class TestParser(unittest.TestCase):
    """Test parser tcp massege"""

    def test_pars_code(self):
        """ """
        test_masseges = [b'\x12\x00\x00',
                         b'\x13\x00\x00',
                         b'\x20\x00\x03\x01\xff\x02']
        answer = [(b'\x12', 0, b''),
                  (b'\x13', 0, b''),
                  (b'\x20', 3, b'\x01\xff\x02')]
        for message_number in range(len(test_masseges)):
            parser = Parser()
            parsed_code = parser.pars_code(test_masseges[message_number])
            self.assertEqual(parsed_code, answer[message_number])

    def test_value_to_name(self):
        """ """
        test_masseges = [b'\x12\x00\x00',
                         b'\x13\x00\x00',
                         b'\x20\x00\x03\x01\xff\x02']
        answer = [('on', ''), ('off', ''), ('change_color', '#01ff02')]
        for message_number in range(len(test_masseges)):
            parser = Parser()
            parsed_code = parser.pars_code(test_masseges[message_number])
            command, arg = parser.value_to_name(parsed_code)
            self.assertEqual((command, arg), answer[message_number])
