#!/usr/bin/env python
# -*- coding: utf-8 -*-

#######################################################################
# Import libraries
#######################################################################
import time
import pigpio


#######################################################################
# Perform initializations
#######################################################################
i2c_bus_ID = 1
i2c_address = 0x40
degree_sign= "deg" # unicode for the degree symbol

# instantiate the local RPi's GPIO
pi = pigpio.pi()
# humidity and temperature sensor - I2C interface detailed on pg. 18
# of si7021 datasheet
si7021 = pi.i2c_open(i2c_bus_ID, i2c_address) 


#######################################################################
# Main logic
#######################################################################
while True:

    # Request rel. humidity w/ command: `Measure Relative Humidity, No
    # Hold Master Mode`
    pi.i2c_write_device(si7021, [0xf5])
    time.sleep(0.1) # wait to ensure proper delay

    # Read the word written back by the si7021; returns (numBytesRead,
    # [msByte, lsByte])
    numBytesRead, word = pi.i2c_read_device(si7021, 3)

    # Format the word's rel. hum. payload
    rh_code = (word[0] << 8) + word[1]

    # Convert the payload to relative (%) humidity (pg. 21 of si7021
    # datasheet)
    rh_value = ((125.0 * rh_code) / 65536.0) - 6.0

    # -----------------------------------------------------------------

    # Request temperature w/ command: `Measure Temperature, No Hold
    # Master Mode`
    pi.i2c_write_device(si7021, [0xf3])
    time.sleep(0.1) # wait to ensure proper delay

    # Read the word written back by the si7021; returns (numBytesRead,
    # [msByte, lsByte])
    numBytesRead, word = pi.i2c_read_device(si7021, 3)

    # Format the word's temperature payload
    t_code = (word[0] << 8) + word[1]

    # Convert the payload to temperature in Celcuis (pg. 22 of si7021
    # datasheet)
    t_value = ((175.72 * t_code) / (65536.0)) - 46.85

    # -----------------------------------------------------------------

    # Print and delay before the next iteration
    print ("Humidity: {:.2f}%, Temperature: {:.2f}" + degree_sign
            + "C").format(rh_value, t_value)
    time.sleep(1)

# house keeping
pi.i2c_close(si7021)
pi.stop()
