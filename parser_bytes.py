import struct


class Parser(object):
    """Parser masseges tcp."""
    
    command_dict = {bytes([0x12]): 'on',
                    bytes([0x13]): 'off',
                    bytes([0x20]): 'change_color'}


    def pars_code(self, code):
        """Pars bytes code"""
        
        if type(code) == bytes and len(code) >= 3:
            length = struct.unpack('!h', code[1:3])[0]
            if length == 0 or length == 3:
                if len(code) == length + 3:
                    parsed_code = struct.unpack(
                        '!ch{}s'.format(length),
                        code)
                    return parsed_code

    def value_to_name(self, parsed_code):
        """Code to command."""
        command = self.command_dict.get(parsed_code[0])
        arg = ''
        if command == 'change_color':
            arg = '#{:02x}{:02x}{:02x}'.format(
                *struct.unpack('!BBB', parsed_code[2])) 
        return command, arg


        

