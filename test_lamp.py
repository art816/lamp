"""Unittest for lamp and parser_bytes."""

import unittest
import json

from lamp import Lamp
from parser_bytes import Parser


class TestLamp(unittest.TestCase):
    """Test class Lamp."""

    @classmethod
    def setUpClass(cls):
        cls.lamp = Lamp()

    def test_init_lamp(self):
        """Init Lamp."""
        self.assertEqual(self. lamp.status, 'off')
        self.assertEqual(self.lamp.color, '#ffffff')

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

    def test_json(self):
        """Get json"""
        test_lamp = Lamp()
        self.assertEqual(
            json.loads(test_lamp.get_json()),
            json.loads('{"status": "off", "color": "#000000"}'))

    def test_change_status_color(self):
        """Test change status and color"""

        test_commands = [('on', ''), ('off', ''), ('change_color', '#01ff02')]
        answer = [('on', '#ffffff'),
                  ('off', '#ffffff'),
                  ('off', '#01ff02')]
        test_lamp = Lamp()
        for message_number in range(len(test_commands)):
            command, arg = test_commands[message_number]
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

    def test_parser_code(self):
        """Parsing byte code."""

        test_messages = [b'\x12\x00\x00',
                         b'\x13\x00\x00',
                         b'\x20\x00\x03\x01\xff\x02']
        for message_number in range(len(test_messages)):
            next_length = self.lamp.parser_code(
                test_messages[message_number][:3])
            if next_length and self.lamp.get_value:
                print('IF', next_length)
                next_length = self.lamp.parser_code(
                    test_messages[message_number][3:3 + next_length])
                self.assertEqual(self.lamp.color, '#01ff02')
                self.assertEqual(self.lamp.status, 'off')


class TestParser(unittest.TestCase):
    """Test parser tcp messsges"""

    def test_pars_code(self):
        """Parsing  code."""
        test_messages = [b'\x12\x00\x00',
                         b'\x13\x00\x00',
                         b'\x20\x00\x03\x01\xff\x02']
        answer = [(b'\x12', 0,),
                  (b'\x13', 0,),
                  (b'\x20', 3, b'\x01\xff\x02')]
        for message_number in range(len(test_messages)):
            parser = Parser()
            parsed_code = parser.pars_type_length(
                test_messages[message_number][:3])
            print('code=', parsed_code, len(parsed_code))
            if parsed_code[1]:
                value = parser.pars_value(
                    test_messages[message_number][3:3+parsed_code[1]],
                    parsed_code[1])
                parsed_code = list(parsed_code)
                parsed_code.append(value)
                parsed_code = tuple(parsed_code)
            print(parsed_code)
            self.assertEqual(parsed_code, answer[message_number])

    def test_value_to_name(self):
        """Get correct name."""
        test_messages = [b'\x12\x00\x00',
                         b'\x13\x00\x00',
                         b'\x20\x00\x03\x01\xff\x02']
        answer = [('on', ''), ('off', ''), ('change_color', '#01ff02')]
        for message_number in range(len(test_messages)):
            parser = Parser()
            parsed_code = parser.pars_type_length(
                test_messages[message_number][:3])
            if parsed_code[1]:
                value = parser.pars_value(
                    test_messages[message_number][3:3+parsed_code[1]],
                    parsed_code[1])
                parsed_code = list(parsed_code)
                parsed_code.append(value)
                parsed_code = tuple(parsed_code)
            command, arg = parser.value_to_name(parsed_code)
            self.assertEqual((command, arg), answer[message_number])
