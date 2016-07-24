#!/usr/bin/env python

# Note: going to import pigpio in main, then pass it to the
#       constructors of a seg7 and si7021 class

##########################################################################################
# Import libraries
##########################################################################################
import time

##########################################################################################
# Class definitions
##########################################################################################
class Seg7:
    def __init__(self, pi_ref, i2c_bus_ID, i2c_address):
        # init
        self.pi = pi_ref
        self.seg7 = pi_ref.i2c_open(i2c_bus_ID, i2c_address)
        self.flashSpeed = 0.2 # seconds

        # Set cursor position to leftmost digit (position 0)
        self.write([0x79]) # cursor control byte
        self.write([0x00]) # data byte specifying pos. 0

    # @desc display a string of characters (max 4) on the seg7
    # @param text The string of chararcters to display
    # @param flash True if this text should flash
    # @param timeout How long (in seconds) to display the text
    def display(self, text, flash, timeout):
        assert isinstance(text, str)
        print("Displaying " + text)
        timeout_count = 0
        enabled = True
        while timeout_count < timeout:
            # write "HELO" if display enabled
            if (enabled):
                try:
                    self.write("HELO")
                    print("Hello")
                except pigpio.error as e:
                    print("ERROR: failed to write to seg7 over I2C")

            # else clear the display
            else:
                try:
                    self.write([0x76])
                    print("Goodbye")
                except pigpio.error as e:
                    print("ERROR: failed to write to seg7 over I2C")

            # toggle enabled if flash==True
            if flash:
                enabled = not enabled

            # delay, and exit if timed out
            time.sleep(self.flashSpeed)
            timeout_count += self.flashSpeed

    # @desc writes a string of characters directly to the display
    def write(self, text):
        for char in text:
            self.pi.i2c_write_device(self.seg7, [char])

    def __exit__(self):
        self.pi.i2c_close(self.seg7)
