

class Lamp(object):
    """Lamp"""

    def __init__(self):
        """Init status=off color = #000000"""
        
        self.status = 'off'
        self.color = '#000000'

    def on(self):
        self.status = 'on'
        self.color = '#ffffff'

    def off(self):
        self.status = 'off'
        self.color = '#000000'

    def change_color(self, color):
        self.color = color
