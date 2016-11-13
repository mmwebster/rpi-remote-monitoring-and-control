#!/usr/bin/env python
# -*- coding: utf-8 -*-

##########################################################################################
# Import libraries
##########################################################################################
import time
import pigpio
from secrets import Secret
from mailer import Mailer
from seg7 import Seg7
from servo import Servo
from si7021 import Si7021

##########################################################################################
# Perform initializations and instantiations
##########################################################################################
h_wet_thresh = 60 # (% humidity) upper threshold for humidity
h_dry_thresh = 40 # (% humidity) lower threshold for humidity
t_hot_thresh = 25 # (deg Celcius) upper threshold for temperature
t_cold_thresh = 18 # (deg Celcius) lower threshold for temperature

# An email will be sent every multiple of `email_period` that the
# system stays in a danger state. The timing of this is currently arbitrary and
# unreliable as all timing functionality is currently implemented in a blocking manner.
email_period = 30

# instantiate secrets pool
secret = Secret()

# instantiate pigpio
pi = pigpio.pi()

# instantiate email class
mailer = Mailer("wilomebster@gmail.com", secret.fetch("email_password"), "milowebster@gmail.com")

# instantiate servo class
servo = Servo(4, 210/2) # start servo via GPIO 25, at 50% rotation

# instantiate seg7 class
seg7 = Seg7(pi, 1, 0x71) # start 7 segment display on I2C bus `1` and address 0x71

# instantiate si7021 class
si7021 = Si7021(pi, 1, 0x40) # start hum. & temp. sensor on I2C bus `1` and address 0x40

##########################################################################################
# FSM state functions
# @desc Definitions for each state of the FSM. They must return a state name
#       corresponding to the next state. Python doesn't have switch statements,
#       so using a lookup table to call the handler associated with each state.
# @note WARNING all timing functions in this tutorial are BLOCKING and must
#       therefore be used with caution. State transitions and actions will be
#       postponed until prior timing periods have ended. If your system must
#       respond quickly to its inputs, refrain from using timing or implement the
#       non-blocking version using Python's `threading` module.
# @note Hot/Cold & Dry/Humid thresholds DO NOT USE HYSTERESIS. They will spam when
#       near the thresholds.
##########################################################################################
def startupState(data):
    print("FSM: Entered STARTUP state")
    # define transitions
    if True:
        # perform outputs
        # -> sent startup email
        mailer.send("RPi Update", "System: STARTUP")
        # -> display IDLE
        seg7.display("ldLE", False, 1)
        return { next_state: "IDLE", ds_count: data["ds_count"] }

def idleState(data):
    print("FSM: Entered IDLE state")
    # define transitions
    if data["h"] > h_wet_thresh:
        # perform outputs
        # -> display UET for 3s
        seg7.display("UET ", False, 1)
        # -> turn servo up then back over 3s
        servo.rotateTo(servo.deg_max)
        time.sleep(1)
        servo.rotateTo(servo.deg_mid)
        # -> ds_count = 1
        data["ds_count"] = 1
        return { next_state: "WET", ds_count: data["ds_count"] }
    elif data["t"] < t_cold_thresh:
        # perform outpus
        # -> display COLD for 3s
        seg7.display("COLD", False, 1)
        # -> turn servo up then back over 3s
        servo.rotateTo(servo.deg_max)
        time.sleep(1)
        servo.rotateTo(servo.deg_mid)
        # -> ds_count = 1
        data["ds_count"] = 1
        return { next_state: "COLD", ds_count: data["ds_count"] }
    elif data["t"] > t_hot_thresh:
        # perform outputs
        # -> display HOT for 3s
        seg7.display("HOT ", False, 1)
        # -> turn servo down then back over 3s
        servo.rotateTo(servo.deg_min)
        time.sleep(1)
        servo.rotateTo(servo.deg_mid)
        # -> ds_count = 1
        data["ds_count"] = 1
        return { next_state: "HOT", ds_count: data["ds_count"] }
    elif data["h"] < h_dry_thresh:
        # perform outputs
        # -> display DRY for 3s
        seg7.display("DRY ", False, 1)
        # -> turn servo down then back over 3s
        servo.rotateTo(servo.deg_min)
        time.sleep(1)
        servo.rotateTo(servo.deg_mid)
        # -> ds_count = 1
        data["ds_count"] = 1
        return { next_state: "DRY", ds_count: data["ds_count"] }
    else:
        # no danger state transitions evaluated..remaining in IDLE
        # -> display humidity for 1s, then temp for 1s
        seg7.display("HU__", False, 1)
        seg7.display("tP__", False, 1)
        return { next_state: "IDLE", ds_count: data["ds_count"] }

