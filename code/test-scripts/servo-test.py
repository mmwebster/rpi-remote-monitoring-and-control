#!/usr/bin/env python
# -*- coding: utf-8 -*-

#######################################################################
# Import libraries
#######################################################################
import time
import RPi.GPIO as GPIO

#######################################################################
# Perform initializations
#######################################################################
GPIO.setmode(GPIO.BCM) # pin numbering scheme that uses GPIO numbers
GPIO.setwarnings(False)
GPIO.setup(4, GPIO.OUT) # set GPIO 4 as output
servo = GPIO.PWM(4, 50) # instantiate PWM output to GPIO 4 @ 50Hz

degree_sign= u'\N{DEGREE SIGN}' # unicode for the degree symbol
dc_min = 2.1 # the min duty cycle corresponding to 210deg rotation
dc_max = 12.3 # the max duty cycle corresponding to 0deg rotation

#######################################################################
# Main logic
#######################################################################
servo.start((dc_min + dc_max) / 2) # start at 105deg
time.sleep(1) # wait until rotation is finished
print("Rotated to 105" + degree_sign)

servo.ChangeDutyCycle(dc_min) # move to 210deg
time.sleep(1) # wait until rotation is finished
print("Rotated to 210" + degree_sign)

servo.ChangeDutyCycle((dc_min + dc_max) / 2) # move to 105deg
time.sleep(1) # wait until rotation is finished
print("Rotated to 105" + degree_sign)

servo.ChangeDutyCycle(dc_max) # move to 0deg
time.sleep(1) # wait until rotation is finished
print("Rotated to 0" + degree_sign)

# house keeping
servo.stop()
GPIO.cleanup()
