import json
import struct

class Lamp(object):
    """Lamp"""

    def __init__(self):
        """Init status=off color = #000000"""
        
        self.status = 'off'
        self.color = '#ffffff'

        self.commands_dict = {
            bytes([0x12]): ('status', 'on'),
            bytes([0x13]): ('status', 'off'),
            bytes([0x20]): ('color', None)}
        
        self.command = None
        self._get_value = False
        self._length = 0

    def on(self):
        self.status = 'on'

    def off(self):
        self.status = 'off'

    def change_color(self, color):
        self.color = color

    def _get_json(self):
        return json.dumps({'status': self.status,
                           'color': '#000000' if self.status == 'off' else self.color})

    def parser_code(self, code):
        """ """
        if self._get_value:
            self._pars_value(code)
            return 0
        else:
            return self._pars_type_length(code)

    def _pars_type_length(self, code):
        """Pars bytes code"""
        next_length = 3
        if type(code) == bytes and len(code) == 3:
            length = struct.unpack('!H', code[1:3])[0]
            parsed_type = struct.unpack('!c', code[0:1])[0]
            command_arg = self.commands_dict.get(parsed_type)
            if command_arg:
                self.command = command_arg[0]
                arg = command_arg[1]
                if self.command and arg:
                    setattr(self, self.command, arg)
            if length:
                next_length = length
                self._get_value = True
            #TODO: if length == 0 return 3 (get new type, length)
        return next_length
    
    def _pars_value(self, code):
        """Pars bytes code"""
        arg = None
        if self.command:    
            if self.command == 'color' and type(code) == bytes and\
                    len(code) == 3:
                value = struct.unpack('!3s', code)[0]
                arg = '#{:02x}{:02x}{:02x}'.format(
                    *struct.unpack('!BBB', value))
            if self.command and arg:
                setattr(self, self.command, arg)    
        self._get_value = False

