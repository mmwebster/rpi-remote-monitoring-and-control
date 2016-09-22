#!/usr/bin/env python
# -*- coding: utf-8 -*-

##########################################################################################
# Import libraries
##########################################################################################
import time
from pymail import Email


##########################################################################################
# Perform initializations and instantiations
##########################################################################################
h_wet_thresh = 60 # (% humidity) upper threshold for humidity
h_dry_thresh = 40 # (% humidity) lower threshold for humidity
t_hot_thresh = 25 # (deg Celcius) upper threshold for temperature
t_cold_thresh = 18 # (deg Celcius) lower threshold for temperature

# An email will be sent every multiple of `email_period` that the
# system stays in a danger state.
email_period = 10

# This counter keeps track of the time elapsed since entering a "danger" state
ds_count = 0

# instantiate email class
email = Email("wilomebster@gmail.com", "dracula08", "milowebster@gmail.com")

# instantiate servo class

# instantiate seg7 class

# instantiate si7021 class

##########################################################################################
# FSM state functions
# @desc Definitions for each state of the FSM. They must return a state name
##########################################################################################
def startupState(data):
    print("Entered STARTUP state")
    # define transitions
    if True:
        # perform outputs
        # -> display IDLE for 3s
        # -> email STARTUP
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
        # -> email "WET for ds_count time"
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
        # -> email "COLD for ds_count time"
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
        # -> email "HOT for ds_count time"
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
        # -> email "DRY for ds_count time"
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
    states = {"STARTUP": startupState, "IDLE": idleState, "WET": wetState,
              "COLD": coldState, "HOT": hotState, "DRY": dryState}
    start_state = "STARTUP"

    count = 0
    # set initial state
    next_state = states[start_state]
    # call the state function associated with the current state
    while count < 10:
        # get the current inputs
        t = 0
        h = 0
        # call the state function associated with the current state
        next_state_str = next_state({"h": h, "t": t))
        # set the next state function
        next_state = states[next_state_str]
        count += 1

main()

####
# NOTE: currently at finishing state definitions, using globally defined thresholds
