""" Lamp.
    Parsing bytes code and change status, color by commands.
    Commands in config.
"""

import json
import struct

import config as cfg


class Lamp(object):
    """Lamp"""
    def __init__(self):
        """Init status=off color = #000000"""
        self.status = 'off'
        self.color = '#ffffff'
        self.commands_dict = cfg.commands_dict
        self.command = None
        self._get_value = False

    def _get_json(self):
        """Return json string {status: value, color: value}."""
        return json.dumps(
            {'status': self.status,
             'color': '#000000' if self.status == 'off' else self.color})

    def parser_code(self, code):
        """Parsing bytes code."""
        #Check waiting value.
        if self._get_value:
            self._pars_value(code)
            return 0
        else:
            return self._pars_type_length(code)

    def _pars_type_length(self, code):
        """Get type and length from byte code.
           Set self.command if type in commands_dict.
           Return length next message. Default next_length = 3.
        """
        next_length = 3
        if type(code) == bytes and len(code) == 3:
            #Unpack length, 2 bytes unsigned int.
            length = struct.unpack(cfg.unpack_string['length'], code[1:3])[0]
            #Unpack type, 1 bytes char.
            parsed_type = struct.unpack(cfg.unpack_string['type'], code[0:1])[0]
            #Find type in commands_dict
            command_arg = self.commands_dict.get(parsed_type)
            if command_arg:
                self.command = command_arg[0]
                arg = command_arg[1]
                #If ard is, set command.
                if self.command and arg:
                    setattr(self, self.command, arg)
            if length:
                next_length = length
                #Key that we waiting value.
                self._get_value = True
        return next_length

    def _pars_value(self, code):
        """Get value from byte code.
           Set self.command if self.command and
           value have corect length.
        """
        arg = None
        if self.command:
            if self.command == 'color' and type(code) == bytes and\
                    len(code) == 3:
                #Unpack value, 3 bytes str and format to rgb (#******).
                value = struct.unpack(cfg.unpack_string['color'], code)[0]
                arg = '#{:02x}{:02x}{:02x}'.format(
                    *struct.unpack(cfg.unpack_string['rgb'], value))
            if arg:
                setattr(self, self.command, arg)
        self._get_value = False

