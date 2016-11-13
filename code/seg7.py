#!/usr/bin/env python

##########################################################################################
# Import libraries
##########################################################################################
import time
import pigpio

##########################################################################################
# Class definitions
##########################################################################################
class Seg7:
    def __init__(self, pi_ref, i2c_bus_ID, i2c_address):
        # init
        self.pi = pi_ref
        self.flashSpeed = 0.2 # seconds

        # Open I2C com with Seg7
        attempts = 0
        while attempts < 10:
            try:
                self.seg7 = pi_ref.i2c_open(i2c_bus_ID, i2c_address)
                break
            except pigpio.error as e:
                print("Seg7: ERROR: failed to open com over I2C")
                attempts += 1
                if attempts == 9:
                    raise "Seg7: FATAL ERROR: failed to open com over I2C"

        # Set cursor position to leftmost digit (position 0)
        attempts = 0
        while attempts < 10:
            try:
                self.write([0x79]) # cursor control byte
                self.write([0x00]) # data byte specifying pos. 0
                break
            except pigpio.error as e:
                print("Seg7: ERROR: failed to init seg7")
            attempts += 1

    # @desc display a string of characters (max 4) on the seg7 w/ timing
    #       resolution of .2s
    # @notes Use of the timing/flashing feature of this function is blocking,
    #        and must therefore be used with caution. Any parent code, such as
    #        a state machine, will be suspended, pending the end of the timer
    # @param text The string of chararcters to display
    # @param flash True if this text should flash
    # @param timeout How long (in seconds) to display the text
    def display(self, text, flash, timeout):
        assert isinstance(text, str)
        timeout_count = 0
        enabled = True
        while timeout_count < timeout:
            # write "HELO" if display enabled
            if (enabled):
                try:
                    self.write(text)
                    print("Seg7: Displaying '" + str(text) + "'")
                except pigpio.error as e:
                    print("Seg7: ERROR: failed to write " + str(text) + " seg7 over I2C")

            # else clear the display
            else:
                try:
                    self.write([0x76])
                    print("Seg7: <flashed off>")
                except pigpio.error as e:
                    print("Seg7: ERROR: failed to write to seg7 over I2C")

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

    def test(self):
        self.display("HELO", True, 1.2) # flash alt. 6 times (aka 1.2/.2 = 6)

    def __exit__(self, exc_type, exc, traceback):
        print("Seg7: Exiting, cleaning up")
        self.pi.i2c_close(self.seg7)
