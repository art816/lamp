"""Config for lamp.py and app.py"""
#Lamp config
commands_dict = {bytes([0x12]): ('status', 'on'),
                 bytes([0x13]): ('status', 'off'),
                 bytes([0x20]): ('color', None)}

unpack_string = {'type': '!c',
                 'length': 'H',
                 'color': '!3s',
                 'rgb': '!BBB'}

#App config
tcp_host = '127.0.0.1'
tcp_port = '9999'
http_port = '8888'
default_length_data_tcp = 3
