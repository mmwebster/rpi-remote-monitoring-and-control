#!/usr/bin/env python

#######################################################################
# Import libraries
#######################################################################
import time
import pigpio


#######################################################################
# Perform initializations
#######################################################################
i2c_bus_ID = 1
i2c_address = 0x71
enabled = True # boolean to control flashing
delay = 0.2 # period of alternating (1/2 total period)

# instantiate the local RPi's GPIO
pi = pigpio.pi()
# instantiate the seg7 I2C device
seg7 = pi.i2c_open(i2c_bus_ID, i2c_address)


#######################################################################
# Main logic
#######################################################################

# Set cursor position to leftmost digit (position 0)
pi.i2c_write_device(seg7, [0x79]) # cursor control byte
pi.i2c_write_device(seg7, [0x00]) # data byte specifying pos. 0

while True:
    # write "HELO" if is display enabled
    if (enabled):
        try: # I2C write can fail, this will catch the failure
            pi.i2c_write_device(seg7, ["H"])
            pi.i2c_write_device(seg7, ["E"])
            pi.i2c_write_device(seg7, ["L"])
            pi.i2c_write_device(seg7, ["O"])
            print("Hello")
        except pigpio.error as e:
            print("ERROR: failed to write to seg7 over I2C")

    # else clear the display
    else:
        try:
            pi.i2c_write_device(seg7, [0x76]) # reset byte
            print("Goodbye")
        except pigpio.error as e:
            print("ERROR: failed to write to seg7 over I2C")

    # toggle enabled
    enabled = not enabled

    # wait until next iteration
    time.sleep(delay)

# house keeping
pi.i2c_close(seg7)
pi.stop()
