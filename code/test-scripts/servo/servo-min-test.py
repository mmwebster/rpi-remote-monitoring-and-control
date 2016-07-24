import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(25, GPIO.OUT)

servo = GPIO.PWM(25, 50)

dc = 2.1
servo.start(dc)
time.sleep(1)


servo.stop()
GPIO.cleanup()
