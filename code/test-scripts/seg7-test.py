#!/usr/bin/env python

##########################################################################################
# Import libraries
##########################################################################################
import time
import pigpio


##########################################################################################
# Perform initializations
##########################################################################################
i2c_bus_ID = 1
i2c_address = 0x71
enabled = True
delay = 0.2

# instantiate the local RPi's GPIO
pi = pigpio.pi()
# humidity and temperature sensor - I2C interface detailed on pg. 18 of si7021 datasheet
seg7 = pi.i2c_open(i2c_bus_ID, i2c_address)


##########################################################################################
# Main logic
##########################################################################################

# Set cursor position to leftmost digit (position 0)
pi.i2c_write_device(seg7, [0x79]) # cursor control byte
pi.i2c_write_device(seg7, [0x00]) # data byte specifying pos. 0

while True:
    # write "helo" if display enabled
    if (enabled):
        try:
            pi.i2c_write_device(seg7, ['H'])
            pi.i2c_write_device(seg7, ['E'])
            pi.i2c_write_device(seg7, ['L'])
            pi.i2c_write_device(seg7, ['O'])
            print("Hello")
        except pigpio.error as e:
            print("ERROR: failed to write to seg7 over I2C")

    # else clear the display
    else:
        try:
            pi.i2c_write_device(seg7, [0x76])
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
