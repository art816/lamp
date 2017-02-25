#Lamp config
commands_dict = {bytes([0x12]): ('status', 'on'),
                 bytes([0x13]): ('status', 'off'),
                 bytes([0x20]): ('color', None)}

unpack_string = {'type': '!c',
                 'length': '!H',
                 'color': '!3s',
                 'rgb': '!BBB'}
