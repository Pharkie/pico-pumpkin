import machine
from micropython import const

class max7219_matrix:
    _NOOP = const(0)
    _DIGIT0 = const(1)
    _DECODEMODE = const(9)
    _INTENSITY = const(10)
    _SCANLIMIT = const(11)
    _SHUTDOWN = const(12)
    _DISPLAYTEST = const(15)

    def __init__(self, spi, cs):
        self.spi = spi
        self.cs = cs
        self.setup()
        self.left_char = [0x3c,0x56,0x93,0xdb,0xff,0xff,0xdd,0x89]
        self.right_char = [0x3c,0x56,0x93,0xdb,0xff,0xff,0xdd,0x89]
        self.left_brightness = 1 # 0-15, 1 is dim but 5 seems to be the same as 15
        self.right_brightness = 1 # 0-15, 1 is dim but 5 seems to be the same as 15
        
    def setup(self):
        self.write(_SHUTDOWN, 0) # Does not work with self._SHUTDOWN or max7219_matrix._SHUTDOWN
        self.write(_DISPLAYTEST, 0)
        self.write(_SCANLIMIT, 7)
        self.write(_DECODEMODE, 0)
        self.write(_SHUTDOWN, 1)

    def write(self, command, data):
        self.cs.value(0)
        self.spi.write(bytearray([command, data]))
        self.spi.write(bytearray([command, data]))
        self.cs.value(1)

    def show_char(self, cl, cr):
        for i in range(8):
            self.cs.value(0)
            self.spi.write(bytearray([i+1, cr[i]]))
            self.spi.write(bytearray([i+1, cl[i]]))
            self.cs.value(1)
            
    def set_brightness(self, brightness):
        self.write(_INTENSITY, brightness)
                