def wetState(data):
    print("FSM: Entered WET state")
    # catch extended periods of time in WET state
    if data["ds_count"] != 0 and data["ds_count"] % email_period == 0:
        # perform outputs
        mailer.send("RPi Warning", "System: WET for " + str(data["ds_count"]) + " cyles")
    # define transitions
    if data["h"] > h_wet_thresh:
        # perform outputs
        # -> display humidity for 1s, then temp for 1s
        seg7.display("HU__", False, 1)
        seg7.display("tP__", False, 1)
        # -> turn servo up then back over 3s
        servo.rotateTo(servo.deg_max)
        time.sleep(1)
        servo.rotateTo(servo.deg_mid)
        # -> ds_count += 1
        data["ds_count"] += 1
        return { next_state: "WET", ds_count: data["ds_count"] }
    else:
        # perform outputs
        # -> display IDLE for 3s
        seg7.display("ldLE", False, 1)
        # -> ds_count = 0
        data["ds_count"] = 0
        return { next_state: "IDLE", ds_count: data["ds_count"] }

def coldState(data):
    print("FSM: Entered COLD state")
    # catch extended periods of time in COLD state
    if data["ds_count"] != 0 and data["ds_count"] % email_period == 0:
        # perform outputs
        mailer.send("RPi Warning", "System: COLD for " + str(data["ds_count"]) + " cycles")
    if data["t"] < t_cold_thresh:
        # perform outputs
        # -> display humidity for 1s, then temp for 1s
        seg7.display("HU__", False, 1)
        seg7.display("tP__", False, 1)
        # -> turn servo down then back over 3s
        servo.rotateTo(servo.deg_min)
        time.sleep(1)
        servo.rotateTo(servo.deg_mid)
        # -> ds_count += 1
        data["ds_count"] += 1
        return { next_state: "COLD", ds_count: data["ds_count"] }
    else:
        # perform outputs
        # -> display IDLE for 3s
        seg7.display("ldLE", False, 1)
        # -> ds_count = 0
        data["ds_count"] = 0
        return { next_state: "IDLE", ds_count: data["ds_count"] }

def hotState(data):
    print("FSM: Entered HOT state")
    # catch extended periods of time in HOT state
    if data["ds_count"] != 0 and data["ds_count"] % email_period == 0:
        # perform outputs
        mailer.send("RPi Warning", "System: HOT for " + str(data["ds_count"]) + " cycles")
    if data["t"] > t_hot_thresh:
        # perform outputs
        # -> display humidity for 1s, then temp for 1s
        seg7.display("HU__", False, 1)
        seg7.display("tP__", False, 1)
        # -> turn servo down then back over 3s
        servo.rotateTo(servo.deg_min)
        time.sleep(1)
        servo.rotateTo(servo.deg_mid)
        # -> ds_count += 1
        data["ds_count"] += 1
        return { next_state: "HOT", ds_count: data["ds_count"] }
    else:
        # perform outputs
        # -> display IDLE for 3s
        seg7.display("ldLE", False, 1)
        # -> ds_count = 0
        data["ds_count"] = 0
        return { next_state: "IDLE", ds_count: data["ds_count"] }

def dryState(data):
    print("FSM: Entered DRY state")
    # catch extended periods of time in DRY state
    if data["ds_count"] != 0 and data["ds_count"] % email_period == 0:
        # perform outputs
        mailer.send("RPi Warning", "System: DRY for " + str(data["ds_count"]) + " cycles")
    if data["h"] < h_dry_thresh:
        # perform outputs
        # -> display humidity for 1s, then temp for 1s
        seg7.display("HU__", False, 1)
        seg7.display("tP__", False, 1)
        # -> turn servo down then back over 3s
        servo.rotateTo(servo.deg_min)
        time.sleep(1)
        servo.rotateTo(servo.deg_mid)
        # -> ds_count += 1
        data["ds_count"] += 1
        return { next_state: "DRY", ds_count: data["ds_count"] }
    else:
        # perform outputs
        # -> display IDLE for 3s
        seg7.display("ldLE", False, 1)
        # -> ds_count = 0
        data["ds_count"] = 0
        return { next_state: "IDLE", ds_count: data["ds_count"] }

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

    # print("MAIN: Started up! Running tests.")
    # mailer.test()
    # seg7.test()
    # servo.test()
    # time.sleep(1) # give servo time to move
    # si7021.test()
    # print("MAIN: All tests passed? Check their outputs to confirm.")

    print("MAIN: Starting up the main FSM...")

    # This counter keeps track of the time elapsed since entering a "danger" state
    ds_count = 0
    # Main FSM runloop
    count = 0
    # set initial state
    next_state = states[start_state]
    # call the state function associated with the current state
    # TODO: remove this counter so that more than 10 transitions can occur
    while count < 15:
        # get the current inputs
        t = si7021.readTemperature()
        h = si7021.readRelativeHumidity()
        # call the state function associated with the current state and store
        # the returned next state str
        state_return = next_state({"h": h, "t": t, "ds_count": ds_count})
        next_state_str = state_return["next_state"]
        ds_count = state_return["ds_count"]
        # set the next state function
        next_state = states[next_state_str]
        count += 1
        print("T: " + str(t) + ", H: " + str(h))
        time.sleep(.1)


    # clean up all libs on exit
    si7021.__exit__(None, None, None)
    seg7.__exit__(None, None, None)
    servo.__exit__(None, None, None)
    mailer.__exit__(None, None, None)
    # close pi gpio ref
    pi.stop()

main()

####
#) NOTE: left off at filling out the "->" actions in the state machine, where first needed to finish consildating and packaging the routines for which tests were originally written.
