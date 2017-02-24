import struct


class Parser(object):
    """Parser masseges tcp."""
    
    command_dict = {bytes([0x12]): 'on',
                    bytes([0x13]): 'off',
                    bytes([0x20]): 'change_color'}
    parse_value = False
    parsed_type = b''
    length = 0
    value = ''

    def pars_type_length(self, code):
        """Pars bytes code"""
        if type(code) == bytes and len(code) == 3:
            length = struct.unpack('!H', code[1:3])[0]
            parsed_type = struct.unpack('!c', code[0:1])[0]
            return parsed_type, length
    
    def pars_value(self, code, length):
        """Pars bytes code"""
        
        if type(code) == bytes and len(code) == length:
            value = struct.unpack('!{}s'.format(length), code)[0]
            return value
        else:
            return b''

    def value_to_name(self, parsed_code):
        """Code to command."""
        command = self.command_dict.get(parsed_code[0])
        arg = ''
        if command == 'change_color' and parsed_code[1] == 3:
            arg = '#{:02x}{:02x}{:02x}'.format(
                *struct.unpack('!BBB', parsed_code[2])) 
        return command, arg


        

