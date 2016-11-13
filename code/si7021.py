#!/usr/bin/env python

# TODO: reduce (and test) the read latency, .1s is a crazy amount of time to wait

#######################################################################
# Import libraries
#######################################################################
import time
import pigpio

#######################################################################
# Class definitions
#######################################################################
class Si7021:
    def __init__(self, pi_ref, i2c_bus_ID, i2c_address):
        # init vars and the I2C comm
        self.degree_sign = u'\N{DEGREE SIGN}' # unicode for the degree symbol
        self.pi = pi_ref

        # Open I2C com with si7021
        attempts = 0
        while attempts < 10:
            try:
                self.si7021 = pi_ref.i2c_open(i2c_bus_ID, i2c_address)
                break
            except pigpio.error as e:
                print("Si7021: ERROR: failed to open com over I2C")
                attempts += 1
                if attempts == 9:
                    raise "Si7021: FATAL ERROR: failed to open com over I2C"

        self.rh_i2c_addr = 0xf5
        self.t_i2c_addr = 0xf3

    def readRelativeHumidity(self):
        # Request rel. humidity w/ command: `Measure Relative Humidity, No Hold Master Mode`
        self.pi.i2c_write_device(self.si7021, [self.rh_i2c_addr])
        time.sleep(0.1) # wait to ensure proper delay

        # Read the word written back by the si7021; returns (numBytesRead, [msByte, lsByte])
        numBytesRead, word = self.pi.i2c_read_device(self.si7021, 3)

        # Format the word's rel. hum. payload
        rh_code = (word[0] << 8) + word[1]

        # Convert the payload to relative (%) humidity (pg. 21 of si7021 datasheet)
        return ((125.0 * rh_code) / 65536.0) - 6.0

    def readTemperature(self):
        # Request temperature w/ command: `Measure Temperature, No Hold Master Mode`
        self.pi.i2c_write_device(self.si7021, [self.t_i2c_addr])
        time.sleep(0.1) # wait to ensure proper delay

        # Read the word written back by the si7021; returns (numBytesRead, [msByte, lsByte])
        numBytesRead, word = self.pi.i2c_read_device(self.si7021, 3)

        # Format the word's temperature payload
        t_code = (word[0] << 8) + word[1]

        # Convert the payload to temperature in Celcuis (pg. 22 of si7021 datasheet)
        return ((175.72 * t_code) / (65536.0)) - 46.85

    def test(self):
        ticks = 0
        numTicks = 3
        # iterate `numTicks` times
        while ticks < numTicks:
            # read humidity
            rh_value = self.readRelativeHumidity()
            # read temperature
            t_value = self.readTemperature()
            # print stats
            print ("Si7021: Humidity: {:.2f}%, Temperature: {:.2f}" + self.degree_sign + "C").format(rh_value, t_value)
            # wait until next iteration
            time.sleep(1)
            # inc ticks
            ticks += 1


    def __exit__(self, exc_type, exc, traceback):
        print("Si7021: Exiting, cleaning up")
        self.pi.i2c_close(self.si7021)
