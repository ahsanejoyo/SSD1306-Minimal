# Based on the official MicroPython SSD1306 driver architecture, 
# optimized for minimal memory footprint.

import framebuf

# BUILT-IN MINIMAL SSD1306 DRIVER (I2C)
class SSD1306(framebuf.FrameBuffer):
    def __init__(self, width, height):

        # Variables
        self.width, self.height = width, height
        self.pages = self.height // 8 # Sections of screen are divided into 8 pixel tall "Pages", varies based on screen height
        self.buffer = bytearray(self.pages * self.width) # Buffer of size: pages*screen width (1 byte = 8 pixels)

        # Tuple w/ defined hex commands (change to const for further memory optimization?)
        config_cmds = (
            0xAE,        # Turn display off
            0x20, 0x00,  # Memory addressing mode set to horizontal
            0x40,        # Starting line
            0xA1,        # Segment re-map (Column 127 mapped to SEG0)
            0xA8, self.height - 1, # Set multiplex ratio
            0xC8,        # COM output scan direction
            0xD3, 0x00,  # Display offset
            0xDA, 0x02 if self.width > 2 * self.height else 0x12, # COM pins configuration
            0xD5, 0x80,  # Display clock divide ratio / oscillator frequency
            0xD9, 0xF1,  # Pre-charge Pperiod
            0xDB, 0x30,  # VCOMH deselect level
            0x81, 0xFF,  # Contrast control (Set to max brightness)
            0xA4,        # ENTIRE display ON (Resume from RAM)
            0xA6,        # Normal display (non-inverted) 
            0x8D, 0x14,  # Charge pump control (Enables charge pump)
            0xAF         # Display ON
        )

        # MP's framebuffer is initialized, framebuffer is set to Monochrome & Vertical Least Significant Bit
        super().__init__(self.buffer, self.width, self.height, framebuf.MONO_VLSB) 

        # For loop cycles iterates through tuple containing various hex & standard commands to configure OLED controller hardware
        for cmd in (config_cmds):
            self.write_cmd(cmd) # Current command is written directly to screen/display chip

    def show(self): # Function to take drawn pixels sitting in RAM and display them on screen
        self.write_cmd(0x21); self.write_cmd(0); self.write_cmd(self.width - 1)
        self.write_cmd(0x22); self.write_cmd(0); self.write_cmd(self.pages - 1)
        self.write_framebuf() # Sends byte array from RAM to display chip

class SSD1306_I2C(SSD1306): # Graphic capabilities from previous function are transferred here and specified to work w/ I2C

    def __init__(self, width, height, i2c, addr=0x3C):
        self.i2c, self.addr = i2c, addr
        super().__init__(width, height)

    def write_cmd(self, cmd): # Function to set configuration info to display chip
        self.i2c.writeto(self.addr, bytearray([0x00, cmd])) # 0x00 signifies control byte to diffrentiate from visual/pixel data

    def write_framebuf(self): # Bit block transfer of pixel data to screen 
        self.i2c.writeto(self.addr, b'\x40' + self.buffer) # 0x40 signifies following info is visual/pixel data
