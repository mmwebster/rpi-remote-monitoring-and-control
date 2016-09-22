#!/usr/bin/env python

#######################################################################
# Import libraries
#######################################################################
import time
import RPi.GPIO as GPIO

#######################################################################
# Class definitions
#######################################################################
class Servo:
    def __init__(self, initDegrees):
        GPIO.setmode(GPIO.BCM) # pin numbering scheme that uses GPIO numbers
        GPIO.setwarnings(False)
        GPIO.setup(25, GPIO.OUT) # set GPIO 25 as output
        self.servo = GPIO.PWM(25, 50) # instantiate PWM output to GPIO 25 @ 50Hz

        self.degree_sign= u'\N{DEGREE SIGN}' # unicode for the degree symbol
        self.dc_min = 2.1 # the min duty cycle corresponding to 210deg rotation
        self.dc_max = 12.3 # the max duty cycle corresponding to 0deg rotation
        self.deg_min = 0
        self.deg_max = 210

        # start at the provided rotation
        _initRotateTo(initDegrees)

    def _degreesToDutyCycle(self, degrees):
        # assert proper use
        assert isinstance(degrees, int)
        assert (self.deg_min <= degrees <= self.deg_max)
        # convert degrees to fraction out of 210
        rotation = degrees / 210
        # convert fraction to the duty cycle from that corresponding to 0deg
        # looks odd since max_dc corresponds to min degree position,
        # and vice-versa
        dc_from_max = ((self.dc_max - self.dc_min) * init_rotation)
        # return the dc for the deg position
        return self.dc_max - dc_from_max

    def _initRotateTo(self, degrees):
        duty_cycle = _degreesToDutyCycle(degrees)
        servo.start(duty_cycle) # start at init degree position
        print("Rotated to " + str(degrees) + degree_sign)

    def rotateTo(self, degrees):
        # convert to the duty cycle
        duty_cycle = _degreesToDutyCycle(degrees)
        # adjust duty cycle
        servo.ChangeDutyCycle(duty_cycle)
        print("Rotated to " + str(degrees) + degree_sign)

    def __exit__(self):
        self.servo.stop()
        GPIO.cleanup()
