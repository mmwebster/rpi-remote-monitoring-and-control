#!/usr/bin/env python
# -*- coding: utf-8 -*-

##########################################################################################
# Import libraries
##########################################################################################
import time
import pigpio
from secrets import Secret
from pymail import Mailer
from seg7 import Seg7
from servo import Servo
from si7021 import Si7021
# TODO: import pigpio and pass to seg7 and si7021 instances


##########################################################################################
# Perform initializations and instantiations
##########################################################################################
h_wet_thresh = 60 # (% humidity) upper threshold for humidity
h_dry_thresh = 40 # (% humidity) lower threshold for humidity
t_hot_thresh = 25 # (deg Celcius) upper threshold for temperature
t_cold_thresh = 18 # (deg Celcius) lower threshold for temperature

# An email will be sent every multiple of `email_period` that the
# system stays in a danger state.
email_period = 30

# This counter keeps track of the time elapsed since entering a "danger" state
ds_count = 0

# instantiate secrets pool
secret = Secret()

# instantiate pigpio
pi = pigpio.pi()

# instantiate email class
mailer = Mailer("wilomebster@gmail.com", secret.fetch("email_password"), "milowebster@gmail.com")

# instantiate servo class
servo = Servo(25, 210/2) # start servo via pin 25, at 50% rotation

# instantiate seg7 class
seg7 = Seg7(pi, 1, 0x71) # start 7 segment display on I2C bus `1` and address 0x71

# instantiate si7021 class
si7021 = Si7021(pi, 1, 0x40) # start hum. & temp. sensor on I2C bus `1` and address 0x40

##########################################################################################
# FSM state functions
# @desc Definitions for each state of the FSM. They must return a state name
#       corresponding to the next state. Python doesn't have switch statements,
#       so using a lookup table to call the handler associated with each state.
##########################################################################################
def startupState(data):
    print("Entered STARTUP state")
    # define transitions
    if True:
        # perform outputs
        # -> display IDLE for 3s
        email.send("RPi Update", "System: STARTUP")
        return "IDLE"
def idleState(data):
    print("Entered IDLE state")
    # define transitions
    if data["h"] > h_wet_thresh:
        # perform outputs
        # -> display UET for 3s
        # -> turn servo up then back over 3s
        # -> ds_count = 1
        return "WET"
    elif data["t"] < t_cold_thresh:
        # perform outpus
        # -> display COLD for 3s
        # -> turn servo up then back over 3s
        # -> ds_count = 1
        return "COLD"
    elif data["t"] > t_hot_thresh:
        # perform outputs
        # -> display HOT for 3s
        # -> turn servo down then back over 3s
        # -> ds_count = 1
        return "HOT"
    elif data["h"] < h_dry_thresh:
        # perform outputs
        # -> display DRY for 3s
        # -> turn servo down then back over 3s
        # -> ds_count = 1
        return "DRY"
    else:
        # no danger state transitions evaluated..remaining in IDLE
        # -> display humidity for 1s, then temp for 1s
        return "IDLE"
def wetState(data):
    print("Entered WET state")
    # catch extended periods of time in WET state
    if ds_count % email_period == 0:
        # perform outputs
        email.send("RPi Warning", "System: WET for " + ds_count + "s")
    # define transitions
    if data["h"] > h_wet_thresh:
        # perform outputs
        # -> display humidity for 1s, then temp for 1s
        # -> turn servo up then back over 3s
        # -> ds_count += 1
        return "WET"
    elif data["h"] <= h_wet_thresh:
        # perform outputs
        # -> display IDLE for 3s
        # -> ds_count = 0
        return "IDLE"
def coldState(data):
    print("Entered COLD state")
    # catch extended periods of time in COLD state
    if ds_count % email_period == 0:
        # perform outputs
        email.send("RPi Warning", "System: COLD for " + ds_count + "s")
    if data["t"] < t_cold_thresh:
        # perform outputs
        # -> display humidity for 1s, then temp for 1s
        # -> turn servo down then back over 3s
        # -> ds_count += 1
        return "COLD"
    elif data["t"] >= t_cold_thresh:
        # perform outputs
        # -> display IDLE for 3s
        # -> ds_count = 0
        return "IDLE"
    return "HOT"
def hotState(data):
    print("Entered HOT state")
    # catch extended periods of time in HOT state
    if ds_count % email_period == 0:
        # perform outputs
        email.send("RPi Warning", "System: HOT for " + ds_count + "s")
    if data["t"] > t_hot_thresh:
        # perform outputs
        # -> display humidity for 1s, then temp for 1s
        # -> turn servo down then back over 3s
        # -> ds_count += 1
        return "HOT"
    elif data["t"] <= t_hot_thresh:
        # perform outputs
        # -> display IDLE for 3s
        # -> ds_count = 0
        return "IDLE"
def dryState(data):
    print("Entered DRY state")
    # catch extended periods of time in DRY state
    if ds_count % email_period == 0:
        # perform outputs
        email.send("RPi Warning", "System: DRY for " + ds_count + "s")
    if data["h"] < h_dry_thresh:
        # perform outputs
        # -> display humidity for 1s, then temp for 1s
        # -> turn servo down then back over 3s
        # -> ds_count += 1
        return "DRY"
    elif data["h"] >= h_dry_thresh:
        # perform outputs
        # -> display IDLE for 3s
        # -> ds_count = 0
        return "IDLE"

##########################################################################################
# Utility functions
##########################################################################################
# def getState(name):
#     possibilities = 

##########################################################################################
# Main logic
##########################################################################################
def main():
    # define FSM properties
    states = {"STARTUP": startupState, "IDLE": idleState, "WET": wetState, "COLD": coldState, "HOT": hotState, "DRY": dryState}
    start_state = "STARTUP"

    print("Started up! Running tests.")
    mailer.test()
    seg7.test()
    servo.test()
    si7021.test()
    print("All tests passed? Check their outputs")


    # count = 0
    # # set initial state
    # next_state = states[start_state]
    # # call the state function associated with the current state
    # # TODO: remove this counter so that more than 10 transitions can occur
    # while count < 10:
    #     # get the current inputs
    #     # TODO: make this actually fetch the current values
    #     t = 0
    #     h = 0
    #     # call the state function associated with the current state and store
    #     # the returned next state str
    #     next_state_str = next_state({"h": h, "t": t))
    #     # set the next state function
    #     next_state = states[next_state_str]
    #     count += 1

main()

####
# NOTE: left off at filling out the "->" actions in the state machine, where first needed to finish consildating and packaging the routines for which tests were originally written.
