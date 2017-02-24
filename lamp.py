import json

class Lamp(object):
    """Lamp"""

    def __init__(self):
        """Init status=off color = #000000"""
        
        self.status = 'off'
        self.color = '#000000'

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
                           'color': self.color})

    def parser_code(self, code):
        """ """
        if self._get_value:
            self._pars_value(code)
            return 0
        else:
            return self._pars_type_length(code)

    def _parsed_type_length(self, code):
        """Pars bytes code"""
        if type(code) == bytes:
            length = struct.unpack('!H', code[1:3])[0]
            parsed_type = struct.unpack('!c', code[0:1])[0]
            self.command, arg = self.command_dict.get(parsed_type)
            if self.command and arg:
                setattr(self, self.command, arg)
            if length:
                self._get_value = True
            #TODO: if length == 0 return 3 (get new type, length)
            else:
                length = 3
            return length
    
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

